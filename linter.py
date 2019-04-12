#
# linter.py
# Linter for SublimeLinter4, a code checking framework for Sublime Text 3
#
# Written by Jack Cherng
# Copyright (c) 2017-2019 jfcherng
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

    return getattr(SublimeLinter.lint, "VERSION", 3)


def get_syntax():
    """
    Return the lowercase syntax name of the current view.
    """

    view = sublime.active_window().active_view()

    if get_SL_version() == 3:
        return persist.get_syntax(view)
    else:
        return util.get_syntax(view)


def get_project_folder():
    """
    Return the current project directory.
    """

    project_file = sublime.active_window().project_file_name()

    # use current file's folder when no project file is opened
    if not project_file:
        project_file = sublime.active_window().active_view().file_name()

    return os.path.dirname(project_file) if project_file else "."


def apply_template(s):
    """
    Return a string with variables inside it gets interpreted.
    """

    # fmt: off
    mapping = {
        "project_folder": get_project_folder(),
    }
    # fmt: on

    return string.Template(s).safe_substitute(mapping)


class Gcc(Linter):
    """
    Provides an interface to gcc/g++.
    """

    # fmt: off
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

    defaults = {
        'executable': 'gcc',
        'extra_flags': [],
        'include_dirs': [],
    }
    # fmt: on

    if sublime.platform() == "windows":
        garbage_file = os.path.join(tempfile.gettempdir(), "SublimeLinter-gcc.o")
    else:
        garbage_file = "/dev/null"

    cmd_template = " ".join(
        [
            "{executable}",
            "{common_flags}",
            "{extra_flags}",
            "{include_dirs}",
            "-x {c_or_cpp}",
            "-o {garbage_file}",
            "-",
        ]
    )

    # SublimeLinter capture settings
    executable = None
    on_stderr = None  # handle stderr via split_match
    multiline = True
    syntax = list(c_syntaxes | cpp_syntaxes)
    regex = (
        r"<stdin>:(?P<line>\d+):((?P<col>\d+):)?\s*"
        r".*?((?P<error>error)|(?P<warning>warning|note)):\s*"
        r"(?P<message>.+)"
    )

    if get_SL_version() == 3:
        # Note: This is a dirty hack to use a dynamical "executable" for SL3.
        #
        # If "executable" is not found here, this linter just won't be activated.
        # The following if-branch makes sure an "executable" could be found.
        # The actual "executable" is in the returned command from cmd(self).
        #
        # @see https://git.io/vb5Nb
        executable = "cmd" if sublime.platform() == "windows" else "cat"

    def cmd(self):
        """
        Return the command line to be executed.

        We override this method, so we can change executable, add extra flags
        and include directories basing on settings.
        """

        c_or_cpp = "c" if get_syntax() in self.c_syntaxes else "c++"
        settings = self.get_syntax_specific_settings(c_or_cpp)

        return self.cmd_template.format(
            executable=settings["executable"],
            common_flags=" ".join(self.common_flags),
            extra_flags=apply_template(" ".join(settings["extra_flags"])),
            include_dirs=apply_template(
                " ".join(
                    {"-I" + shlex.quote(include_dir) for include_dir in settings["include_dirs"]}
                )
            ),
            c_or_cpp=c_or_cpp,
            garbage_file=shlex.quote(self.garbage_file),
        )

    def get_syntax_specific_settings(self, c_or_cpp):
        """
        Return the syntax specific settings.
        """

        settings = self.get_view_settings()

        ret = {
            attr: settings.get(
                "{}_{}".format(c_or_cpp, attr), settings.get(attr, self.defaults[attr])
            )
            for attr in self.defaults
        }

        # append the directory of the current file to the include directory
        file_path = self.view.file_name()
        if file_path:
            ret["include_dirs"].append(os.path.dirname(file_path))

        # just for BC, always convert "extra_flags" into a list
        if isinstance(ret["extra_flags"], str):
            ret["extra_flags"] = shlex.split(ret["extra_flags"])

        return ret


class SublimeLinterGccRunTests(sublime_plugin.WindowCommand):
    """
    To do unittests, run the following command in ST's console:
    window.run_command('sublime_linter_gcc_run_tests')
    """

    def run(self):
        from .tests.regex_tests import run_tests

        run_tests(Gcc.regex)
