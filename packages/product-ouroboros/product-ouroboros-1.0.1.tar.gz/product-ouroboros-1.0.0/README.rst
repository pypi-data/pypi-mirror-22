ouroboros
=========

A wrapper for the moviepy library.

Required -Python 3.\_ -moviepy

Common Errors Encountered
-------------------------

ImageIO and FFMPEG Error
~~~~~~~~~~~~~~~~~~~~~~~~

Open an interactive python shell by running:

::

    python3

Within the interactive shell run the commands:

::

    import imageio
    imageio.plugins.ffmpeg.download()

This will fix the issue.

Not Valid Win32 Application.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you get the error:

::

    'osError: [WinError 193] %1 is not a valid Win32 application' 

then your ffmpeg doesn't match your python install, 32-bit or 64-bit. A
manual install of ffmeg can fix this.
