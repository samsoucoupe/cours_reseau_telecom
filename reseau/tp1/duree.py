import random
import matplotlib.pyplot as plt

def temps_suivant(lmbda, mu, N):
    if N == 0:
        return random.expovariate(lmbda)
    else:
        return min(random.expovariate(lmbda), random.expovariate(mu))

def evenement(lmbda, mu, N):
    if N == 0:
        return 1  # prochain événement est une arrivée
    elif N > 0:
        p_arrivee = lmbda / (lmbda + mu)
        p_depart = mu / (lmbda + mu)
        r = random.random()
        if r < p_arrivee:
            return 1  # prochain événement est une arrivée
        else:
            return -1  # prochain événement est un départ

lmbda = 6.0
mu = 3.0
N = 0  # nombre de clients dans le système
t = 0.0  # temps courant
delais = []  # liste des délais de traversée

for i in range(10000):
    temps_prochain = temps_suivant(lmbda, mu, N)
    t += temps_prochain
    even = evenement(lmbda, mu, N)
    N += even
    if even == 1:
        delais.append(0.0)  # nouveau client, pas de délai de traversée
    else:
        # client sortant, calcul du délai de traversée
        delai = t - temps_prochain - delais.pop(0)
        delais.append(delai)

# tracé de l'histogramme des délais de traversée
plt.hist(delais, bins=50)
plt.xlabel("Délai de traversée")
plt.ylabel("Nombre de clients")
plt.show()