from numpy import *
from matplotlib import pyplot as plt
from matplotlib import animation
plt.style.use('seaborn-pastel')

def magsq(z):
    return z.real**2 + z.imag**2

def E(n=1):
    return -13.6 / n**2

def psi_200(x, y, z, Z=1, a0=1):
    r = sqrt(x**2 + y**2 + z**2)
    return 1/sqrt(pi) * (Z/(2*a0))**(3/2) * (1 - (Z*r/(2*a0))) * exp(-Z*r/(2*a0))

def psi_210(x, y, z, Z=1, a0=1):
    r = sqrt(x**2 + y**2 + z**2)
    return 1/(2*sqrt(pi)) * (Z/(2*a0))**(3/2) * (Z*r/a0) * exp(-Z*r/(2*a0)) * (z/r)

def psi(x,y,z, alpha=0):
    return magsq(sqrt(4/5)*psi_200(x,y,z) + exp(1j*alpha)*sqrt(1/5)*psi_210(x,y,z))

def psi_t(x, y, z, t, alpha=0):
    hbar = 1.05*10**-34
    return magsq(sqrt(4/5)*psi_200(x,y,z)*exp(-1j*E(2)*t/hbar) +  exp(1j*alpha)*sqrt(1/5)*psi_210(x,y,z)*exp(-1j*E(2)*t/hbar))


dom = linspace(-10, 10, 1000)
x, z = meshgrid(dom, dom)
G = psi(x,0,z)
t = 0
fig, ax = plt.subplots(figsize=(6, 6))
plt.pcolormesh(x,z,G, vmin=0, vmax=0.0014, cmap='gray')

def animate(i):
    a = i % (2*pi)
    G = psi(x,0,z, alpha=a)
    plt.pcolormesh(x, z, G, vmin=0, vmax=0.0014, cmap='gray')
    plt.title(f"frame {i}")
    # cax.set_array(G[:-1, :-1].flatten())

anim = animation.FuncAnimation(fig, animate, interval=100, frames=1000, repeat=True)
plt.show()