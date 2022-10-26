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
DivAllign(self, other, offset=0) -> function to allign mantissa for divisions
ToInt(self) -> function to convert Binary to int
DoubleToBin(self, a, precision=0) -> function to convert double to Binary with arbitrary precision
__eq__(self, other) -> equals comparison
__gt__(self, other) -> greater than comparison
__ge__(self, other) -> greater or equals comparison
__lt__(self, other) -> less than comparison
__le__(self, other) -> less or equals comparison
__ne__(self, other) -> not equals comparison
Abs(self) -> Absolute function, for omitting the sign for positive
__repr__(self) -> representation override for Binary class
__str__(self) -> string  representation override for Binary

For hpf:

__init__(self, mantissa=None, exp=None, sign=None) -> Initialization with optional initialization
Allign(self, other, additive=True) -> function to allign mantissa based on actual value with respect to exponent, additive for alligning for floating point arithmetic
__pure_add__(self, other) -> primitive function for add hpf
__pure_sub__(self, other) -> primitive function for sub hpf
__add__(self, other) -> full propper function to add arbitrary hpf
__sub__(self, other) -> full propper function to sub arbitrary hpf
__mul__(self, other) -> function for multiplication
__truediv__(self, other) -> function for division
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
	
	def __pure_add__(self, other, ci=False):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
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
		
		if ci:
			q.append(True)
		
		return Binary(q, ci, self.sign)
	def __pure_sub__(self, other, ci=True, using_twos_compliment=True):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
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
		
		if using_twos_compliment:
			if ci == True:
				return Binary(q, ci, ci)
			for i, e in enumerate(q):
				q[i] = not e
			
			_t_q_b = Binary(q)
			_t_q_b += Binary([True])
			q = _t_q_b.data
			sign = False
			return Binary(q, ci, sign)
		
		return Binary(q, ci, ci)
	
	def __add__(self, other):
		if self.sign:
			if other.sign:
				return self.__pure_add__(other)
			return self.__pure_sub__(other)
		if other.sign:
			return other.__pure_sub__(self)
		_t_q = self.__pure_add__(other)
		_t_q.sign = False
		return _t_q
	def __sub__(self, other):
		if self.sign:
			if other.sign:
				return self.__pure_sub__(other)
			_t_q = other.__pure_add__(self)
			_t_q.sign = True
			return _t_q
		if other.sign:
			_t_q = self.__pure_add__(other)
			_t_q.sign = False
			return _t_q
		_t_q = self.__pure_sub__(other)
		_t_q.sign = not _t_q.sign
		return _t_q
	
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
	def DivAllign(self, other, offset=0):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		#Get lengths
		_self_len = _new_self_bin.GetLength()
		_other_len = _new_other_bin.GetLength()
		
		_new_self_bin.InverseLengthAppend(offset)
		_new_other_bin.LengthAppend(offset)
		
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
	
	def LimitedToInt(self, depth=75):
		q = 0
		for i in range(depth):
			q += 2**i*self.data[self.GetLength()-depth+i]
		return q
	
	def DoubleToBin(self, a, precision=0):
		t = []
		xl = 0
		while 2**xl <= a:
			xl += 1
		for i in range(xl+precision):
			t.append(a % 2)
			if a % 2 == 1:
				a -= 1
			a /= 2
		
		self.data = t
	
	def GetLength(self):
		return len(self.data)
	
	def __eq__(self, other):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
		#Naive check by sign
		if _new_self_bin.sign != _new_other_bin.sign:
			return False
		
		#Allign mantissa
		_self_bin, _other_bin = _new_self_bin.Allign(_new_other_bin)
		
		temp_true  = self.sign
		temp_false = not self.sign
		
		#Iterate over bits from top down
		_max = _self_bin.GetLength()-1
		for i in range(_max+1):
			#If self is larger
			if _self_bin.data[_max-i] == True and _other_bin.data[_max-i] != True:
				return temp_false
			#If other is larger
			if _self_bin.data[_max-i] != True and _other_bin.data[_max-i] == True:
				return temp_false
		
		return True
	def __gt__(self, other, Inverse=False):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
		#Naive check by sign
		if _new_self_bin.sign == True and _new_other_bin.sign != True:
			return True
		elif _new_self_bin.sign != True and _new_other_bin.sign == True:
			return False
		
		#Allign mantissa
		_self_bin, _other_bin = _new_self_bin.Allign(_new_other_bin, Inverse)
		
		temp_true  = self.sign
		temp_false = not self.sign
		
		#Iterate over bits from top down
		_max = _self_bin.GetLength()-1
		for i in range(_max+1):
			#If self is larger
			if _self_bin.data[_max-i] == True and _other_bin.data[_max-i] != True:
				return temp_true
			#If other is larger
			if _self_bin.data[_max-i] != True and _other_bin.data[_max-i] == True:
				return temp_false
		
		return False
	def __ge__(self, other, Inverse=False):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
		#Naive check by sign
		if _new_self_bin.sign == True and _new_other_bin.sign != True:
			return True
		elif _new_self_bin.sign != True and _new_other_bin.sign == True:
			return False
		
		#Allign mantissa
		_self_bin, _other_bin = _new_self_bin.Allign(_new_other_bin, Inverse)
		
		temp_true  = self.sign
		temp_false = not self.sign
		
		#Iterate over bits from top down
		_max = _self_bin.GetLength()-1
		for i in range(_max+1):
			#If self is larger
			if _self_bin.data[_max-i] == True and _other_bin.data[_max-i] != True:
				return temp_true
			#If other is larger
			if _self_bin.data[_max-i] != True and _other_bin.data[_max-i] == True:
				return temp_false
		
		return True
	def __lt__(self, other, Inverse=False):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
		#Naive check by sign
		if _new_self_bin.sign == True and _new_other_bin.sign != True:
			return False
		elif _new_self_bin.sign != True and _new_other_bin.sign == True:
			return True
		
		#Allign mantissa
		_self_bin, _other_bin = _new_self_bin.Allign(_new_other_bin, Inverse)
		
		temp_true  = self.sign
		temp_false = not self.sign
		
		#Iterate over bits from top down
		_max = _self_bin.GetLength()-1
		for i in range(_max+1):
			#If self is larger
			if _self_bin.data[_max-i] == True and _other_bin.data[_max-i] != True:
				return temp_false
			#If other is larger
			if _self_bin.data[_max-i] != True and _other_bin.data[_max-i] == True:
				return temp_true
		
		return False
	def __le__(self, other, Inverse=False):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
		#Naive check by sign
		if _new_self_bin.sign == True and _new_other_bin.sign != True:
			return False
		elif _new_self_bin.sign != True and _new_other_bin.sign == True:
			return True
		
		#Allign mantissa
		_self_bin, _other_bin = _new_self_bin.Allign(_new_other_bin, Inverse)
		
		temp_true  = self.sign
		temp_false = not self.sign
		
		#Iterate over bits from top down
		_max = _self_bin.GetLength()-1
		for i in range(_max+1):
			#If self is larger
			if _self_bin.data[_max-i] == True and _other_bin.data[_max-i] != True:
				return temp_false
			#If other is larger
			if _self_bin.data[_max-i] != True and _other_bin.data[_max-i] == True:
				return temp_true
		
		return True
	def __ne__(self, other):
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data, self.co, self.sign)
		_new_other_bin = Binary(other.data, other.co, other.sign)
		
		#Naive check by sign
		if _new_self_bin.sign == True and _new_other_bin.sign != True:
			return True
		elif _new_self_bin.sign != True and _new_other_bin.sign == True:
			return True
		
		#Allign mantissa
		_self_bin, _other_bin = _new_self_bin.Allign(_new_other_bin)
		
		temp_true  = self.sign
		temp_false = not self.sign
		
		#Iterate over bits from top down
		_max = _self_bin.GetLength()-1
		for i in range(_max+1):
			#If self is larger
			if _self_bin.data[_max-i] == True and _other_bin.data[_max-i] != True:
				return temp_true
			#If other is larger
			if _self_bin.data[_max-i] != True and _other_bin.data[_max-i] == True:
				return temp_true
		
		return False
	
	def Abs(self):
		return Binary(self.data, self.co, True)
	
	def __repr__(self):
		_str = ("-" * (self.sign == False)) + "0b"
		for bit in self.data:
			_str += "1" if bit else "0"
		return _str
	
	def __str__(self):
		return str(self.ToInt() * (1 * self.sign + -1 * (not self.sign)))

