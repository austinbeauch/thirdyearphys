import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
plt.style.use('seaborn-pastel')

def magsq(z):
    return z.real**2 + z.imag**2

def psi_0(x, a=1e-9):
    return np.sqrt(105*a) * x * (a-x)**2 / a**4

def psi(x, t, a=1e-9, m=9.1*10**-31):
    const = 2*np.sqrt(420)/(np.pi**3 * np.sqrt(a))
    
    wave = 0
    for n in range(1,100):
        f = (2 + (-1)**n) / n**3
        s = np.sin(n * np.pi * x / a)
        e = np.exp(-1j*n**2 * np.pi**2 * hbar * t / (2*m*a**2))
        wave += f*s*e
    return magsq(const*wave)

def book(x, t, m=9.1*10**-31):
    const = np.sqrt(30/a) * (2/np.pi)**3
    wave = 0
    for n in range(1,100):
        f = 1 / n**3
        s = np.sin(n * np.pi * x / a)
        e = np.exp(-1j*n**2 * np.pi**2 * hbar * t / (2*m*a**2))
        wave += f*s*e
    return magsq(const*wave)

domain = np.linspace(0, 1e-9, 100)
a = 1e-9
hbar = 1.05*10**-34

fig = plt.figure()
ax = plt.axes(xlim=(0, a), ylim=(-2*10**9, 3*10**9))
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,
def animate(i):
    y = psi(domain, i*10**-16/2)
    print(np.trapz(y, domain))
    line.set_data(domain, y.real)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=10, blit=True)
plt.show()