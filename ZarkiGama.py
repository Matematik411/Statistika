from matplotlib import scale
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import math
import scipy.integrate as integrate

with open("ZarkiGama.csv", 'r', encoding="UTF-8") as f:
    podatki = f.readlines()
    n = len(podatki)
    podatki= list(map(float, podatki))
    podatki.sort()


# ---- a) ------------------
m = min(podatki)
M = max(podatki)
print(M, m, n)

IQR = podatki[(3*n) // 4] - podatki[n // 4]
d = 2.6 * IQR / (n ** (1/3))
x = 700 / d
print("d, IQR", d, IQR)

st = round(x)
print("st,   ", st)

# 1.)
# plt.hist(podatki, np.linspace(m, M, round((M-m)/d)))

# 2.)
# plt.hist(podatki, np.linspace(m, M, round((M-m)/d)), density=True)


# 3.)
# log(M) ~ 2.86, zato tu 3.86
plt.hist(podatki, [M * 10 ** (-(1+2.86) + ((1+2.86)/(st-1))*i) for i in range(st)], density=True)

plt.xlabel("medprihodni čas")
plt.ylabel("relativna gostota frekvenc")



# ---- b) ------------------
povprecje = 0
povprecje_kvadratov = 0
povprecje_logaritmov = 0
for x in podatki:
    povprecje += x
    povprecje_kvadratov += x**2
    povprecje_logaritmov += math.log(x)

povprecje /= n
povprecje_kvadratov /= n
povprecje_logaritmov /= n

a_mm = (povprecje ** 2) / (povprecje_kvadratov - (povprecje ** 2))
lam_mm = povprecje / (povprecje_kvadratov - (povprecje ** 2))

a = 1 / (2 * (math.log(povprecje) - povprecje_logaritmov))
lam = a / povprecje


print(a, lam, a_mm, lam_mm, 1/povprecje, "-----------------------------")

x = np.linspace(m, M, 1000)
y1 = stats.gamma.pdf(x, a=a_mm, scale=1/lam_mm)
y2 = stats.gamma.pdf(x, a=a, scale=1/lam)
y3 = stats.gamma.pdf(x, a=1, scale=povprecje)


plt.plot(x, y1, color='r', label="metoda momentov") 
plt.plot(x, y2, color='y', label="najv. verjetje") 
plt.plot(x, y3, color='b', label="eksponentna")
# plt.xscale('log')
plt.xlim(left = 0.09, right=M)
plt.legend()
plt.show()
