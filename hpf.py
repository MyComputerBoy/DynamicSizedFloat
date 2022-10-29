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
__init__(self, mantissa=None, exp=None, sign=None) -> initialization with optional initialization
Allign(self, other, additive=True) -> function to allign mantissa based on actual value with respect to exponent, additive for alligning for floating point arithmetic
__pure_add__(self, other) -> primitive function for add hpf
__pure_sub__(self, other) -> primitive function for sub hpf
__add__(self, other) -> full propper function to add arbitrary hpf
__sub__(self, other) -> full propper function to sub arbitrary hpf
__mul__(self, other) -> function for multiplication
__truediv__(self, other) -> function for division
__eq__(self, other) -> equals overload
__lt__(self, other) -> less than overload
__le__(self, other) -> less than or equals overload
__gt__(self, other) -> greater than overload
__ge__(self, other) -> greater than or equals overload
__ne__(self, other) -> not equals overload
DeepCopy(self) -> clone hpf with absolutely no ccopy of old object for no reference in any ways
ToFloat(self) -> Converts to float
Abs(self) -> Absolute function, for omitting the sign for positive
__repr__(self) -> representation override for hpf
__str__(self) -> string representation override for hpf
For __name__:
factorial(n) -> factorial of hpf n
x_to_the_y(x, y) -> x to the power of y or x**y
sin(n, iters=15, depth=1000, show_iters=False) -> sin in rads
exp(n, iters=15, show_iters=False) -> the exponential function
sqrt(n, depth=2000, iters=15, show_iters=True) -> square root of n
pi(depth=10000, iters=10) -> The Ramanujan-Sato approximation of pi
"""
from dataclasses import dataclass
import os
from time import time
import math as m 

#Set terminal colour to green (To look like it's from the Matrix)
os.system('color 2')

class CustomException(Exception):
	pass

@dataclass
class Binary:
	"""Class Binary: Proprietary format for arbitrarily large signed binary numbers
	Main user functions:
	
	__add__(self, other) -> add overload
	__sub__(self, other) -> sub overload
	Append(self, value) -> appends value to self.data
	Pop(self, index=0) -> pops self.data[index]
	LengthPop(self, value=1, index=0) -> pops value lengths of self.data[index]
	InverseAppend(self, value=False) -> self.data.insert(0, value)
	InverseLengthAppend(self, length=1, fill=False) -> InverseAppend(fill) length times
	ToInt(self) -> Converts to int
	LimitedToInt(self) -> Converts to Int without 'Infinity' problem
	DoubleToBin(self, a, precision=0) -> converts double to Binary with precision precision
	GetLength(self) -> Gets data length
	__eq__(self, other) -> equals comparison
	__gt__(self, other) -> greater than comparison
	__ge__(self, other) -> greater or equals comparison
	__lt__(self, other) -> less than comparison
	__le__(self, other) -> less or equals comparison
	__ne__(self, other) -> not equals comparison
	Abs(self) -> Absolute function, for omitting the sign for positive
	
	Main structure:
	Binary initializes to data=[0 for i in range(24)], co=False, sign=False
	data -> main data as mantissa
	co -> carry out flag
	sign -> sign flag, true is positive, false is negative
	"""
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
	
	def __pure_add__(self, other, ci=False, append_ci=True, propper_clean=True):
		if propper_clean:
			#Clone Binary objects to new temporary variables to not mess with original objects
			_new_self_bin = Binary(self.data, self.co, self.sign)
			_new_other_bin = Binary(other.data, other.co, other.sign)
			
			#Allign sizes for compatible addition
			[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin)
		else:
			_new_self_bin = self
			_new_other_bin = other
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate addition
		for i, e in enumerate(_new_self_bin.data):
			t = _new_self_bin.data[i] + _new_other_bin.data[i] + ci
			q[i] = t % 2
			ci = (t - (t % 2))/2
		
		if ci and append_ci:
			q.append(True)
		
		return Binary(q, ci, self.sign)
	def __pure_sub__(self, other, ci=True, using_twos_compliment=True, propper_clean=True):
		if propper_clean:
			#Clone Binary objects to new temporary variables to not mess with original objects
			_new_self_bin = Binary(self.data, self.co, self.sign)
			_new_other_bin = Binary(other.data, other.co, other.sign)
			
			#Allign sizes for compatible addition
			[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin)
		else:
			_new_self_bin = self
			_new_other_bin = other
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate subtraction
		for i, e in enumerate(_new_self_bin.data):
			t = _new_self_bin.data[i] + (not _new_other_bin.data[i]) + ci
			q[i] = t % 2
			ci = (t - (t % 2))/2
		
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
	
	def __float_add__(self, other, ci=False, propper_clean=True):
		if propper_clean:
			#Clone Binary objects to new temporary variables to not mess with original objects
			_new_self_bin = Binary(self.data)
			_new_other_bin = Binary(other.data)
		else:
			_new_self_bin = self 
			_new_other_bin = other
		
		#Allign sizes for compatible addition
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin, True, False)
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate addition
		for i, e in enumerate(_new_self_bin.data):
			t = _new_self_bin.data[i] + _new_other_bin.data[i] + ci
			q[i] = t % 2
			ci = (t - (t % 2))/2
		return Binary(q, ci)
	def __float_sub__(self, other, ci=True, propper_clean=True):
		if propper_clean:
			#Clone Binary objects to new temporary variables to not mess with original objects
			_new_self_bin = Binary(self.data)
			_new_other_bin = Binary(other.data)
		else:
			_new_self_bin = self 
			_new_other_bin = other
		
		#Allign sizes for compatible addition
		[_new_self_bin, _new_other_bin] = _new_self_bin.Allign(_new_other_bin, True, False)
		
		#Create output list
		q = [False for i in range(_new_self_bin.GetLength())]
		
		#Calculate subtraction
		for i, e in enumerate(_new_self_bin.data):
			t = _new_self_bin.data[i] + (1-_new_other_bin.data[i]) + ci
			q[i] = t % 2
			ci = (t - (t % 2))/2
		return Binary(q, ci)
	
	def Allign(self, other, Inverse=False, offset=0, propper_clean=True):
		if propper_clean:
			#Clone Binary objects to new temporary variables to not mess with original objects
			_new_self_bin = Binary(self.data)
			_new_other_bin = Binary(other.data)
			
		else:
			_new_self_bin = self
			_new_other_bin = other
		
		#Get lengths
		_self_len = _new_self_bin.GetLength()
		_other_len = _new_other_bin.GetLength()
		
		#Append appropriate lengths to appropriate object
		if Inverse:
			if _self_len < _other_len:
				_new_self_bin.InverseLengthAppend(_other_len-_self_len)
			else:
				_new_other_bin.InverseLengthAppend((_self_len-_other_len)-offset)
				_new_other_bin.LengthAppend(offset)
			
			return _new_self_bin, _new_other_bin
		
		if _self_len < _other_len:
			if _other_len - _self_len >= 1:
				_new_self_bin.LengthAppend(_other_len-_self_len)
		else:
			if _self_len - _other_len >= 1:
				_new_other_bin.LengthAppend((_self_len-_other_len)-offset)
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
	"""Class hpf -> Proprietary format for arbitrarily high precision floating point numbers
	Main user functions:
	
	__add__(self, other) -> add overload
	__sub__(self, other) -> sub overload
	__mul__(self, other, set_precision=False) -> mul overload with optional predefined precision
	__truediv__(self, other, set_precision=False, preemptive_offset=None) -> truediv overload with optional predefined precision and optional exponent offset
	__eq__(self, other) -> equals overload
	__lt__(self, other) -> less than overload
	__le__(self, other) -> less than or equals overload
	__gt__(self, other) -> greater than overload
	__ge__(self, other) -> greater than or equals overload
	__ne__(self, other) -> not equals overload
	DeepCopy(self) -> clone hpf with absolutely no ccopy of old object for no reference in any ways
	ToFloat(self) -> Converts to float
	Abs(self) -> Absolute function, for omitting the sign for positive
	__repr__(self) -> representation override for hpf
	__str__(self) -> string representation override for hpf
	
	Main structure:
	hpf initializes to mantissa=Binary([0 for i in range(24)]), exp=Binary([0 for i in range(8)]), sign=Binary([1]), is_integer=Binary([0])
	mantissa -> main data or mantissa
	exp -> exponent, is defined as (2**(exp.GetLength()-1))-exp, meaning in a positive Binary it' possible to define positive and negative values 
	sign -> sign
	is_zero -> is is_integer is true it's zero
	
	"""
	def __init__(self, mantissa=None, exp=None, sign=None, is_zero=None):
		if type(mantissa) == type(None):
			#Initialize mantissa for 24 bits, exponent for 8 bits and sign for 1 bit
			__mant_len__ = 24
			__expo_len__ = 8
			self.mant	 = Binary([False for i in range(__mant_len__)])
			self.exp	 = Binary([False for i in range(__expo_len__)])
			self.sign	 = Binary([True])
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
	
	def Allign(self, other, additive=True, propper_clean=True):
		bin = Binary()
		Zero = Binary([False])
		One = Binary([True])
		reverse_shift = False
		
		if propper_clean:
			#Clone hpf objects to new temporary variables to not mess with original objects
			_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
			_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		else:
			_new_self = self
			_new_other = other
		
		#Calculate exponent values
		_self_exp = _new_self.exp.__xor__(_new_self.exp)
		_other_exp = _new_other.exp.__xor__(_new_other.exp)
		
		_self_exp.data[_self_exp.GetLength()-1] = True
		_other_exp.data[_other_exp.GetLength()-1] = True
		
		_self_exp_val = _self_exp-_new_self.exp
		_other_exp_val = _other_exp-_new_other.exp
		
		#Add leading one for calculations
		if additive:
			_new_self.mant.Append(True)
			_new_other.mant.Append(True)
		
		#If self represents a larger number
		if _other_exp_val < _self_exp_val:
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
	
	def __pure_add__(self, other, preemptive_offset=False, set_precision=False, propper_clean=True):
		bin = Binary()
		Zero = Binary([False],False,True)
		One = Binary([True],False,True)
		
		#Handle zeros
		if self.is_zero.data[0]:
			if other.is_zero.data[0]:
				return hpf(Binary([False]), Binary([False]), Binary([True]), Binary([True]))
			else:
				return other
		else:
			if other.is_zero.data[0]:
				return self
		
		if propper_clean:
			#Clone hpf objects to new temporary variables to not mess with original objects
			_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
			_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		else:
			_new_self = self
			_new_other = other
		
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
		
		if type(preemptive_offset) != type(False):
			_t_q_exp_v += preemptive_offset
		
		#Get lengths of mantissa
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		
		#Get longest mantissa length based on reverse_shift
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		if type(set_precision) != type(False):
			t = _new_self.mant.GetLength() - set_precision
			if t > 0:
				print("lps: %s" % (t))
				_new_self.mant.LengthPop(t)
				_new_other.mant.LengthPop(t)
		
		#Allign mantissa
		_new_self, _new_other, reverse_shift = _new_self.Allign(_new_other, True, False)
		
		#Add mantissa
		_t_q_mant = _new_self.mant.__float_add__(_new_other.mant, False, False)
		
		#Get longest mantissa length based on reverse_shift
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		if type(set_precision) != type(False):
			t = _t_q_mant.GetLength() - set_precision
			if t > 0:
				_t_q_mant.LengthPop(t)
		
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
		
		return hpf(_t_q_mant, _t_q_exp, self.sign, self.is_zero)
	def __pure_sub__(self, other, preemptive_offset=False, set_precision=False, propper_clean=True):
		bin  = Binary()
		Zero = Binary([False])
		One  = Binary([True])
		
		#Handle zeros
		if self.is_zero.data[0]:
			if other.is_zero.data[0]:
				return hpf(Binary([False]), Binary([False]), Binary([True]), Binary([True]))
			else:
				return hpf(other.mant, other.exp, Binary([not other.sign.data[0]]), other.is_zero)
		else:
			if other.is_zero.data[0]:
				return hpf(self.mant, self.exp, self.sign, self.is_zero)
		
		if propper_clean:
			#Clone hpf objects to new temporary variables to not mess with original objects
			_new_self = hpf(self.mant, self.exp, self.sign, self.is_zero)
			_new_other = hpf(other.mant, other.exp, other.sign, other.is_zero)
		else:
			_new_self = self
			_new_other = other
		
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
		
		if type(preemptive_offset) != type(False):
			_t_q_exp_v += preemptive_offset
		
		#Allign mantissa
		_new_self, _new_other, reverse_shift = _new_self.Allign(_new_other)
		if type(set_precision) != type(False):
			t = (_t_q_mant.GetLength()-1-_new_self_exp_v.ToInt()) - set_precision
			if t > 0:
				_t_q_mant.LengthPop(t)
				_new_self.mant.LengthPop(t)
		
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		
		_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
		
		#Add mantissa
		_t_q_mant = _new_self.mant.__float_sub__(_new_other.mant, True, False)
		
		#Handle carry out
		if _t_q_mant.co == False:
			# _t_q_mant.Append(False)
			_t_q_mant_len = _t_q_mant.GetLength()
			two_compliment = Binary([True for i in range(_t_q_mant_len)])
			_t_q_mant = _t_q_mant.__xor__(two_compliment)
			_t_q_mant = _t_q_mant + One
			_t_q_sign = Binary([False])
		else:
			_t_q_sign = Binary([True])
		
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
		
		return hpf(_t_q_mant, _t_q_exp, _t_q_sign, self.is_zero)
	
	def __add__(self, other, preemptive_offset=False, set_precision=False, propper_clean=True):
		if self.sign.data[0]:
			if other.sign.data[0]:
				return self.__pure_add__(other, preemptive_offset, set_precision, propper_clean=True)
			return self.__pure_sub__(other, preemptive_offset, set_precision, propper_clean=True)
		if other.sign.data[0]:
			return other.__pure_sub__(self, preemptive_offset, set_precision, propper_clean=True)
		return self.__pure_add__(other, preemptive_offset, set_precision, propper_clean=True)
	def __sub__(self, other, preemptive_offset=False, set_precision=False, propper_clean=True):
		if self.sign.data[0]:
			if other.sign.data[0]:
				return self.__pure_sub__(other, preemptive_offset, set_precision, propper_clean=True)
			return self.__pure_add__(other, preemptive_offset, set_precision, propper_clean=True)
		if other.sign.data[0]:
			_t_q = self.__pure_add__(other, preemptive_offset, set_precision, propper_clean=True)
			_t_q.sign.data[0] = False
			return _t_q
		_t_q = self.__pure_sub__(other, preemptive_offset, set_precision, propper_clean=True)
		_t_q.sign.data[0] = not _t_q.sign.data[0]
		return _t_q
	
	def __mul__(self, other, set_precision=False):
		bin = Binary()
		Zero = Binary([False])
		One = Binary([True])
		
		#Handle zeros
		if self.is_zero.data[0] or other.is_zero.data[0]:
			return hpf(Binary([False]), Binary([True]), Binary([True]), Binary([True]))
		
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
		_t_q_exp_v = _new_self_exp_v + _new_other_exp_v
		
		if _t_q_exp_v.co:
			_t_q_exp_v.Append(True)
		
		#Make _t_q object for computation
		_t_q_mant_len = _new_self.mant.GetLength()+_new_other.mant.GetLength()
		_t_q = Binary([False for i in range(_t_q_mant_len)])
		
		#Calculate multiplication of mantissa
		co_offset = 0
		_t_q, _t_other = _t_q.Allign(_new_other.mant, True)
		
		for i in range(_new_self.mant.GetLength()-1, -1, -1):
			if _new_self.mant.data[i]:
				_t_q += _t_other
				if _t_q.co:
					_t_q_exp_v += One
					_t_other.Append(False)
			_t_other.Pop()
			_t_other.Append(False)
		
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
			
			_bin_largest_one = ReturnableDoubleToBin(largest_one)
		
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
	def __truediv__(self, other, set_precision=False, preemptive_offset=None):
		bin = Binary()
		One = Binary([True])
		Zero = Binary([False])
		
		remainders = dict()
		
		#Handle zeros
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
		
		t = _new_self.mant.GetLength() + _t_q_exp_v.ToInt()
		if t > set_precision:
			try:
				_new_self.mant.LengthPop(t)
				_new_other.mant.LengthPop(t)
			except IndexError:
				pass
		
		# #Allign mantissas
		_new_self.mant, _new_other.mant = _new_self.mant.Allign(_new_other.mant, True)
		
		t = _new_self.mant.GetLength() + _t_q_exp_v.ToInt()
		if t > set_precision:
			try:
				_new_self.mant.LengthPop(t)
			except IndexError:
				pass
			try:
				_new_other.mant.LengthPop(t)
			except IndexError:
				pass
		
		#Set _t_q_mant_len based on set_precision
		if type(set_precision) != type(False):
			_t_q_mant_len = set_precision
		else:
			_t_q_mant_len = 2 * _new_self.mant.GetLength() - _t_q_exp_v.ToInt()
		_t_q_mant = Binary([False for i in range(_t_q_mant_len)])
		
		#Calculate actual division
		_max = _t_q_mant.GetLength()-1
		_t_self_mant = _new_self.mant
		_t_other_mant = _new_other.mant
		for i in range(_max):
			_t_sub_res = _t_self_mant.__pure_sub__(_t_other_mant, True, False, False)
			
			#If subtraction is positive
			if _t_sub_res.co == True:
				if str(_t_sub_res) in remainders:
					try:
						__max = _max-i
						for j in range(__max):
							_t_q_mant.data[__max-j] = remainders[str(_t_sub_res)][(__max-j) % (len(remainders[str(_t_sub_res)]))]
						break
					except ZeroDivisionError:
						break
				else:
					_t_q_mant.data[_max-i] = True
					_new_self.mant = _t_sub_res
					
					_t_self_mant = _new_self.mant
					_t_other_mant = _new_other.mant
					remainders[str(_t_sub_res)] = []
			try:
				for key in remainders:
					remainders[key].insert(0, _t_sub_res.co)
			except:
				pass
				
			_t_self_mant.InverseAppend(False)
			_t_other_mant.Append(False)
		
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
		
		if type(preemptive_offset) != type(None):
			_t_q_exp_v += preemptive_offset
		
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
		Zero = Binary([False], False, True)
	
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
		
		# Add leading ones back in within the size of the exponents
		_self_exp_l_bin.data[_self_exp_l_bin.GetLength()-1] = True
		
		# Calculate actual values of exponents
		_new_self_exp_v  = _self_exp_l_bin-od.exp
		
		if _new_self_exp_v >= Zero:
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

#Define 0, 1 and 2
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

xtyc = dict()

def x_to_the_y(x, y):
	One = _One.DeepCopy()
	
	global xtyc
	
	if str(x.ToFloat()) in xtyc:
		if str(y.ToFloat()) in xtyc[str(x.ToFloat())]:
			return xtyc[str(x.ToFloat())][str(y.ToFloat())][0]
		largest = list(xtyc[str(x.ToFloat())].keys())[-1]
		if int(largest[0]) < y.ToFloat():
			q = xtyc[str(x.ToFloat())][largest][0]
			i = xtyc[str(x.ToFloat())][largest][1]
			_max = y.DeepCopy() + One
			while i < _max:
				q *= x
				i += One
			xtyc[str(x.ToFloat())] = dict()
			xtyc[str(x.ToFloat())][str(y.ToFloat())] = [q,i]
			return q
	
	i = _One.DeepCopy()
	q = One.DeepCopy()
	_max = y.DeepCopy() + One
	while i.Abs() < _max.Abs():
		q *= x
		i += One
	
	if str(x) not in xtyc:
		xtyc[str(x.ToFloat())] = dict()
		xtyc[str(x.ToFloat())][str(y.ToFloat())] = [q,i]
	return q

def _exp_temp(n):
	print("_exp_temp:")
	One = _One.DeepCopy()
	Two = _Two.DeepCopy()
	q = OffsetExponentValue(Two, Binary([True]))
	q = q + One
	return q

def sin(n, iters=15, depth=1000, show_iters=False):
	#Boring setup
	q = _Zero.DeepCopy()
	i = _Zero.DeepCopy()
	One = _One.DeepCopy()
	
	#Actual computation
	for _i in range(iters):
		if show_iters:
			print("i: %s, q: %s" % (_i, q))
		
		_temp = _exp_temp(i)
		_exp_divisor = x_to_the_y(n, _temp)
		_fac_dividend = factorial(_temp)
		_exp_divided = _exp_divisor.__truediv__(_fac_dividend, depth)
		
		if _i % 2 == 0:
			q = q + _exp_divided
		else:
			q = q - _exp_divided
		i += One
	
	return q

def exp(n, iters=15, show_iters=False):
	#Boring setup
	q = _Zero.DeepCopy()
	i = _Zero.DeepCopy()
	One = _One.DeepCopy()
	
	for _i in range(iters):
		if show_iters:
			print("i: %s, q: %s" % (_i, q))
		
		_exp_divisor = x_to_the_y(n, i)
		_fac_dividend = factorial(i)
		_exp_divided = _exp_divisor.__truediv__(_fac_dividend, _exp_divisor.mant.GetLength()+_fac_dividend.mant.GetLength()+(15*(iters-_i)))
		
		q += _exp_divided
		i += One
	
	return q

def OffsetExponentValue(x, offset):
	Zero = Binary([False])
	One = Binary([True])
	
	_n_x = x.DeepCopy()
	
	_n_e_b = _n_x.exp.__xor__(_n_x.exp)
	_n_e_b.data[_n_e_b.GetLength()-1] = True
	
	_n_e_v = _n_e_b-_n_x.exp
	
	_n_e_v += offset
	
	#Calculate _t_q_exp
	_t_q_exp_v_l = Binary()
	while TwosPow(_t_q_exp_v_l) < _n_e_v.Abs():
		_t_q_exp_v_l += One
	_t_q_exp_v_l += One
	
	#Remove leading zeros for propper calculation
	_t_q_exp = TwosPow(_t_q_exp_v_l)-_n_e_v
	while _t_q_exp.data[_t_q_exp.GetLength()-1] != True and _t_q_exp.GetLength() > 1:
		_t_q_exp.Pop(_t_q_exp.GetLength()-1)
	
	#Calculate _t_q_exp_l
	_t_q_exp_l = Binary()
	_t_q_exp_l.DoubleToBin(_t_q_exp.GetLength()-1)
	
	#Add leading zero for propper exponent value
	i = _t_q_exp_v_l-_t_q_exp_l
	while i > Zero:
		_t_q_exp.Append(_n_e_v < Zero)
		i -= One
	
	return hpf(x.mant, _t_q_exp, x.sign, x.is_zero)

def sqrt(n, depth=2000, iters=15, show_iters=True, show_in_percentage=True):
	NegOne = Binary([True], False, False)
	Two = _Two.DeepCopy()
	q = _One.DeepCopy()
	
	for i in range(iters):
		start = time()
		if show_iters == True:
			if show_in_percentage:
				if len(str(i)) < len(str(iters)):
					_i_s = "0" * (len(str(iters))-len(str(i))) + str(i)
				else:
					_i_s = str(i)
				print("i: %s/%s, %s%%" % (_i_s, iters-1, 100*i/iters))
				print("q: %s, %s" % (q, q.__repr__()))
			else:
				print("i: %s, %s, %s" % (str(i), q, q.__repr__()))
		
		div = n.__truediv__(q, m.floor(2*depth/3))
		nt = time()
		print("div dt: %s" % (nt-start))
		start = time()
		q = q.__add__(div, NegOne, depth, False)
		nt = time()
		print("add dt: %s" % (nt-start))
	
	return q

def pi(depth=10000, iters=10, show_iters=True, show_in_percentage=True):
	global xtyc
	One				= _One.DeepCopy()
	two				= _Two.DeepCopy()
	four			= hpf()
	nn				= hpf()
	thns			= hpf()
	eht				= hpf()
	tstt			= hpf()
	
	#Define four
	four.mant		= Binary([False])
	four.exp		= Binary([0,0])
	four.sign		= Binary([True])
	four.is_zero	= Binary([False])
	
	#Def 99
	nn.mant			= Binary([1,1,0,0,0,1])
	nn.exp			= Binary([0,1,0,0])
	nn.sign			= Binary([True])
	nn.is_zero		= Binary([False])
	
	#Define 396
	thns.mant		= Binary([0,0,1,1,0,0,0,1])
	thns.exp		= Binary([0,0,0,0])
	thns.sign		= Binary([True])
	thns.is_zero	= Binary([False])
	
	#Define 1103
	eht.mant		= Binary([1,1,1,1,0,0,1,0,0,0])
	eht.exp			= Binary([0,1,1,0,0])
	eht.sign		= Binary([True])
	eht.is_zero		= Binary([False])
	
	#Define 26390
	tstt.mant		= Binary([0,1,1,0,1,0,0,0,1,1,1,0,0,1])
	tstt.exp		= Binary([0,1,0,0,0])
	tstt.sign		= Binary([True])
	tstt.is_zero	= Binary([False])
	
	i = _Zero.DeepCopy()
	summated = _Zero.DeepCopy()
	
	#Scalar
	print("\nScalar")
	
	trt = two * sqrt(two, depth, iters, show_iters, show_in_percentage)
	scalar = trt/x_to_the_y(nn, two)
	
	#Main Ramanujan-Sato body
	print("\nMain Ramanujan-Sato body:")
	
	for _i in range(iters):
		start = time()
		if show_iters:
			if show_in_percentage:
				if len(str(_i)) < len(str(iters)):
					_i_s = "0" * (len(str(iters))-len(str(_i))) + str(_i)
				else:
					_i_s = str(i)
				print("i: %s/%s, %s%%" % (_i_s, iters-1, 100*_i/iters))
				print("q: %s, %s" % (summated, summated.__repr__()))
			else:
				print("i: %s, %s, %s" % (_i, str(summated), summated.__repr__()))
		
		dividend = factorial(four * i) * ((tstt * i) + eht)
		divisor  = x_to_the_y(factorial(i), four) * (x_to_the_y(thns, four*i))
		
		summated = summated.__add__(dividend.__truediv__(divisor, depth), False, depth, False)
		
		i += One
		
		nt = time()
		print("dt: %s" % (nt-start))
	
	start = time()
	pi = One.__truediv__(scalar * summated, depth)
	nt = time()
	print("dt: %s" % (nt-start))
	
	print(pi)
	print(pi.__repr__())
	
	return pi

hpf_pi = pi(1000, 50)

def test():
	a = hpf()
	b = hpf()
	
	a.mant		= Binary([1,0])
	a.exp		= Binary([1,0,0])
	a.sign		= Binary([True])
	a.is_zero	= Binary([False])
	
	b.mant		= Binary([1])
	b.exp		= Binary([1,0])
	b.sign		= Binary([True])
	b.is_zero	= Binary([False])
	
	print(a)
	print(b)
	
	c = a.__truediv__(b, 100)
	
	print(c)
	print(c.__repr__())

# test()
