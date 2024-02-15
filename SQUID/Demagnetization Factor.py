import math


Happ = 0.3  #Oe
m_5k = -9.436477E-005 #emu

pi = math.pi
v_p = 4*pi*1E-7


# Dimensions
a = 2205E-6
b = 1830E-6
d = 2.707E-6
V = a*b*d

A = (abs(m_5k)*1E-3/V)/(Happ*1E-4/v_p)
D = 1 - (1/A)

print(f"Demagnetization constant is {A:.2f}")
print(f"Demagnetization factor is {D:.5f}")

