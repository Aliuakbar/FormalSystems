import regex as re # externes regex Modul wird benötigt für sub.endpos support
import toml # Parser für Konfigurationsdateien
import reprlib # Stelle lange Listen benutzerfreundlich dar
import sys

from iteration import triangle_iteration # Importiere Dreiecksiteration-Modul


class Axiom:

    def __init__(self, axiom, wildcards=None):
        self.axiom = axiom
        self.wildcards = wildcards
        if self.is_axiom_schema:
            self.formattable_string = self._make_formattable_string()
            self.regex = self._make_regex()


    def _make_regex(self):
        """ returnt einen regex string, der verwendet werden kann, um
        herauszufinden, ob Sätze dem Muster Axiomschemata entsprechen, d.h.
        Axiome sind. """
        regex = self.axiom
        # starte mit der Wildcard, die zuerst vorkommt
        for i, (k, v) in enumerate(sorted(self.wildcards.items(), key=lambda q:
            self.axiom.find(q[0]))):
            regex = regex.replace(k, f"({v})", 1)
            # alle Instanzen der gleichen Wildcard müssen das gleiche matchen
            regex = regex.replace(k, f"\\{i+1}")
        return regex


    def _make_formattable_string(self):
        """ returnt ein formatierbarer string, der für die Produktion aus
        Axiomschemata verwendet werden kann """
        formattable_string = self.axiom
        self.chars = []
        self.starts = []
        self.stops = []
        self.names = []
        for wildcard, re in self.wildcards.items():
            char, specifier = re[0].strip(), re[1:].strip()
            formattable_string = formattable_string.replace(wildcard,"{" + wildcard + "}")
            self.names.append(wildcard)
            self.chars.append(char)
            # Die unterstützten Regex quantifizierer
            if specifier == "*":
                self.starts.append(0)
                self.stops.append(-1)
            elif specifier == "+":
                self.start.append(1)
                self.stops.append(-1)
            elif specifier == "?":
                self.start.append(0)
                self.stops.append(1)
            else:
                raise ValueError(f"Unsupported expression: {wildcard}: {value}")
        return formattable_string


    @property
    def is_axiom_schema(self):
        return len(self.wildcards) > 0


    def produce_axioms(self):
        """ iteriere mit der Dreiecksiteration über die Wildcards """
        assert self.is_axiom_schema
        for x in triangle_iteration(self.starts, self.stops):
            yield Theorem(self.formattable_string.format(
                **{name: c * i for c, i, name
                    in zip(self.chars, x, self.names)}), None, None)


    def __repr__(self):
        return f"Axiom({self.axiom})"



class Theorem:

    def __init__(self, theorem, parent, rule):
        self.theorem = theorem
        self.parent = parent
        self.rule = rule


    def __repr__(self):
        if self.parent:
            p = self.parent.theorem
        else:
            p = "AXIOM"
        return f"{self.theorem} <- Rule {self.rule} from {p}"


    def __hash__(self):
        """ wird benötig, damit Theoreme in der set Data-Struktur gespeichert
        werden können und mittels Hashtable O(1) Zugriff gestattet. """
        return hash(self.theorem)



class Rule:
    def __init__(self, pattern, sub):
        self.pattern = pattern
        self.sub = sub
        self.regex = re.compile(pattern)
        self.formatted_rule = f"{self.pattern} => {self.sub}"


    def __repr__(self):
        return f"Rule({self.formatted_rule})"



