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
import pickle
from pathlib import Path

from telethon.tl.session import Session

from pytgasu.strings import *


class CustomisedSession(Session):
    """
    Override telethon.tl.session for fixed session file path.
    """
    def __init__(self, session_user_id='asu'):
        super().__init__(session_user_id)

    def save(self):
        with Path(PATH_TGSESSION_FILE).open(mode='wb') as file:
            pickle.dump(self, file)

    def delete(self):
        try:
            Path(PATH_TGSESSION_FILE).unlink()
            return True
        except ValueError:
            return False

    @staticmethod
    def try_load_or_create_new(session_user_id=None):
        path = Path(PATH_TGSESSION_FILE)

        if path.exists():
            with path.open(mode='rb') as file:
                return pickle.load(file)
        else:
            return CustomisedSession()
