from fluids.units import *
from math import pi
L = 50*u.miles
dH = 2000*u.foot
efficiency = 0.67

# Note in pint the default barrel is for US dry barrel
Q = 1900*u.oil_barrel/u.hour
mu = 12.5*u.cP
rho = 54.64*u.lb/u.ft**3

NPS, Di, Do, t = nearest_pipe(NPS=12, schedule='30')

A = 0.25*pi*Di**2
v = Q/A
Re = rho*v*Di/mu
print(Re.to_base_units())
fd = friction_factor(Re=Re, eD=0.0022*u.inch/Di)
print(fd)

K_tot = K_from_f(fd=fd, L=L, D=Di)
dP = dP_from_K(K=K_tot, rho=rho, V=v) + rho*dH*1*u.gravity
dP.to(u.psi), v.to(u.foot/u.s)

head = head_from_P(dP, rho).to(u.foot)
print('head = %s' %head)
power = Q*dP/efficiency
print('power = %s' %(power.to(u.hp)))
