import gpib
"""test!"""
<<<<<<< HEAD
"""test3!"""
=======
"""test2!"""
>>>>>>> 18d526c5be9cfd98ce023b1528c2a556d1ccdda5
class GpibDevice:
	"""Generic lowelevel GPIB device for the Budker-phys gpib python library"""
	DEFAULT_READ_LENGTH=1000
	def __init__(self, name):
		self.device = gpib.find(name)
		self.read_length = self.DEFAULT_READ_LENGTH
	def setReadLength(self, length):
		"""Sets the read_length for this GPIB device"""
		self.read_length = length
	def write(self, command):
		"""Write a lowlevel gpib command"""
		gpib.write(self.device, command)
	def read(self, length=self.read_length):
		"""Read from the gpib device, number of characters, defined by read_length"""
		return gpib.read(self.device, length)
	def readBinary(self,length=self.read_length):
		return gpib.readbin(self.device,length)


