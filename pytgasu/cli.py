#! /usr/bin/env python3
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
import click
from pytgasu.constants import *


@click.group()
@click.version_option()
def cli():
    pass


@cli.command(short_help=CLI_SHELP_UPLOAD_COMMAND)
@click.option('-s', '/s', is_flag=True,  help=CLI_SHELP_UPLOAD_SUBFLAG)
@click.argument('paths', nargs=-1, required=True,
                type=click.Path(exists=True))
def upload(paths, s):
    """Upload sticker sets to Telegram.

    \b
    Paths can be:
        1. directories with a .ssd (sticker set definitions) file, or
        2. .ssd files themselves
    """
    import logging
    from telethon import TelegramClient
    from telethon.errors import RPCError
    from pytgasu.upload import CustomisedSession, SetDefParse, SetUploader

    # region Telegram init
    # TODO: strip Telethon to avoid too much implicit import
    # Probably have to let the 'update' thread stay even we don't need it
    # as ping-pongs prevent server from disconnecting us,
    # but what's the point as we are constantly talking while running this function?
    tc = TelegramClient(
        session=CustomisedSession.try_load_or_create_new(),
        api_id=TG_API_ID,
        api_hash=TG_API_HASH)
    logging.getLogger('TelethonLogger').setLevel(logging.ERROR)  # suppress logging from telethon

    # Stolen from telethon.InteractiveTelegramClient :P
    tc.connect()
    if not tc.is_user_authorized():
        print(PROMPT_ON_FIRST_LAUNCH)
        user_phone = input(PROMPT_PHONE_NUMBER)
        tc.send_code_request(user_phone)
        code_ok = False
        while not code_ok:
            code = input(PROMPT_LOGIN_CODE)
            try:
                code_ok = tc.sign_in(user_phone, code)

            # Two-step verification may be enabled
            except RPCError as e:
                from getpass import getpass
                if e.password_required:
                    pw = getpass(PROMPT_2FA_PASSWORD)
                    code_ok = tc.sign_in(password=pw)
                else:
                    raise e
    # endregion

    # region Set list init
    sticker_sets = list()
    for setpath in paths:
        print(NOTICE_PREPARING % setpath)
        path = Path(setpath).resolve()
        set_def_tuple = ()
        if path.is_dir():
            for d in path.glob('*.ssd'):
                set_def_tuple = SetDefParse(d)  # only process one
                break
        elif path.suffix == '.ssd':
            set_def_tuple = SetDefParse(path)
        if set_def_tuple:
            sticker_sets.append(set_def_tuple)
    # endregion

    SetUploader(tc=tc, sets=sticker_sets, subscribe=s)

    tc.disconnect()


@cli.command(short_help=CLI_SHELP_PREPARE_COMMAND)
@click.argument(
    'sets', nargs=-1, required=True,
    type=click.Path(exists=True, file_okay=False, writable=True))
def prepare(sets):
    """Prepare sticker sets to be uploaded by this tool.

    Reads any given directory.
    Overwrites existing .ssd file.
    """
    from pytgasu.defgen import SetDefGenerator

    # TODO: do first-run configurations to setting paths to executables of pngquant and/or waifu2x

    SetDefGenerator(set_dir=set_dir)


@cli.command(short_help=CLI_SHELP_LOGOUT_COMMAND)
def logout():
    """Logout from Telegram."""
    if not Path(PATH_TGSESSION_FILE).exists():
        # Return early because TelegramClient creates a session first,
        # but only when you can log_out() the session file gets deleted.
        # If it's not there, don't create it and waste time talking to Telegram.
        print(ERROR_NOT_LOGGEDIN)
        return

    from telethon import TelegramClient
    from pytgasu.upload import CustomisedSession
    tc = TelegramClient(
        session=CustomisedSession.try_load_or_create_new(),
        api_id=TG_API_ID,
        api_hash=TG_API_HASH)
    tc.connect()
    # I guess even if user is not authorised, invoking LogOutRequest does not cause problems
    tc.log_out()
    Path(PATH_TGSESSION_FILE).parent.unlink()

if __name__ == "__main__":
    cli()
