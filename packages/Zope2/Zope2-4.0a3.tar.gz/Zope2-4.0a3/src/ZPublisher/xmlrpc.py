##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zope.deferredimport import deprecated

# BBB Zope 5.0
deprecated(
    'Please import from ZServer.ZPublisher.xmlrpc.',
    dump_instance='ZServer.ZPublisher.xmlrpc:dump_instance',
    parse_input='ZServer.ZPublisher.xmlrpc:parse_input',
    response='ZServer.ZPublisher.xmlrpc:response',
    Response='ZServer.ZPublisher.xmlrpc:Response',
    WRAPPERS='ZServer.ZPublisher.xmlrpc:WRAPPERS',
)
