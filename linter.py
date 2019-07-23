#
# linter.py
# Linter for SublimeLinter4, a code checking framework for Sublime Text 3
#
# Written by Jack Cherng
# Copyright (c) 2017-2018 jfcherng
#
# License: MIT
#

from SublimeLinter.lint import Linter, persist, util
import os
import shlex
import string
import sublime
import sublime_plugin
import SublimeLinter.lint
import tempfile


def get_SL_version():
    """
    Return the major version number of SublimeLinter.
    """

    return getattr(SublimeLinter.lint, 'VERSION', 3)


def get_project_folder():
    """
    Return the current project directory.
    """

    project_file = sublime.active_window().project_file_name()

    # use current file's folder when no project file is opened
    if not project_file:
        project_file = sublime.active_window().active_view().file_name()

    return os.path.dirname(project_file) if project_file else '.'


def apply_template(s):
    """
    Return a string with variables inside it gets interpreted.
    """

    mapping = {
        'project_folder': get_project_folder(),
    }

    return string.Template(s).safe_substitute(mapping)


def get_executable():
  if get_SL_version() == 3:
    # Note: This is a dirty hack to use a dynamical "executable" for SL3.
    #
    # If "executable" is not found here, this linter just won't be activated.
    # The following if-branch makes sure an "executable" could be found.
    # The actual "executable" is in the returned command from cmd(self).
    #
    # @see https://git.io/vb5Nb
    return 'cmd' if sublime.platform() == 'windows' else 'cat'
  return 'gcc'

class Gcc(Linter):
    """
    Provides an interface to gcc/g++.
    """
    common_flags = [
        '-c',
        '-Wall',
        '-O0',
        '-x c',
    ]

    default_settings = {
        'executable': get_executable(),
        'extra_flags': [],
        'include_dirs': [],
    }

    defaults = {
        'selector': "source.c",
    }

    if sublime.platform() == 'windows':
        garbage_file = os.path.join(tempfile.gettempdir(), 'SublimeLinter-gcc.o')
    else:
        garbage_file = '/dev/null'

    cmd_template = '{executable} {common_flags} {extra_flags} {include_dirs} -o {garbage_file} -'

    # SublimeLinter capture settings
    on_stderr = None  # handle stderr via split_match
    multiline = True
    regex = (
        r'<stdin>:(?P<line>\d+):((?P<col>\d+):)?\s*'
        r'.*?((?P<error>error)|(?P<warning>warning|note)):\s*'
        r'(?P<message>.+)'
    )

    def cmd(self):
        """
        Return the command line to be executed.

        We override this method, so we can change executable, add extra flags
        and include directories basing on settings.
        """
        extra_flags = self.settings['extra_flags']
        if isinstance(extra_flags, list):
          extra_flags = ' '.join(extra_flags)
        return self.cmd_template.format(
            executable = self.settings['executable'],
            common_flags = ' '.join(self.common_flags),
            extra_flags = apply_template(extra_flags),
            include_dirs = apply_template(' '.join({
                '-I' + shlex.quote(include_dir)
                for include_dir in self.settings['include_dirs']
            })),
            garbage_file = shlex.quote(self.garbage_file),
        )

class GccPlus(Gcc):
    name = "gcc++"
    is_cpp = True

    common_flags = [
        '-c',
        '-Wall',
        '-O0',
        '-x c++',
    ]

    defaults = {
        'selector': "source.c++",
    }


class SublimeLinterGccRunTests(sublime_plugin.WindowCommand):
    """
    To do unittests, run the following command in ST's console:
    window.run_command('sublime_linter_gcc_run_tests')
    """

    def run(self):
        from .tests.regex_tests import run_tests

        run_tests(Gcc.regex)
