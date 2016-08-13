=====
XoLib
=====

^^^^^^^^
Overview
^^^^^^^^
This is a simple helper Python 2 & 3 package to interface with the
JSON-RPC over WebSockets API of `XenOrchestra's <https://xen-orchestra.com/#!/>`_
`xo-server <https://github.com/vatesfr/xo-server>`_.

^^^^^
Usage
^^^^^

::

  from xolib import xo, XoError, XoApiError, XoTimeoutError
  from __future__ import print_function

  xo_instance = xo(ws://localhost)
  try:
    xo.signIn_withPassword(username='lala', password='test')
  except XoError:
    print('Wrong password?')

  try:
    xo.call('somemethod', timeout=20, somemethod_arg1=arg1, somemethod_arg2=arg2)
  except XoTimeoutError:
    print('xo-server did not respond within 20 seconds.')
  except XoApiError:
    print('Fix your arguments.')


