import struct

def leftRotate(a, b):
	return ((a << b) | (a >> (32 - b))) & 0xffffffff

message = "test"

h0 = 0x67452301
h1 = 0xEFCDAB89
h2 = 0x98BADCFE
h3 = 0x10325476
h4 = 0xC3D2E1F0

messageLengthInBytes = len(message)
messageLengthInBits = messageLengthInBytes * 8

# Pre-proccessing:

# append bit '1'
message += b'\x80'

# Pad message with zeros until bit length is congruent to 448 (mod 512)
message += b'\x00' * ((56 - (messageLengthInBytes + 1) % 64) % 64)

# Split message into 512 bit chunks (64 bytes)
message += struct.pack(b'>Q', messageLengthInBits)
print(message)
# Proccess chunks
for i in range(0, len(message), 64):
	w = [0] * 80
	# break chunk into sixteen 32-bit big-endian words w[i]
	for j in range(16):
		w[j] = struct.unpack(b'>I', message[i + j*4:i + j*4 + 4])[0]
		#Extend the sixteen 32-bit words into eighty 32-bit words:
	for j in range(16, 80):
		w[j] = leftRotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)

	# Initialize hash values for chunk
	a = h0
	b = h1
	c = h2
	d = h3
	e = h4

	for i in range(80):
		if 0 <= i <= 19:
			f = d ^ (b & (c ^ d))
			k = 0x5A827999
		elif 20 <= i <= 39:
			f = b ^ c ^ d
			k = 0x6ED9EBA1
		elif 40 <= i <= 59:
			f = (b & c) | (b & d) | (c & d)
			k = 0x8F1BBCDC
		elif 60 <= i <= 79:
			f = b ^ c ^ d
			k = 0xCA62C1D6

		temp = leftRotate(a, 5) + f + e + k + w[i] & 0xffffffff # Why this?
		e = d
		d = c
		c = leftRotate(b, 30)
		b = a
		a = temp

	h0 = (h0 + a) & 0xffffffff # Why this?
	h1 = (h1 + b) & 0xffffffff
	h2 = (h2 + c) & 0xffffffff
	h3 = (h3 + d) & 0xffffffff
	h4 = (h4 + e) & 0xffffffff

print ('%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4))
