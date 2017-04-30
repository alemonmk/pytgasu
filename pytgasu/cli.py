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

from uploader import SetUploader
from defgen import SetDefGenerator
from strings import *


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
    SetUploader(paths).upload(s)


@cli.command(short_help=CLI_SHELP_DEFGEN_COMMAND)
@click.argument(
    'sets', nargs=-1, required=True,
    type=click.Path(exists=True, file_okay=False, writable=True))
def defgen(sets):
    """Generate sticker set definition.
    
    Reads any given directory.
    Overwrites existing .ssd file.
    """
    SetDefGenerator(sets).generate()

if __name__ == "__main__":
    cli()