def ReturnableDoubleToBin(a, precision=0):
		t = []
		xl = 0
		while 2**xl <= a:
			xl += 1
		for i in range(xl+precision):
			t.append(a % 2)
			if a % 2 == 1:
				a -= 1
			a /= 2
		
		return Binary(t)

def TwosPow(n):
	q    = Binary([True])
	i	 = Binary([False], False, True)
	One  = Binary([True], False, True)
	while i < n:
		q.InverseAppend(False)
		i += One
	return q

@dataclass
class hpf:
	def __init__(self, mantissa=None, exp=None, sign=None, is_zero=None):
		if type(mantissa) == type(None):
			#Initialize mantissa for 24 bits, exponent for 8 bits and sign for 1 bit
			__mant_len__ = 24
			__expo_len__ = 8
			self.mant	 = Binary([False for i in range(__mant_len__)])
			self.exp	 = Binary([False for i in range(__expo_len__)])
			self.sign	 = Binary([False])
			self.is_zero = Binary([False])
			
			self.mant_length = __mant_len__
			self.exp_length  = __expo_len__
		else:
			_NoneType = type(None)
			if type(exp) == _NoneType or type(sign) == _NoneType or type(is_zero) == _NoneType:
				raise CustomException("Error: Initialization of hpf class requires mantissa, exp, sign and is_zero to be declared")
			self.mant	 = Binary(mantissa.data)
			self.exp	 = Binary(exp.data)
			self.sign	 = Binary(sign.data)
			self.is_zero = Binary(is_zero.data)
			
			self.mant_length	= mantissa.GetLength()
			self.exp_length		= exp.GetLength()
	
	def Allign(self, other, additive=True):
		# print("\nhpf.Allign:")
		bin = Binary()
		Zero = Binary([False])
		One = Binary([True])
		reverse_shift = False
		
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Calculate exponent values
		_self_exp = _new_self.exp.__xor__(_new_self.exp)
		_other_exp = _new_other.exp.__xor__(_new_other.exp)
		
		_self_exp.data[_self_exp.GetLength()-1] = True
		_other_exp.data[_other_exp.GetLength()-1] = True
		
		_self_exp_val = _self_exp-_new_self.exp
		_other_exp_val = _other_exp-_new_other.exp
		
		# print("_self_exp_val:  %s" % (_self_exp_val))
		# print("_other_exp_val: %s" % (_other_exp_val))
		
		#Add leading one for calculations
		if additive:
			_new_self.mant.Append(True)
			_new_other.mant.Append(True)
		
		#If self represents a larger number
		if _other_exp_val < _self_exp_val:
			# print("Greater")
			#Calculate amount to shift
			shift = _self_exp_val - _other_exp_val
			offset = _new_self.mant.GetLength() - _new_other.mant.GetLength()
			
			#Shift the mantissa the appropriate amounts
			if shift < Zero:
				_new_self.mant.InverseLengthAppend(shift.Abs().ToInt())
				reverse_shift = True
			else:
				_new_other.mant.LengthAppend(shift.ToInt())
				_new_other.mant.InverseLengthAppend(offset)
		else:	#If other represents a larger number
			# print("Lesser")
			#Calculate amount to shift
			shift = _other_exp_val - _self_exp_val
			offset = _new_self.mant.GetLength() - _new_other.mant.GetLength()
			
			#Shift the mantissa the appropriate amounts
			if shift < Zero:
				_new_other.mant.InverseLengthAppend(shift.Abs().ToInt())
				reverse_shift = True
			else:
				_new_self.mant.LengthAppend(shift.ToInt())
				_new_self.mant.InverseLengthAppend(offset)
		
		return _new_self, _new_other, reverse_shift
	
	def __pure_add__(self, other):
		bin = Binary()
		Zero = Binary([False],False,True)
		One = Binary([True],False,True)
		
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Calculate exponent values
		#Zero out exp values for length and value calculations
		_self_exp_l_bin = _new_self.exp.__xor__(_new_self.exp)
		_other_exp_l_bin = _new_other.exp.__xor__(_new_other.exp)
		
		#Add leading ones back in within the size of the exponents
		_self_exp_l_bin.data[_self_exp_l_bin.GetLength()-1] = True
		_other_exp_l_bin.data[_other_exp_l_bin.GetLength()-1] = True
		
		#Calculate actual values of exponents
		_new_self_exp_v  = _self_exp_l_bin-_new_self.exp
		_new_other_exp_v = _other_exp_l_bin-_new_other.exp
		
		#Check which has the largest value
		if _new_self_exp_v > _new_other_exp_v:
			_t_q_exp_v = _new_self_exp_v
		else:
			_t_q_exp_v = _new_other_exp_v
		
		#Get lengths of mantissa
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		
		#Allign mantissa
		_new_self, _new_other, reverse_shift = _new_self.Allign(_new_other)
		
		#Get longest mantissa length based on reverse_shift
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		if reverse_shift:	
			_o_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
		else:
			_o_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len < _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len >= _new_other_mant_len)
		
		#Add mantissa
		_t_q_mant = _new_self.mant.__float_add__(_new_other.mant)
		
		one = Binary([True])
		#Handle carry out
		if _t_q_mant.co:
			_t_q_mant.Append(True)
			_t_q_exp_v += One
		
		#Find leading one
		largest_one = -1
		_max = _t_q_mant.GetLength()-1
		for i in range(_max):
			if _t_q_mant.data[_max-i]:
				largest_one = i
				break
		
		#Pop leading one for floating point compliance
		#Shift is how many bits was popped at the top 
		if largest_one != -1:
			popped = largest_one
			_t_q_mant.LengthPop(popped+1, -1)
			
			_bin_largest_one = ReturnableDoubleToBin(largest_one)
			_t_q_exp_v += _bin_largest_one
			
			#resized is how many bits was popped at the bottom
			for i in range(_t_q_mant.GetLength()-2):
				if _t_q_mant.data[0]:
					break
				_t_q_mant.Pop(0)
		
		#Calculate _t_q_exp
		_t_q_exp_v_l = Binary([False],False,True)
		while TwosPow(_t_q_exp_v_l) <= _t_q_exp_v.Abs():
			_t_q_exp_v_l += One
		_t_q_exp_v_l += One
		
		#Remove leading zeros for propper calculation
		_t_q_exp = TwosPow(_t_q_exp_v_l)-_t_q_exp_v
		try:
			while _t_q_exp.data[_t_q_exp.GetLength()-1] != True:
				_t_q_exp.Pop(_t_q_exp.GetLength()-1)
		except IndexError:
			pass
		
		#Calculate _t_q_exp_l
		_t_q_exp_l = Binary()
		_t_q_exp_l.DoubleToBin(_t_q_exp.GetLength()-1)
		
		#Add leading zero for propper exponent value
		i = Binary([False], False, True)
		while i < _t_q_exp_v_l-_t_q_exp_l.Abs():
			_t_q_exp.Append(_t_q_exp_v < Zero)
			i += One
		
		#Handle zero
		if self.is_zero.data[0]:
			if other.is_zero.data[0]:
				return hpf(Binary([False]), Binary([False]), Binary([True]), Binary([True]))
			else:
				return other
		else:
			if other.is_zero.data[0]:
				return self
		
		return hpf(_t_q_mant, _t_q_exp, self.sign, self.is_zero)
	def __pure_sub__(self, other):
		bin  = Binary()
		Zero = Binary([False])
		One  = Binary([True])
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Calculate exponent values
		_new_self_exp	= _new_self.exp.__xor__(  _new_self.exp)
		_new_other_exp	= _new_other.exp.__xor__(_new_other.exp)
		
		_new_self_exp.data[  _new_self_exp.GetLength()-1] = True
		_new_other_exp.data[_new_other_exp.GetLength()-1] = True
		
		_self_exp_val	= _new_self_exp- _new_self.exp
		_other_exp_val	= _new_other_exp-_new_other.exp
		
		if _self_exp_val > _other_exp_val:
			_t_q_exp_v = _self_exp_val
		else:
			_t_q_exp_v = _other_exp_val
		
		#Allign mantissa
		_new_self, _new_other, reverse_shift = _new_self.Allign(_new_other)
		
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		
		_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
		
		#Add mantissa
		_t_q_mant = _new_self.mant.__float_sub__(_new_other.mant)
		
		#Handle carry out
		if _t_q_mant.co == False:
			# _t_q_mant.Append(False)
			_t_q_mant_len = _t_q_mant.GetLength()
			two_compliment = Binary([True for i in range(_t_q_mant_len)])
			_t_q_mant = _t_q_mant.__xor__(two_compliment)
			_t_q_mant = _t_q_mant + One
			_new_self.sign = Binary([False])
		
		#Find leading one
		largest_one = -1
		_max = _t_q_mant.GetLength()-1
		for i in range(_max):
			if _t_q_mant.data[_max-i]:
				largest_one = i
				break
		
		#Pop leading one for floating point compliance
		if largest_one == -1:
			_t_q_mant = Binary([False for i in range(_t_q_mant_len)])
			_new_self.is_zero = Binary([True])
		else:
			#Shift is how many bits was popped at the top
			_t_q_mant.LengthPop(largest_one+1, -1)
			
			shifted_b = ReturnableDoubleToBin(largest_one)
			_t_q_exp_v -= shifted_b
			
			#resized is how many bits was popped at the bottom
			for i in range(_t_q_mant.GetLength()-2):
				if _t_q_mant.data[0]:
					break
				_t_q_mant.Pop(0)
		
		#Calculate _t_q_exp
		_t_q_exp_v_l = Binary()
		while TwosPow(_t_q_exp_v_l) <= _t_q_exp_v.Abs():
			_t_q_exp_v_l += One
		_t_q_exp_v_l += One
		
		#Remove leading zeros for propper calculation
		_t_q_exp = TwosPow(_t_q_exp_v_l)-_t_q_exp_v
		while _t_q_exp.data[_t_q_exp.GetLength()-1] != True and _t_q_exp.GetLength() > 1:
			_t_q_exp.Pop(_t_q_exp.GetLength()-1)
		
		#Calculate _t_q_exp_l
		_t_q_exp_l = Binary()
		_t_q_exp_l.DoubleToBin(_t_q_exp.GetLength()-1)
		
		#Add leading zero for propper exponent value
		i = _t_q_exp_v_l-_t_q_exp_l
		while i > Zero:
			_t_q_exp.Append(_t_q_exp_v <= Zero)
			i -= One
		
		#Handle zero
		if self.is_zero.data[0]:
			if other.is_zero.data[0]:
				hpf(Binary([False]), Binary([False]), Binary([True]), Binary([True]))
			else:
				self.is_zero = Binary([False])
				return hpf(other.mant, other.exp, Binary([not other.sign.data[0]]), other.is_zero)
		else:
			if other.is_zero.data[0]:
				return self
		
		return hpf(_t_q_mant, _t_q_exp, _new_self.sign, self.is_zero)
	
	def __add__(self, other):
		if self.sign.data[0]:
			if other.sign.data[0]:
				return self.__pure_add__(other)
			return self.__pure_sub__(other)
		if other.sign.data[0]:
			return self.__pure_sub__(other)
		_t_q = self.__pure_add__(other)
		_t_q.sign.data[0] = False
		return _t_q
	def __sub__(self, other):
		if self.sign.data[0]:
			if other.sign.data[0]:
				return self.__pure_sub__(other)
			return self.__pure_add__(other)
		if other.sign.data[0]:
			_t_q = self.__pure_add__(other)
			_t_q.sign.data[0] = False
			return _t_q
		_t_q = self.__pure_sub__(other)
		_t_q.sign.data[0] = not _t_q.sign.data[0]
		return _t_q
	
	def __mul__(self, other, set_precision=False):
		bin = Binary()
		Zero = Binary([False])
		One = Binary([True])
		
		if self.is_zero.data[0] or other.is_zero.data[0]:
			return hpf(Binary([False]), Binary([True]), Binary([True]), Binary([True]))
		
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Add leading one for computation
		_new_self.mant.Append(True)
		_new_other.mant.Append(True)
		
		#Make _t_q object for computation
		_t_q_mant_len = _new_self.mant.GetLength()+_new_other.mant.GetLength()
		_t_q = Binary([False for i in range(_t_q_mant_len)])
		
		#Calculate exponent values
		#Zero out exp values for length and value calculations
		_self_exp_l_bin = _new_self.exp.__xor__(_new_self.exp)
		_other_exp_l_bin = _new_other.exp.__xor__(_new_other.exp)
		
		#Add leading ones back in within the size of the exponents
		_self_exp_l_bin.data[_self_exp_l_bin.GetLength()-1] = True
		_other_exp_l_bin.data[_other_exp_l_bin.GetLength()-1] = True
		
		#Calculate actual values of exponents
		_new_self_exp_v  = _self_exp_l_bin-_new_self.exp
		_new_other_exp_v = _other_exp_l_bin-_new_other.exp
		_t_q_exp_v = _new_self_exp_v + _new_other_exp_v
		
		if _t_q_exp_v.co:
			_t_q_exp_v.Append(True)
		
		#Calculate multiplication of mantissa
		co_offset = 0
		for i in range(len(_new_self.mant.data)-1, -1, -1):
			if _new_self.mant.data[i]:
				_t_q_mant, _t_other = _t_q.Allign(_new_other.mant, True, (_new_self.mant.GetLength()+co_offset)-(i+1))
				_t_q = _t_q_mant + _t_other
				if _t_q.co:
					co_offset += 1
					_t_q_exp_v += One
					_t_q.Append(True)
		
		#Calculate _t_q sign
		_t_q_sig = Binary([self.sign.data[0] and other.sign.data[0]])
		
		#Find leading one
		largest_one = -1
		_max = _t_q.GetLength()-1
		for i in range(_max):
			if _t_q.data[_max-i]:
				largest_one = i
				break
		
		#Pop leading one for floating point compliance
		if largest_one == -1:
			_t_q = Binary([False for i in range(_t_q.GetLength())])
		else:
			#Shift is how many bits was popped at the top
			_t_q.LengthPop(largest_one+1, -1)
			
			# _bin_largest_one = ReturnableDoubleToBin(largest_one)
			
			#resized is how many bits was popped at the bottom
			resized = _t_q_mant_len-_t_q.GetLength()
			i = 0
			while _t_q.data[0] != True and i < resized:
				_t_q.Pop(0)
				i += 1
		
		#Calculate _t_q_exp
		_t_q_exp_v_l = Binary()
		while TwosPow(_t_q_exp_v_l) <= _t_q_exp_v.Abs():
			_t_q_exp_v_l += One
		_t_q_exp_v_l += One
		
		#Remove leading zeros for propper calculation
		_t_q_exp = TwosPow(_t_q_exp_v_l)-_t_q_exp_v
		while _t_q_exp.data[_t_q_exp.GetLength()-1] != True:
			_t_q_exp.Pop(_t_q_exp.GetLength()-1)
		
		#Calculate _t_q_exp_l
		_t_q_exp_l = Binary()
		_t_q_exp_l.DoubleToBin(_t_q_exp.GetLength()-1)
		
		#Add leading zero for propper exponent value
		i = _t_q_exp_v_l-_t_q_exp_l
		while i > Zero:
			_t_q_exp.Append(_t_q_exp_v < Zero)
			i -= One
		
		return hpf(_t_q, _t_q_exp, _t_q_sig, self.is_zero)
	def __truediv__(self, other, set_precision=False):
		bin = Binary()
		One = Binary([True])
		Zero = Binary([False])
		if self.is_zero.data[0]:
			return hpf(Binary([False]), Binary([True]), Binary([True]), Binary([True]))
		if other.is_zero.data[0]:
			raise ZeroDivisionError
		
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Add leading one for computation
		_new_self.mant.Append(True)
		_new_other.mant.Append(True)
		
		#Calculate exponent values
		#Zero out exp values for length and value calculations
		_self_exp_l_bin = _new_self.exp.__xor__(_new_self.exp)
		_other_exp_l_bin = _new_other.exp.__xor__(_new_other.exp)
		
		#Add leading ones back in within the size of the exponents
		_self_exp_l_bin.data[_self_exp_l_bin.GetLength()-1] = True
		_other_exp_l_bin.data[_other_exp_l_bin.GetLength()-1] = True
		
		#Calculate actual values of exponents
		_new_self_exp_v  = _self_exp_l_bin-_new_self.exp
		_new_other_exp_v = _other_exp_l_bin-_new_other.exp
		_t_q_exp_v = _new_self_exp_v - _new_other_exp_v
		
		#Allign mantissas
		_new_self.mant, _new_other.mant = _new_self.mant.Allign(_new_other.mant, True)
		
		#Set _t_q_mant_len based on set_precision
		if type(set_precision) != type(False):
			_t_q_mant_len = set_precision
		else:
			_t_q_mant_len = 2 * _new_self.mant.GetLength()
		_t_q_mant = Binary([False for i in range(_t_q_mant_len)])
		
		#Calculate actual division
		offs = 0
		_max = _t_q_mant.GetLength()-1
		for i in range(_max):
			_t_self_mant, _t_other_mant = _new_self.mant.DivAllign(_new_other.mant, offs)
			offs += 1
			_t_sub_res = _t_self_mant - _t_other_mant
			
			#If subtraction is positive
			if _t_sub_res.sign:
				offs = 1
				_t_q_mant.data[_max-i] = True
				_new_self.mant = _t_sub_res
		
		#Find leading one
		largest_one = -1
		for i in range(_max):
			if _t_q_mant.data[_max-i]:
				largest_one = i
				break
		
		#Pop leading one for floating point compliance
		if largest_one != -1:
			#Shift is how many bits was popped at the top
			_t_q_mant.LengthPop(largest_one+1, -1)
			
			_bin_largest_one = ReturnableDoubleToBin(largest_one)
			_t_q_exp_v -= _bin_largest_one
		
		#Calculate _t_q_exp
		_t_q_exp_v_l = Binary()
		while TwosPow(_t_q_exp_v_l) < _t_q_exp_v.Abs():
			_t_q_exp_v_l += One
		_t_q_exp_v_l += One
		
		#Remove leading zeros for propper calculation
		_t_q_exp = TwosPow(_t_q_exp_v_l)-_t_q_exp_v
		while _t_q_exp.data[_t_q_exp.GetLength()-1] != True and _t_q_exp.GetLength() > 1:
			_t_q_exp.Pop(_t_q_exp.GetLength()-1)
		
		#Calculate _t_q_exp_l
		_t_q_exp_l = Binary()
		_t_q_exp_l.DoubleToBin(_t_q_exp.GetLength()-1)
		
		#Add leading zero for propper exponent value
		i = _t_q_exp_v_l-_t_q_exp_l
		while i > Zero:
			_t_q_exp.Append(_t_q_exp_v < Zero)
			i -= One
		
		return hpf(_t_q_mant, _t_q_exp, _new_self.sign, self.is_zero)
	
	def __eq__(self, other):
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Add leading one for computation
		_new_self.mant.Append(True)
		_new_other.mant.Append(True)
		
		#Check by is_zero
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0] == True:
			return True
		if _new_self.is_zero.data[0] != True and _new_other.is_zero.data[0] == True:
			return False
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0]!= True:
			return False
			
		od = _new_self / _new_other
		ad = _new_other / _new_self
		
		if od.sign != ad.sign:
			return False
		if od.exp != ad.exp:
			return False
		if od.mant != ad.mant:
			return False
		
		return True
	def __lt__(self, other):
	
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Check by is_zero
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0] == True:
			return False
		if _new_self.is_zero.data[0] != True and _new_other.is_zero.data[0] == True:
			return new_self.sign.data[0] != True
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0]!= True:
			return _new_other.sign.data[0] != True
		
		od = _new_self.__truediv__(_new_other, _new_self.mant.GetLength()+_new_other.mant.GetLength()+25)
		
		#Add leading one for computation
		od.mant.Append(True)
		
		#Calculate exponent values
		#Zero out exp values for length and value calculations
		_self_exp_l_bin = od.exp.__xor__(od.exp)
		
		#Add leading ones back in within the size of the exponents
		# _self_exp_l_bin.data[_self_exp_l_bin.GetLength()-1] = True
		
		#Calculate actual values of exponents
		_new_self_exp_v  = _self_exp_l_bin-od.exp
		
		if od.exp.data[od.exp.GetLength()-1]:
			return False
		
		return True
	def __le__(self, other):
		if self.__eq__(other) or self.__lt__(other):
			return True
		return False
	def __gt__(self, other):
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Check by is_zero
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0] == True:
			return False
		if _new_self.is_zero.data[0] != True and _new_other.is_zero.data[0] == True:
			return new_self.sign.data[0] == True
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0]!= True:
			return new_self.sign.data[0] == True
		
		od = _new_self.__truediv__(_new_other, 50)
		
		#Add leading one for computation
		od.mant.Append(True)
		
		#Calculate exponent values
		#Zero out exp values for length and value calculations
		_self_exp_l_bin = od.exp.__xor__(od.exp)
		
		#Add leading ones back in within the size of the exponents
		_self_exp_l_bin.data[_self_exp_l_bin.GetLength()-1] = True
		
		#Calculate actual values of exponents
		_new_self_exp_v  = _self_exp_l_bin-od.exp	
		if od.exp.data[od.exp.GetLength()-1]:
			return True
		
		return False
	def __ge__(self, other):
		if self.__eq__(other) or self.__gt__(other):
			return True
		return False
	def __ne__(self, other):
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
		_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		
		#Check by is_zero
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0] == True:
			return False
		if _new_self.is_zero.data[0] != True and _new_other.is_zero.data[0] == True:
			return True
		if _new_self.is_zero.data[0] == True and _new_other.is_zero.data[0]!= True:
			return True
			
		od = _new_self.__truediv__(_new_other, 50)
		ad = _new_other.__truediv__(_new_self, 50)
		
		#Add leading one for computation
		_new_self.mant.Append(True)
		_new_other.mant.Append(True)
		
		if od.sign != ad.sign:
			return True
		if od.exp != ad.exp:
			return True
		if od.mant != ad.mant:
			return True
		
		return False
	
	def DeepCopy(self):
		return hpf(self.mant, self.exp, self.sign, self.is_zero)
	
	def ToFloat(self):
		temp_mant = Binary(self.mant.data)
		temp_mant.Append(True)
		try:
			exp_v = 2**(self.exp.GetLength()-1)-self.exp.ToInt()
			q = 2**exp_v*temp_mant.ToInt()/(2**(temp_mant.GetLength()-1))
		except OverflowError:
			q = float('inf')
		if self.sign.data[0] == False:
			q *= -1
		return q
	
	def Abs(self):
		return hpf(self.mant, self.exp, Binary([True]), self.is_zero)
	
	def __repr__(self):
		if self.is_zero.data[0]:
			return "0|0"
		temp_mant = Binary(self.mant.data)
		temp_mant.Append(True)
		if self.sign.data:
			return "+%s|%s" % (self.exp.__repr__(), self.mant.__repr__())
			
		return "-%s|%s" % (self.exp.__repr__(), self.mant.__repr__())
	
	def __str__(self):
		depth = 85
		if self.is_zero.data[0]:
			return "0"
		temp_mant = Binary(self.mant.data)
		temp_mant.Append(True)
		try:
			exp_v = 2**(self.exp.GetLength()-1)-self.exp.ToInt()
			if temp_mant.GetLength() > depth:
				v = 2**exp_v*temp_mant.LimitedToInt(depth)/(2**(depth-1))
			else:
				v = 2**exp_v*temp_mant.ToInt()/(2**(temp_mant.GetLength()-1))
		except OverflowError:
			v = "Infinity"
		sign = "-" * (self.sign.data[0] == False)
		return sign + str(v)

