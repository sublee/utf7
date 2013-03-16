# -*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement
import io

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
    assert utf7.packb(127) == b'\x7f'
    assert utf7.packb(256) == b'\x80\x02'
    assert utf7.packb(64) == b'\x40'
    assert utf7.packb(42) == b'\x2a'
    assert utf7.packb(65536) == b'\x80\x80\x04'
    assert utf7.packb(1234567890) == b'\xd2\x85\xd8\xcc\x04'
    assert utf7.packb(2 ** 64 - 1) == b'\xff' * 9 + b'\x01'
    assert utf7.packb(2 ** 64) == b'\x80' * 9 + b'\x02'
    assert utf7.packb(2 ** 128) == b'\x80' * 18 + b'\x04'


def test_unpackb(utf7):
    assert utf7.unpackb(b'\x00') == 0
    assert utf7.unpackb(b'\x7f') == 127
    assert utf7.unpackb(b'\x80\x02') == 256
    assert utf7.unpackb(b'\x40') == 64
    assert utf7.unpackb(b'\x2a') == 42
    assert utf7.unpackb(b'\x80\x80\x04') == 65536
    assert utf7.unpackb(b'\xd2\x85\xd8\xcc\x04') == 1234567890
    assert utf7.unpackb(b'\xff' * 9 + b'\x01') == 2 ** 64 - 1
    assert utf7.unpackb(b'\x80' * 9 + b'\x02') == 2 ** 64
    assert utf7.unpackb(b'\x80' * 18 + b'\x04') == 2 ** 128


def test_pack(utf7):
    buf = io.BytesIO()
    nums = [127, 256, 64, 42, 65536, 1234567890]
    for num in nums:
        assert utf7.pack(num, buf) > 0
    assert buf.getvalue() == \
        b'\x7f\x80\x02\x40\x2a\x80\x80\x04\xd2\x85\xd8\xcc\x04'


def test_unpack(utf7):
    buf = io.BytesIO(b'\x7f\x80\x02\x40\x2a\x80\x80\x04\xd2\x85\xd8\xcc\x04')
    nums = []
    for x in range(6):
        num = utf7.unpack(buf)
        nums.append(num)
    with pytest.raises(StopIteration):
        next(buf)
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


def test_various_streams(utf7):
    import socket
    import tempfile
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 0))
    server_sock.listen(5)
    client_sock.connect(server_sock.getsockname())
    server_sock.accept()
    sock_file = client_sock.makefile()
    assert utf7.pack(65536, io.BytesIO()) == 3
    assert utf7.pack(65536, tempfile.TemporaryFile()) == 3
    assert utf7.pack(65536, sock_file) == 3
