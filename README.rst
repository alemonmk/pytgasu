=======
PyTgASU
=======

Telegram sticker sets creation automated (partially).

Features
--------
PyTgASU frees you from selecting files and emojis repeatedly when creating sticker sets on Telegram.

Better yet, it makes sticker sets kind of "distributable" and "installable".

Motivation
----------
There was a `Telegram Stickers Uploader <http://telegramsu.lostberry.com/>`_ (link dead, don't bother), but:

1. It has limited choices of emojis
    - Well, 250. Really? This is not enough. UTR #51 4.0 defined 910 code points with Emoji_Presentation=Yes.

2. It does not work with current Telegram Desktop
    - It does send commands through it, but it cannot upload anything. At least not for me.

And now ``pytgasu`` comes to your rescue.

Installation
------------

Requirement
+++++++++++
- Python >= 3.5

Dependency
++++++++++
- `Telethon <https://github.com/LonamiWebs/Telethon>`_
- `Click <http://github.com/mitsuhiko/click>`_
- `Pillow <https://python-pillow.org/>`_

Use ``pip`` to install:

.. code-block:: bash

    $ pip install pytgasu

or

.. code-block:: bash

   $ git clone https://github.com/alemonmk/pytgasu.git
   $ cd pytgasu
   $ pip install .

Usage
-----

Prepare set
+++++++++++
``pytgasu`` needs to work with set definition file for each sticker set you want to create.

Telegram also has limitations on sticker images.

You can take care of all above with this command:

.. code-block:: bash

    $ pytgasu prepare <dir>...

At first launch it will ask you paths to some tools (namely pngquant and waifu2x-caffe), if you prefer not using any of them you can just leave it empty. This saves a yaml-formatted configuration file at ``~/.pytgasu/asu.cfg``.

You need to provide a descriptive name of the set, and a short name that enables you to share it with ``https://t.me/addsticker/<short_name>``.

Finally open the generated ``.def`` file(s) with text editor of your choice to assign emojis (and **only** emojis, preferably copied from Telegram).

Upload sticker sets
+++++++++++++++++++
Once you are done editing the ``.def`` file(s), let ``pytgasu`` do the heavy lifting.

.. code-block:: bash

    $ pytgasu upload [-s] (<dir>|<path_to.def>)...

By specifying ``-s``, you will be automatically subscribed to the set once it's uploaded.

You have to log in to Telegram at the first run. A session file will be created at ``~/.pytgasu/asu.session``.

Log out of Telegram
+++++++++++++++++++
If you have no more business with ``pytgasu``, you may want to log it out from Telegram.

.. code-block:: bash

    $ pytgasu logout

This terminates your session to Telegram, deletes the stored session file and its folder, saving you few clicks in other Telegram client and file manager.

Limitions & TODOs
-----------------
1. No GUI.
    - Well...I hope you are crazy enough to make one for me ;)

Contributing
------------
You may request new features, report bugs or leave suggestions through `GitHub issue <https://github.com/alemonmk/pytgasu/issues>`_, or just code and fire a `pull request <https://github.com/alemonmk/pytgasu/pulls>`_.

You may contact me via e-mail if you want to stay private or just don't bother with GitHub.

Stuff in need
+++++++++++++
- Tests. Preferably something ``nose`` uses.
- Better documents. There's not much to document though ...
- Feature requests. Keep it simple, don't complicate this tool.
- Debug. I'm not that exhaustive and may leave edge cases here and there.

Author
------
\(c) 2017 Lemon Lam <'%s@%s' % ('almk', 'rmntn.net')>

License
-------
Licensed under `GNU General Public License Version 3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_.
