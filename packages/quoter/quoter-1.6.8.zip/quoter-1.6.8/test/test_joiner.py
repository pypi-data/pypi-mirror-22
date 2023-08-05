
from quoter import *
from quoter.joiner import is_sequence
import pytest
import six
import sys


### Helper functions

def single(s):
    return "'" + s + "'"


def brackets(s):
    return "[" + s + "]"


### Tests


def test_doc_example():

    mylist = list("ABCD")
    assert join(mylist) == "A, B, C, D"
    assert join(mylist, sep=" | ", endcaps=braces) == "{A | B | C | D}"
    assert join(mylist, sep=" | ", endcaps=braces.clone(padding=1)) == \
            "{ A | B | C | D }"
    assert join(mylist, sep=" | ", endcaps=braces.but(padding=1)) == \
            "{ A | B | C | D }"
    assert and_join(mylist[:2]) == "A and B"
    assert and_join(mylist[:3]) == "A, B, and C"
    assert and_join(mylist) == "A, B, C, and D"
    assert and_join(mylist, quoter=double, lastsep=" and ") == \
            '"A", "B", "C" and "D"'


def test_margins_and_padding():
    mylist = list("ABCD")
    bl = join.but(sep="|", prefix='{', suffix='}')

    assert bl(mylist) =="{A|B|C|D}"
    assert bl(mylist, margin=1) ==" {A|B|C|D} "
    assert bl(mylist, padding=2) =="{  A|B|C|D  }"
    assert bl(mylist, margin=2, padding=1) =="  { A|B|C|D }  "


def test_oxford():
    assert and_join([]) == ''
    assert and_join([1]) == '1'
    assert and_join([1, 2]) == '1 and 2'
    assert and_join([1, 2, 3]) == '1, 2, and 3'
    assert and_join([1, 2, 3, 4]) == '1, 2, 3, and 4'


def test_heathen():
    # non Oxford Comma
    assert and_join([], lastsep=' and ') == ''
    assert and_join([1], lastsep=' and ') == '1'
    assert and_join([1, 2], lastsep=' and ') == '1 and 2'
    assert and_join([1, 2, 3], lastsep=' and ') == '1, 2 and 3'
    assert and_join([1, 2, 3, 4], lastsep=' and ') == '1, 2, 3 and 4'


def test_quoted():
    assert and_join([], quoter=single) == ""
    assert and_join([1], quoter=single) == "'1'"
    assert and_join([1, 2], quoter=single) == "'1' and '2'"
    assert and_join([1, 2, 3], quoter=single) == "'1', '2', and '3'"


def test_listy():
    assert join([], quoter=single, endcaps=brackets) == "[]"
    assert join([1], quoter=single, endcaps=brackets) == "['1']"
    assert join([1, 2], quoter=single, endcaps=brackets) == "['1', '2']"
    assert join([1, 2, 3], quoter=single, endcaps=brackets) == "['1', '2', '3']"


def test_sep():
    assert join([], sep='|') == ''
    assert join([1], sep='|') == '1'
    assert join([1, 2], sep='|') == '1|2'
    assert join([1, 2, 3], sep='|') == '1|2|3'


def test_twosep_and_lastsep():
    assert join([1, 2, 3, 4], sep='|', lastsep='+') == '1|2|3+4'

    assert join([], sep='|', twosep='*', lastsep='+') == ''
    assert join([1], sep='|', twosep='*', lastsep='+') == '1'
    assert join([1, 2], sep='|', twosep='*', lastsep='+') == '1*2'
    assert join([1, 2, 3], sep='|', twosep='*', lastsep='+') == '1|2+3'
    assert join([1, 2, 3, 4], sep='|', twosep='*', lastsep='+') == '1|2|3+4'


def test_no_twostep():
    assert join([], sep='|', twosep=None, lastsep='+') == ''
    assert join([1], sep='|', twosep=None, lastsep='+') == '1'
    assert join([1, 2], sep='|', twosep=None, lastsep='+') == '1+2'
    assert join([1, 2, 3], sep='|', twosep=None, lastsep='+') == '1|2+3'
    assert join([1, 2, 3, 4], sep='|', twosep=None, lastsep='+') == '1|2|3+4'


def test_concat():
    assert concat([4, 5, 6]) == '456'
    assert concat(range(3)) == '012'
    assert concat([4, 5, 6]) == '456'
    assert concat(['a','b','c']) == 'abc'


def test_joinlines():
    assert joinlines([]) == '\n'
    assert joinlines(list('a')) == 'a\n'
    assert joinlines(list('ab')) == 'a\nb\n'
    assert joinlines(list('abc')) == 'a\nb\nc\n'


def test_and_join():
    assert and_join([]) == ''
    assert and_join([1]) == '1'
    assert and_join([1, 2]) == '1 and 2'
    assert and_join([1, 2, 3]) == '1, 2, and 3'
    assert and_join([1, 2, 3, 4]) == '1, 2, 3, and 4'


def test_or_join():
    assert or_join([]) == ''
    assert or_join([1]) == '1'
    assert or_join([1, 2]) == '1 or 2'
    assert or_join([1, 2, 3]) == '1, 2, or 3'
    assert or_join([1, 2, 3, 4]) == '1, 2, 3, or 4'


#@pytest.mark.xfail(reason='road out')
def test_named_endpoints():
    mylist = list('ABCD')
    assert join.and_join(mylist) == and_join(mylist)
    assert join.or_join(mylist) == or_join(mylist)
    assert join.lines(mylist) == joinlines(mylist)


def test_items():
    alist = [1, 2, 3, 'string']
    assert items(alist) == "0: 1\n1: 2\n2: 3\n3: 'string'"

    assert items(alist, header="---") == "---\n0: 1\n1: 2\n2: 3\n3: 'string'"
    assert items(alist, footer="===") == "0: 1\n1: 2\n2: 3\n3: 'string'\n==="
    assert items(alist, header='---', footer="===") == "---\n0: 1\n1: 2\n2: 3\n3: 'string'\n==="

    try:
        from collections import OrderedDict
        answer = "this: something\nthat: else\nplus: additionally"
    except ImportError:
        OrderedDict = dict  # py26
        parts = ["this: something", "plus: additionally", "that: else"]
        # output in different order because unordred dict

    od = OrderedDict()
    od['this'] = 'something'
    od['that'] = 'else'
    od['plus'] = 'additionally'

    result1 = items(od, fmt="{key}: {value}")
    result2 = items(od, fmt="{key}: {value}", header="KEY: VALUE")

    if OrderedDict is dict:
        for p in parts:
            assert p in result1
            assert p in result2
    else:
        assert result1 == answer
        assert result2 == "KEY: VALUE\n" + answer
