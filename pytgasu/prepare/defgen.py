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
from ..constants import *

__all__ = ['generate']


def generate(set_dir):
    """Walk through supplied directory and generate sticker definition files."""
    from pathlib import Path

    path_set_dir = Path(set_dir)
    print(NOTICE_START_GENERATE % path_set_dir.stem)
    set_title = ''
    set_short_name = ''
    try:
        while not set_title:
            set_title = input(PROMPT_SET_TITLE)
        while not set_short_name:
            set_short_name = input(PROMOT_SET_SHORTNAME)
    except EOFError:
        print(ERROR_EOF_FROM_INPUT)
        return

    def_file_path = path_set_dir.joinpath(''.join((set_short_name, '.ssd')))
    with open(def_file_path, mode='w', encoding='utf-8', errors='strict') as f:
        f.write('%s\n' % set_title)
        f.write('%s\n' % set_short_name)
        for fn in path_set_dir.glob('*.png'):
            f.write('%s\n' % ''.join([fn.name, '/']))

    print(NOTICE_DONE_GENERATE % (path_set_dir.stem, def_file_path))
