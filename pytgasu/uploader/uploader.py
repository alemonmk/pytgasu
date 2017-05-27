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
from time import sleep
from os import urandom
from ..strings import *

from telethon.tl.types import InputPeerUser
# it only talks to @Stickers, so just hardcode it
# invoke(ResolveUsernameRequest(username='Stickers')) returns
#   contacts.resolvedPeer = \
#       (..., users=[(..., id=429000, access_hash=9143715803499997149, username=Stickers, ...)])
_stickersbot = InputPeerUser(user_id=429000, access_hash=9143715803499997149)

__all__ = ['upload']


def upload(tc, sets, subscribe=False):
    """Talk to Stickers bot and create the sets."""
    from functools import partial
    from telethon.tl.functions.messages import SendMessageRequest, SendMediaRequest, InstallStickerSetRequest
    from telethon.tl.types import InputMediaUploadedDocument, DocumentAttributeFilename, InputStickerSetShortName
    from telethon.tl.types.messages import StickerSetInstallResultSuccess

    send_bot_cmd = partial(_send_bot_cmd, tc=tc)
    upload_file = partial(_upload_file, tc=tc)

    if sets:
        # TODO: check if set already created (by anyone), ask to subscribe if set exists
        send_bot_cmd(SendMessageRequest, message='/cancel')
        send_bot_cmd(SendMessageRequest, message='/start')

        for _set in sets:
            set_title, set_short_name, stickers = _set

            send_bot_cmd(SendMessageRequest, message='/newpack')
            send_bot_cmd(SendMessageRequest, message=set_title)
            for index, (sticker_image, emojis) in enumerate(stickers):
                uploaded_file = upload_file(sticker_image)
                uploaded_doc = InputMediaUploadedDocument(
                    file=uploaded_file,
                    mime_type='image/png',
                    attributes=[DocumentAttributeFilename(uploaded_file.name)],
                    caption='')
                send_bot_cmd(SendMediaRequest, media=uploaded_doc)
                send_bot_cmd(SendMessageRequest, message=emojis)
                print(NOTICE_UPLOADED % {'fn': uploaded_file.name, 'cur': index + 1, 'total': len(stickers)})
            send_bot_cmd(SendMessageRequest, message='/publish')
            send_bot_cmd(SendMessageRequest, message=set_short_name)
            print(NOTICE_SET_AVAILABLE % {'title': set_title, 'short_name': set_short_name})

            if subscribe:
                result = tc.invoke(
                    InstallStickerSetRequest(
                        InputStickerSetShortName(short_name=set_short_name), archived=False))
                if isinstance(result, StickerSetInstallResultSuccess):
                    print(NOTICE_SET_SUBSCRIBED % set_title)
    else:
        print(ERROR_NO_SET_UPLOAD)


def _get_random_id():
    return int.from_bytes(urandom(8), signed=True, byteorder='little')


def _send_bot_cmd(tc, request, **kwargs):
    """
    An 'interface' to send `MTProtoRequest`s.

    :param tc: A TelegramClient
    :param request: An MTProtoRequest
    :param kwargs: Parameters for the MTProtoRequest
    :return: None
    """
    tc.invoke(request=request(**kwargs, peer=_stickersbot, random_id=_get_random_id()))
    sleep(1)  # wait for bot reply, but can ignore the content


def _upload_file(tc, filepath):
    """
    Upload a file to Telegram cloud.
    Stolen from telethon.TelegramClient.upload_file().
    Specialised for upload sticker images.

    :param tc: A TelegramClient
    :param filepath: A path-like object
    :return: An InputFile handle.
    """
    from telethon.tl.types import InputFile
    from telethon.tl.functions.upload import SaveFilePartRequest

    file = Path(filepath)
    file_id = _get_random_id()
    file_name = file.name
    part_size_kb = 32 * 1024  # just hardcode it, every file is under 350KB anyways
    part_count = (file.stat().st_size + part_size_kb - 1) // part_size_kb
    file_hash = md5()
    with open(file, mode='rb') as f:
        for part_index in range(part_count):
            part = f.read(part_size_kb)
            tc.invoke(request=SaveFilePartRequest(file_id, part_index, part))
            file_hash.update(part)
    return InputFile(id=file_id, parts=part_count, name=file_name, md5_checksum=file_hash.hexdigest())
