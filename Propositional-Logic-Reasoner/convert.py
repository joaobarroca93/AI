import sys
import operator
from logic import Sentence, Atom, Neg, Disj, Conj
from logic import Rules

def read_stdin():
    data = sys.stdin.readlines()
    sentences = []
    for i in range(len(data)):
        data[i] = data[i].replace('\n','')
    for s in data:
        if s: sentences.append(eval(s))
    return sentences

# Loop throught a disjunction, including all its terms as literals of a clause
def disjLoop(inst):
    c = []
    f = [inst]
    while(f):
        s = f.pop(0)
        if isinstance(s.term_l, Atom): c.extend(s.term_l.s)
        elif isinstance(s.term_l, Neg): c.append(s.term_l.s)
        else: f.append(s.term_l)
        if isinstance(s.term_r, Atom): c.extend(s.term_r.s)
        elif isinstance(s.term_r, Neg): c.append(s.term_r.s)
        else: f.append(s.term_r)
    return c

# Generate all the clauses correspondent to a sentence in CNF
def clauseGen(sentence):
    frontier = [sentence]
    clauses = []
    while(frontier):
        s = frontier.pop(0)
        if isinstance(s, Conj):
            frontier.append(s.term_l)
            frontier.append(s.term_r)
        elif isinstance(s, Atom) or isinstance(s, Neg):
            clauses.append(s.s)
        elif isinstance(s, Disj):
            clauses.append(disjLoop(s))
    return clauses

# CNF converter, which applies the equivalence elimination, implication elimination,
# move negation inwards and distribution of ^ over V.
# it starts by converting the deeper terms, till it reaches the father sentence
# applying each rule, term by term, will lead to a sentence in CNF
def cnf():
    while(Sentence.equi):
        Sentence.equi.sort(key = operator.attrgetter('depth'))
        s = Sentence.equi.pop()
        Rules.EquiElimination(s, s.term_l.s, s.term_r.s, s.hier, s.father)
    while(Sentence.impl):
        Sentence.impl.sort(key = operator.attrgetter('depth'))
        s = Sentence.impl.pop()
        Rules.ImplElimination(s, s.term_l.s, s.term_r.s, s.hier, s.father)
    while(Sentence.neg):
        Sentence.neg.sort(key = operator.attrgetter('depth'))
        s = Sentence.neg.pop()
        Rules.NegExpansion(s, s.term.s, s.hier, s.father)
    while(Sentence.disj):
        Sentence.disj.sort(key = operator.attrgetter('depth'))
        s = Sentence.disj.pop()
        Rules.DistributiveDisj(s, s.term_l.s, s.term_r.s, s.hier, s.father)

    for sentence in list(Sentence.fatherSentences):
        clauses = clauseGen(sentence)
        for c in clauses:
            if isinstance(c, list) or isinstance(c, tuple): print(c)
            else: print("'{}'".format(c))

def main():
    sentences = read_stdin()
    for s in sentences:
        Sentence.clear(Sentence)
        Sentence.checkType(s)
        cnf()
        while Sentence.waitingList:
            s2 = Sentence.waitingList.pop()
            Sentence.clear(Sentence)
            Sentence.checkType(s2.s)
            cnf()

if __name__ == '__main__':
    print()
    main()
