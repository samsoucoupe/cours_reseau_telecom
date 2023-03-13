import binascii


def readtrames(filename):
    """
    Cette fonction fabrique une liste de chaines de caracteres a partir du
    fichier contenant les trames.

    Chaque chaine de la liste rendue est une trame du fichier.

    return : liste des trames contenues dans le fichier
    """
    with open(filename, "r") as f:
        lestrames = []  # List of frames (= lestrames)
        trame = ""  # Current frame .. string vide

        for line in f:  # acces au fichier ligne par ligne
            line = line.rstrip("\n")  # on enleve le retour chariot de la ligne
            line = line[5:53]  # on ne garde que les colonnes interessantes

            trame += line

            if len(line) == 0:  # Trame separator

                # On enregistre la trame dans lestrames
                trame = trame.replace(" ", "")  # on enleve les blancs
                lestrames.append(trame)  # on ajoute la trame a la liste
                trame = ""  # reset trame

        # Si a la fin du fichier, il reste une trame à enregister
        if len(trame) != 0:  # Last frame
            trame = trame.replace(" ", "")  # on enleve les blancs
            lestrames.append(trame)  # on ajoute la trame a la liste

    return lestrames


def unhexlify_lestrames(l):
    """l : liste de trames"""
    for i, trame in enumerate(l):
        print("{}({})".format(type(trame), len(trame)), end="")
        l[i] = binascii.unhexlify(trame)
        print("   --> {}({}) : {} ...".format(type(trame), len(trame), trame[0:10]))


def extract_mac_address(trame):
    """Extraire l'adresse MAC source et destination de la trame"""
    src_mac = binascii.hexlify(trame[0:6]).decode("utf-8")
    dst_mac = binascii.hexlify(trame[6:12]).decode("utf-8")

    return src_mac, dst_mac


def extract_ip_address(trame):
    """Extraire l'adresse IP source et destination de la trame"""
    src_ip = ".".join(
        [str(int(binascii.hexlify(trame[26 + i: 27 + i]), 16)) for i in range(4)]
    )
    dst_ip = ".".join(
        [str(int(binascii.hexlify(trame[30 + i: 31 + i]), 16)) for i in range(4)]
    )
    return src_ip, dst_ip


def extract_protocol_name(trame):
    """Extraire le nom du protocole utilisé dans la trame"""
    protocol = ""
    if trame[12:14] == b"\x08\x00":
        protocol = "IPv4"
    elif trame[12:14] == b"\x08\x06":
        protocol = "ARP"
    elif trame[12:14] == b"\x86\xdd":
        protocol = "IPv6"
    return protocol


def extract_payload_data(trame):
    """Extraire les données utiles contenues dans la trame"""
    protocol = extract_protocol_name(trame)
    payload_data = ""

    if protocol == "IPv4":
        payload_data = trame[34:]
    elif protocol == "IPv6":
        payload_data = trame[54:]
    else:
        payload_data = trame[14:]

    return payload_data


if __name__ == "__main__":
    filename = "t1.txt"
    trames = readtrames(filename)
    unhexlify_lestrames(trames)

    for trame in trames:
        src_mac, dst_mac = extract_mac_address(trame)
        src_ip, dst_ip = extract_ip_address(trame)
        protocol = extract_protocol_name(trame)
        payload_data = extract_payload_data(trame)

        dst_mac_bytes = binascii.unhexlify(dst_mac)
        dst_mac_bytes = int.from_bytes(dst_mac_bytes, byteorder="big")
        src_mac_bytes = binascii.unhexlify(src_mac)
        src_mac_bytes = int.from_bytes(src_mac_bytes, byteorder="big")

        src_mac = ":".join([src_mac[i:i + 2] for i in range(0, len(src_mac), 2)])
        dst_mac = ":".join([dst_mac[i:i + 2] for i in range(0, len(dst_mac), 2)])

        print("Adresse Ethernet de destination : ", dst_mac)
        print("Adresse Ethernet de destination : ", src_mac)

        print("Type d'adresse Ethernet de destination : ", dst_mac_bytes)
        print("Type d'adresse Ethernet de source : ", src_mac_bytes)

        print(f"Src MAC: {src_mac}")
        print(f"Dst MAC: {dst_mac}")
        print(f"Src IP: {src_ip}")
        print(f"Dst IP: {dst_ip}")
        print(f"Protocol: {protocol}")
        print(f"Payload Data: {payload_data}")
        print(f"Data: {trame[42:]}")
