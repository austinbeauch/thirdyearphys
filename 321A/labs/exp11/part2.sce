t = mgetl("C:\Users\austi\Documents\thirdyearphys\321A\labs\exp11\data.txt");
c = evstr(t);
time = c(:,1);
force = c(:,2);
x = c(:,3);
middle = (max(x) + min(x))/2
x = x-middle;
v = c(:,4);
acc = c(:,5);

plot(time, x)
xlabel("Time")
ylabel("Position")
title("Position vs Time")

plot(x, v)
xlabel("Positon")
ylabel("Velocity")
title("Phase Space")

plot3d3(x,v,time)
xlabel("Positon")
ylabel("Velocity")
zlabel("Time")
title("Phase Space")

figure(1);
plot(time, [x,v,acc,force])
hl=legend(['Position';'Velocity';'Acceleration';'Force']);
xlabel("Time")
ylabel("x, v, a, F")
title("Position, Velocity, Acceleration, and Force versus Time")

m_cart = 0.4831;
m_springs =  .02240;
m_effective = m_cart + m_springs/3;
T = 2.95;
//T = 2*3.14*sqrt(m_effective/k)
k = (T/(2*3.14))^-2 * m_effective;
K = 0.5 * m_effective * v^2;
P = 0.5 * k * x^2;
E = K + P;
m = 25
plot(x(1:m), [K(1:m), P(1:m), E(1:m)]);
xlabel("Position")
ylabel("Energy")
title("Energy Space")
hl=legend(['Kinetic';'Potential';'Total'], 4);
