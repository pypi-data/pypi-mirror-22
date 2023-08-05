##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Deprecated - use DTMLMethod
"""

from zope.deferredimport import deprecated

# BBB Zope 5.0
deprecated(
    'Please import from OFS.DTMLMethod.',
    Document='OFS.DTMLMethod:Document',
    manage_addDocument='OFS.DTMLMethod:manage_addDocument',
)
