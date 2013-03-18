# -*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement
import io
import socket
import tempfile
import time

import pytest


utf7s = [__import__('utf7')]
# test _utf7 also if it exists
try:
    _utf7 = __import__('_utf7')
except ImportError:
    _utf7 = None
else:
    utf7s.append(_utf7)


# fixture 'utf7' will be an usable utf7 module
def pytest_generate_tests(metafunc):
    if 'utf7' in metafunc.fixturenames:
        metafunc.parametrize(['utf7'], [[utf7] for utf7 in utf7s],
                             ids=[m.__name__ for m in utf7s])


def test_pack_bytes(utf7):
    assert utf7.pack_bytes(0) == b'\x00'
    assert utf7.pack_bytes(127) == b'\x7f'
    assert utf7.pack_bytes(256) == b'\x80\x02'
    assert utf7.pack_bytes(64) == b'\x40'
    assert utf7.pack_bytes(42) == b'\x2a'
    assert utf7.pack_bytes(65535) == b'\xff\xff\x03'
    assert utf7.pack_bytes(1234567890) == b'\xd2\x85\xd8\xcc\x04'


def test_unpack_bytes(utf7):
    assert utf7.unpack_bytes(b'\x00') == 0
    assert utf7.unpack_bytes(b'\x7f') == 127
    assert utf7.unpack_bytes(b'\x80\x02') == 256
    assert utf7.unpack_bytes(b'\x40') == 64
    assert utf7.unpack_bytes(b'\x2a') == 42
    assert utf7.unpack_bytes(b'\xff\xff\x03') == 65535
    assert utf7.unpack_bytes(b'\xd2\x85\xd8\xcc\x04') == 1234567890


def test_pack(utf7):
    buf = io.BytesIO()
    nums = [127, 256, 64, 42, 65535, 1234567890]
    for num in nums:
        assert utf7.pack(num, buf) > 0
    assert buf.getvalue() == \
        b'\x7f\x80\x02\x40\x2a\xff\xff\x03\xd2\x85\xd8\xcc\x04'


def test_unpack(utf7):
    buf = io.BytesIO(b'\x7f\x80\x02\x40\x2a\xff\xff\x03\xd2\x85\xd8\xcc\x04')
    nums = []
    for x in range(6):
        num = utf7.unpack(buf)
        nums.append(num)
    with pytest.raises(StopIteration):
        next(buf)
    assert nums == [127, 256, 64, 42, 65535, 1234567890]


def test_aliases(utf7):
    assert utf7.dump is utf7.pack
    assert utf7.dumps is utf7.pack_bytes
    assert utf7.load is utf7.unpack
    assert utf7.loads is utf7.unpack_bytes
    assert utf7.encode is utf7.pack_bytes
    assert utf7.decode is utf7.unpack_bytes


def test_negative(utf7):
    with pytest.raises(OverflowError):
        utf7.pack_bytes(-1)


def test_file_like(utf7):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 0))
    server_sock.listen(5)
    client_sock.connect(server_sock.getsockname())
    server_sock.accept()
    sock_file = client_sock.makefile('wb')
    assert utf7.pack(65535, io.BytesIO()) == 3
    assert utf7.pack(65535, tempfile.TemporaryFile()) == 3
    assert utf7.pack(65535, sock_file) == 3


def test_socket(utf7):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 0))
    server_sock.listen(5)
    client_sock.connect(server_sock.getsockname())
    peer_sock, peer_addr = server_sock.accept()
    assert utf7.pack_socket(65535, client_sock) == 3
    assert utf7.unpack_socket(peer_sock) == 65535
    assert utf7.pack_socket(65535, peer_sock) == 3
    assert utf7.unpack_socket(client_sock) == 65535
    assert utf7.pack_socket(1, client_sock) == 1
    assert utf7.pack_socket(2, client_sock) == 1
    assert utf7.pack_socket(3, client_sock) == 1
    assert utf7.pack_socket(4, client_sock) == 1
    assert utf7.pack_socket(5, client_sock) == 1
    assert utf7.unpack_socket(peer_sock) == 1
    assert utf7.unpack_socket(peer_sock) == 2
    assert utf7.unpack_socket(peer_sock) == 3
    assert utf7.unpack_socket(peer_sock) == 4
    assert utf7.unpack_socket(peer_sock) == 5


def test_large_number(utf7):
    if utf7 is _utf7:
        with pytest.raises(OverflowError):
            _utf7.pack_bytes(2 ** 64)
        with pytest.raises(OverflowError):
            _utf7.pack_bytes(2 ** 128)
        with pytest.raises(OverflowError):
            _utf7.unpack_bytes(b'\x80' * 9 + b'\x02')
        with pytest.raises(OverflowError):
            _utf7.unpack_bytes(b'\x80' * 18 + b'\x04')
    else:
        assert utf7.pack_bytes(2 ** 64) == b'\x80' * 9 + b'\x02'
        assert utf7.pack_bytes(2 ** 128) == b'\x80' * 18 + b'\x04'
        assert utf7.unpack_bytes(b'\x80' * 9 + b'\x02') == 2 ** 64
        assert utf7.unpack_bytes(b'\x80' * 18 + b'\x04') == 2 ** 128


def test_gevent_socket(utf7):
    delay = 0.001
    try:
        import gevent
    except ImportError:
        pytest.skip()
    from gevent.socket import socket, AF_INET, SOCK_STREAM
    server_sock = socket(AF_INET, SOCK_STREAM)
    client_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind(('127.0.0.1', 0))
    server_sock.listen(5)
    client_sock.connect(server_sock.getsockname())
    peer_sock, peer_addr = server_sock.accept()
    def send():
        peer_sock.send('x')
        for b in utf7.pack_bytes(2 ** 64 - 1):
            gevent.sleep(delay)
            peer_sock.send(b)
    def recv():
        assert client_sock.recv(1) == 'x'
        t = time.time()
        assert utf7.unpack_socket(client_sock) == 2 ** 64 - 1
        assert time.time() - t >= delay * 10
    gevent.joinall([gevent.spawn(send), gevent.spawn(recv)], raise_error=True)
