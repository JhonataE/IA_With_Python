from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "Sou um cavalheiro e um patife (Knave)."
knowledge0 = And(
    Or(AKnight, AKnave),  ## A e ou um Cavaleiro ou um Patife (exclusivo)
    Not(And(AKnight, AKnave)),   # A nao pode ser ambos
    Implication(AKnight, And(AKnight, AKnave))   # Se A e um Cavaleiro, sua afirmacao deve ser verdadeira
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And( 
    Or(AKnight, AKnave),  # A e ou um Cavaleiro ou um Patife
    Or(BKnight, BKnave),  # B e ou um Cavaleiro ou um Patife
    Not(And(AKnight, AKnave)),  # A nao pode ser ambos
    Not(And(BKnight, BKnave)),  # B nao pode ser ambos
    Implication(AKnight, And(AKnave, BKnave)),  # Se A e um Cavaleiro, sua afirmacao e verdadeira
    Implication(AKnave, Not(And(AKnave, BKnave)))  # Se A e um Patife, sua afirmacao e falsa
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # A e ou um Cavaleiro ou um Patife
    Or(BKnight, BKnave),  # B e ou um Cavaleiro ou um Patife
    Not(And(AKnight, AKnave)),  # A nao pode ser ambos
    Not(And(BKnight, BKnave)),  # B nao pode ser ambos
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),  # A esta dizendo a verdade
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),  # A esta mentindo
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),  # B esta dizendo a verdade
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))  # B esta mentindo
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A e ou um Cavaleiro ou um Patife
    Or(BKnight, BKnave),  # B e ou um Cavaleiro ou um Patife
    Or(CKnight, CKnave),  # C e ou um Cavaleiro ou um Patife
    Not(And(AKnight, AKnave)),  # A nao pode ser ambos
    Not(And(BKnight, BKnave)),  # B nao pode ser ambos
    Not(And(CKnight, CKnave)),  # C nao pode ser ambos
    Implication(AKnight, Or(AKnight, AKnave)),  # Se A e um Cavaleiro, sua afirmacao e verdadeira
    Implication(AKnave, Not(Or(AKnight, AKnave))),  # Se A e um Patife, sua afirmacao e falsa
    Implication(BKnight, And(Implication(AKnight, AKnave), CKnave)),  # B esta dizendo a verdade
    Implication(BKnave, Not(And(Implication(AKnight, AKnave), CKnave))),  # B esta mentindo
    Implication(CKnight, AKnight),  # C esta dizendo a verdade
    Implication(CKnave, Not(AKnight))  # C esta mentindo
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
