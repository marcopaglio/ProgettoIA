import numpy as np
from copy import deepcopy


def delete(mainList, lit):
    stop = False
    for i in mainList:
        if not stop and i == lit:
            mainList.remove(i)
            stop = True


def clauseGenerator(literals, k, m):
    # literals è una copia difensiva di una lista di numeri positivi E negativi (letterali)

    clauses = []

    numClause = 0
    while numClause < m:
        clause = set([])
        ### copia profonda dei letterali
        remainderList = deepcopy(literals)

        for numLiteral in range(k):
            # GARANZIA DI CLAUSOLE NON BANALI #
            ### scelgo uniformemente un letterale dall'insieme, lo tolgo e lo inserisco nella clausola
            newLit = remainderList.pop(np.random.randint(0, len(remainderList)))
            clause.add(newLit)

            # GARANZIA DI NON AVERE TAUTOLOGIE #
            ### elimino il letterale negato nel momento in cui numPair è pari a k/2-1
            delete(remainderList, -newLit)

        ### aggiungo la clausola se non presente nel modello
        if clause not in clauses:
            clauses.append(clause)
            numClause += 1
    return clauses
