from fluids.units import *
from math import pi
L1 = 10*u.foot
L2 = 20*u.foot

dH = 11.5*u.foot

mu = 1.1*u.cP
rho = 62.364*u.lb/u.ft**3

NPS1, Di1, Do1, t1 = nearest_pipe(NPS=3, schedule='40')
NPS2, Di2, Do2, t2 = nearest_pipe(NPS=2, schedule='40')

A1 = 0.25*pi*Di1**2
A2 = 0.25*pi*Di2**2

ft1 = ft_Crane(Di1)
ft2 = ft_Crane(Di2)

roughness = 0.0018*u.inch

dP = rho*dH*1*u.gravity

fd1 = fd2 = 0.018 # assumed; solve with sequential substitution
# Take the 3" diameter as the reference for K
for i in range(10):
    K_entrance = entrance_sharp(method='Crane')
    K_exit = change_K_basis(exit_normal(), 2*u.inch, 3*u.inch)
    K_gate = K_gate_valve_Crane(D1=Di1, D2=Di1, angle=0.0*u.degrees)
    K_elbow = bend_miter(Di=Di1, angle=90*u.degrees, method='Crane')
    K_contraction = change_K_basis(contraction_conical_Crane(3*u.inch, 2*u.inch, l=0*u.m), 2*u.inch, 3*u.inch)

    K_tot = K_entrance + K_elbow + K_gate + K_exit + K_contraction
    K_f1 = K_from_f(fd=fd1, L=L1, D=Di1)
    K_f2 = change_K_basis(K_from_f(fd=fd2, L=L2, D=Di2), 2*u.inch, 3*u.inch)
    K_tot += K_f1 + K_f2

    K_tot_basis2 = change_K_basis(K_tot, 3*u.inch, 2*u.inch)

    v1 = (2*dP/(K_tot*rho))**0.5
    v2 = (2*dP/(K_tot_basis2*rho))**0.5

    Re1 = rho*v1*Di1/mu
    Re2 = rho*v2*Di2/mu
    fd1 = friction_factor(Re=Re1, eD=roughness/Di1)
    fd2 = friction_factor(Re=Re2, eD=roughness/Di2)

Q = A1*v1
Q.to(u.gal/u.min)
