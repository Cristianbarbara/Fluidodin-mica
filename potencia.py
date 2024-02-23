from fluids.units import *
from math import pi
L = (30+100+70+300)*u.foot
dH = 400*u.foot
efficiency = 0.7

Q = 100*u.gallon/u.min
mu = 0.95*u.cP
rho = 62.298*u.lb/u.ft**3

NPS, Di, Do, t = nearest_pipe(Do=3*u.inch, schedule='40')

Di_reducer = nearest_pipe(Do=2.5*u.inch, schedule='40')[1]

A = 0.25*pi*Di**2
v = Q/A
Re = rho*v*Di/mu
fd = friction_factor(Re=Re, eD=0.0022*u.inch/Di)

K_exit = exit_normal()
K_gate = K_gate_valve_Crane(D1=Di, D2=Di, angle=0.0*u.degrees)
K_elbow = bend_rounded(Di=Di, angle=90*u.degrees, Re=Re, method='Crane standard')
K_lift_valve = K_lift_check_valve_Crane(D1=Di_reducer, D2=Di, angled=False)

K_tot = K_exit + K_gate + 4*K_elbow + K_lift_valve
K_tot += K_from_f(fd=fd, L=L, D=Di)

dP = dP_from_K(K=K_tot, rho=rho, V=v) + rho*dH*1*u.gravity
dP.to(u.psi), v.to(u.foot/u.s)

head = head_from_P(dP, rho).to(u.foot)
print('head = %s' %head)
power = Q*dP/efficiency
print('power = %s' %(power.to(u.hp)))