class FormalSystem:

    def __init__(self, axioms, rules):
        self.theorems = dict()
        self._generators = [] # Axiomgeneratoren
        self._active = [] # Aktiver Eimer
        self._add_axioms(axioms) # initialisiere die Axiome
        self._add_rules(rules) # initialisiere die Regeln
        self._axioms = axioms # speichere den Anfanszustand ab,
        self._rules = rules # damit zurückgesetzt werden kann


    def _reset(self, verbose=True):
        """ Setzte das System zurück: löscht alle produzierten Sätze (und Axiome)"""
        self.theorems = dict()
        self._generators = []
        self._active = []
        self._add_axioms(self._axioms)
        self._add_rules(self._rules)
        if verbose:
            print("Resetted")


    def _add_axioms(self, axioms):
        self.axioms = []
        i = 0
        for ax in axioms:
            axiom = Axiom(ax["axiom"], ax["wildcards"])
            self.axioms.append(axiom)
            if not axiom.is_axiom_schema:
                self.theorems.update({ ax["axiom"]: Theorem(ax["axiom"], None, None) })
                self._active.append(Theorem(axiom.axiom, None, None))
            else:
                self._generators.append(axiom.produce_axioms())
                new_ax = next(self._generators[i]) # generiere erstes Axiom
                i += 1
                self.theorems.update({new_ax.theorem: new_ax})
                self._active.append(new_ax)


    def _add_rules(self, rules):
        self.rules = list()
        for rule in rules:
            self.rules.append(Rule(rule["pattern"], rule["sub"]))


    def __repr__(self):
        return f"FormalSystem({self.axioms, self.rules})"


    @classmethod
    def from_file(cls, path):
        parsed = toml.load(path)
        return cls(parsed["axiom"], parsed["rule"])


    def apply_rules(self, sequence, as_theorems=True) -> set:
        """ Wendet alle Regeln möglichst viel mal an
        wenn as_theorems wird eine Menge von Theorem Objekten returnt, sonst
        strings"""
        news = set()
        for i, rule in enumerate(self.rules):
            if rule.regex.search(sequence):
                for _ in range(len(sequence)+1):
                    res = rule.regex.sub(rule.sub, sequence, pos=_-1, count=1)
                    if res != sequence:
                        if as_theorems:
                            news.add(Theorem(res, None, i))
                        else:
                            news.add(res)
        return news


    def _step_production(self, verbose=True):
        """ Generator, der pro Schritt wenn möglich ein neues Axiom produziert
        und alle Regeln auf alle aktiven Sätze anwendet"""
        nexts = list()
        for gen in self._generators:
            new_axiom = next(gen)
            if verbose: print("New axiom added")
            self._active.append(new_axiom)
            yield new_axiom
        if self._active:
            for a in self._active:
                seq = a.theorem
                news = self.apply_rules(seq)
                for new_theorem in news:
                    new_theorem.parent = a
                    if new_theorem.theorem not in self.theorems:
                        nexts.append(new_theorem)
                        yield new_theorem
            self._active = nexts


    def step_production(self, n=1, verbose=True):
        for i in range(n):
            if verbose:
                print(f"Step {i}: {len(self.theorems)} theorems produced")
            for new_theorem in self._step_production(verbose):
                self.theorems.update({new_theorem.theorem: new_theorem})
                if verbose:
                    print(new_theorem)


    def _produce(self, verbose=True):
        nexts = list()
        while self._active:
            for gen in self._generators:
                new_axiom = next(gen)
                if new_axiom.theorem not in self.theorems:
                    print("New axiom added")
                    self._active.append(new_axiom)
                    yield new_axiom
            for a in self._active:
                seq = a.theorem
                news = self.apply_rules(seq)
                for theorem in news:
                    if theorem.theorem not in self.theorems:
                        theorem.parent = a
                        nexts.append(theorem)
                        yield theorem
            self._active = nexts


    def produce(self, n, verbose=True):
        """ produziere n neue Theoreme """
        gen = self._produce(verbose)
        for _ in range(n):
            new_theorem = next(gen)
            self.theorems.update({new_theorem.theorem: new_theorem})
            if verbose:
                print(new_theorem)


    def proof(self, sentence, verbose=True):
        try:
            return self.derive(sentence, verbose)
        except:
            if verbose: print("Not yet produced")
            gen = self._produce()
            while True:
                for new_theorem in self._step_production(1):
                    self.theorems.update({new_theorem.theorem: new_theorem})
                    if new_theorem.theorem == sentence:
                        return self.derive(sentence, verbose)
                print(f"{len(self.theorems)} Theoreme produziert, aber {sentence} nicht gefunden :( - Ctrl-C um abzubrechen.")


    def _derive(self, theorem, production, verbose=True):
        if theorem not in self.theorems:
            raise Exception(f"'{theorem}' is not a theorem or not yet produced")
        parent = self.theorems[theorem].parent
        rule = self.theorems[theorem].rule
        if verbose:
            if parent is None:
                print("AXIOM")
            else:
                print(parent, rule)
        if parent is None:
            return production
        production.append([parent, rule])
        parent = parent.theorem
        self._derive(parent, production)


    def derive(self, theorem, verbose=True):
        if verbose:
            print(f"Starting to derive from \n{theorem}")
        return self._derive(theorem, [theorem])


    def is_proof(self, derivation, formula, verbose=True):
        if verbose:
            print(f"Starting to check derivation {derivation} of {formula}")
        last = None
        for i, step in enumerate(reversed(derivation)):
            if last is not None:
                options = self.apply_rules(last, as_theorems=False)
                if verbose: print(options)
            if i == 0:
                if step not in [a.axiom for a in self.axioms]:
                    for ax in self.axioms:
                        if ax.is_axiom_schema:
                            if re.match(ax.regex, step):
                                print("Matched schema")
                                continue
                    if verbose:
                        print(f"Derivation {derivation} does not end with Axiom")
                    return False
            elif step not in options:
                if verbose:
                    print(f"Sentence {step} not producable out of {last}")
                return False
            last = step
        options = self.apply_rules(last, as_theorems=False)
        if verbose: print(options)
        if not formula in options:
            if verbose:
                print("Last step of derivation is incorrect")
            return False
        if verbose:
            print("Derivation is correct")
        return True


    def _tree_produce(self, theorem, depth, n, ref, verbose):
        if verbose:
            print("  "*depth+theorem)
        if depth >= n:
            return
        seen = set()
        for i in self.apply_rules(theorem):
            i = i.theorem
            if i in seen: continue
            seen.add(i)
            ref[i] = dict()
            ref = ref[i]
            self._tree_produce(i, depth+1,n, ref, verbose)


    def tree_produce(self, n, verbose=True):
        """ make production depth first by recursion depth (DFS)"""
        # only for finite axioms
        root = dict()
        ref = root
        for a in self.axioms:
            assert not a.is_axiom_schema
            a = a.axiom
            ref[a] = dict()
            ref = ref[a]
            self._tree_produce(a, 0, n, ref, verbose)
        return root


