import math


# Constants
phi_0 = 2.067833848E-15  # Wb
mu_0  = 1.25663706212E-6
pi_value = math.pi
lambda_value = 124E-9

slope = (phi_0)/(8*pi_value*mu_0*(lambda_value)**2)

print(slope)