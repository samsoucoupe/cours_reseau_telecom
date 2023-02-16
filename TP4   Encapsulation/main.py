import binascii
import struct  # pour unpack


def readtrames(filename):
    file = open(filename, "r")
    lestrames = []
    trame = ""
    i = 1
    for line in file:
        line = line.rstrip("\n")
        line = line[5:53]
        print("ligne {} : {}".format(i, line))
        trame = trame + line
        if len(line) == 0:
            trame = trame.replace(" ", "")
            lestrames.append(trame)
            trame = ""
        i += 1
    if len(trame) != 0:
        trame = trame.replace(" ", "")
        lestrames.append(trame)
    return lestrames


def unhexlify_lestrames(l):
    for i, trame in enumerate(l):
        print("{}({})".format(type(trame), len(trame)), end="")
        l[i] = binascii.unhexlify(trame)
        print("   --> {}({}) : {} ...".format(type(trame), len(trame), trame[0:10]))


def analyse_syntaxique(filename):
    trames = readtrames(filename)
    print("=" * 60)
    print("\nTrames lues depuis le fichier :\n")
    for i, t in enumerate(trames):
        print("trame #{} : {}".format(i, t))
    unhexlify_lestrames(trames)
    return trames


r = readtrames("XXX.txt")

r = analyse_syntaxique("XXX.txt")


# pour unpack


def analyse_semantique(trame):
    """
    Analyse une trame Ethernet :  cf https://fr.wikipedia.org/wiki/Ethernet
    Input : trame est un tableau d'octets
    """
    print("-" * 60)
    print("\nTrame Ethernet en cours d'analyse ({}): \n{} ... ".format(type(trame), trame[0:10]))

    # Analyse du header ETHERNET
    eth_header = trame[0:14]
    # print(eth_header)
    eth_mac_dest, eth_mac_src, eth_type = struct.unpack('!6s6sH',
                                                        eth_header)  # https://docs.python.org/fr/3/library/struct.html

    print('Destination MAC : {}'.format(eth_mac_dest.hex(":")))  # .hex() ssi Python > 3.8
    print('Source MAC \t: {}'.format(binascii.hexlify(eth_mac_src)))
    print('Type \t: {}'.format(eth_type))
    # Adresses logiques (IP)
    if eth_type == 2048:
        print("Adresse IP source : {}".format(trame[26:30]))
        print("Adresse IP destination : {}".format(trame[30:34]))
        # Ports
        print("Port source : {}".format(trame[34:36]))
        print("Port destination : {}".format(trame[36:38]))
        # Protocole
        print("Protocole : {}".format(trame[23]))
        # données envoyées
        print("Données envoyées : {}".format(trame[34:]))


for trame in r:
    print(trame)
    analyse_semantique(trame)
