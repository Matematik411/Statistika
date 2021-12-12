import random
import math
from scipy.stats import t 
import matplotlib.pyplot as plt


with open("Kibergrad.csv", 'r', encoding="UTF-8") as f:
    podatki = f.readlines()[1:]
    N = len(podatki)
    for i in range(N):
        podatki[i] = list(map(int, podatki[i].split(",")))
    print(podatki[0], N)

n = 400
izbrana_stevila = set()
while len(izbrana_stevila) < n:
    a = random.randint(0, N-1)
    izbrana_stevila.add(a)

ocena_st_otrok = sum([podatki[i][2] for i in izbrana_stevila]) / n
print("ocena", ocena_st_otrok)

ocena_stand_napaka_kvadrat = sum([(podatki[i][2] - ocena_st_otrok) ** 2 for i in izbrana_stevila]) * (N - n) / (N * n *(n-1))
print("SE_+^2", ocena_stand_napaka_kvadrat)

ocena_stand_napaka = math.sqrt(ocena_stand_napaka_kvadrat)
print("SE_+", ocena_stand_napaka)   

alfa = 0.05

leva_meja = ocena_st_otrok + t.isf(1 - alfa/2, n-1) * ocena_stand_napaka
print(leva_meja)
desna_meja = ocena_st_otrok - t.isf(1 - alfa/2, n-1) * ocena_stand_napaka
print(desna_meja)

# -------------------- stratificiran vzorec -----------------
cetrt = 4
N_i = [0, 0, 0, 0]
for j in podatki:
    N_i[j[4]-1] += 1
w_i = [N_i[i] / N for i in range(cetrt)]
n_i = [w_i[i] * n for i in range(cetrt)]
n_i = [int(n_i[0]), int(n_i[1]) + 1, int(n_i[2]) + 1, int(n_i[3])]


strat_izbrane = [set() for _ in range(cetrt)]
konec = [False for _ in range(cetrt)]
while not all(konec):
    a = random.randint(0, N-1)
    a_cetrt = podatki[a][4]
    if not konec[a_cetrt - 1]:
        strat_izbrane[a_cetrt - 1].add(a)
        if len(strat_izbrane[a_cetrt - 1]) == n_i[a_cetrt - 1]:
           konec[a_cetrt - 1] = True


st_otrok_i = [sum([podatki[j][2] for j in strat_izbrane[i]]) / n_i[i]
                for i in range(cetrt)]
print(st_otrok_i)

strat_ocena_st_otrok = sum([w_i[i] * st_otrok_i[i] for i in range(cetrt)])
print("strat_ocena_st_otrok", strat_ocena_st_otrok)

strat_stand_odklon_kvadrat_i = [sum([(podatki[j][2] - st_otrok_i[i]) ** 2 for j in strat_izbrane[i]]) / (n_i[i] - 1)
for i in range(cetrt)]
print("strat_stand_odklon_kvadrat_i", strat_stand_odklon_kvadrat_i)

strat_ocena_stand_napaka_kvadrat = sum([(w_i[i]**2) * strat_stand_odklon_kvadrat_i[i] / n_i[i] for i in range(cetrt)])
print(strat_ocena_stand_napaka_kvadrat)
strat_ocena_stand_napaka = math.sqrt(strat_ocena_stand_napaka_kvadrat)
print(strat_ocena_stand_napaka)

ocena_ni = strat_ocena_stand_napaka_kvadrat ** 2 / sum([
    ((w_i[i] ** 4) * (strat_stand_odklon_kvadrat_i[i] ** 2)) / ((n_i[i] ** 2) * (n_i[i] - 1)) 
for i in range(cetrt)])
print(ocena_ni)

strat_leva_meja = strat_ocena_st_otrok + t.isf(1 - alfa/2, ocena_ni) * strat_ocena_stand_napaka
print(strat_leva_meja)

strat_desna_meja = strat_ocena_st_otrok - t.isf(1 - alfa/2, n-1) * strat_ocena_stand_napaka
print(strat_desna_meja)


plt.plot([leva_meja, desna_meja], [1, 1], label="navadno")
plt.plot([strat_leva_meja, strat_desna_meja], [2, 2], label="stratificirano")
plt.plot([strat_leva_meja, strat_leva_meja], [0.5, 2.5], linestyle='dashed')
plt.plot([strat_desna_meja, strat_desna_meja], [0.5, 2.5], linestyle='dashed')
plt.xlim(0.7, 1.2)
plt.ylim(0.5, 2.5)
plt.legend()
plt.show()
