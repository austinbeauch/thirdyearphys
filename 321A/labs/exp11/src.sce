gcf().background = 1;
n=150;
t=(0:0.1:n);
s=sin(t);
c=cos(t);

figure(1);
plot(t, s)
xlabel("t")
ylabel("sin(t)")
xtitle("Resitricted Sin Graph")

figure(2);
plot3d3(t, s, c)
xlabel("t")
ylabel("sin(t)")
xtitle("3D sine/cosine plot");

figure(3)
plot(t, sin(t) .* exp(-t/10))
xlabel("t")
ylabel("sin(t) .* exp(-t/10)")
xtitle("Sine wave: Amplitude Decay");

figure(4)
plot(t, sin(t .* exp(-t/160)))
xlabel("t")
ylabel("sin(t .* exp(-t/10))")
xtitle("Sine wave: Frequency Decay");

figure(5)
plot(t, sin(t .* exp(-t/50)) .* exp(-t/10))
xlabel("t")
ylabel("sin(t .* exp(-t/50)) .* exp(-t/10)")
xtitle("Sine wave: Frequency and Amplitude Decay");

figure(6)
plot(t, sin(t) + sin(0.9.*t))
xlabel("t")
ylabel("sin(t) + sin(0.9.*t)")
xtitle("Beat frequency")

