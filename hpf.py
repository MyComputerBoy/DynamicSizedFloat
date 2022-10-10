"""hpf.py -> proprietary high precision floating point format
Main classes:

Binary -> dynamically sized binary format
hpf -> proprietary high precision float with arbitrarily high precision floating point format

Main user functions:
For Binary:

__init__(self, data=None, co=None, sign=None) -> Initialization with optional initialization
__add__(self, other) -> add override
__sub__(self, other) -> sub override
__float_add__(self, other) -> function for floating point add
__float_sub__(self, other) -> function for floating point sub
Allign(self, other, Inverse=False) -> function to allign mantissa for general functions, Inverse for floating point arithmetic
ToInt(self) -> function to convert Binary to int
DoubleToBin(self, a, precision=0) -> function to convert double to Binary with arbitrary precision
__repr__(self) -> representation override for Binary class
__str__(self) -> string  representation override for Binary

For hpf:

__init__(self, mantissa=None, exp=None, sign=None) -> Initialization with optional initialization
Allign(self, other, additive=True) -> function to allign mantissa based on actual value with respect to exponent, additive for alligning for floating point arithmetic
__pure_add__(self, other) -> primitive function for add hpf
__pure_sub__(self, other) -> primitive function for sub hpf
__add__(self, other) -> full propper function to add arbitrary hpf
__sub__(self, other) -> full propper function to sub arbitrary hpf
__repr__(self) -> representation override for hpf
__str__(self) -> string representation override for hpf
"""
from dataclasses import dataclass
import math as m 

class CustomException(Exception):
	pass

