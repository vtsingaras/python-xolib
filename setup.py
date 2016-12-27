from setuptools import setup

setup(
    name='xolib',
    version='0.2.0',
    author='Vyronas Tsingaras',
    author_email='vyronas@vtsingaras.me',
    packages=['xolib'],
    url='http://pypi.python.org/pypi/xolib/',
    license='LICENSE.txt',
    description='Helper library for interfacing with xo-server.',
    long_description=open('README.rst').read(),
    install_requires=[
        "websocket-client==0.37.0",
        "six",
        "pysynthetic"
    ],
)
