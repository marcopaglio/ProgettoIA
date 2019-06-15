from decimal import *
import matplotlib.pyplot as plt
import pickle

getcontext().prec = 4


def binomial(n, k):
    if 0 <= k <= n:
        num = 1
        denum = 1
        for t in range(1, min(k, n - k) + 1):
            num *= n
            denum *= t
            n -= 1
        return num // denum
    else:
        return 0


def maxClausesCalculator(n, k):
    sum = 0
    for i in range(k + 1):
        sum += binomial(n - i, k - i) * binomial(n, i)
    return sum


# Ok controlled
def literalGenerator(n):
    literals = []
    code = 1
    for x in range(n):
        literals.append(code + x)          ### not negative literals are positive numbers
        literals.append(-(code + x))       ### negative literals are negative numbers
    return literals


# Ok controlled
def symbolsDetector(clauses):
    # clauses è una lista di insiemi di numeri positivi e/o negativi (letterali)

    symbols = set([])
    for clause in clauses:
        for literal in clause:
            ### prelevo solo i simboli
            if literal > 0:
                newSymbol = literal
            else:
                newSymbol = -literal
            symbols.add(newSymbol)
    return symbols


def successProb(responses):
    count = 0
    for i in responses:
        if i:
            count += 1
    count = Decimal(count/len(responses))
    return count


def takeValues(tupleList, index):
    records = []
    for i in tupleList:
        records.append(i[index])
    return records


def showGraphs(nameFile):
    rec = pickle.load(open(nameFile, "rb"))
    x = rec.keys()
    runtime = takeValues(rec.values(), 0)
    satisfability = takeValues(rec.values(), 1)

    plt.plot(x, satisfability, 'x-')
    plt.xlabel('m/n')
    plt.ylabel('Probabilità')
    plt.title('Soddisfacibilità ' + nameFile)
    plt.show()

    plt.plot(x, runtime, '|-')
    plt.xlabel('m/n')
    plt.ylabel('Tempo')
    plt.title('Runtime DPLL ' + nameFile)
    plt.show()