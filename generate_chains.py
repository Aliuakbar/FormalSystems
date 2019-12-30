from itertools import combinations, product

def generate_chains(alphabet):
    """
    alphabet: Liste mit Symbolen
    returns: Generator mit allen möglichen Kombinationen
    Es wird alles generiert, was mit dem Alphabet möglich ist, das beinhaltet
    alle Sätze, Wohlgeformte Formeln, aber auch alle nicht Sätze und alle
    Schlechtgeformte Formeln.
    """
    i = 0
    while True:
        for chain in product(alphabet, repeat=i):
            yield "".join(chain)
        i += 1

if __name__ == "__main__":
    # Druckt die ersten 100 Ketten, die der Länge nach geordnet in ALI gäbe
    g = generate_chains(["A", "L", "I"])
    for i in range(100):
        print(next(g), end=" ")
