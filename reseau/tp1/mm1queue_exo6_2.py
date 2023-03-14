#-----------------------------------------------------------------------
# mm1queue.py
#-----------------------------------------------------------------------
import sys
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

# Calculer temps suivant d'un evenment en utilisant une loi proba exponential ou le parametre est taux
def temps_suivant(taux):
    y = 0 # a completer avec numpy.random.exponential
    return y 

# Determiner si le prochain evenement est arrivee ou depart
# Egalement possible d'utiliser: numpy.random.choice
def evenement(taux_arrivees, taux_departs):
    proba = np.random.rand(1)
    if proba <= taux_arrivees /(taux_arrivees+taux_departs) :
        even = 0 # l'evenement est une arrivee  
    else :
        even = 0 # l'evenement est un depart  
    return even 

def simulation (taux_arrivees, taux_departs, iterations, plotting):
    facteur_charge = np.divide(taux_arrivees, taux_departs)
    clients = 0
    tps = 0
    client_arrivee = 0
    client_depart = 0
    liste_temps = []
    liste_clients = []
    for i in xrange(iterations) :
        if clients == 0 :
            tps = np.sum([tps, temps_suivant(taux_arrivees)])
            clients = np.sum([clients, 0])
            client_arrivee = np.sum([client_arrivee, 0])
            if not(client_arrivee==len(liste_traversee)) :
                sys.exit("Erreur: liste_traversee n'a pas la bonne taille")
        else :
            tps = np.sum([tps, temps_suivant(taux_arrivees + taux_departs)])
            ev = evenement(taux_arrivees, taux_departs)
            clients = np.sum([clients, ev])
            if ev == 1 :
                client_arrivee = np.sum([client_arrivee, 0])
                if not(client_arrivee==len(liste_traversee)) :
                    sys.exit("Erreur: liste_traversee n'a pas la bonne taille")
            else :
                client_depart =  np.sum([client_depart , 0]);
        liste_temps.append(tps)
        liste_clients.append(clients)
        

def main ():
    iterations = int(sys.argv[1]) # int
    nbr_simulations = int(sys.argv[2]) # int
    
#     taux_arrivees = 10.0
#     taux_departs = 20.0
#     delai_moyen = simulation (taux_arrivees, taux_departs, iterations, 1)
#     
    taux_arrivees = 30.0
    taux_departs = 20.0
    simulation (taux_arrivees, taux_departs, iterations, 1)
    
#    list_delais_moyens = []
#   taux_departs = 20.0 #ts = 0.05 s
#  list_facteurs_charge = np.linspace(0.1, 0.9 , nbr_simulations).tolist()
#   for sim in xrange(nbr_simulations) :
#      delai_moyen = simulation (taux_arrivees, taux_departs, iterations, 1)
  
    
    sys.exit()


main()

# python mm1queue.py num_iter num_sim