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

# config
PATH_CONFIG_FOLDER = '~/.pytgasu/asu.cfg'
PATH_TGSESSION_FILE = '~/.pytgasu/asu.session'

# telegram specified
TG_API_ID = 173590
TG_API_HASH = "9b05a9d53a77019aa1d615f27776e60f"
PROMPT_ON_FIRST_LAUNCH = "It's your first run of this program, please login first.\n" \
                         "Login session will be preserved, you don't need to login next time."
PROMPT_PHONE_NUMBER = 'Your phone number -> '
PROMPT_LOGIN_CODE = 'Enter the login code -> '
PROMPT_2FA_PASSWORD = 'Two step verification is enabled. Please enter your password -> '

# upload
ERROR_NO_SET_UPLOAD = 'No sticker set need to be uploaded, aborting.'
ERROR_NO_STICKER_IN_SET = 'No sticker can be uploaded from this set, skipping.'
ERROR_INCORRECT_STICKER_LINE = 'Incorrect sticker line (should be ^<filename>/<emoji>?$), ignoring line: %s'
ERROR_DEFFILE_ENCODING = '%s is not in UTF-8 encoding, ignoring.'
ERROR_INVAILD_STICKER_IMAGE = '%s is not valid image for sticker, ignoring.'

NOTICE_PREPARING = 'Preparing %s for upload...'
NOTICE_UPLOADED = '%(fn)s uploaded. %(cur)d/%(total)d\r'
NOTICE_SET_AVAILABLE = '%(title)s is published and now available at https://t.me/addstickers/%(short_name)s.'
NOTICE_SET_SUBSCRIBED = '%s has been subscribed.'

DEFAULT_EMOJI = '\u26aa\ufe0f'  # MEDIUM WHITE CIRCLE

