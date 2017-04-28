#! /usr/bin/env python
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

from core import SetUploader
from defgen import SetDefGenerator


@click.group()
@click.version_option()
def cli():
    pass


@cli.command(short_help='Upload sticker sets to Telegram.')
@click.option('--sub', '/sub', is_flag=True,  help='Subscribe to created set(s).')
@click.argument('paths', nargs=-1)
def upload(paths, subscribe):
    """Upload sticker sets to Telegram.
    
    \b
    Takes paths of:
        1. directories with a .ssd (sticker set definitions) file, or
        2. .ssd files themselves
    as arguments.
    """
    # Looks like I have to check if the path exist as click doesn't do dynamic validation
    _paths = [p for p in paths if Path(p).exists()]
    for nep in set(paths) - set(_paths):
        print("{} does not exist, ignoring!" % nep)

    SetUploader(_paths, subscribe)


@cli.command()
@click.argument(
    'sets', nargs=-1,
    type=click.Path(exists=True, file_okay=False, writable=True)
)
def defgen(sets):
    """Generate sticker set definition.
    
    Take any paths of directory as arguments.
    """
    SetDefGenerator(sets)

if __name__ == "__main__":
    cli()
