#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Jack Cherng
# https://github.com/jfcherng/SublimeLinter-contrib-gcc
# Copyright (c) 2017 jfcherng
#
# License: MIT
#

from SublimeLinter.lint import Linter, persist
import os
import shlex
import string
import sublime


def get_project_folder():
    proj_file = sublime.active_window().project_file_name()
    if proj_file:
        return os.path.dirname(proj_file)
    # Use current file's folder when no project file is opened.
    return os.path.dirname( sublime.active_window().active_view().file_name() )


def apply_template(s):
    mapping = {
        "project_folder": get_project_folder()
    }
    templ = string.Template(s)
    return templ.safe_substitute(mapping)


class Gcc(Linter):
    """ Provides an interface to gcc. """

    cmd = None
    executable = 'gcc'
    multiline = False
    syntax = ('c', 'c improved', 'c++', 'c++11')
    regex = (
        r'<stdin>:(?P<line>\d+):(?P<col>\d+):\s*'
        r'.*?((?P<error>error)|(?P<warning>warning|note)):\s*'
        r'(?P<message>.+)'
    )

    defaults = {
        'include_dirs': [],
        'extra_flags': ""
    }

    base_cmd = (
        '-c '
        '-fsyntax-only '
        '-Wall '
        '-O0 '
    )

    def cmd(self):
        """
        Return the command line to execute.

        We override this method, so we can add extra flags and include paths
        based on the 'include_dirs' and 'extra_flags' settings.
        """

        result = self.executable + ' ' + self.base_cmd
        settings = self.get_view_settings()
        include_dirs = settings.get('include_dirs', [])

        result += apply_template( settings.get('extra_flags', '') )

        if include_dirs:
            result += apply_template( ''.join([' -I' + shlex.quote(include) for include in include_dirs]) )

        if persist.get_syntax(self.view) in ['c', 'c improved']:
            code_type = 'c'
        else:
            code_type = 'c++'

        # to compile code from the standard input
        result += ' -x {0} -'.format(code_type)

        return result
