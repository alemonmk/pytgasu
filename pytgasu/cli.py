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
from pytgasu import __version__


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
    from telethon import TelegramClient
    from pytgasu.upload import SetDefParse, SetUploader

    # region Telegram init
    Path(PATH_TGSESSION_FILE).expanduser().parent.mkdir(exist_ok=True)

    tc = TelegramClient(
        session=str(Path(PATH_TGSESSION_FILE).expanduser()),
        api_id=TG_API_ID,
        api_hash=TG_API_HASH,
        update_workers=0,
        app_version=__version__)
    tc.start()
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

    Reads any given directories, process any file Telegram won't accept.
    Generates and overwrites existing .ssd file.
    """

    from pytgasu.prepare import SetDefGenerator, PrepareImageFiles

    for set_dir in sets:
        set_dir = Path(set_dir).resolve()
        PrepareImageFiles(set_dir=set_dir)
        SetDefGenerator(set_dir=set_dir)

    print(NOTICE_GO_EDIT_DEFS)


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

    tc = TelegramClient(
        session=str(Path(PATH_TGSESSION_FILE).expanduser()),
        api_id=TG_API_ID,
        api_hash=TG_API_HASH,
        update_workers=None,
        spawn_read_thread=False,
        app_version=__version__)
    tc.connect()
    tc.log_out()


if __name__ == "__main__":
    cli()
