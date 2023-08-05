#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Cross-platform Sound Playing with StdLib only,No Sound file required."""


import logging as log
import os
import sys

from shutil import which
from subprocess import run
from tempfile import gettempdir


def beep(waveform=(79, 45, 32, 50, 99, 113, 126, 127)):
    """Cross-platform Sound Playing with StdLib only,No Sound file required."""
    log.debug("Generating and Playing Sound...")
    wavefile = os.path.join(gettempdir(), "beep.wav")
    if not os.path.isfile(wavefile) or not os.access(wavefile, os.R_OK):
        with open(wavefile, "w+") as wave_file:
            for sample in range(0, 1000, 1):
                for wav in range(0, 8, 1):
                    wave_file.write(chr(waveform[wav]))
    if sys.platform.startswith("linux"):
        repro = which("aplay")
        return not bool(run("{repro} '{fyle}'".format(
            fyle=wavefile, repro=repro), shell=True).returncode)
    elif sys.platform.startswith("darwin"):
        repro = which("afplay")
        return not bool(run("{repro} '{fyle}'".format(
            fyle=wavefile, repro=repro), shell=True).returncode)
    elif sys.platform.startswith("win"):  # FIXME: This is Ugly.
        log.debug("Playing Sound Natively not supported by this OS.")
        return False  # this SHOULD work on all windows,but it doesnt :(
        # return run("start /low /min '{fyle}'".format(fyle=wavefile),shell=1)
