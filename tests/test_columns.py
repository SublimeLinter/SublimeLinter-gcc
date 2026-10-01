import importlib
import unittest

import sublime
from SublimeLinter.lint import persist
from SublimeLinter.lint.linter import VirtualView


Linters = importlib.import_module('SublimeLinter-gcc.linter')
RegexExamples = importlib.import_module('SublimeLinter-gcc.tests.regex_tests')


class TestExistingRegex(RegexExamples.RegexTests):
    regex = Linters.Gcc.regex


class TestColumns(unittest.TestCase):
    def test_issue_19_utf8_stdin_and_ascii_diagnostics_both_classes(self):
        source = ('int main(void) {\n'
                  '\tint a = 1; int b = undefined_one;\n'
                  '\tchar *s = "é😀"; int c = undefined_two;\n'
                  '\treturn 0\n}\n')
        output = ("<stdin>:3:30: error: 'undefined_two' undeclared (first use in this function)\n"
                  "<stdin>:3:26: warning: unused variable 'c' [-Wunused-variable]\n"
                  "<stdin>:2:21: error: 'undefined_one' undeclared\n")
        self.assertDiagnostics(output, source, [(2, 25, 'undefined_two'), (2, 21, 'c'), (1, 20, 'undefined_one')])

    def test_missing_columns_are_preserved_both_classes(self):
        settings = sublime.load_settings('SublimeLinter-gcc-test-columns.sublime-settings')
        settings.set('no_column_highlights_line', True)
        self.addCleanup(setattr, persist, 'settings', persist.settings)
        persist.settings = settings
        self.assertDiagnostics('<stdin>:1: error: problem', 'int main(void) {\n', [(0, 0, 'int main(void) {')])

    def assertDiagnostics(self, output, source, expected):
        for cls in (Linters.Gcc, Linters.GPlusPlus):
            with self.subTest(linter=cls.name):
                linter = cls(sublime.View(0), {})
                vv = VirtualView(source)
                matches = list(linter.find_errors(output))
                self.assertEqual(len(matches), len(expected))
                for match, (line, col, text) in zip(matches, expected):
                    error = linter.process_match(match, vv)
                    self.assertIsNotNone(error)
                    begin = vv.full_line(line)[0] + col
                    self.assertEqual({k: error[k] for k in ('line', 'start', 'region', 'offending_text')}, {
                        'line': line, 'start': col, 'region': sublime.Region(begin, begin + len(text)),
                        'offending_text': text,
                    })
