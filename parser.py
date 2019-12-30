from pyparsing import *

integer = Combine(ZeroOrMore("S") + Literal('0'))
variable = Combine(Word(alphas,exact=1) + ZeroOrMore("'"))
operand = integer | variable

multop = Literal('*') # Multiplikation
plusop = Literal('+') # Addition
eqop = Literal('=') # Gleichheit
negop = Literal('!') # Negation
andop = Literal('^') # logisches und
orop = Literal('v') # logischer oder
impop = Literal('>') # folglich

atom = infixNotation( operand,
    [
     (multop, 2, opAssoc.LEFT), # x * y
     (plusop, 2, opAssoc.LEFT),] # x + y
    )

term = infixNotation( atom,
    [
        (eqop, 2, opAssoc.LEFT), # a = b
        (negop, 1, opAssoc.RIGHT), # !a
        (andop, 2, opAssoc.LEFT), # a ^ b
        (orop, 2, opAssoc.LEFT), # a v b
        (impop, 2, opAssoc.LEFT), # a > b
    ]
                    )


atom_test = ["0 + 0 + 0",
        "0 + 0 * SS0",
        "(0 + 0) * S0",
        "(0 + 0) * 0*0*0",
        "a''+b'*c''''*D",
        "M*X + B",
        "M*(X + B)",
       ]
term_test = [
        "a=0",
        "S0=a*b'",
        "!(S0=a*b)",
        "b=S0^a=S0>c*S0=0",
       ]
fail_test = [
        "SS",
        "b=S^a=S0>c*S0=0",
        ]

def test():
    # test Terme
    for t in atom_test:
        print(f"Parsing {t}")
        print(atom.parseString(t))
        print()
    # test terme
    for t in term_test:
        print(f"Parsing: {t}")
        print(term.parseString(t))
        print()

if __name__ == "__main__":
    test()
