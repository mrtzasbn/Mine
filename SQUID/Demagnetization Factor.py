import math


Happ = 0.3  #Oe
m_5k = -1.30641E-4 #emu

pi = math.pi
v_p = 4*pi*1E-7


# Dimensions
a = 2275E-6
b = 2143E-6
d = 2.717E-6
V = a*b*d

D = (abs(m_5k)*1E-3/V)/(Happ*1E-4/v_p)

print(f"Demagnetization factor is {D:.2f}")