# Emoji filtering regular expression construct
# Taken from https://github.com/TakumiHQ/emoji-unicode/blob/update-emoji-data/emoji_unicode/pattern.py
# According to the aforementioned repository, this supports Unicode version 9
_CODE_POINTS = '\xa9\xae\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9-\u21aa\u231a-\u231b\u2328\u23cf\u23e9-\u23f3' \
               '\u23f8-\u23fa\u24c2\u25aa-\u25ab\u25b6\u25c0\u25fb-\u25fe\u2600-\u2604\u260e\u2611\u2614-\u2615' \
               '\u2618\u261d\u2620\u2622-\u2623\u2626\u262a\u262e-\u262f\u2638-\u263a\u2640\u2642\u2648-\u2653\u2660' \
               '\u2663\u2665-\u2666\u2668\u267b\u267f\u2692-\u2697\u2699\u269b-\u269c\u26a0-\u26a1\u26aa-\u26ab' \
               '\u26b0-\u26b1\u26bd-\u26be\u26c4-\u26c5\u26c8\u26ce\u26cf\u26d1\u26d3-\u26d4\u26e9-\u26ea' \
               '\u26f0-\u26f5\u26f7-\u26fa\u26fd\u2702\u2705\u2708-\u2709\u270a-\u270b\u270c-\u270d\u270f\u2712' \
               '\u2714\u2716\u271d\u2721\u2728\u2733-\u2734\u2744\u2747\u274c\u274e\u2753-\u2755\u2757\u2763-\u2764' \
               '\u2795-\u2797\u27a1\u27b0\u27bf\u2934-\u2935\u2b05-\u2b07\u2b1b-\u2b1c\u2b50\u2b55\u3030\u303d\u3297' \
               '\u3299\U0001f004\U0001f0cf\U0001f170-\U0001f171\U0001f17e\U0001f17f\U0001f18e\U0001f191-\U0001f19a' \
               '\U0001f1e6-\U0001f1ff\U0001f201-\U0001f202\U0001f21a\U0001f22f\U0001f232-\U0001f23a' \
               '\U0001f250-\U0001f251\U0001f300-\U0001f320\U0001f321\U0001f324-\U0001f32c\U0001f32d-\U0001f32f' \
               '\U0001f330-\U0001f335\U0001f336\U0001f337-\U0001f37c\U0001f37d\U0001f37e-\U0001f37f' \
               '\U0001f380-\U0001f393\U0001f396-\U0001f397\U0001f399-\U0001f39b\U0001f39e-\U0001f39f' \
               '\U0001f3a0-\U0001f3c4\U0001f3c5\U0001f3c6-\U0001f3ca\U0001f3cb-\U0001f3ce\U0001f3cf-\U0001f3d3' \
               '\U0001f3d4-\U0001f3df\U0001f3e0-\U0001f3f0\U0001f3f3-\U0001f3f5\U0001f3f7\U0001f3f8-\U0001f3ff' \
               '\U0001f400-\U0001f43e\U0001f43f\U0001f440\U0001f441\U0001f442-\U0001f4f7\U0001f4f8' \
               '\U0001f4f9-\U0001f4fc\U0001f4fd\U0001f4ff\U0001f500-\U0001f53d\U0001f549-\U0001f54a' \
               '\U0001f54b-\U0001f54e\U0001f550-\U0001f567\U0001f56f-\U0001f570\U0001f573-\U0001f579\U0001f57a' \
               '\U0001f587\U0001f58a-\U0001f58d\U0001f590\U0001f595-\U0001f596\U0001f5a4\U0001f5a5\U0001f5a8' \
               '\U0001f5b1-\U0001f5b2\U0001f5bc\U0001f5c2-\U0001f5c4\U0001f5d1-\U0001f5d3\U0001f5dc-\U0001f5de' \
               '\U0001f5e1\U0001f5e3\U0001f5e8\U0001f5ef\U0001f5f3\U0001f5fa\U0001f5fb-\U0001f5ff\U0001f600' \
               '\U0001f601-\U0001f610\U0001f611\U0001f612-\U0001f614\U0001f615\U0001f616\U0001f617\U0001f618' \
               '\U0001f619\U0001f61a\U0001f61b\U0001f61c-\U0001f61e\U0001f61f\U0001f620-\U0001f625' \
               '\U0001f626-\U0001f627\U0001f628-\U0001f62b\U0001f62c\U0001f62d\U0001f62e-\U0001f62f' \
               '\U0001f630-\U0001f633\U0001f634\U0001f635-\U0001f640\U0001f641-\U0001f642\U0001f643-\U0001f644' \
               '\U0001f645-\U0001f64f\U0001f680-\U0001f6c5\U0001f6cb-\U0001f6cf\U0001f6d0\U0001f6d1-\U0001f6d2' \
               '\U0001f6e0-\U0001f6e5\U0001f6e9\U0001f6eb-\U0001f6ec\U0001f6f0\U0001f6f3\U0001f6f4-\U0001f6f6' \
               '\U0001f910-\U0001f918\U0001f919-\U0001f91e\U0001f920-\U0001f927\U0001f930\U0001f933-\U0001f93a' \
               '\U0001f93c-\U0001f93e\U0001f940-\U0001f945\U0001f947-\U0001f94b\U0001f950-\U0001f95e' \
               '\U0001f980-\U0001f984\U0001f985-\U0001f991\U0001f9c0\u231a-\u231b\u23e9-\u23ec\u23f0\u23f3' \
               '\u25fd-\u25fe\u2614-\u2615\u2648-\u2653\u267f\u2693\u26a1\u26aa-\u26ab\u26bd-\u26be' \
               '\u26c4-\u26c5\u26ce\u26d4\u26ea\u26f2-\u26f3\u26f5\u26fa\u26fd\u2705\u270a-\u270b\u2728\u274c\u274e' \
               '\u2753-\u2755\u2757\u2795-\u2797\u27b0\u27bf\u2b1b-\u2b1c\u2b50\u2b55\U0001f004\U0001f0cf\U0001f18e' \
               '\U0001f191-\U0001f19a\U0001f1e6-\U0001f1ff\U0001f201\U0001f21a\U0001f22f\U0001f232-\U0001f236' \
               '\U0001f238-\U0001f23a\U0001f250-\U0001f251\U0001f300-\U0001f320\U0001f32d-\U0001f32f' \
               '\U0001f330-\U0001f335\U0001f337-\U0001f37c\U0001f37e-\U0001f37f\U0001f380-\U0001f393' \
               '\U0001f3a0-\U0001f3c4\U0001f3c5\U0001f3c6-\U0001f3ca\U0001f3cf-\U0001f3d3\U0001f3e0-\U0001f3f0' \
               '\U0001f3f4\U0001f3f8-\U0001f3ff\U0001f400-\U0001f43e\U0001f440\U0001f442-\U0001f4f7\U0001f4f8' \
               '\U0001f4f9-\U0001f4fc\U0001f4ff\U0001f500-\U0001f53d\U0001f54b-\U0001f54e\U0001f550-\U0001f567' \
               '\U0001f57a\U0001f595-\U0001f596\U0001f5a4\U0001f5fb-\U0001f5ff\U0001f600\U0001f601-\U0001f610' \
               '\U0001f611\U0001f612-\U0001f614\U0001f615\U0001f616\U0001f617\U0001f618\U0001f619\U0001f61a' \
               '\U0001f61b\U0001f61c-\U0001f61e\U0001f61f\U0001f620-\U0001f625\U0001f626-\U0001f627' \
               '\U0001f628-\U0001f62b\U0001f62c\U0001f62d\U0001f62e-\U0001f62f\U0001f630-\U0001f633\U0001f634' \
               '\U0001f635-\U0001f640\U0001f641-\U0001f642\U0001f643-\U0001f644\U0001f645-\U0001f64f' \
               '\U0001f680-\U0001f6c5\U0001f6cc\U0001f6d0\U0001f6d1-\U0001f6d2\U0001f6eb-\U0001f6ec' \
               '\U0001f6f4-\U0001f6f6\U0001f910-\U0001f918\U0001f919-\U0001f91e\U0001f920-\U0001f927\U0001f930' \
               '\U0001f933-\U0001f93a\U0001f93c-\U0001f93e\U0001f940-\U0001f945\U0001f947-\U0001f94b' \
               '\U0001f950-\U0001f95e\U0001f980-\U0001f984\U0001f985-\U0001f991\U0001f9c0\U0001f3fb-\U0001f3ff' \
               '\u261d\u26f9\u270a-\u270b\u270c-\u270d\U0001f385\U0001f3c2-\U0001f3c4\U0001f3c7\U0001f3ca' \
               '\U0001f3cb-\U0001f3cc\U0001f442-\U0001f443\U0001f446-\U0001f450\U0001f466-\U0001f469\U0001f46e' \
               '\U0001f470-\U0001f478\U0001f47c\U0001f481-\U0001f483\U0001f485-\U0001f487\U0001f4aa' \
               '\U0001f574-\U0001f575\U0001f57a\U0001f590\U0001f595-\U0001f596\U0001f645-\U0001f647' \
               '\U0001f64b-\U0001f64f\U0001f6a3\U0001f6b4-\U0001f6b6\U0001f6c0\U0001f6cc\U0001f918' \
               '\U0001f919-\U0001f91c\U0001f91e\U0001f926\U0001f930\U0001f933-\U0001f939\U0001f93d-\U0001f93e'
