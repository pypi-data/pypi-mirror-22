# pytgasu - Automating creation of Telegram sticker packs
# Copyright (C) 2017 Lemon Lam <almk@rmntn.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from pathlib import Path
from hashlib import md5
import logging

from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.tl.functions.messages import (SendMessageRequest, SendMediaRequest, InstallStickerSetRequest)
from telethon.tl.functions.upload import SaveFilePartRequest
from telethon.tl.types import (InputPeerUser, InputMediaUploadedDocument, DocumentAttributeFilename,
                               InputFile, InputStickerSetShortName)
from telethon.tl.types.messages import StickerSetInstallResultSuccess
from os import urandom
from time import sleep

from pytgasu.uploader import defparse
from pytgasu.uploader.customised_session import CustomisedSession
from pytgasu.strings import *


class SetUploader:
    _telegram_api_id, _telegram_api_hash = 173590, "9b05a9d53a77019aa1d615f27776e60f"
    # it only talks to @Stickers, so just hardcode it
    # invoke(ResolveUsernameRequest(username='Stickers')) returns
    #   contacts.resolvedPeer = \
    #       (..., users=[(..., id=429000, access_hash=9143715803499997149, username=Stickers, ...)])
    _stickersbot = InputPeerUser(user_id=429000, access_hash=9143715803499997149)

    def __init__(self, set_paths):
        """
        Log in to Telegram and prepare for upload.
        
        :param set_paths: See the docstring of `cli.upload()`
        """
        # TODO: strip Telethon to avoid too much implicit import
        self._TC = TelegramClient(
            session=CustomisedSession.try_load_or_create_new(),
            api_id=self._telegram_api_id,
            api_hash=self._telegram_api_hash)
        logging.getLogger('TelethonLogger').setLevel(logging.ERROR)  # suppress logging from telethon

        # Stolen from telethon.InteractiveTelegramClient :P
        self._TC.connect()
        if not self._TC.is_user_authorized():
            print(PROMPT_ON_FIRST_LAUNCH)
            user_phone = input(PROMPT_PHONE_NUMBER)
            self._TC.send_code_request(user_phone)
            code_ok = False
            while not code_ok:
                code = input(PROMPT_LOGIN_CODE)
                try:
                    code_ok = self._TC.sign_in(user_phone, code)

                # Two-step verification may be enabled
                except RPCError as e:
                    from getpass import getpass
                    if e.password_required:
                        pw = getpass(PROMPT_2FA_PASSWORD)
                        code_ok = self._TC.sign_in(password=pw)
                    else:
                        raise e

        self._stickersets = list()
        for setpath in set_paths:
            print(NOTICE_PREPARING % setpath)
            path = Path(setpath)
            set_def_tuple = ()
            if path.is_dir():
                for d in path.glob('*.ssd'):
                    set_def_tuple = defparse.parse(d)  # only process one
                    break
            elif path.suffix == '.ssd':
                set_def_tuple = defparse.parse(path)
            if set_def_tuple:
                self._stickersets.append(set_def_tuple)

    def upload(self, subscribe=False):
        """
        Start uploads, and disconnect from Telegram after finish.
        
        :param subscribe: See `strings.CLI_SHELP_UPLOAD_SUBFLAG`
        :return: None
        """
        if self._stickersets:
            self._do_uploads(subscribe=subscribe)
        else:
            print(ERROR_NO_SET_UPLOAD)
        self._TC.disconnect()

    def _do_uploads(self, subscribe):
        """Talk to Stickers bot and create the sets."""
        self._sticker_bot_cmd(SendMessageRequest, message='/cancel')
        self._sticker_bot_cmd(SendMessageRequest, message='/start')

        for _set in self._stickersets:
            set_title, set_short_name, stickers = _set

            self._sticker_bot_cmd(SendMessageRequest, message='/newpack')
            self._sticker_bot_cmd(SendMessageRequest, message=set_title)
            for index, (sticker_image, emojis) in enumerate(stickers):
                uploaded_file = self._do_upload_file(sticker_image)
                uploaded_doc = InputMediaUploadedDocument(
                    file=uploaded_file,
                    mime_type='image/png',
                    attributes=[DocumentAttributeFilename(uploaded_file.name)],
                    caption='')
                self._sticker_bot_cmd(SendMediaRequest, media=uploaded_doc)
                self._sticker_bot_cmd(SendMessageRequest, message=emojis)
                print(NOTICE_UPLOADED % {'fn': uploaded_file.name, 'cur': index + 1, 'total': len(stickers)})
            self._sticker_bot_cmd(SendMessageRequest, message='/publish')
            self._sticker_bot_cmd(SendMessageRequest, message=set_short_name)
            print(NOTICE_SET_AVAILABLE % {'title': set_title, 'short_name': set_short_name})

            if subscribe:
                result = self._TC.invoke(InstallStickerSetRequest(
                    InputStickerSetShortName(short_name=set_short_name), archived=False))
                if type(result) == StickerSetInstallResultSuccess:
                    print(NOTICE_SET_SUBSCRIBED % set_title)

    @staticmethod
    def _get_random_id():
        return int.from_bytes(urandom(8), signed=True, byteorder='little')

    def _sticker_bot_cmd(self, request, **kwargs):
        """
        An 'interface' to send `MTProtoRequest`s.
        
        :param request: An MTProtoRequest
        :param kwargs: Parameters for the MTProtoRequest
        :return: None
        """
        random_id = self._get_random_id()
        self._TC.invoke(request=request(**kwargs, peer=self._stickersbot, random_id=random_id))
        sleep(1)  # wait for bot reply, but can ignore the content

    def _do_upload_file(self, filepath):
        """
        Upload a file to Telegram cloud.
        Stolen from telethon.TelegramClient.upload_file().
        Specialised for upload sticker images.
        
        :param filepath: A path-like object
        :return: An InputFile handle.
        """
        file = Path(filepath)
        file_id = self._get_random_id()
        file_name = file.name
        part_size_kb = 32 * 1024  # just hardcode it, every file is under 350KB anyways
        part_count = (file.stat().st_size + part_size_kb - 1) // part_size_kb
        file_hash = md5()
        with open(file, mode='rb') as f:
            for part_index in range(part_count):
                part = f.read(part_size_kb)
                self._TC.invoke(request=SaveFilePartRequest(file_id, part_index, part))
                file_hash.update(part)
        return InputFile(id=file_id, parts=part_count, name=file_name, md5_checksum=file_hash.hexdigest())
