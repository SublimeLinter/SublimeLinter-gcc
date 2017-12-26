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

from SublimeLinter.lint import Linter, persist, util
import os
import shlex
import string
import sublime
import sublime_plugin
import tempfile


def get_SL_version():
    if hasattr(persist, 'get_syntax'):
        return '3'

    return '4'


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

    return string.Template(s).safe_substitute(mapping)


class Gcc(Linter):
    """ Provides an interface to gcc. """

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

    default_settings = {
        'executable': 'gcc',
        'extra_flags': '',
        'include_dirs': [],
    }

    common_flags = [
        '-c',
        '-Wall',
        '-O0',
    ]

    # SublimeLinter capture settings
    multiline = True
    syntax = list(c_syntaxes | cpp_syntaxes)
    regex = (
        r'<stdin>:(?P<line>\d+):((?P<col>\d+):)?\s*'
        r'.*?((?P<error>error)|(?P<warning>warning|note)):\s*'
        r'(?P<message>.+)'
    )

    if get_SL_version() == '3':
        # We would like to bind "executable" later in cmd(self), but
        # if "executable" is not found here, this linter won't be activated.
        # The following if-branch just makes sure an "executable" could be found.
        if sublime.platform() == 'windows':
            # Windows OS would have "cmd" (or "explorer") binary in its PATH
            executable = 'cmd'
        else:
            # A non-Windows OS would have "cat" binary in its PATH?
            executable = 'cat'

    cmd_template = '{executable} {common_flags} {extra_flags} {include_dirs} -x {c_or_cpp} -o {garbage_file} -'

    def cmd(self):
        """
        Return the command line to be executed.

        We override this method, so we can change executable, add extra flags
        and include paths based on settings.
        """

        settings = self.get_view_settings()

        if get_SL_version() == '3':
            syntax = persist.get_syntax(self.view)
        else:
            syntax = util.get_syntax(self.view)

        if syntax in self.c_syntaxes:
            c_or_cpp = 'c'
        else:
            c_or_cpp = 'c++'

        if sublime.platform() == 'windows':
            garbage_file = tempfile.gettempdir() + r'\SublimeLinter-contrib-gcc.o'
        else:
            garbage_file = '/dev/null'

        base_settings = {
            'executable'   : settings.get('executable',   self.default_settings['executable']),
            'extra_flags'  : settings.get('extra_flags',  self.default_settings['extra_flags']),
            'include_dirs' : settings.get('include_dirs', self.default_settings['include_dirs']),
        }

        merged_settings = {
            'executable'   : settings.get(c_or_cpp + '_executable',   base_settings['executable']),
            'extra_flags'  : settings.get(c_or_cpp + '_extra_flags',  base_settings['extra_flags']),
            'include_dirs' : settings.get(c_or_cpp + '_include_dirs', base_settings['include_dirs']),
        }

        return self.cmd_template.format(
            executable = merged_settings['executable'],
            common_flags = ' '.join(self.common_flags),
            extra_flags = apply_template(merged_settings['extra_flags']),
            include_dirs = apply_template(
                ' '.join({
                    '-I' + shlex.quote(include_dir)
                    for include_dir in merged_settings['include_dirs']
                })
            ),
            c_or_cpp = c_or_cpp,
            garbage_file = shlex.quote(garbage_file),
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


class SublimeLinterContribGccRunTests(sublime_plugin.WindowCommand):
    """
    To do unittests, run the following command in ST's console:

    window.run_command('sublime_linter_contrib_gcc_run_tests')
    """

    def run(self):
        from .tests.regex_tests import run_tests

        run_tests(Gcc.regex)