def tests():
    f = FormalSystem.from_file("ali.toml")
    f.step_production(3)
    input()
    f.is_proof(["ALALI", "AAI", "AI", "I"], "LALLALI")
    input()
    f.is_proof(["LLALLI", "LALI", "AI", "I"], "ALI")
    input()
    f.tree_produce(3, True)
    input()
    f.proof("I")
    input()
    f.produce(20)
    f.proof("ALLI")
    input()
    f.proof("ALLALLI")
    input()
    #f.proof("ALI")
    f = FormalSystem.from_file("pg.toml")
    f.step_production(3)
    input()
    f.is_proof(["---p-g----", "--p-g---", "-p-g--"], "---p--g-----")
    input()
    f.is_proof(["--p--g---"], "--p-g---")
    input()
    f.tree_produce(3, True)
    input()
    f.proof("--p-g---")
    input()
    f.proof("--p---g-----")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Geben sie den Pfad zur Definitionsdatei als Argument an! Z.B.:
python -i FormalSystem.py ali.toml""")
        sys.exit()
    if len(sys.argv) > 2:
        print(""" Zu viele Argumente! Geben sie nur einen Pfad an.""")
        sys.exit()
    f = FormalSystem.from_file(sys.argv[1])
    print(f"""System {sys.argv[1]} erfolgreich geladen. Es ist zugänglich unter
            der variable f""")

