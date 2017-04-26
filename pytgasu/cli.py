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
import click
from os import path
from core import PackUploader
from defgen import PackDefGenerator


@click.group()
@click.version_option()
def cli():
    pass


@cli.command(short_help='Upload sticker packs to Telegram.')
@click.option('--sub', '/sub', is_flag=True,  help='Subscribe to created pack(s).')
@click.argument('packs', nargs=-1)
def upload(packs, subscribe):
    """Upload specific sticker packs to Telegram.
    
    \b
    Takes paths of:
        1. directories with a .spd (sticker pack definitions) file, or
        2. .spd files themselves
    as arguments.
    """
    # packs can be a path to sticker directory or sticker definition file
    # Looks like I have to check if the path exist as click doesn't do dynamic validation
    _packs = list(packs)
    for _path in _packs:
        if not path.exists(_path):
            print("{} does not exist, ignoring!".format(_path))
            _packs.remove(_path)

    PackUploader(_packs, subscribe).upload()


@cli.command()
@click.argument(
    'packs', nargs=-1,
    type=click.Path(exists=True, file_okay=False, writable=True)
)
def defgen(packs):
    """Generate sticker pack definition.
    
    Take any paths of directory as arguments.
    """
    PackDefGenerator(packs).run()

if __name__ == "__main__":
    cli()
