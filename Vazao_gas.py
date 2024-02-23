'''Dado: Um coletor contém vapor saturado de 170 psi que alimenta um digestor
de polpa de celulose através de 30 pés de tubo de 2” cronograma 40. Inclui 1
cotovelo padrão de 90 graus, uma válvula global de disco tipo plugue convencional
totalmente aberta. A pressão inicial no digestor é atmosférica.
Encontre a vazão inicial em libras/hora.'''




from fluids.units import *
from math import pi
from CoolProp.CoolProp import PropsSI
P1 = 170*u.psi
P2_spec = P2 = 1*u.atm
L = 30*u.foot
NPS, D_pipe, Do_pipe, t = nearest_pipe(NPS=2, schedule=40)
A = 0.25*pi*D_pipe**2

fd = 0.019 # assumed, initial guess
Re = 1e6 # also assumed
mu = 1.8e-8*u.Pa*u.s

rho = 5.988612037578836*u.kg/u.m**3 # Density at inlet from steam tables
roughness = 0.0018*u.inch

for i in range(5):
    K = K_from_f(fd=fd, L=L, D=D_pipe)
    K += entrance_sharp()
    K += exit_normal()
    K += K_globe_valve_Crane(D1=D_pipe, D2=D_pipe)
    K += bend_rounded(Di=D_pipe, angle=90*u.degrees, fd=fd,
                 Re=Re, roughness=roughness, method='Crane')

    # lump the losses together for the `isothermal_gas` function
    fd_tot = f_from_K(L=L, D=D_pipe, K=K)

    P2_choke = P_isothermal_critical_flow(P=P1, fd=fd_tot, D=D_pipe, L=L)
    if P2_choke.to_base_units().magnitude > P2_spec.to_base_units().magnitude:
        P2 = P2_choke
    else:
        P2 = P2_spec

    m = isothermal_gas(rho=rho, fd=fd_tot, P1=P1, P2=P2, L=L, D=D_pipe)
    Q = m/rho
    v = Q/A
    # update friction factor
    Re = Reynolds(D=D_pipe, rho=rho, mu=mu, V=v)
    fd = friction_factor(Re=Re, eD=roughness/D_pipe)

# choke pressure found to be 3 bar instead of 2.5 in Crane example
print('The mass flow rate is found to be %s' %(m.to(u.lb/u.hour)))
