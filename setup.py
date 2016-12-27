from setuptools import setup

setup(
    name='xolib',
    version='0.2.2',
    author='Vyronas Tsingaras',
    author_email='vyronas@vtsingaras.me',
    packages=['xolib'],
    url='https://github.com/vtsingaras/python-xolib',
    download_url='https://github.com/vtsingaras/python-xolib/archive/v0.2.2.tar.gz',
    license='LICENSE.txt',
    description='Helper library for interfacing with xo-server.',
    long_description=open('README.rst').read(),
    install_requires=[
        "websocket-client==0.37.0",
        "six",
        "pysynthetic"
    ],
)
