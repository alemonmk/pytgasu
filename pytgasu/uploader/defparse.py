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
from ..strings import *

__all__ = ['parse']


def parse(def_file):
    """
    Parse specified sticker set definition file.

    :param def_file: A Path-like object to .ssd file
    :return: A tuple of set_title, set_short_name, [(image_fullpath, emojis)] representing the set
             None on error
    """
    from pathlib import Path
    import regex

    _sticker_line_pattern = regex.compile(REGEX_MATCHING_EMOJI)
    try:
        with open(def_file, encoding='utf-8', errors='strict') as f:
            lines = [l.rstrip() for l in f]  # strip line breaks
            set_title = lines[0]
            set_short_name = lines[1]
            stickers = list()  # there may be a 120 stickers per set hard limit, idk
            for sticker_line in lines[2:]:
                if not _sticker_line_pattern.fullmatch(sticker_line):
                    print(ERROR_INCORRECT_STICKER_LINE % sticker_line)
                    continue
                image_filename, emoji_seq = sticker_line.split('/')
                image_path = def_file.with_name(image_filename)
                if not _validate_image(image_path):
                    continue
                if not emoji_seq:
                    emoji_seq = DEFAULT_EMOJI
                stickers.append((image_path, emoji_seq))
            if not stickers:
                print(ERROR_NO_STICKER_IN_SET)
                return None
            return set_title, set_short_name, stickers
    except ValueError:
        print(ERROR_DEFFILE_ENCODING % def_file)
        return None


def _validate_image(image_path):
    """
    Check file existence, image is correct PNG,
        dimension is 512x? or ?x512 and file size < 350KB

    :param image_path: The image for a sticker
    :return: Boolean if all limits on stickers met
    """
    # TODO: ditch PIL
    from PIL.Image import open as pil_open

    # TODO: adjust image instead check only
    # TODO: having done above, copy to prepare and leave this one check only?
    try:
        with pil_open(image_path) as image:
            criteria = [
                max(image.size) == 512,
                image.format == 'PNG',
                image_path.stat().st_size < 350 * 1000
            ]
            return True if all(criteria) else False
    except IOError:
        print(ERROR_INVAILD_STICKER_IMAGE % image_path.name)
        return False  # invalid image or just 404
