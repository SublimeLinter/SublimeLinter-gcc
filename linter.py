#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Jack Cherng
# https://github.com/jfcherng/SublimeLinter-contrib-gcc
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
import SublimeLinter
import tempfile


def get_SL_version():
    """
    Return the major version number of SublimeLinter.
    """

    return getattr(SublimeLinter.lint, 'VERSION', 3)


def get_project_folder():
    proj_file = sublime.active_window().project_file_name()
    if proj_file:
        return os.path.dirname(proj_file)

    # use current file's folder when no project file is opened
    proj_file = sublime.active_window().active_view().file_name()
    if proj_file:
        return os.path.dirname(proj_file)

    return '.'


def apply_template(s):
    mapping = {
        'project_folder': get_project_folder(),
    }

    return string.Template(s).safe_substitute(mapping)


class Gcc(Linter):
    """
    Provides an interface to gcc/g++.
    """

    c_syntaxes = {
        'c',
        'c99',
        'c11',
        'c improved',
    }

    cpp_syntaxes = {
        'c++',
        'c++11',
    }

    common_flags = [
        '-c',
        '-Wall',
        '-O0',
    ]

    default_settings = {
        'executable': 'gcc',
        'extra_flags': [],
        'include_dirs': [],
    }

    if sublime.platform() == 'windows':
        garbage_file = tempfile.gettempdir() + r'\SublimeLinter-contrib-gcc.o'
    else:
        garbage_file = '/dev/null'

    cmd_template = '{executable} {common_flags} {extra_flags} {include_dirs} -x {c_or_cpp} -o {garbage_file} -'

    # SublimeLinter capture settings
    executable = None
    multiline = True
    syntax = list(c_syntaxes | cpp_syntaxes)
    regex = (
        r'<stdin>:(?P<line>\d+):((?P<col>\d+):)?\s*'
        r'.*?((?P<error>error)|(?P<warning>warning|note)):\s*'
        r'(?P<message>.+)'
    )

    if get_SL_version() == 3:
        # Note: This is a dirty hack to use a dynamical "executable".
        #
        # If "executable" is not found here, this linter just won't be activated.
        # The following if-branch makes sure an "executable" could be found.
        # The actual "executable" is in the returned command from cmd(self).
        #
        # @see https://git.io/vb5Nb
        executable = 'cmd' if sublime.platform() == 'windows' else 'cat'

    def cmd(self):
        """
        Return the command line to be executed.

        We override this method, so we can change executable, add extra flags
        and include paths based on settings.
        """

        c_or_cpp = 'c' if self.get_syntax() in self.c_syntaxes else 'c++'
        settings = self.get_syntax_specific_settings(c_or_cpp)

        return self.cmd_template.format(
            executable = settings['executable'],
            common_flags = ' '.join(self.common_flags),
            extra_flags = apply_template(' '.join(settings['extra_flags'])),
            include_dirs = apply_template(' '.join({
                '-I' + shlex.quote(include_dir)
                for include_dir in settings['include_dirs']
            })),
            c_or_cpp = c_or_cpp,
            garbage_file = shlex.quote(self.garbage_file),
        )

    @classmethod
    def can_lint_syntax(cls, syntax):
        """
        Return whether a linter can lint a given syntax.

        Subclasses may override this if the built in mechanism in can_lint
        is not sufficient. When this method is called, cls.executable_path
        has been set. If it is '', that means the executable was not specified
        or could not be found.
        """

        return True

    def get_syntax(self):
        """
        Return the lowercase syntax name of the current view.
        """

        if get_SL_version() == 3:
            return persist.get_syntax(self.view)
        else:
            return util.get_syntax(self.view)

    def get_syntax_specific_settings(self, c_or_cpp):
        settings = self.get_view_settings()

        ret = {
            attr: settings.get(
                "{}_{}".format(c_or_cpp, attr),
                settings.get(attr, self.default_settings[attr])
            )
            for attr in self.default_settings
        }

        # always convert "extra_flags" into a list
        if isinstance(ret['extra_flags'], str):
            ret['extra_flags'] = shlex.split(ret['extra_flags'])

        return ret


class SublimeLinterContribGccRunTests(sublime_plugin.WindowCommand):
    """
    To do unittests, run the following command in ST's console:

    window.run_command('sublime_linter_contrib_gcc_run_tests')
    """

    def run(self):
        from .tests.regex_tests import run_tests

        run_tests(Gcc.regex)
