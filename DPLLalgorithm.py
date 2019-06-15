from copy import deepcopy


def findPureSymbol(symbols, clauses):
    # symbols è un insieme di numeri positivi (simboli proposizionali)
    # clauses è una lista di insiemi di numeri positivi e/o negativi (letterali)

    ### purity inizializzato a None, settato a True non appena trova il simbolo nelle clausole, diventa False se trova anche il suo coniugato
    purity = [None]*len(symbols)
    # segno = None se non trovato ancora o se il simbolo non è puro, = True se letterale positivo, = False se letterale negativo
    sign = [None]*len(symbols)
    controller = dict(zip(symbols, zip(purity, sign)))

    for clause in clauses:
        for literal in clause:
            if literal > 0:
                thisPurity = controller[literal][0]

                ### non semplificare la seguente guardia: thisPurity potrebbe essere None!
                if thisPurity != False:
                    if thisPurity is None:
                        controller[literal] = (True, True)
                    else:
                        thisSign = controller[literal][1]
                        if not thisSign:
                            controller[literal] = (False, None)
            else:
                thisPurity = controller[-literal][0]

                ### non semplificare la seguente guardia: thisPurity potrebbe essere None!
                if thisPurity != False:
                    if thisPurity is None:
                        controller[-literal] = (True, False)
                    else:
                        thisSign = controller[-literal][1]
                        if thisSign:
                            controller[-literal] = (False, None)
    pureSymbols = []
    for literal in symbols:
        thisPurity = controller[literal][0]
        if thisPurity:
            thisSign = controller[literal][1]

            ### i simboli puri sono sempre gli stessi, al massimo vengono eliminati quindi va bene usare tuple
            newPureSymbol = (literal, thisSign)
            pureSymbols.append(newPureSymbol)
    return pureSymbols


def removeClauses(clauses, pureSym, sign):
    # clauses è una lista di insiemi di numeri postitivi e/o negativi (letterali)
    # pureSym è un numero positivo (simbolo proposizionale)
    # value indica se è un letterale positivo (True) o negativo (False)

    if sign:
        trueSym = pureSym
        falseSym = -trueSym
    else:
        trueSym = -pureSym
        falseSym = pureSym

    # EARLY TERMINATION EURISTIC #
    ### NON è consentito modificare l'insieme su cui si sta iterando
    ### le clausole da eliminare vengono conservate in toRemove...
    toRemove = []

    for clause in clauses:
        if trueSym in clause:
            toRemove.append(clause)
        elif falseSym in clause:
            clause.remove(falseSym)

            # clausola falsa => sistema non soddisfacibile!!
            if len(clause) == 0:
                return False

    ###... ed eliminate alla fine.
    for clause in toRemove:
        ### DISCARD e REMOVE tolgono l'elemento specificato dall'insieme, ma se non presente solo il secondo metodo genera un'eccezione
        clauses.remove(clause)

    # sistema soddisfatto!!
    if len(clauses) == 0:
        return True

    return None


def findUnitClause(clauses):
    # clauses è una lista di insiemi di numeri positivi e/o negativi (letterali)
    for clause in clauses:
        if len(clause) == 1:
            return clause
    return None


def DPLL(clauses, symbols, model):
    # model è una lista di tuple con chiave un simbolo proposizionale e valore un booleano indicante il valore datogli
    # symbols è un insieme di numeri positivi (simboli proposizionali)
    # clauses è una lista di insiemi di numeri positivi e/o negativi (letterali)

    if len(model) == 0:
        # PURE SYMBOL EURISTIC #
        pureSymbols = findPureSymbol(symbols, clauses)

        while len(pureSymbols) > 0:
            couple = pureSymbols.pop()

            pureSym = couple[0]
            pureSign = couple[1]

            ### aggiorno clauses
            response = removeClauses(clauses, pureSym, pureSign)
            if response is None:
                ### aggiorno symbols
                symbols.remove(pureSym)
                ### aggiorno model
                model.append(couple)
            else:
                return response

        # UNIT CLAUSE EURISTIC #
        # found è un booleano per indicare se nell'ultima iter è stata trovata una unit clause; è inizializzato a True per determinare un ciclo do-while
        found = True
        trueValue = True

        while found:
            ### copia profonda necessaria per evitare che venga eliminato il letterale
            unitClause = deepcopy(findUnitClause(clauses))

            if unitClause is None:
                found = False

            else:
                unit = unitClause.pop()
                if unit > 0:
                    sign = True
                    symbol = unit
                else:
                    sign = False
                    symbol = -unit
                couple = (symbol, trueValue)

                response = removeClauses(clauses, symbol, sign)
                if response is None:
                    ### aggiorno symbols
                    symbols.remove(symbol)
                    ### aggiorno model
                    model.append(couple)
                else:
                    return response

    # NOT OTHER EURISTICS TO USE #
    ### applico l'ultimo assegnamento effettuato
    else:
        ### prelevo l'ultimo assegnamento effettuato
        lastAssignement = model.pop(len(model)-1)
        lastLiteral = lastAssignement[0]
        lastValue = lastAssignement[1]

        ### aggiorno clauses
        response = removeClauses(clauses, lastLiteral, lastValue)
        if response is not None:
            return response

    p = symbols.pop()
    modelTrue = deepcopy(model)
    modelTrue.append((p, True))
    modelFalse = deepcopy(model)
    modelFalse.append((p, False))
    return DPLL(deepcopy(clauses), deepcopy(symbols), modelTrue) or DPLL(deepcopy(clauses), deepcopy(symbols), modelFalse)