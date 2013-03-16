# -*- coding: utf-8 -*-
import utf7


def test_write_utf7():
    assert utf7.packb(127) == '\x7f'
    assert utf7.packb(256) == '\x80\x02'
    assert utf7.packb(64) == '\x40'
    assert utf7.packb(42) == '\x2a'
    assert utf7.packb(65536) == '\x80\x80\x04'
    assert utf7.packb(1234567890) == '\xd2\x85\xd8\xcc\x04'


def test_read_utf7():
    assert utf7.unpackb('\x00') == 0
    assert utf7.unpackb('\x7f') == 127
    assert utf7.unpackb('\x80\x02') == 256
    assert utf7.unpackb('\x40') == 64
    assert utf7.unpackb('\x2a') == 42
    assert utf7.unpackb('\x80\x80\x04') == 65536
    assert utf7.unpackb('\xd2\x85\xd8\xcc\x04') == 1234567890