_Zero = hpf(Binary([False]), Binary([False]), Binary([True]), Binary([True]))
_One = hpf(Binary([False]), Binary([True]), Binary([True]), Binary([False]))
_Two = hpf(Binary([False]), Binary([False]), Binary([True]), Binary([False]))

def factorial(n: hpf):
	One = _One.DeepCopy()
	i = _One.DeepCopy()
	q = _One.DeepCopy()
	top = n + One
	while i != top:
		q *= i
		i += One
	return q

def x_to_the_y(x, y):
	One = _One.DeepCopy()
	i = _One.DeepCopy()
	q = x.DeepCopy()
	while i.Abs() < y.Abs():
		q *= x
		i += One
	return q

def _exp_temp(n):
	One = _One.DeepCopy()
	Two = _Two.DeepCopy()
	return Two * n + One

def sin(n, iters=50, show_iters=True):
	#Boring setup
	q = _Zero.DeepCopy()
	i = _Zero.DeepCopy()
	One = _One.DeepCopy()
	
	#Actual computation
	for _i in range(iters):
		if show_iters:
			print("\ni: %s, q: %s" % (_i, q))
		_temp = _exp_temp(i)
		_exp_divisor = x_to_the_y(n, _temp)
		_fac_dividend = factorial(_temp)
		_exp_divided = _exp_divisor.__truediv__(_fac_dividend, _exp_divisor.mant.GetLength()+_fac_dividend.mant.GetLength()+100)
		if _i % 2 == 0:
			q = q + _exp_divided
		else:
			q = q - _exp_divided
		i += One
	return q

def test():
	a = hpf()
	
	a.mant		= Binary([0])
	a.exp		= Binary([1])
	a.sign		= Binary([True])
	a.is_zero	= Binary([False])
	
	tf = sin(a)
	
	print("sin(%s) = %s" % (a, tf))
	print(tf.__repr__())

test()
