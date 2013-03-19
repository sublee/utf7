# -*- coding: utf-8 -*-
r"""
utf7
~~~~

Encoder/decoder of an UTF-7 encoded unsigned integer.

.. sourcecode:: pycon

   >>> utf7.pack_bytes(65535)
   b'\xff\xff\x03'
   >>> utf7.unpack_bytes(b'\xff\xff\x03')
   65535

UTF-7 uint is used for `BinaryWriter.Write(String)
<http://msdn.microsoft.com/en-us/library/yzxa6408.aspx>`_ in
`Microsoft .NET Framework <http://www.microsoft.com/net>`_. Here's an example
of ping-pong between Python server and C# client:

.. sourcecode:: python

   while not socket.closed:
       # recv ping
       ping_size = utf7.unpack_socket(socket)
       ping_data = socket.recv(ping_size)
       assert ping_data == b'ping'
       # send pong
       pong_data = b'pong'
       pong_size = len(pong_data)
       utf7.pack_socket(pong_size, socket)
       socket.send(pong_data)

You can also use ``_utf7`` written in C to take high-speed:

.. sourcecode:: python

   import _utf7 as utf7

Links
`````

* `GitHub repository <http://github.com/sublee/utf7>`_
* `development version
  <http://github.com/sublee/utf7/zipball/master#egg=utf7-dev>`_

"""
from __future__ import unicode_literals, with_statement
import re
from setuptools import setup
from setuptools.command.test import test
from setuptools.extension import Extension
import sys


# detect the current version
with open('utf7.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version


# use pytest instead
def run_tests(self):
    pyc = re.compile(r'\.pyc|\$py\.class')
    test_file = pyc.sub('.py', __import__(self.test_suite).__file__)
    raise SystemExit(__import__('pytest').main([test_file]))
test.run_tests = run_tests


# cython
b = bytes if sys.version_info < (3,) else str
try:
    from Cython.Distutils import build_ext
except ImportError:
    ext_modules = [Extension(b('_utf7'), [b('_utf7.c'), b('utf7.c')])]
    cmdclass = {}
else:
    ext_modules = [Extension(b('_utf7'), [b('_utf7.pyx'), b('utf7.c')])]
    cmdclass = {'build_ext': build_ext}


setup(
    name='utf7',
    version=version,
    license='BSD',
    author='Heungsub Lee',
    author_email=re.sub('((sub).)(.*)', r'\2@\1.\3', 'sublee'),
    url='https://github.com/sublee/utf7',
    download_url='utf7'.join([
        'http://github.com/sublee/', '/zipball/master#egg=', '-dev']),
    description='UTF-7 encoded unsigned integer',
    long_description=__doc__,
    platforms='any',
    py_modules=['utf7'],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.1',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy'],
    install_requires=['distribute'],
    test_suite='utf7tests',
    tests_require=['pytest'],
)
