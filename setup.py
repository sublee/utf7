# -*- coding: utf-8 -*-
r"""
utf7
~~~~

Encoder/decoder of an UTF-7 encoded unsigned integer. UTF-7 uint is used for
`BinaryWriter.Write(String) <http://msdn.microsoft.com/en-us/library/
yzxa6408.aspx>`_ in `Microsoft .NET Framework <http://www.microsoft.com/net>`_.

.. sourcecode:: pycon

   >>> utf7.packb(65536)
   '\x80\x80\x04'

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
try:
    from Cython.Distutils import build_ext
except ImportError:
    ext_modules = []
    cmdclass = {}
else:
    b = bytes if sys.version_info < (3,) else str
    ext_modules = [Extension(b('_utf7'), [b('utf7.py')])]
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
    install_requires=['distribute', 'cython'],
    test_suite='utf7tests',
    tests_require=['pytest'],
)