@dataclass
class Binary:
	def __init__(self, data=None, co=None, sign=None):
		# print("\nBinary.__init__():")
		if type(data) == type(None):
			#Initialize data for 8 bits, co and sign
			self.data = [False for i in range(8)]
			self.co = False
			self.sign = True
		else:
			#If cloning make absolutely no copy of old object for no reference in any ways
			t = [False for i in range(len(data))]
			for i, e in enumerate(data):
				if e:
					t[i] = True
				else:
					t[i] = False
			self.data = t
			# print(self.__str__())
			if type(co) == type(None):
				self.co = False
			else:
				if co:
					self.co = True
				else:
					self.co = False
			if type(sign) == type(None):
				self.sign = True
			else:
				if sign:
					self.sign = True
				else:
					self.sign = False
	
	def __and__(self, other):
		_new_self_bin = Binary(self.data)
		_new_toehr_bin = Binary(other.data)
		
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin)
		
		q = [False for i in range(_new_self_bin.GetLength())]
		
		for i in range(_new_self_bin.data):
			q.append(_new_self_bin.data[i] and _new_other_bin.data[i])
		
		return Binary(q)
	
	def __or__(self, other):
		_new_self_bin = Binary(self.data)
		_new_toehr_bin = Binary(other.data)
		
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin)
		
		q = [False for i in range(_new_self_bin.GetLength())]
		
		for i in range(_new_self_bin.data):
			q.append(_new_self_bin.data[i] or _new_other_bin.data[i])
		
		return Binary(q)
	
	def __xor__(self, other):
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin)
		
		q = []
		
		for i in range(self.GetLength()):
			if (_new_self_bin.data[i] + _new_other_bin.data[i]) == 1:
				q.append(True)
			else:
				q.append(False)
		
		return Binary(q)
	
	def __not__(self, other):
		
		q = [False for i in range(_new_self_bin.GetLength())]
		
		for i in range(_new_self_bin.data):
			if _new_self_bin.data[i]:
				q.append(False)
			else:
				q.append(True)
		
		return Binary(q)
	
	def __add__(self, other, ci=False):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		#Allign sizes for compatible addition
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin)
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate addition
		for i, e in enumerate(_new_self_bin.data):
			xo = (_new_self_bin.data[i] + _new_other_bin.data[i]) % 2
			ao = _new_self_bin.data[i] * _new_other_bin.data[i]
			q[i] = (xo + ci) % 2
			at = xo * ci 
			ci = m.ceil(ao/2 + at/2)
		return Binary(q, ci)
	def __sub__(self, other, ci=True):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		#Allign sizes for compatible addition
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin)
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate subtraction
		for i, e in enumerate(_new_self_bin.data):
			xo = (_new_self_bin.data[i] + (1-_new_other_bin.data[i])) % 2
			ao = _new_self_bin.data[i] * (1-_new_other_bin.data[i])
			q[i] = (xo + ci) % 2
			at = xo * ci 
			ci = m.ceil(ao/2 + at/2)
		return Binary(q, ci)
	
	def __float_add__(self, other, ci=False):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		#Allign sizes for compatible addition
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin, True)
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate addition
		for i, e in enumerate(_new_self_bin.data):
			xo = (_new_self_bin.data[i] + _new_other_bin.data[i]) % 2
			ao = _new_self_bin.data[i] * _new_other_bin.data[i]
			q[i] = (xo + ci) % 2
			at = xo * ci 
			ci = m.ceil(ao/2 + at/2)
		return Binary(q, ci)
	def __float_sub__(self, other, ci=True):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		#Allign sizes for compatible addition
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin, True)
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate subtraction
		for i, e in enumerate(_new_self_bin.data):
			xo = (_new_self_bin.data[i] + (1-_new_other_bin.data[i])) % 2
			ao = _new_self_bin.data[i] * (1-_new_other_bin.data[i])
			q[i] = (xo + ci) % 2
			at = xo * ci 
			ci = m.ceil(ao/2 + at/2)
		return Binary(q, ci)
	
	def Allign(self, other, Inverse=False, offset=0):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		#Get lengths
		_self_len = _new_self_bin.GetLength()
		_other_len = _new_other_bin.GetLength()
		
		#Check which is greater
		_max_len = _self_len * (_self_len > _other_len) + _other_len * (_self_len <= _other_len)
		#Append appropriate lengths to appropriate object
		if Inverse:
			if _self_len < _max_len:
				_new_self_bin.InverseLengthAppend(_max_len-_self_len)
			else:
				_new_other_bin.InverseLengthAppend((_max_len-_other_len)-offset)
				_new_other_bin.LengthAppend(offset)
			
			return _new_self_bin, _new_other_bin
		
		if _self_len < _max_len:
			if _max_len - _self_len >= 1:
				_new_self_bin.LengthAppend(_max_len-_self_len)
		else:
			if _max_len - _other_len >= 1:
				_new_other_bin.LengthAppend((_max_len-_other_len)-offset)
				_new_other_bin.InverseLengthAppend(offset)
		
		return _new_self_bin, _new_other_bin
	
	def Append(self, value=False):
		self.data.append(value)
	
	def Pop(self, index=0):
		self.data.pop(index)
	
	def LengthPop(self, value=1, index=0):
		for i in range(value):
			self.Pop(index)
	
	def InverseAppend(self, value=False):
		self.data.insert(0, value)
	
	def LengthAppend(self, length=1, fill=False):
		if length >= 1:
			for i in range(length):
				self.Append(fill)
	
	def InverseLengthAppend(self, length=1, fill=False):
		for i in range(length):
			self.InverseAppend(fill)
	
	def ToInt(self):
		q = 0
		#Convert to int
		for i, e in enumerate(self.data):
			q += 2**i*e 
		return q
	
	def DoubleToBin(self, a, precision=0):
		t = []
		xl = 0
		while 2**xl < a:
			xl += 1
		for i in range(xl+precision):
			t.append(a % 2)
			if a % 2 == 1:
				a -= 1
			a /= 2
		self.data = t
	
	def GetLength(self):
		return len(self.data)
	
	def __repr__(self):
		return "Binary: " + str(self.ToInt())
	
	def __str__(self):
		_str = "0b"
		for bit in self.data:
			_str += "1" if bit else "0"
		return _str

