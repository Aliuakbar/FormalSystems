from functools import lru_cache # memoization für bessere Performance


def goodstein(n):
    """
    Theorem: jede Goodstein-Folge terminiert mit 0
    Unbeweisbar in der Arithmetik, aber wahr in Mengenlehre
    """
    print(f"Goodstein-Folge für {n}")
    i = 2
    s = hereditary_base(n, i)
    print(f"Base {i}: {s} = {n}")
    i += 1
    while n:
        # ersetze k mit k + 1 und subtrahiere 1
        s = s.replace(str(i-1), str(i))
        n = int(eval(s)) - 1
        print(f"Base {i}: {s} - 1 = {n}")
        s = hereditary_base(n, i)
        i += 1


@lru_cache
def hereditary_base(n, k):
    """
    stellt n in Basis k dar sowohl die Exponenten rekursiv in Basis k
    hereditary_base(42, 2) = 2**5 + 2**3 + 2**1 = 2**(2**2 + 1) + 2**(2 + 1) + 2
    """
    q = -1
    while n >= k**q:
        q += 1
    string = ""
    while n >= 1:
        div, n = divmod(n, k**q)
        if div != 0: # Wenn der Koeffizient 0 ist, kann man den Schritt überspringen
            exponent = q
            if exponent > k: # Wenn der Exponent grösser ist als die Basis, wird er rekursiv zur Basis dargestellt
                exponent = hereditary_base(exponent, k)
            if div != 1: # 1 als Koeffizient kann weggelassen werden
                string += str(div) + " * "
            string += f"{k}**({exponent})"
            if n >= 1: string += " + "
        q -= 1
    string = string.replace(f"{str(k)}**(0)", "1") # leserlicherer Output
    string = string.replace(f"{str(k)}**(1)", str(k)) # leserlicherer Output
    return string


if __name__ == "__main__":
    for i in range(1, 5):
        print("#" * 40)
        goodstein(i)
        if i == 4:
            input("Achtung, Goodstein(4) läuft sehr lange! Drücken Sie Ctrl+C, um es anzuhalten.")
        else:
            input("Beliebige Taste drücken, um fortzufahren")

