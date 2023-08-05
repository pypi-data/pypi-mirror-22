#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Determine OS and set copy() and paste() functions accordingly."""


import logging as log
import os
import subprocess
import sys

from shutil import which
from typing import NamedTuple


# Dot notation and static typed and built-in version of collections.namedtuple.
Clipboard = NamedTuple("Clipboard", fields=(("copy", callable),
                                            ("paste", callable)))


def __osx_clipboard():
    def copy_osx(text):
        subprocess.run(["pbcopy"], timeout=9, input=text.encode('utf-8'))

    def paste_osx():
        os.environ["LANG"] = "en_US.utf-8"
        return subprocess.run(["pbpaste"], stdout=subprocess.PIPE,
                              timeout=9).stdout.decode("utf-8")

    return copy_osx, paste_osx


def __xclip_clipboard():
    def copy_xclip(text):
        subprocess.run(("xclip", "-selection", "clipboard"),
                       timeout=9, input=text.encode('utf-8'))
        if which("xsel"):
            subprocess.run(("xclip", "-selection", "primary"),
                           timeout=9, input=text.encode('utf-8'))

    def paste_xclip():
        return subprocess.run((
            "xclip", "-selection", "primary" if which("xsel") else "clipboard",
            "-o"), stdout=subprocess.PIPE, timeout=9).stdout.decode("utf-8")

    return copy_xclip, paste_xclip


def __win32_clibboard():
    import win32clipboard
    import win32con

    def copy_win32(text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()

    def paste_win32():
        win32clipboard.OpenClipboard()
        text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return text

    return copy_win32, paste_win32


def __determine_clipboard():
    """Determine OS and set copy() and paste() functions accordingly."""
    if sys.platform.startswith("darwin"):
        return __osx_clipboard()
    elif sys.platform.startswith("win"):
        try:  # Determine which command/module is installed, if any.
            import win32clipboard  # lint:ok noqa
            assert win32clipboard
        except ImportError:
            log.error("Install Win32 API Python packages for Windows.")
            return None, None  # install Win32.
        else:
            return __win32_clibboard()
    elif sys.platform.startswith("linux") and which("xclip"):
        return __xclip_clipboard()
    else:
        log.error("Install XClip and XSel Linux Packages at least.")
        return None, None  # install Qt or GTK or Tk or XClip.


def get_clipboard():
    """Crossplatform crossdesktop Clipboard."""
    log.debug("Querying Copy/Paste Clipboard functionality.")
    global clipboard_copy, clipboard_paste
    clipboard_copy, clipboard_paste = None, None
    clipboard_copy, clipboard_paste = __determine_clipboard()
    return Clipboard(clipboard_copy, clipboard_paste)
