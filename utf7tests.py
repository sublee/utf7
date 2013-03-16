# -*- coding: utf-8 -*-
from __future__ import with_statement
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

import pytest

import utf7


def test_packb():
    assert utf7.packb(127) == '\x7f'
    assert utf7.packb(256) == '\x80\x02'
    assert utf7.packb(64) == '\x40'
    assert utf7.packb(42) == '\x2a'
    assert utf7.packb(65536) == '\x80\x80\x04'
    assert utf7.packb(1234567890) == '\xd2\x85\xd8\xcc\x04'


def test_unpackb():
    assert utf7.unpackb('\x00') == 0
    assert utf7.unpackb('\x7f') == 127
    assert utf7.unpackb('\x80\x02') == 256
    assert utf7.unpackb('\x40') == 64
    assert utf7.unpackb('\x2a') == 42
    assert utf7.unpackb('\x80\x80\x04') == 65536
    assert utf7.unpackb('\xd2\x85\xd8\xcc\x04') == 1234567890


def test_pack():
    buf = BytesIO()
    nums = [127, 256, 64, 42, 65536, 1234567890]
    for num in nums:
        assert utf7.pack(num, buf) > 0
    assert buf.getvalue() == \
        '\x7f\x80\x02\x40\x2a\x80\x80\x04\xd2\x85\xd8\xcc\x04'


def test_unpack():
    buf = BytesIO('\x7f\x80\x02\x40\x2a\x80\x80\x04\xd2\x85\xd8\xcc\x04')
    nums = []
    for x in xrange(6):
        num = utf7.unpack(buf)
        nums.append(num)
    with pytest.raises(StopIteration):
        buf.next()
    assert nums == [127, 256, 64, 42, 65536, 1234567890]


def test_aliases():
    assert utf7.dump is utf7.pack
    assert utf7.dumps is utf7.packb
    assert utf7.load is utf7.unpack
    assert utf7.loads is utf7.unpackb
    assert utf7.encode is utf7.packb
    assert utf7.decode is utf7.unpackb
