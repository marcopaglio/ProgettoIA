from timeit import default_timer as timer
from copy import deepcopy

from kCNFCreator import clauseGenerator
from DPLLalgorithm import DPLL
from GenericAlgorithms import *

# Il programma principale si occupa di fissare k, fissare n e aumentare m per creare le kCNF
# Nel secondo passaggio risolve la proposizione logica tramite DPLL e ne calcola la soddisfacibilità
# Inoltre ad ogni calcolo si misura il tempo del DPLL
# Con k fissato, si costruiscono archivi di informazioni indicizzati su m/n
# n = # simboli proposizionali
# m = # clausole
# k = lunghezza clausola

# numero cifre decimali
getcontext().prec = 4
# smoothNumber = # iterazioni per esperimento
smoothNumber = 10
# initialCount = min # di valori uguali a 0 da registrare in prob
initialCount = 2
# addCount = # di partenza di max conteggi per scattare la procedura lineare
addCount = 1

#PARAMETRI di test
iterN = 3
iterK = 1
minK = 3
startN = 2


def kernel(maxM, literals, k, n, record):
    m = n/2

    # alreadyUnderOne = False è già stato trovato una misura di probabilità non certa
    alreadyUnderOne = False
    # lastValue = False => ultimo valore uguale a 1 o 0
    lastValue = False
    step: int = 1
    count = 0
    maxCount = 0

    while m <= maxM:
        recTime = 0
        responses = []

        for i in range(smoothNumber):
            clauses = clauseGenerator(deepcopy(literals), k, m)

            # fine prima parte
            # inizio seconda parte

            # trovo i simboli
            symbols = symbolsDetector(clauses)
            model = []

            # calcolo il tempo di computazione
            startTime = Decimal(timer())
            response = DPLL(clauses, symbols, model)
            endTime = Decimal(timer())

            time = endTime - startTime
            recTime += time
            responses.append(response)

        recTime /= smoothNumber
        key = Decimal(m / n)
        prob = successProb(responses)

        if prob == 1:
            if alreadyUnderOne or count == k + addCount:
                step = n
            else:
                step *= 2
                count += 1
                maxCount = count - 1
            lastValue = False
        elif prob == 0:
            if lastValue:
                step = n/2
            else:
                count -= 1
                ### condizione di terminazione
                if count == 0:
                    step = maxM + 1
                else:
                    step = n
            lastValue = False
        else:
            if not alreadyUnderOne:
                alreadyUnderOne = True
                step = k + addCount
            else:
                step = max(1, int(step/2))
                count = maxCount
            lastValue = True

        record[key] = (recTime, prob)
        m += step


def main():
    # PARAMETRO di test
    stepN = 4

    for x in range(iterN):
        record = {}
        n = startN + ((x + 1) * stepN)
        literals = literalGenerator(n)

        for y in range(iterK):
            k = minK + y
            if k > n:
                print("k non può essere più grande di n.")
                break

            maxM = maxClausesCalculator(n, k)

            print("Inizia elaborazione per k : " + str(k) + " e n : " + str(n))

            kernel(maxM, literals, k, n, record)

            print("Finita elaborazione per k : " + str(k) + " e n : " + str(n))

            ### riordino i dati
            ratio = []
            runtime = []
            satisfability = []
            cdeorr = sorted(record)
            for key in cdeorr:
                ratio.append(key)
                runtime.append(record[key][0])
                satisfability.append(record[key][1])
            sortedRecord = dict(zip(ratio, zip(runtime, satisfability)))

            ### memorizzo dati in file .pickle
            nameFile = "Runtime&SatFor" + str(k) + "and" + str(n) + ".p"
            pickle.dump(sortedRecord, open(nameFile, "wb"))

        stepN += 2

    ### realizzazione grafici
    stepN = 4
    for x in range(iterN):
        n = startN + ((x + 1) * stepN)

        for y in range(iterK):
            k = minK + y

            nameFile = "Runtime&SatFor" + str(k) + "and" + str(n) + ".p"
            showGraphs(nameFile)
        stepN += 2

if __name__ == '__main__':
    main()
