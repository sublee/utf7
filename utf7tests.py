# -*- coding: utf-8 -*-
from __future__ import with_statement
try:
    from io import BytesIO
except ImportError:
    try:
        from cStringIO import StringIO as BytesIO
    except ImportError:
        from StringIO import StringIO as BytesIO

import pytest


utf7s = [__import__('utf7')]
# test _utf7 also if it exists
try:
    utf7s.append(__import__('_utf7'))
except ImportError:
    pass


# fixture 'utf7' will be an usable utf7 module
def pytest_generate_tests(metafunc):
    if 'utf7' in metafunc.fixturenames:
        metafunc.parametrize(['utf7'], [[utf7] for utf7 in utf7s],
                             ids=[m.__name__ for m in utf7s])


def test_packb(utf7):
    assert utf7.packb(127) == '\x7f'
    assert utf7.packb(256) == '\x80\x02'
    assert utf7.packb(64) == '\x40'
    assert utf7.packb(42) == '\x2a'
    assert utf7.packb(65536) == '\x80\x80\x04'
    assert utf7.packb(1234567890) == '\xd2\x85\xd8\xcc\x04'
    assert utf7.packb(2 ** 64 - 1) == '\xff' * 9 + '\x01'
    assert utf7.packb(2 ** 64) == '\x80' * 9 + '\x02'
    assert utf7.packb(2 ** 128) == '\x80' * 18 + '\x04'


def test_unpackb(utf7):
    assert utf7.unpackb('\x00') == 0
    assert utf7.unpackb('\x7f') == 127
    assert utf7.unpackb('\x80\x02') == 256
    assert utf7.unpackb('\x40') == 64
    assert utf7.unpackb('\x2a') == 42
    assert utf7.unpackb('\x80\x80\x04') == 65536
    assert utf7.unpackb('\xd2\x85\xd8\xcc\x04') == 1234567890
    assert utf7.unpackb('\xff' * 9 + '\x01') == 2 ** 64 - 1
    assert utf7.unpackb('\x80' * 9 + '\x02') == 2 ** 64
    assert utf7.unpackb('\x80' * 18 + '\x04') == 2 ** 128


def test_pack(utf7):
    buf = BytesIO()
    nums = [127, 256, 64, 42, 65536, 1234567890]
    for num in nums:
        assert utf7.pack(num, buf) > 0
    assert buf.getvalue() == \
        '\x7f\x80\x02\x40\x2a\x80\x80\x04\xd2\x85\xd8\xcc\x04'


def test_unpack(utf7):
    buf = BytesIO('\x7f\x80\x02\x40\x2a\x80\x80\x04\xd2\x85\xd8\xcc\x04')
    nums = []
    for x in xrange(6):
        num = utf7.unpack(buf)
        nums.append(num)
    with pytest.raises(StopIteration):
        buf.next()
    assert nums == [127, 256, 64, 42, 65536, 1234567890]


def test_aliases(utf7):
    assert utf7.dump is utf7.pack
    assert utf7.dumps is utf7.packb
    assert utf7.load is utf7.unpack
    assert utf7.loads is utf7.unpackb
    assert utf7.encode is utf7.packb
    assert utf7.decode is utf7.unpackb


def test_negative(utf7):
    with pytest.raises(OverflowError):
        utf7.packb(-1)