@dataclass
class hpf:
	def __init__(self, mantissa=None, exp=None, sign=None):
		if type(mantissa) == type(None):
			#Initialize mantissa for 24 bits, exponent for 8 bits and sign for 1 bit
			self.mant	= Binary([False for i in range(24)])
			self.exp	= Binary([False for i in range( 8)])
			self.sign	= Binary([False])
			
			self.mant_length = 24
			self.exp_length = 8
		else:
			if type(exp) == type(None) or type(sign) == type(None):
				raise CustomException("Error: Initialization of hpf class requires mantissa, exp and sign to be declared")
			self.mant	= Binary(mantissa.data)
			self.exp	= Binary(exp.data)
			self.sign	= Binary(sign.data)
			
			self.mant_length	= mantissa.GetLength()
			self.exp_length		= exp.GetLength()
	
	def Allign(self, other, additive=True):
		# print("\nhpf.Allign:")
		reverse_shift = False
		
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign)
		_new_other = hpf(other.mant, other.exp, other.sign)
		
		#Calculate exponent values
		_self_exp_val	= 2**(_new_self.exp.GetLength()-1)-_new_self.exp.ToInt()
		_other_exp_val	= 2**(_new_other.exp.GetLength()-1)-_new_other.exp.ToInt()
		
		#Add leading one for calculations
		if additive:
			_new_self.mant.Append(True)
			_new_other.mant.Append(True)
		
		# print("self : %s" % (_new_self.mant))
		# print("other: %s" % (_new_other.mant))
		
		
		#Find the largest exponent
		_max_exp_val = (_self_exp_val) * (_self_exp_val > _other_exp_val) + (_other_exp_val) * (_self_exp_val <= _other_exp_val)
		
		#If self represents a larger number
		if _max_exp_val < _self_exp_val:
			# print("<")
			#Calculate amount to shift
			shift = _other_exp_val - _self_exp_val
			
			#Shift the mantissa the appropriate amounts
			difference = _new_other.mant.GetLength()-_new_self.mant.GetLength()
			if difference < 0:
				difference = 0
			if shift < 0:
				_new_other.mant.LengthAppend(abs(shift))
				reverse_shift = True
			else:
				_new_self.mant.LengthAppend(shift)
		else:	#If other represents a larger number
			# print(">=")
			#Calculate amount to shift
			shift = _self_exp_val - _other_exp_val
			
			#Shift the mantissa the appropriate amounts
			difference = _new_self.mant.GetLength()-_new_other.mant.GetLength()
			if difference < 0:
				difference = 0
			if shift < 0:
				_new_self.mant.LengthAppend(abs(shift))
				reverse_shift = True
			else:
				_new_other.mant.LengthAppend(shift)
		
		# print("shift: %s" % (shift))
		# print("diffe: %s" % (difference))
		
		return _new_self, _new_other, reverse_shift
	
	def __pure_add__(self, other):
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign)
		_new_other = hpf(other.mant, other.exp, other.sign)
		
		_new_self_exp_v  = 2**(_new_self.exp.GetLength()-1)-_new_self.exp.ToInt()
		_new_other_exp_v = 2**(_new_other.exp.GetLength()-1)-_new_other.exp.ToInt()
		
		#Check which has the largest value
		_t_q_exp_v = _new_self_exp_v * (_new_self_exp_v > _new_other_exp_v) + _new_other_exp_v * (_new_self_exp_v <= _new_other_exp_v)
		
		#Get lengths of mantissa
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		
		#Allign mantissa
		_new_self, _new_other, reverse_shift = _new_self.Allign(_new_other)
		
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		if reverse_shift:	#Get longest mantissa length based on reverse_shift
			_t_q_mant_len = _o_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
		else:
			_t_q_mant_len = _o_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len < _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len >= _new_other_mant_len)
		
		#Add mantissa
		_t_q_mant = _new_self.mant.__float_add__(_new_other.mant)
		
		one = Binary([True])
		#Handle carry out
		if _t_q_mant.co:
			_t_q_mant.Append(True)
			_t_q_mant_len = _t_q_mant.GetLength()
			_t_q_exp_v += 1
		
		#Find leading one
		largest_one = -1
		for i in range(_t_q_mant.GetLength()-1, -1, -1):
			if _t_q_mant.data[i]:
				largest_one = i
				break
		
		#Pop leading one for floating point compliance
		#Shift is how many bits was popped at the top 
		if largest_one != -1:
			popped = _t_q_mant_len-(largest_one)
			_t_q_mant.LengthPop(popped, -1)
			
			if popped > 1:
				_t_q_exp_v -= popped-1
		
		#resized is how many bits was popped at the bottom
		resized = _o_t_q_mant_len-_t_q_mant_len
		i = 0
		try:
			while _t_q_mant.data[_t_q_mant.GetLength()-1] != True and i < resized:
				_t_q_mant.LengthPop(1)
				_t_q_exp_v += 1
				i += 1
		except IndexError:
			pass
		
		_t_q_exp_v_l = 0
		while 2**_t_q_exp_v_l <= abs(_t_q_exp_v):
			_t_q_exp_v_l += 1
		_t_q_exp_v_l += 1
		
		_t_q_exp = Binary()
		_t_q_exp.DoubleToBin(2**(_t_q_exp_v_l)-abs(_t_q_exp_v))
		_t_q_exp_l = _t_q_exp.GetLength()-1
		for i in range(_t_q_exp_v_l-_t_q_exp_l):
			_t_q_exp.Append(False)
		
		return hpf(_t_q_mant, _t_q_exp, self.sign)
	def __pure_sub__(self, other):
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign)
		_new_other = hpf(other.mant, other.exp, other.sign)
		
		#Check which has the largest value
		if _new_self.exp.ToInt() < _new_other.exp.ToInt():
			_t_q_exp = _new_self.exp
		else:
			_t_q_exp = _new_other.exp
		
		#Get lengths of mantissa
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		
		#Allign mantissa
		_new_self, _new_other, reverse_shift = _new_self.Allign(_new_other)
		# print("self : %s" % (_new_self.mant))
		# print("other: %s" % (_new_other.mant))
		
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		if reverse_shift:	#Get longest mantissa length based on reverse_shift
			_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
		else:
			_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len < _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len >= _new_other_mant_len)
		
		#Add mantissa
		_t_q_mant = _new_self.mant.__float_sub__(_new_other.mant)
		
		one = Binary([True])
		#Handle carry out
		if _t_q_mant.co == False:
			# _t_q_mant.Append(False)
			_t_q_mant_len = _t_q_mant.GetLength()
			two_compliment = Binary([True for i in range(_t_q_mant_len)])
			_t_q_mant = _t_q_mant.__xor__(two_compliment)
			_t_q_mant = _t_q_mant + one
			_new_self.sign = Binary([False])
		
		#Find leading one
		largest_one = -1
		for i in range(_t_q_mant_len):
			if _t_q_mant.data[i]:
				largest_one = i
				break
		
		#Pop leading one for floating point compliance
		if largest_one == -1:
			_t_q_mant = Binary([False for i in range(_t_q_mant_len)])
		else:
			#Shift is how many bits was popped at the top
			_t_q_mant.LengthPop(largest_one+1, -1)
			
			shifted_b = Binary()
			shifted_b.DoubleToBin(largest_one+1)
			_t_q_exp -= shifted_b
			
			#resized is how many bits was popped at the bottom
			resized = _t_q_mant.GetLength()-_t_q_mant_len
			i = 0
			while _t_q_mant.data[_t_q_mant.GetLength()-1] != True and i < resized:
				_t_q_mant.LengthPop(1)
				_t_q_exp -= one
				i += 1
		
		return hpf(_t_q_mant, _t_q_exp, _new_self.sign)
	
	def __add__(self, other):
		if self.sign.data[0]:
			if other.sign.data[0]:
				return self.__pure_add__(other)
			return self.__pure_sub__(other)
		if other.sign.data[0]:
			return other.__pure_sub__(self)
		_t_q = self.__pure_add__(other)
		_t_q.sign.data[0] = False
		return _t_q
	def __sub__(self, other):
		if self.sign.data[0]:
			if other.sign.data[0]:
				return self.__pure_sub__(other)
			return other.__pure_sub__(self)
		if other.sign.data[0]:
			_t_q = self.__pure_add__(other)
			_t_q.sign.data[0] = False
		_t_q = self.__pure_sub__(other)
		_t_q.sign.data[0] = not _t_q.sign.data[0]
		return _t_q
	
	def __mul__(self, other, set_precision=False):
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign)
		_new_other = hpf(other.mant, other.exp, other.sign)
		
		#Add leading one for computation
		_new_self.mant.Append(True)
		_new_other.mant.Append(True)
		
		#Make _t_q object for computation
		_t_q_mant_len = _new_self.mant.GetLength()+_new_other.mant.GetLength()
		_t_q = Binary([False for i in range(_t_q_mant_len)])
		
		#Calculate exponent values
		_new_self_exp_v = 2**(self.exp.GetLength()-1)-self.exp.ToInt()
		_new_other_exp_v = 2**(other.exp.GetLength()-1)-other.exp.ToInt()
		_t_q_exp_v = _new_self_exp_v + _new_other_exp_v
		
		#Calculate multiplication of mantissa
		co_offset = 0
		for i in range(len(_new_self.mant.data)-1, -1, -1):
			if _new_self.mant.data[i]:
				_t_q_mant, _t_other = _t_q.Allign(_new_other.mant, True, (_new_self.mant.GetLength()+co_offset)-(i+1))
				_t_q = _t_q_mant + _t_other
				if _t_q.co:
					co_offset += 1
					_t_q_exp_v += 1
					_t_q.Append(True)
		
		
		#Calculate _t_q sign
		_t_q_sig = Binary([self.sign.__xor__(other.sign).data[0]])
		
		#Find leading one
		largest_one = -1
		for i in range(_t_q.GetLength()-1):
			if _t_q.data[_t_q.GetLength()-1-i]:
				largest_one = i
				break
		
		#Pop leading one for floating point compliance
		if largest_one == -1:
			_t_q = Binary([False for i in range(_t_q.GetLength())])
		else:
			#Shift is how many bits was popped at the top
			_t_q.LengthPop(largest_one+1, -1)
			
			_t_q_exp_v += largest_one
			
			#resized is how many bits was popped at the bottom
			resized = _t_q_mant_len-_t_q.GetLength()
			i = 0
			while _t_q.data[0] != True and i < resized:
				_t_q.LengthPop(1)
				# _t_q_exp_v += 1
				i += 1
		
		#Calculate _t_q_exp
		_t_q_exp_v_l = 0
		while 2**_t_q_exp_v_l <= abs(_t_q_exp_v):
			_t_q_exp_v_l += 1
		_t_q_exp_v_l += 1
		
		_t_q_exp = Binary()
		_t_q_exp.DoubleToBin(2**(_t_q_exp_v_l)-(_t_q_exp_v))
		
		_t_q_exp_l = _t_q_exp.GetLength()-1
		for i in range(_t_q_exp_v_l-_t_q_exp_l):
			_t_q_exp.Append(_t_q_exp_v >= 0)
		
		return hpf(_t_q, _t_q_exp, _t_q_sig)
	def __r_div__(self, other, set_precision=False):
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign)
		_new_other = hpf(other.mant, other.exp, other.sign)
		
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		
		#Add leading one for computation
		_new_self.mant.Append(True)
		_new_other.mant.Append(True)
		
		if set_precision:
			_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
			_t_q_mant = Binary([False for i in range(_t_q_mant_len)])
		else:
			_t_q_mant_len = set_precision
			_t_q_mant = Binary([False for i in range(set_precision)])
		
		for i in range(_t_q_mant_len):
			pass
		
	
	def __repr__(self):
		temp_mant = Binary(self.mant.data)
		temp_mant.Append(True)
		if self.sign.data:
			return "+%s|%s" % (str(self.exp), str(self.mant))
		else:
			return "-%s|%s" % (str(self.exp), str(self.mant))
	
	def __str__(self):
		temp_mant = Binary(self.mant.data)
		temp_mant.Append(True)
		try:
			exp_v = 2**(self.exp.GetLength()-1)-self.exp.ToInt()
			v = 2**exp_v*temp_mant.ToInt()/(2**(temp_mant.GetLength()-1))
		except OverflowError:
			v = "Infinity"
		sign = "-" * (self.sign.data[0] == False)
		return sign + str(v)

