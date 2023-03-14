import random
import matplotlib.pyplot as plt

# Paramètres de la simulation
lambda_ = 20  # taux d'arrivée des clients (en nombre moyen de clients par unité de temps)
mu = 10  # taux de service (en nombre moyen de clients traités par unité de temps)


# Fonction auxiliaire qui calcule le temps jusqu'au prochain événement
def temps_suivant(parametre):
    return random.expovariate(parametre)


# Fonction auxiliaire qui détermine si le prochain événement est une arrivée ou un départ
def evenement(lambda_, mu):
    # Calcul de la probabilité que le prochain événement soit une arrivée ou un départ
    p_arrivee = lambda_ / (lambda_ + mu)
    p_depart = mu / (lambda_ + mu)

    # Génération d'un nombre aléatoire entre 0 et 1 pour déterminer le prochain événement
    p = random.uniform(0, 1)

    if p < p_arrivee:
        return 1  # Prochain événement est une arrivée
    else:
        return -1  # Prochain événement est un départ


# Boucle principale de la simulation
temps = 0  # Temps courant
N = 0  # Nombre de clients dans le système
evenements = [(0, 0)]  # Liste des événements (temps, nombre de clients)
duree_simulation = 100  # Durée de la simulation (en unités de temps)

while temps < duree_simulation:
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

# Affichage du graphe de l'évolution du nombre de clients dans le système
temps, clients = zip(*evenements)
plt.step(temps, clients, where='post')
plt.xlabel('Temps')
plt.ylabel('Nombre de clients')
plt.show()