"""
Die Dreiecksiteration wird benützt, um neue Axiome zu produzieren, wenn das
Axiomschema über mehrere Wildcards verfügt. Wenn es nur eine Wildcard hat,
kann linear darüber iteriert werden:
z.B: -*
 , -, --, ---, ----, -----, ...
Wenn es 2 Wildcards hat und die gleiche Technik wie oben würde andgewendet, würde das wie
oben für die erste passieren, während die zweite unverändert bliebe, weil sie
erst drankäme, wenn die unendlich lange dauernde erste Iteration fertig wäre.
Deshalb brauchen wir die Dreiecksiteration, die gleichmässig ist.
für -*,-*
-,
 ,-
--,
-,-
 ,--
"""

def triangle_iteration(start, stop):
    """
    start: Liste mit n Ganzzahlen, die den Anfangszustand beschreiben.
    stop:  Liste mit n Ganzzahlen, die den Endzustand beschreiben.
    -1 in stop, wenn die Iteration unendlich weitergehen soll.
    Beispiel:
    triangle_iteration([2, 0, 1], [3, 2, 3])
    2 0 1
    2 1 1
    3 0 1
    2 0 2
    . . .
    2 2 3
    3 2 3
    """

    def increase_at_index(p, i):
        """ helper function """
        new = list(p)
        new[i] += 1
        if stop[i] > 0 and new[i] > stop[i]:
            return None
        return tuple(new)

    n = len(start)
    if n != len(stop):
        raise Exception("start und end müssen gleich lange sein")
    active = set([tuple(start)]) # start initialisieren
    yield tuple(start)
    while active:
        new = set()
        for p in active:
            for i in range(n):
                # für jedes element in active, erhöhe jedes Element
                # einmal um 1
                c = increase_at_index(p, i)
                if c: # wenn stop für das Element nicht erreicht worden ist
                    new.add(c)
                    yield c
        active = new


def pprint(nums):
    """
    Verbildlicht die abstrakten Zahlenfolgen.
    a b c
    aa ab ac ac bc cc ab bb bc
    aac abc acc aab abb abc abb bbb
    """
    from string import ascii_letters as letters
    n = len(nums)
    print("".join(l * x for l, x in zip(letters[:n], nums)))


def test():
    for i in triangle_iteration([0, 0, 0], [2, 2, 2]):
        pprint(i)

if __name__ == "__main__":
    test()
