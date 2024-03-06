import math


Happ = 0.3  #Oe
m_5k = -1.465331e-004 #emu

pi = math.pi
v_p = 4*pi*1E-7


# Dimensions
a = 2497E-6
b = 2185E-6
d = 3.19E-6
V = a*b*d

A = (abs(m_5k)*1E-3/V)/(Happ*1E-4/v_p)
D = 1 - (1/A)

print(f"Demagnetization constant is {A:.2f}")
print(f"Demagnetization factor is {D:.5f}")

