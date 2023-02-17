def input_phone_number(nb):
    """
    nb : nombre de chiffre dans le numero de telephone
    return la liste des couples de fréquences DTMF du numero tape au clavier
    """
    l = []
    keys = '1', '2', '3', 'A', \
        '4', '5', '6', 'B', \
        '7', '8', '9', 'C', \
        '*', '0', '#', 'D'
    F1 = [697, 770, 852, 941]  # frequences horizontales
    F2 = [1209, 1336, 1477, 1633]  # frequences verticales
    num = input('Entrer un numero de telephone (sans espaces et avec {} chiffres) : '.format(nb))
    if (len(num) != nb):
        print('Invalid number...')
        exit(0)
    for c in num:  # Pour chaque digit
        if c not in keys:
            print('Invalid number...')
            exit(0)
        else:
            # Selection des deux frequences a utiliser en fonction du chiffre
            for i in range(16):
                if c == keys[i]:
                    f1 = F1[i // 4]  # row
                    f2 = F2[i % 4]  # column
                    l.append([f1, f2])
                    print("touche {} => f1 : {} et f2 : {}".format(c, f1, f2))
    return l


from commun.Graph_f import *
from commun.classe import *

# ================================================================


if __name__ == "__main__":
    Signal = DTMF09()
    Signal.generate_with_space()
    Signal.title = "dtmf"
    Signal.convert_to_wav()
    Graph([Signal, Signal.make_spectrum()], subplot=True, plot_type="line", xlabel="t", ylabel="Amplitude").plot()
