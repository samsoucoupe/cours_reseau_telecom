import matplotlib.pyplot as plt
import numpy as np

# Simulation de système M/M/1

# Paramètres de la simulation
lambda_ = (
    6  # taux d'arrivée des clients (en nombre moyen de clients par unité de temps)
)

mu = 3  # taux de service (en nombre moyen de clients traités par unité de temps)
N_iter = 10000  # nombre d'itérations de la simulation


# Fonction auxiliaire qui calcule le temps jusqu'au prochain événement
def temps_suivant(parametre):
    return np.random.exponential(1 / parametre)


# Fonction auxiliaire qui détermine si le prochain événement est une arrivée ou un départ
def evenement(lambda_, mu):
    p_arrivee = lambda_ / (lambda_ + mu)
    r = np.random.uniform(0, 1)
    if r < p_arrivee:
        return 1  # prochain événement est une arrivée
    else:
        return -1  # prochain événement est un départ


if __name__ == "__main__":
    # Boucle principale de la simulation
    temps = 0  # Temps courant
    N = 0  # Nombre de clients dans le système
    evenements = [(0, 0)]  # Liste des événements (temps, nombre de clients)
    temps_attente = []
    rhos = []

    for i in range(N_iter):
        # Calcul du temps jusqu'au prochain événement
        temps_suiv = temps_suivant(lambda_ + mu)
        temps += temps_suiv

        # Détermination du type du prochain événement
        if evenements[-1][1] == 0:
            even = 1  # Si le système est vide, le prochain événement est forcément une arrivée
        else:
            even = evenement(lambda_, mu)

        # Mise à jour du nombre de clients dans le système en fonction du type d'événement
        N += even

        # Ajout du nouvel événement dans la liste des événements
        evenements.append((temps, N))
        if even == 1:
            temps_attente.append(temps_suiv)
        elif even == -1:
            temps_attente.append(0)

    # Affichage du graphe de l'évolution du nombre de clients dans le système
    temps, clients = zip(*evenements)
    plt.step(temps, clients, where="post")
    plt.xlabel("Temps")
    plt.ylabel("Nombre de clients")
    plt.show()

    # Affichage du graphe de l'évolution du temps d'attente
    plt.hist(temps_attente, bins=50)
    plt.xlabel("Délai de traversée")
    plt.ylabel("Nombre de clients")
    plt.show()

    # Affichage du temps d'attente moyen
    print("Temps d'attente moyen :", np.mean(temps_attente))
