import numpy as np
import math
from numpy.core.function_base import linspace
from scipy.stats import t
import matplotlib.pyplot as plt

with open("Zobje.csv", 'r', encoding="UTF-8") as f:
    podatki = f.readlines()[1:]
    n = len(podatki)
    n_i = [0, 0]
    for i in range(n):
        podatki[i] = podatki[i].split(",")
        podatki[i] = [float(podatki[i][0]), podatki[i][1], float(podatki[i][2])]
        if podatki[i][1] == "VC":
            n_i[0] += 1
        else:
            n_i[1] += 1

Y_draw = [podatki[i][0] for i in range(n)]
Y_draw21 = np.array(Y_draw[:30])
Y_draw22 = np.array(Y_draw[30:])
Y_draw = np.array(Y_draw) 
Y = [[podatki[i][0]] for i in range(n)]
Y = np.array(Y)

X_draw = [podatki[i][2] for i in range(n)]
X_draw21 = np.array(X_draw[:30])
X_draw22 = np.array(X_draw[30:])
X_draw = np.array(X_draw)
X = [[1, podatki[i][2]] for i in range(n)]
X = np.array(X)
p = len(X[0])
c = np.array([[0], [1]])

ocena_bete = np.matmul(np.linalg.inv(np.matmul(np.transpose(X), X)), np.matmul(np.transpose(X), Y))

ocena_epsilon_vek = Y - np.matmul(X, ocena_bete)
ocena_sigma = math.sqrt(np.matmul(np.transpose(ocena_epsilon_vek), ocena_epsilon_vek) / (n-p))

koren = np.matmul(np.transpose(c), np.matmul(np.linalg.inv(np.matmul(np.transpose(X), X)), c))
koren = math.sqrt(koren)

vrednost_T = (np.matmul(np.transpose(c), ocena_bete)) / (ocena_sigma * koren)
vrednost_T = vrednost_T[0][0]

print("ocena bete", ocena_bete)
print("ocena sigme", ocena_sigma)
print("koren", koren)
print("vrednost T", vrednost_T)
print("n-p", n-p)

alfa = 0.05
meja_intervala_pet = - t.isf(1 - alfa/2, n - p)
print(meja_intervala_pet)


alfa = 0.01
meja_intervala_ena = - t.isf(1 - alfa/2, n - p)
print(meja_intervala_ena)
print("---------------------------")

# graf 1. podnaloge
# x = np.linspace(0, 2.5)
# y_1 = ocena_bete[0] + ocena_bete[1]*x
# plt.scatter(X_draw, Y_draw)
# plt.plot(x, y_1, 'r', label="regresijska premica")
# plt.xlabel("kolicina vitamina")
# plt.ylabel("dolzina zob")
# plt.xlim(0, 2.2)
# plt.legend()
# plt.show()




# ------------------ primerjava ------------------------

X = [[1, podatki[i][2], 0, 0] for i in range(n_i[0])]
X += [[0, 0, 1, podatki[i][2]] for i in range(n_i[0], n)]
X = np.array(X)

locena_ocena_bete = np.matmul(np.linalg.inv(np.matmul(np.transpose(X), X)), np.matmul(np.transpose(X), Y))
print("locena beta", locena_ocena_bete)

c = np.array([[0], [1], [0], [-1]])
p = len(X[0])

locena_ocena_epsilon_vek = Y - np.matmul(X, locena_ocena_bete)
p = len(X[0])
locena_ocena_sigma = math.sqrt(np.matmul(np.transpose(locena_ocena_epsilon_vek), locena_ocena_epsilon_vek) / (n-p))

locen_koren = np.matmul(np.transpose(c), np.matmul(np.linalg.inv(np.matmul(np.transpose(X), X)), c))
locen_koren = math.sqrt(locen_koren)

locena_vrednost_T = (np.matmul(np.transpose(c), locena_ocena_bete)) / (locena_ocena_sigma * locen_koren)
locena_vrednost_T = locena_vrednost_T[0][0]

print(locena_vrednost_T)

alfa = 0.05
meja_intervala_pet = - t.isf(1 - alfa/2, n - p)
print(meja_intervala_pet)


alfa = 0.01
meja_intervala_ena = - t.isf(1 - alfa/2, n - p)
print(meja_intervala_ena)
print("---------------------------")

x = np.linspace(0, 2.5)
y_21 = locena_ocena_bete[0] + locena_ocena_bete[1]*x
y_22 = locena_ocena_bete[2] + locena_ocena_bete[3]*x
plt.scatter(X_draw21, Y_draw21, c='b')
plt.plot(x, y_21, 'b', label="neposredni vnos")
plt.scatter(X_draw22, Y_draw22, c='r')
plt.plot(x, y_22, 'r', label="pomarancni sok")
plt.xlabel("kolicina vitamina")
plt.ylabel("dolzina zob")
plt.xlim(0, 2.2)
plt.legend()
plt.show()