_TXT_VARIATION = '\uFE0E'
_EMO_VARIATION = '\uFE0F'
_FITZ_MODIFIER = '\U0001F3FB-\U0001F3FF'
_KC_MODIFIER = '\u20E3'
_ZWJ = '\u200D'
_FLAGS = '\U0001F1E6-\U0001F1FF'
_KEY_CAPS = '0-9\*#'
_EMOJI_REGEX = (
    r'(?P<emoji>'
        r'(?:'
            r'(?:[%(key_caps)s](?:%(emo_variation)s)?%(kc_modifier)s)'
            r'|'
            r'(?:[%(flags)s]){2}'
            r'|'
            r'(?:[%(emojis)s])(?!%(txt_variation)s)'
        r')'
        r'(?:'
            r'(?:(?:%(emo_variation)s)?(?:[%(fitz_modifier)s]))'  # fitzpatrick modifier
            r'|'
            r'(?:(?:%(emo_variation)s)?(?:[%(zwj)s])(?:.)){1,4}'  # Multi glyphs (up to 4)
            r'|'
            r'(?:%(emo_variation)s)'  # Emoji variation
        r')?'
    r')'
    ) % {
        'emojis': _CODE_POINTS,
        'txt_variation': _TXT_VARIATION,
        'emo_variation': _EMO_VARIATION,
        'fitz_modifier': _FITZ_MODIFIER,
        'zwj': _ZWJ,
        'flags': _FLAGS,
        'kc_modifier': _KC_MODIFIER,
        'key_caps': _KEY_CAPS
    }

REGEX_MATCHING_EMOJI = ''.join([
    r'^[^*&%\s]+\.png\/',  # http://stackoverflow.com/questions/10324228/
    _EMOJI_REGEX,
    r'*$'
])

# prepare
PROMPT_SET_TITLE = 'Title of this set -> '
PROMOT_SET_SHORTNAME = 'Identifier of this set -> '

NOTICE_START_GENERATE = 'Generating definition for %s'
NOTICE_DONE_GENERATE = 'Done generating for %s at %s'
NOTICE_GO_EDIT_DEFS = 'You can now open definitions and assign emojis to stickers. ' \
                      'Uploader will automatically assign MEDIUM WHITE CIRCLE to any sticker that has none.'

ERROR_EOF_FROM_INPUT = 'EOF detected, skipping this set...'

# cli
CLI_SHELP_UPLOAD_COMMAND = 'Upload sticker sets to Telegram.'
CLI_SHELP_UPLOAD_SUBFLAG = 'Subscribe to created set(s).'
CLI_SHELP_PREPARE_COMMAND = 'Generate sticker set definition.'
CLI_SHELP_LOGOUT_COMMAND = 'Log out from Telegram.'
ERROR_NOT_LOGGEDIN = 'You are not logged in.'
