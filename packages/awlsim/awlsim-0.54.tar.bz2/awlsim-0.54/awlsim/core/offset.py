# -*- coding: utf-8 -*-
#
# AWL data offset
#
# Copyright 2012-2017 Michael Buesch <m@bues.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import division, absolute_import, print_function, unicode_literals
from awlsim.common.compat import *

from awlsim.common.datatypehelpers import * #+cimport

from awlsim.core.util import *


__all__ = [ "AwlOffset", ]


class AwlOffset(object): #+cdef
	"""Memory area offset
	"""

	# A DB-number for fully qualified access, or None.
	dbNumber = None #@nocy

	# A symbolic DB-name for fully qualified access, or None.
	dbName = None #@nocy

	# An AwlDataIdentChain, or None.
	# Used for fully qualified (DBx.VAR) or named local (#VAR)
	# global symbolic ("VAR") accesses.
	# For global symbols the chain only has one element.
	identChain = None #@nocy

	# A (S)FB-number for multi-instance calls, or None.
	fbNumber = None #@nocy

	# Additional sub-offset that is added to this offset, or None.
	# This is used for arrays and structs.
	subOffset = None #@nocy

#@cy	def __cinit__(self):
#@cy		self.dbNumber = None
#@cy		self.dbName = None
#@cy		self.identChain = None
#@cy		self.fbNumber = None
#@cy		self.subOffset = None

	def __init__(self, byteOffset=0, bitOffset=0): #@nocy
#@cy	def __init__(self, int64_t byteOffset=0, int32_t bitOffset=0):
		self.byteOffset, self.bitOffset =\
			byteOffset, bitOffset

	def __eq__(self, other): #@nocy
#@cy	cpdef __eq(self, object other):
		"""Equality operator.
		This does only compare byte and bit offset and
		does _not_ check dynAttrs.
		"""
		return (self is other) or (\
			isinstance(other, AwlOffset) and\
			self.byteOffset == other.byteOffset and\
			self.bitOffset == other.bitOffset\
		)

#@cy	def __richcmp__(self, object other, int op):
#@cy		if op == 2: # __eq__
#@cy			return self.__eq(other)
#@cy		elif op == 3: # __ne__
#@cy			return not self.__eq(other)
#@cy		return False

	def __ne__(self, other):		#@nocy
		return not self.__eq__(other)	#@nocy

	def dup(self):
		offset = AwlOffset(self.byteOffset,
				   self.bitOffset)
		offset.dbNumber = self.dbNumber
		return offset

	@classmethod
	def fromPointerValue(cls, value):
		return cls((value & 0x0007FFF8) >> 3,
			   (value & 0x7))

	def toPointerValue(self): #@nocy
#@cy	cpdef uint32_t toPointerValue(self):
		return ((self.byteOffset << 3) & 0x0007FFF8) |\
		       (self.bitOffset & 0x7)

	@classmethod
	def fromLongBitOffset(cls, bitOffset):
		return cls(bitOffset // 8, bitOffset % 8)

	def toLongBitOffset(self):				#@nocy
#@cy	cpdef uint64_t toLongBitOffset(self):
#@cy		return <int64_t>self.byteOffset * <int64_t>8 + <int64_t>self.bitOffset
		return self.byteOffset * 8 + self.bitOffset	#@nocy

	def __add__(self, other): #@nocy
#@cy	def __add__(self, AwlOffset other):
#@cy		cdef int64_t bitOffset
#@cy		bitOffset = ((<int64_t>self.byteOffset + <int64_t>other.byteOffset) * <int64_t>8 +
#@cy			     <int64_t>self.bitOffset + <int64_t>other.bitOffset)
		bitOffset = ((self.byteOffset + other.byteOffset) * 8 +	#@nocy
			     self.bitOffset + other.bitOffset)		#@nocy
		return AwlOffset(bitOffset // 8, bitOffset % 8)

	def __iadd__(self, other): #@nocy
#@cy	def __iadd__(self, AwlOffset other):
#@cy		cdef int64_t bitOffset
#@cy		bitOffset = ((<int64_t>self.byteOffset + <int64_t>other.byteOffset) * <int64_t>8 +
#@cy			     <int64_t>self.bitOffset + <int64_t>other.bitOffset)
		bitOffset = ((self.byteOffset + other.byteOffset) * 8 +	#@nocy
			     self.bitOffset + other.bitOffset)		#@nocy
		self.byteOffset = bitOffset // 8
		self.bitOffset = bitOffset % 8
		return self

	# Round the offset to a multiple of 'byteBase' bytes.
	# Returns an AwlOffset.
	def roundUp(self, byteBase):
#@cy		cdef int64_t byteOffset

		byteOffset = self.byteOffset
		if self.bitOffset:
			byteOffset += 1
		byteOffset = roundUp(byteOffset, byteBase)
		return AwlOffset(byteOffset)

	def __repr__(self):
		prefix = ""
		if self.dbNumber is not None:
			prefix = "DB%d" % self.dbNumber
		if self.dbName is not None:
			prefix = '"%s"' % self.dbName
		if self.identChain is not None:
			if prefix:
				return prefix + "." + self.identChain.getString()
			return "#" + self.identChain.getString()
		else:
			if prefix:
				prefix = prefix + ".DBX "
			return "%s%d.%d" % (prefix,
					    self.byteOffset,
					    self.bitOffset)
