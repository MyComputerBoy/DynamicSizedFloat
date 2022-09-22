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
	
	def Allign(self, other):
		#Get lengths
		_self_len = self.GetLength()
		_other_len = other.GetLength()
		
		#Check which is greater
		_max_len = _self_len * (_self_len > _other_len) + _other_len * (_self_len <= _other_len)
		
		#Clone Binary objects to new temporary variables to not mess with original objects
		_new_self_bin = Binary(self.data)
		_new_other_bin = Binary(other.data)
		
		#Append appropriate lengths to appropriate object
		if _self_len < _max_len:
			_new_self_bin.LengthAppend(_max_len-_self_len)
		else:
			_new_other_bin.LengthAppend(_max_len-_other_len)
		
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
		return str(self.ToInt())
	
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
		print("\nhpf.Allign:")
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign)
		_new_other = hpf(other.mant, other.exp, other.sign)
		
		#Calculate exponent values
		_self_exp_val	= 2**(_new_self.exp.GetLength()-1)-_new_self.exp.ToInt()
		_other_exp_val	= 2**(_new_other.exp.GetLength()-1)-_new_other.exp.ToInt()
		print(_new_self.exp)
		print(_new_other.exp)
		print("_self_exp_val: %s" % (_self_exp_val))
		print("_other_exp_val: %s" % (_other_exp_val))
		
		#Add leading one for calculations
		if additive:
			_new_self.mant.Append(True)
			_new_other.mant.Append(True)
		
		#Find the largest exponent
		_max_exp_val = (_self_exp_val) * (_self_exp_val > _other_exp_val) + (_other_exp_val) * (_self_exp_val <= _other_exp_val)
		
		#If self represents a larger number
		if _max_exp_val < _self_exp_val:
			print("<")
			#Calculate amount to shift
			shift = (_other_exp_val - _self_exp_val)
			
			#Shift the mantissa the appropriate amounts
			difference = _new_other.mant.GetLength()-_new_self.mant.GetLength()
			if difference < 0:
				difference = 0
			_new_other.mant.InverseLengthAppend(difference)
			_new_self.mant.LengthAppend(shift)
		else:	#If other represents a larger number
			print(">=")
			#Calculate amount to shift
			shift = (_self_exp_val - _other_exp_val)
			
			#Shift the mantissa the appropriate amounts
			difference = _new_self.mant.GetLength()-_new_other.mant.GetLength()
			if difference < 0:
				difference = 0
			_new_self.mant.InverseLengthAppend(difference)
			_new_other.mant.LengthAppend(shift)
		
		print(shift)
		print(difference)
		
		return _new_self, _new_other
	
	def __add__(self, other):
		print("\nhpf.__add__():")
		#Clone hpf objects to new temporary variables to not mess with original objects
		_new_self = hpf(self.mant, self.exp, self.sign)
		_new_other = hpf(other.mant, other.exp, other.sign)
		
		#Check which has the largest value
		if _new_self.exp.ToInt() > _new_other.exp.ToInt():
			_t_q_exp = _new_self.exp
		else:
			_t_q_exp = _new_other.exp
		
		#Get lengths of mantissa
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		#Set _t_q_mant_len_ to the largest 
		_t_q_mant_len_ = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
		
		#Allign mantissa
		_new_self, _new_other = _new_self.Allign(_new_other)
		print("Allignment:")
		print(_new_self.mant)
		print(_new_other.mant)
		
		_new_self_mant_len = _new_self.mant.GetLength()
		_new_other_mant_len = _new_other.mant.GetLength()
		_t_q_mant_len = _new_self_mant_len * (_new_self_mant_len > _new_other_mant_len) + _new_other_mant_len * (_new_self_mant_len <= _new_other_mant_len)
		
		#Add mantissa
		_t_q_mant = _new_self.mant + _new_other.mant
		
		one = Binary([True])
		#Handle carry out
		if _t_q_mant.co:
			_t_q_mant.Append(True)
			_t_q_mant_len += 1
			# _t_q_exp += one
		
		#Find leading one
		largest_one = -1
		for i in range(_t_q_mant_len):
			if _t_q_mant.data[i]:
				largest_one = i
		
		#Pop leading one for floating point complience
		if largest_one == -1:
			_t_q_mant = Binary([False for i in range(_t_q_mant_len)])
		else:
			#Shift is how many bits was popped at the top
			shifted = _t_q_mant_len-largest_one
			_t_q_mant.LengthPop(shifted, -1)
			
			shifted_b = Binary()
			shifted_b.DoubleToBin(shifted)
			_t_q_exp -= shifted_b
			
			#resized is how many bits was popped at the bottom
			resized = (_t_q_mant.GetLength()-shifted)-_t_q_mant_len_-1
			i = 0
			while _t_q_mant.data[0] != True and i < resized:
				_t_q_mant.LengthPop(1, 0)
				_t_q_exp += one
				
				i += 1
		
		return hpf(_t_q_mant, _t_q_exp, self.sign)
	
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
		exp_v_t = 2**(self.exp.GetLength()-1)-self.exp.ToInt()
		print(exp_v_t)
		exp_v = exp_v_t
		v = exp_v*temp_mant.ToInt()/(2**(temp_mant.GetLength()-1))
		if self.sign.data:
			return "+%s" % (v)
		else:
			return "-%s" % (v)


va = hpf()
vb = hpf()

#b = 5
vb.mant = Binary([1,0])
vb.exp = Binary([0,0,1,0])
print("b:")
print(vb)
print(vb.__repr__())

#a = 15
va.mant = Binary([1,1,1])
va.exp = Binary([0,0,0,0])
print("a:")
print(va)
print(va.__repr__())

vc = va + vb 

#c
print("c:")
print(vc)
print(vc.__repr__())

# #a = 3
# va.mant = Binary([0,1])
# va.exp = Binary([1,0])
# print("a:")
# print(va)
# print(va.__repr__())

# vc = va + vb 
# print("c:")
# print(vc)
# print(vc.__repr__())

# #a = 1.1
# va.mant = Binary([1,1,0,0,0,1,1,0,0,0,1,1,0,0,0])
# va.exp = Binary([0,1])
# print("a:")
# print(va)
# print(va.__repr__())

# #c
# print("c:")
# vc = va + vb 
# print(vc)
# print(vc.__repr__())

