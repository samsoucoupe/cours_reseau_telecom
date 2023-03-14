import matplotlib.pyplot as plt
import numpy as np


def temps_moyen_sejour(mu, lambda_):
    ts = 1 / mu
    W = (lambda_ / (mu - lambda_)) * (1 / mu)
    T = ts + W
    return T


# Définition des paramètres
mu = 4.0

# Liste pour stocker les temps moyens de séjour dans le système pour différentes valeurs de λ
temps_moyens_sejour = []

# Liste pour stocker les valeurs de λ
lambdas = np.linspace(0.1, 0.9, num=9) * mu

# Calcul et stockage des temps moyens de séjour dans le système pour chaque valeur de λ
for lambda_rho in lambdas:
    temps_moyens_sejour.append(temps_moyen_sejour(mu, lambda_rho))

# Affichage du graphique
plt.plot(lambdas / mu, temps_moyens_sejour)
plt.xlabel("ρ")
plt.ylabel("Temps moyen de séjour dans le système")
plt.title("Évolution du temps moyen de séjour dans le système en fonction de ρ")
plt.show()
