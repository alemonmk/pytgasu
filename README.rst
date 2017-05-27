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
There does is a `Telegram Stickers Uploader <http://telegramsu.lostberry.com/>`_, but:

1. It has limited choices of emojis
    - Well, 250. Really? This is not enough. UTR #51 4.0 defined 910 code points with Emoji_Presentation=Yes.

2. It does not work with current Telegram Desktop
    - It does send commands through it, but it cannot upload anything. At least not for me.

And now you have this.

Installation
------------

Requirement
+++++++++++
- Python >= 3.5

Dependency
++++++++++
- `Telethon <https://github.com/LonamiWebs/Telethon>`_
- `Click <http://github.com/mitsuhiko/click>`_
- `regex <https://bitbucket.org/mrabarnett/mrab-regex>`_
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

Generate set definition
+++++++++++++++++++++++
You need set definition file for each sticker set you want to create.

Generate definition files by running and enter some detail:

.. code-block:: bash

    $ pytgasu defgen <dir>...

Then open the generate ``.ssd`` file with text editor of your choice to assign emojis (and **only** emojis, preferably copied from Telegram).

Upload sticker sets
+++++++++++++++++++
Once you are done editing the ``.ssd`` file(s), you can let ``pytgasu`` do the heavy lifting.

.. code-block:: bash

    $ pytgasu upload (<dir>|<path_to.ssd>)...

By specifying ``upload -s``, it also automatically subscribe to the set once it's uploaded.

You have to log in to Telegram at the first run, it won't ask you again after that. A Telegram session file will be created at ``~/.pytgasu/asu.session``.

Log out of Telegram
+++++++++++++++++++
If you have no business with ``pytgasu`` anymore, you may want to log it out from Telegram.

.. code-block:: bash

    $ pytgasu logout

This terminates your session from Telegram and deletes the stored session file and its folder, saving you few clicks in other Telegram client and file manager.

Limitions & TODOs
-----------------
1. It does not help scale up/down if image is not appropriate size.
    - I can bundle ``waifu2x-caffe``, but that would be a Windows-only feature.
2. It does not help sink image file size if it is too large.
    - I will bundle ``pngquant``.
3. No GUI.
    - Well...I hope you are crazy enough to make one for me ;)

Contributing
------------
Please create feature requests, leave suggestions through `GitHub issue <https://github.com/alemonmk/pytgasu/issues>`_, or just code and fire a `pull request <https://github.com/alemonmk/pytgasu/pulls>`_.

It's okay to talk via e-mail if you want to stay private or just don't bother with GitHub.

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
