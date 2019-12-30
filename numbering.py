from functools import reduce
from operator import mul
from string import ascii_lowercase

"""
`goedelisier`, findet die Gödelnummer zu einer Formel.
Die folgenden Symbole sind unterstützt:
0, S, +, *, =, (, ), ! (anstatt ¬), > (für ->), A (für Alle),
E (Existenzquantor), V (ODER), ^ (UND)
Für Variablen kann man alle Kleinbuchstaben benützen.
`inverse` ist die Umkehroperation. Sie gibt die Formel zu einer
Gödelzahl zurück.
Die Umkehroperation tauscht gelegentlich Variblennamen aus, da den Variablen
möglichst kleine Codenummern aufs neue zugeteilt werden, um die Gödelzahl
klein zu halten. Die Bedeutung bleibt aber erhalten.
"""

symbole = {"0": 1, "S" : 2, "+" : 3, "*" : 4, "=" : 5, "(" : 6, ")": 7,
        "!": 8, ">": 9, "A": 10, "E": 11}


class DefaultDict(dict):
    _counter = len(symbole)
    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except KeyError:
            self._counter += 1
            self.__setitem__(index, self._counter)
            return self._counter

mapping = DefaultDict(symbole)
reversed_mapping = dict((v, k) for k, v in symbole.items())


def primes():
    """ Generator, der alle Primzahlen der Reihe nach generiert """
    def is_prime(x):
        """ testet ob x eine Primzahl ist """
        if x <= 1:
            return False
        for i in range(2, int(x**0.5 + 1)):
            if x % i == 0:
                return False
        return True
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


def goedelisier(formula):
    return reduce(mul, (prime**(mapping[char])
        for char, prime in zip(formula, primes())))


def inverse(n):
    formula = ""
    g = primes()
    p = next(g)
    try:
        while n > 1:
            i = 0
            while n % p == 0:
                i += 1
                n //= p
            p = next(g)
            if i > len(symbole):
                sym = ascii_lowercase[i-1-len(symbole)]
            else:
                sym = reversed_mapping[i]
            formula += sym
        return formula
    except:
        raise Exception("Es existiert keine Formel zu dieser Zahl")


def main():
    sso = "SSO"
    nulleins = "!(0=S0)"
    prim = "Ac(Ed:!Ea(Eb((c+Sd)=(SSa*SSb))))"
    input("Drücken Sie jeweils eine Taste, um fortzufahren")
    input(f"Die Gödelzahl zur Formel {sso}: ", )
    print(goedelisier(sso)); input()
    input(f"Die Formel hinter der Gödelzahl 180")
    print(inverse(180)); input()
    input(f"Die Gödelzahl zur Formel {nulleins}: ", )
    print(goedelisier(nulleins)); input()
    input(f"Die Formel hinter der Gödelzahl {goedelisier(nulleins)}")
    print(inverse(goedelisier(nulleins))); input()
    input(f"Die Gödelzahl zur Formel {prim} (Es gibt unendlich viele Primzahlen): ", )
    print(goedelisier(prim)); input()
    input(f"Die Formel hinter der Gödelzahl {goedelisier(prim)}: ", )
    print(inverse(goedelisier(prim)))
    print("Jetzt sind Sie dran! Benutzen Sie die Funktion goedelisier('S0+S0=SS') und inverse(720326954760913500). Testen Sie natürlich andere Eingabewerte aus.")


if __name__ == "__main__":
    main()

