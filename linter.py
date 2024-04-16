#
# linter.py
# Linter for SublimeLinter4, a code checking framework for Sublime Text 3
#
# Written by Jack Cherng
# Copyright (c) 2017-2024 jfcherng
#
# License: MIT
#

from __future__ import annotations

import os
import re
import tempfile

import sublime
import sublime_plugin
from SublimeLinter.lint import Linter

OUTPUT_RE = re.compile(
    r"<stdin>:(?P<line>\d+):((?P<col>\d+):)?\s*"
    + r".*?((?P<error>error)|(?P<warning>warning|note)):\s*"
    + r"(?P<message>.+)",
    re.MULTILINE,
)


def get_garbabge_file_path() -> str:
    """
    @brief Get the path for generated garbabge file.

    Some checks are not performed when flag "-fsyntax-only" is given.
    To perform those checks in optimization phase, we must do a real compilation.
    This garbage file path is just a dummy output file for that compilation.

    @ref https://github.com/SublimeLinter/SublimeLinter-gcc/issues/4
    @return string The garbabge file path.
    """

    if sublime.platform() == "windows":
        return os.path.join(tempfile.gettempdir(), "SublimeLinter-gcc.o")
    return "/dev/null"


class Gcc(Linter):
    name = "gcc"
    cmd = "gcc ${args} -"
    regex = OUTPUT_RE
    multiline = True
    on_stderr = None

    defaults = {
        "selector": "source.c",
        "args": ["-c", "-Wall", "-O0"],
        "-I +": [],
        "-x": "c",
        "-o": get_garbabge_file_path(),
    }


class GPlusPlus(Linter):
    name = "g++"
    cmd = "g++ ${args} -"
    regex = OUTPUT_RE
    multiline = True
    on_stderr = None

    defaults = {
        "selector": "source.c++",
        "args": ["-c", "-Wall", "-O0"],
        "-I +": [],
        "-x": "c++",
        "-o": get_garbabge_file_path(),
    }


class SublimeLinterGccRunTests(sublime_plugin.WindowCommand):
    """
    To do unittests, run the following command in ST's console:
    window.run_command('sublime_linter_gcc_run_tests')
    """

    def run(self) -> None:
        from .tests.regex_tests import run_tests

        run_tests(Gcc.regex)
