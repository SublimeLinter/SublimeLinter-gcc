# ruff: noqa: E501

from __future__ import annotations

import re
import unittest
from collections import namedtuple


class RegexTests(unittest.TestCase):
    regex: re.Pattern[str] | None = None

    def test_cases(self):
        if not self.regex:
            return

        for case in _cases:
            match_list = [match_tuple(**m.groupdict()) for m in re.finditer(self.regex, case.output)]

            self.assertListEqual(case.matches, match_list, f"matches not as expected for case {case.name}")


def run_tests(regex):
    RegexTests.regex = regex
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RegexTests)
    unittest.TextTestRunner().run(suite)


case_tuple = namedtuple("case_tuple", ("name", "output", "matches"))


match_tuple = namedtuple("match_tuple", ("line", "col", "error", "warning", "message"))


_cases = []
_cases.append(
    case_tuple(
        name="unknown type name 1",
        output="""
In file included from test2.h:1:0,
                 from <stdin>:1:
test1.h:4:1: error: unknown type name ‘SOME’
 SOME *error;
 ^
""",
        matches=[match_tuple(line="1", col=None, error="error", warning=None, message="unknown type name ‘SOME’")],
    )
)


_cases.append(
    case_tuple(
        name="unknown type name 2",
        output="""
In file included from merc.h:4429:0,
                 from <stdin>:11:
tattoo.h:23:21: error: unknown type name ‘RBUFFER’
 void bread_tattoos( RBUFFER *rbuf, tattoo_list tl );
                     ^
In file included from <stdin>:11:0:
merc.h:4721:23: error: unknown type name ‘RBUFFER’
 char    bread_letter( RBUFFER *rbuf );
                       ^
merc.h:4722:23: error: unknown type name ‘RBUFFER’
 int     bread_number( RBUFFER *rbuf );
                       ^
merc.h:4723:21: error: unknown type name ‘RBUFFER’
 long    bread_flag( RBUFFER *rbuf );
                     ^
merc.h:4724:27: error: unknown type name ‘RBUFFER’
 const char* bread_string( RBUFFER *rbuf );
                           ^
merc.h:4725:31: error: unknown type name ‘RBUFFER’
 const char* bread_string_eol( RBUFFER *rbuf );
                               ^
merc.h:4726:23: error: unknown type name ‘RBUFFER’
 void    bread_to_eol( RBUFFER *rbuf );
                       ^
merc.h:4727:25: error: unknown type name ‘RBUFFER’
 const char* bread_word( RBUFFER *rbuf );
                         ^
merc.h:5463:19: error: unknown type name ‘RBUFFER’
 void bread_tflag( RBUFFER *rbuf, tflag f );
                   ^
""",
        matches=[
            match_tuple(
                line="11",
                col=None,
                error="error",
                warning=None,
                message="unknown type name ‘RBUFFER’",
            ),
            match_tuple(
                line="11",
                col="0",
                error="error",
                warning=None,
                message="unknown type name ‘RBUFFER’",
            ),
        ],
    )
)


_cases.append(
    case_tuple(
        name="unknown type name 3",
        output="""
In file included from test2.h:1:0,
                 from <stdin>:1:
test1.h:4:1: error: unknown type name ‘SOME’
 SOME *error;
 ^
""",
        matches=[match_tuple(line="1", col=None, error="error", warning=None, message="unknown type name ‘SOME’")],
    )
)


_cases.append(
    case_tuple(
        name="unknown type name 4",
        output="""
<stdin>:614:5: error: unknown type name ‘time_t’
<stdin>:649:4: error: unknown type name ‘time_t’
<stdin>:4313:1: error: unknown type name ‘time_t’
""",
        matches=[
            match_tuple(
                line="614",
                col="5",
                error="error",
                warning=None,
                message="unknown type name ‘time_t’",
            ),
            match_tuple(
                line="649",
                col="4",
                error="error",
                warning=None,
                message="unknown type name ‘time_t’",
            ),
            match_tuple(
                line="4313",
                col="1",
                error="error",
                warning=None,
                message="unknown type name ‘time_t’",
            ),
        ],
    )
)

_cases.append(
    case_tuple(
        name="case5",
        output="""
In file included from <stdin>:38:0:
interp.h:455:17: warning: redundant redeclaration of ‘void do_tattoo(CHAR_DATA*, const char*)’ in same scope [-Wredundant-decls]
 DECLARE_DO_FUN( do_tattoo   );
                 ^
merc.h:62:47: note: in definition of macro ‘DECLARE_DO_FUN’
 #define DECLARE_DO_FUN( fun )       DO_FUN    fun
                                               ^
tattoo.h:43:16: warning: previous declaration of ‘void do_tattoo(CHAR_DATA*, const char*)’ [-Wredundant-decls]
 DECLARE_DO_FUN(do_tattoo);
                ^
merc.h:62:47: note: in definition of macro ‘DECLARE_DO_FUN’
 #define DECLARE_DO_FUN( fun )       DO_FUN    fun
                                               ^
 """,
        matches=[
            match_tuple(
                line="38",
                col="0",
                error=None,
                warning="warning",
                message="redundant redeclaration of ‘void do_tattoo(CHAR_DATA*, const char*)’ in same scope [-Wredundant-decls]",
            )
        ],
    )
)


_cases.append(
    case_tuple(
        name="case6",
        output="""
In file included from <stdin>:5:0:
merc.h:614:5: error: unknown type name ‘time_t’
     time_t   creation_date;     /* Date clan created */
     ^
merc.h:649:4: error: unknown type name ‘time_t’
    time_t timestamp; /* Date/time player convicted or forgiven */
    ^
""",
        matches=[match_tuple(line="5", col="0", error="error", warning=None, message="unknown type name ‘time_t’")],
    )
)
