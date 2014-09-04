#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct

def rol32(a,n):
	'''Returns a left rotated by n places.'''
	return ((a << n) | (a >> (32 - n))) & 0xffffffff # Ensures 32-bit

class Sha1:
	def __init__(self, message):
		self.msg = bytearray(message, 'utf-8')
		self.msgByteLen = len(self.msg)
		self.msgBitLen = self.msgByteLen * 8

		# Initilise varibles
		self.h0 = 0x67452301
		self.h1 = 0xEFCDAB89
		self.h2 = 0x98BADCFE
		self.h3 = 0x10325476
		self.h4 = 0xC3D2E1F0

	def preProccessing(self):
		'''Add 1 and pad message so bit length is congruent to 448 (mod 512)
		then append the the message bit length'''
		self.msg += b'\x80'
		self.msg += b'\x00' * ((56 - (self.msgByteLen + 1) % 64) % 64)
		self.msg += struct.pack(b'>Q', self.msgBitLen)

	def proccess(self):
		for i in range(0, len(self.msg), 64): # for each 64 byte chunk
			w = [0] * 80 # Generate empty list of 80 words
			for j in range(16): # Spit into 16 4 byte words
				w[j] = struct.unpack(b'>I', self.msg[i + j * 4: i + j * 4 + 4])[0]
			for j in range(16, 80): # Generate another 64 words from original 16
				w[j] = rol32(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)

			# Initilize hash values for chunk
			a = self.h0
			b = self.h1
			c = self.h2
			d = self.h3
			e = self.h4

			# Compression function
			for i in range(80):
				if (0 <= i <= 19):
					f = d ^ (b & (c ^ d))
					k = 0x5A827999
				elif (20 <= i <= 39):
					f = b ^ c ^ d
					k = 0x6ED9EBA1
				elif (40 <= i <= 59):
					f = (b & c) | (b & d) | (c & d)
					k = 0x8F1BBCDC
				elif (60 <= i <= 79):
					f = b ^ c ^ d
					k = 0xCA62C1D6

				temp = rol32(a, 5) + f + e + k + w[i] & 0xffffffff # Ensure 32-bit
				e = d
				d = c
				c = rol32(b, 30)
				b = a
				a = temp

			h0 = (self.h0 + a) & 0xffffffff # Ensure 32-bit
			h1 = (self.h1 + b) & 0xffffffff
			h2 = (self.h2 + c) & 0xffffffff
			h3 = (self.h3 + d) & 0xffffffff
			h4 = (self.h4 + e) & 0xffffffff

		return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

	def digest(self):
		self.preProccessing()
		return self.proccess()

a = Sha1('test')
print(a.digest())