def test():
	va = hpf()
	vb = hpf()

	#a = .1
	va.mant = Binary([1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1])
	va.exp = Binary([0,0,1,1])
	va.sign = Binary([False])
	print("a: %s" % (va))
	print(va.__repr__())

	#b = 5
	vb.mant = Binary([1,0])
	vb.exp = Binary([0,1,0])
	vb.sign = Binary([True])
	print("b: %s" % (vb))
	print(vb.__repr__())

	vc = va * vb 

	#c
	print("c: %s" % (vc))
	print(vc.__repr__())

	#b = 3
	vb.mant = Binary([1])
	vb.exp = Binary([1,0])
	vb.sign = Binary([True])
	print("a: %s" % (va))
	print(va.__repr__())
	print("b: %s" % (vb))
	print(vb.__repr__())

	vc = va * vb 
	print("c: %s" % (vc))
	print(vc.__repr__())

	#b = 1.1
	vb.mant = Binary([1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0])
	vb.exp = Binary([0,1])
	vb.sign = Binary([True])
	print("a: %s" % (va))
	print(va.__repr__())
	print("b: %s" % (vb))
	print(vb.__repr__())

	#c
	vc = vb * va
	print("c: %s" % (vc))
	print(vc.__repr__())

# test()

def Fibonacci():
	a = hpf()
	a.exp = Binary([0,1])
	a.sign = Binary([1])
	
	b = hpf()
	b.exp = Binary([0,1])
	b.sign = Binary([1])
	
	for i in range(100000):
		if i % 2 == 0:
			a = a + b 
			print(a)
		else:
			b = a + b
			print(b)
	return 1