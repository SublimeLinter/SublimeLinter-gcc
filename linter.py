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
    proj_file = sublime.active_window().active_view().file_name()
    if proj_file:
        return os.path.dirname(proj_file)
    return '.'


def apply_template(s):
    mapping = {
        'project_folder': get_project_folder(),
    }
    templ = string.Template(s)
    return templ.safe_substitute(mapping)


class Gcc(Linter):
    """ Provides an interface to gcc. """

    # We would like to bind "executable" later in cmd(self), but
    # if "executable" is not found here, this linter won't be activated.
    # The following if-branch just makes sure an "executable" could be found.
    if sublime.platform() == 'windows':
        # Windows OS would have "cmd" (or "explorer") binary in its PATH
        executable = 'cmd'
    else:
        # A non-Windows OS would have "cat" binary in its PATH?
        executable = 'cat'

    multiline = False
    syntax = ('c', 'c improved', 'c++', 'c++11')
    regex = (
        r'<stdin>:(?P<line>\d+):(?P<col>\d+):\s*'
        r'.*?((?P<error>error)|(?P<warning>warning|note)):\s*'
        r'(?P<message>.+)'
    )

    default_settings = {
        'executable': 'gcc',
        'extra_flags': '',
        'include_dirs': [],
    }

    base_flags = (
        '-c '
        '-fsyntax-only '
        '-Wall '
        '-O0 '
    )

    def cmd(self):
        """
        Return the command line to be executed.

        We override this method, so we can change executable, add extra flags
        and include paths based on settings.
        """

        if persist.get_syntax(self.view) in ['c', 'c improved']:
            code_type = 'c'
        else:
            code_type = 'c++'

        settings = self.get_view_settings()
        executable = settings.get(code_type + '_executable', settings.get('executable', self.default_settings['executable']))
        include_dirs = settings.get(code_type + "_include_dirs", settings.get('include_dirs', self.default_settings['include_dirs']))
        extra_flags = settings.get(code_type + "_extra_flags", settings.get('extra_flags', self.default_settings['extra_flags']))

        cmd = executable + ' ' + self.base_flags + apply_template(extra_flags)

        if include_dirs:
            cmd += apply_template(''.join([' -I' + shlex.quote(include) for include in include_dirs]))

        # to compile code from the standard input
        cmd += ' -x {0} -'.format(code_type)

        return cmd
