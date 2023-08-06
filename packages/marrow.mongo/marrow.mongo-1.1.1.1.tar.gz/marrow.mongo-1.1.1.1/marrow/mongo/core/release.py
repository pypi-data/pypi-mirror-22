# encoding: utf-8

"""Release information about Marrow Mongo."""

from __future__ import unicode_literals

from collections import namedtuple

version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(1, 1, 1, '.', 1)
version = ".".join([str(i) for i in version_info[:3]]) + \
		((version_info.releaselevel[:1] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')

author = namedtuple('Author', ['name', 'email'])("Alice Bevan-McGregor", 'alice@gothcandy.com')

description = "Light-weight utilities to augment, not replace the Python MongoDB driver."
url = 'https://github.com/marrow/mongo/'
