# -------------------------------------------------------------- SENTENCE CLASS
# class whose instances will correspond to the sentences. the father sentences
# and the terms will be well represented in the list atom, neg, conj, disj, impl
# equi and fatherSentences.
# s - corresponds to the sentence expression;
# hier = [None, Term, Term_l, Term_r] - corresponds to the hierarchy of the sentence;
# father - a connection for the father sentence (if the isntance is a term);
# depth - the depth of the term
class Sentence:

    atom, neg, conj, disj, impl, equi, waitingList = (list() for i in range(7))
    fatherSentences = set()

    def __init__(self, s, hier, father):
        self.s = s
        self.hier = hier
        self.father = father
        self.depth = 0

        if not self.validateInput():
            raise TypeError("Input not valid!")

        if not self.validateSentence():
            raise TypeError("Sentence not valid!")

    def __eq__(self, other):
        return self.s == other.s or (isinstance(self, Disj) \
                                and isinstance(other, Disj) \
                                and self.term_l.s == other.term_r.s \
                                and self.term_r.s == other.term_l.s)

    def __hash__(self):
        return hash(self.s)

    def __repr__(self):
        return str(self.s)

    def __str__(self):
        return str(self.s)

    def clear(self):
        self.atom, self.neg, self.conj, self.disj, self.impl, self.equi = (list() for i in range(6))
        self.fatherSentences = set()

    def validateSentence(self):
        if len(self.s) == 1: return True
        elif self.s[0] == 'not' and len(self.s) == 2: return True
        elif self.s[0] == 'or' and len(self.s) == 3: return True
        elif self.s[0] == 'and' and len(self.s) == 3: return True
        elif self.s[0] == '=>' and len(self.s) == 3: return True
        elif self.s[0] == '<=>' and len(self.s) == 3: return True
        return False

    def validateInput(self):
        if isinstance(self.s, str) and len(self.s) == 1: return True
        elif len(self.s) == 2:
            if isinstance(self.s[1], str) or isinstance(self.s[1], tuple):
                return True
        elif len(self.s) == 3:
            if isinstance(self.s[1], str) or isinstance(self.s[1], tuple) \
            and isinstance(self.s[2], str) or isinstance(self.s[2], tuple):
                return True
        return False

    # Updates all sentences ----------------------------------------------------
    # refreshed the current father sentence, refreshing its terms also (by a
    # method associated to each subclass - see below)
    @staticmethod
    def refreshAll():
        [s.refresh() for s in Sentence.fatherSentences]

    # Check sentence type -----------------------------------------------------
    # checks the type of a sentence, creating an instance of the corresponding
    # type
    @staticmethod
    def checkType(s, hier = None, father = None):
        if len(s) == 1: Atom(s, hier, father)
        elif s[0] == 'not': Neg(s, hier, father)
        elif s[0] == 'or': Disj(s, hier, father)
        elif s[0] == 'and': Conj(s, hier, father)
        elif s[0] == '=>': Impl(s, hier, father)
        elif s[0] == '<=>': Equi(s, hier, father)

    # Check term type ---------------------------------------------------------
    # checks the type of a term, creating an instance of the corresponding type
    @staticmethod
    def checkOp(Op, hier = None, father = None):
        if len(Op) == 1: return Atom(Op, hier, father)
        elif Op[0] == 'not': return Neg(Op, hier, father)
        elif Op[0] == 'or': return Disj(Op, hier, father)
        elif Op[0] == 'and': return Conj(Op, hier, father)
        elif Op[0] == '=>': return Impl(Op, hier, father)
        elif Op[0] == '<=>': return Equi(Op, hier, father)
        return None

# --------------------------------------------------------- SENTENCE SUBCLASSES
# -- Atomic sentence ----------------------------------------------------------
# sub class of Sentence and whose instances will be the atomic sentences.
# when an instance is created, it is added to the Sentence atom list.
# if is a father sentence, hier = None, it is also added to the fatherSentences set
# refresh method will refresh the instance expression
class Atom(Sentence):

    def __init__(self, s, hier = None, father = None):
        super(Atom, self).__init__(s, hier, father)
        Sentence.atom.append(self)

        if not hier:
            Sentence.fatherSentences.add(self)
        else:
            self.depth = father.depth + 1

    def refresh(self):
        self.s = self.s

# -- Negation -----------------------------------------------------------------
# sub class of Sentence and whose instances will be the nagation sentences.
# when an instance is created, it is added to the Sentence neg list.
# if is a father sentence, hier = None, it is also added to the fatherSentences set
# the variable term will represent the connection to its term instance
# refresh method will refresh the instance expression and also the term
# (so it will result in a loop refreshing all terms of a sentence)
class Neg(Sentence):

    def __init__(self, s, hier = None, father = None):
        super(Neg, self).__init__(s, hier, father)
        self.term = self.checkOp(s[1], hier = 'Term', father = self)
        Sentence.neg.append(self)

        if not self.term:
            raise TypeError("Error: Could not atribute an term to {}".format(self.s))

        if not hier:
            Sentence.fatherSentences.add(self)
        else:
            self.depth = father.depth + 1

    def refresh(self):
        self.term.refresh()
        self.s = ('not', self.term.s)

# -- Disjunction --------------------------------------------------------------
# sub class of Sentence and whose instances will be the disjunctions.
# when an instance is created, it is added to the Sentence disj list.
# if is a father sentence, hier = None, it is also added to the fatherSentences set
# the variables term_l and term_r will represent the connection to its terms instance
# refresh method will refresh the instance expression and also the terms
# (so it will result in a loop refreshing all terms of a sentence)
class Disj(Sentence):

    def __init__(self, s, hier = None, father = None):
        super(Disj, self).__init__(s, hier, father)
        self.term_l = self.checkOp(s[1], hier = 'Term_l', father = self)
        self.term_r = self.checkOp(s[2], hier = 'Term_r', father = self)
        Sentence.disj.append(self)

        if not self.term_l or not self.term_r:
            raise TypeError("Error: Could not atribute an term to {}".format(self.s))

        if not hier:
            Sentence.fatherSentences.add(self)
        else:
            self.depth = father.depth + 1

    def refresh(self):
        self.s = ('or', self.term_l.s, self.term_r.s)
        self.term_l.refresh()
        self.term_r.refresh()

# -- Conjunction --------------------------------------------------------------
# sub class of Sentence and whose instances will be the conjunctions.
# when an instance is created, it is added to the Sentence conj list.
# if is a father sentence, hier = None, it is also added to the fatherSentences set
# the variables term_l and term_r will represent the connection to its terms instance
# refresh method will refresh the instance expression and also the terms
# (so it will result in a loop refreshing all terms of a sentence)
class Conj(Sentence):

    def __init__(self, s, hier = None, father = None):
        super(Conj, self).__init__(s, hier, father)
        self.term_l = self.checkOp(s[1], hier = 'Term_l', father = self)
        self.term_r = self.checkOp(s[2], hier = 'Term_r', father = self)
        Sentence.conj.append(self)

        if not self.term_l or not self.term_r:
            raise TypeError("Error: Could not atribute an term to {}".format(self.s))

        if not hier:
            Sentence.fatherSentences.add(self)
        else:
            self.depth = father.depth + 1

    def refresh(self):
        self.term_l.refresh()
        self.term_r.refresh()
        self.s = ('and', self.term_l.s, self.term_r.s)

# -- Implication --------------------------------------------------------------
# sub class of Sentence and whose instances will be the implications.
# when an instance is created, it is added to the Sentence impl list.
# if is a father sentence, hier = None, it is also added to the fatherSentences set
# the variables term_l and term_r will represent the connection to its terms instance
# refresh method will refresh the instance expression and also the terms
# (so it will result in a loop refreshing all terms of a sentence)
class Impl(Sentence):

    def __init__(self, s, hier = None, father = None):
        super(Impl, self).__init__(s, hier, father)
        self.term_l = self.checkOp(s[1], hier = 'Term_l', father = self)
        self.term_r = self.checkOp(s[2], hier = 'Term_r', father = self)
        Sentence.impl.append(self)

        if not self.term_l or not self.term_r:
            raise TypeError("Error: Could not atribute a term to {}".format(self.s))

        if not hier:
            Sentence.fatherSentences.add(self)
        else:
            self.depth = father.depth + 1

    def refresh(self):
        self.term_l.refresh()
        self.term_r.refresh()
        self.s = ('=>', self.term_l.s, self.term_r.s)

# -- Equivalence --------------------------------------------------------------
# sub class of Sentence and whose instances will be the equivalences.
# when an instance is created, it is added to the Sentence equi list.
# if is a father sentence, hier = None, it is also added to the fatherSentences set
# the variables term_l and term_r will represent the connection to its terms instance
# refresh method will refresh the instance expression and also the terms
# (so it will result in a loop refreshing all terms of a sentence)
class Equi(Sentence):

    def __init__(self, s, hier = None, father = None):
        super(Equi, self).__init__(s, hier, father)
        self.term_l = self.checkOp(s[1], hier = 'Term_l', father = self)
        self.term_r = self.checkOp(s[2], hier = 'Term_r', father = self)
        Sentence.equi.append(self)

        if not self.term_l or not self.term_r:
            raise TypeError("Error: Could not atribute an term to {}".format(self.s))

        if not hier:
            Sentence.fatherSentences.add(self)
        else:
            self.depth = father.depth + 1

    def refresh(self):
        self.term_l.refresh()
        self.term_r.refresh()
        self.s = ('<=>', self.term_l.s, self.term_r.s)

# ----------------------------------------------------------------- LOGIC RULES
class Rules:

    # Substitution of terms or father sentences ---------------------------
    # breaks the connection between each term and his father, creating a new
    # connection to the new term.
    # if is a father sentence, it clear all the previous data, and crates
    # new data for the new father sentence.
    @staticmethod
    def substitution(_type, inst, s, hier, father):
        if hier == 'Term_l':
            father.term_l = Sentence.checkOp(s, hier, father)
        elif hier == 'Term_r':
            father.term_r = Sentence.checkOp(s, hier, father)
        elif hier == 'Term':
            father.term = Sentence.checkOp(s, hier, father)
        else:
            Sentence.clear(Sentence)
            _type(s, hier, father)
        Sentence.refreshAll()

    # Distributive of V over ^ ------------------------------------------------
    @staticmethod
    def DistributiveDisj(inst, Op1, Op2, hier, father):
        s = inst.s
        if isinstance(inst.term_l, Conj) and not isinstance(inst.term_r, Conj):
            s = ('and', ('or', inst.term_l.term_l.s, Op2), \
                        ('or', inst.term_l.term_r.s, Op2))
        elif isinstance(inst.term_r, Conj) and not isinstance(inst.term_l, Conj):
            s = ('and', ('or', Op1, inst.term_r.term_l.s), \
                        ('or', Op1, inst.term_r.term_r.s))
        elif isinstance(inst.term_l, Conj) and isinstance(inst.term_r, Conj):
            Opp1 = ('and', ('or', inst.term_l.term_l.s,\
                                inst.term_r.term_l.s), \
                          ('or', inst.term_l.term_l.s, \
                                inst.term_r.term_r.s))
            Opp2 = ('and', ('or', inst.term_l.term_r.s,\
                                inst.term_r.term_l.s), \
                          ('or', inst.term_l.term_r.s, \
                                inst.term_r.term_r.s))
            s = ('and', Opp1, Opp2)
        else:
            return # prevents from entering infinite loop
        Rules.substitution(Conj, inst, s, hier, father)

    # Double negation ---------------------------------------------------------
    @staticmethod
    def doubleNegElimination(inst, Op, hier, father):
        s = Op
        if len(s) == 1: _type = Atom
        elif s[0] == 'not': _type = Neg
        elif s[0] == 'or': _type = Disj
        elif s[0] == 'and': _type = Conj
        else: raise TypeError("Error in double negation!")
        Rules.substitution(_type, inst, s, hier, father)

    # De Morgan (Disjunction) -------------------------------------------------
    @staticmethod
    def deMorganDisj(inst, Op1, Op2, hier, father):
        s = ('and', ('not', Op1), ('not', Op2))
        Rules.substitution(Conj, inst, s, hier, father)

    # De Morgan (Conjunction) -------------------------------------------------
    @staticmethod
    def deMorganConj(inst, Op1, Op2, hier, father):
        s = ('or', ('not', Op1), ('not', Op2))
        Rules.substitution(Disj, inst, s, hier, father)

    # Negation Expansion ------------------------------------------------------
    # applies deMorgan or double negation elimination
    @staticmethod
    def NegExpansion(inst, Op, hier, father):
        if isinstance(inst.term, Disj):
            Rules.deMorganDisj(inst, inst.term.term_l.s,
                               inst.term.term_r.s, hier, father)
        elif isinstance(inst.term, Conj):
            Rules.deMorganConj(inst, inst.term.term_l.s,
                               inst.term.term_r.s, hier, father)
        elif isinstance(inst.term, Neg):
            Rules.doubleNegElimination(inst, inst.term.term.s, hier, father)

    # Implication Elimination -------------------------------------------------
    @staticmethod
    def ImplElimination(inst, Op1, Op2, hier, father):
        s = ('or', ('not', Op1) , Op2)
        Rules.substitution(Disj, inst, s, hier, father)

    # Equivalence Elimination -------------------------------------------------
    # when is a father sentence, separates in two different implication sentences
    # (one will be saved in the waitingList - waiting to be converted - and the
    # other will continue to be converted)
    @staticmethod
    def EquiElimination(inst, Op1_s, Op2_s, hier, father):
        if not hier:
            s1 = ('=>', Op1_s, Op2_s)
            s2 = ('=>', Op2_s, Op1_s)
            w = Impl(s2, hier, father)
            Sentence.waitingList.append(w)
            Sentence.clear(Sentence)
            Impl(s1, hier, father)
        else:
            s = ('and', ('=>', Op1_s, Op2_s) , ('=>', Op2_s, Op1_s) )
            Rules.substitution(Conj, inst, s, hier, father)


# ---------------------------------------------------------------- CLAUSE CLASS
# class whose instance will be clauses.
# it will process the raw clauses received, wliminating the repeated literals
# and the tautologies.
class Clause:

    def __init__(self, rawClauses):
        self.rawClauses = rawClauses
        self.clausesList = list()
        self.process()

    def process(self):
        for c in self.rawClauses:
            if isinstance(c, list):
                clauseSet = set(c)
                self.clausesList.append(list(clauseSet))
            elif isinstance(c, str):
                self.clausesList.extend(c)
            elif isinstance(c, tuple):
                self.clausesList.append(c)
            else:
                raise TypeError("Error in Creating Clauses List")
        self.checkTautologies()

    def checkTautologies(self):
        addStack = list()
        removeStack = list()
        while(self.clausesList):
            c = self.clausesList.pop(0)
            status = None
            if isinstance(c, list):
                for element in c:
                    if Clause.negate(element) in c:
                        status = 'remove'
            if status == 'remove':
                removeStack.append(c)
            else:
                addStack.append(c)
        self.clausesList = addStack

    @staticmethod
    def negate(element):
        if isinstance(element, tuple):
            return str(list(element)[1])
        elif isinstance(element, str):
            return ('not', str(element))
        else:
            raise TypeError("Error negating CLause Element")

# ---------------------------------------------------------------- CLAUSE CLASS
# Resolution.applyStep will take two clauses, apply the resolution step and give
# a resolvent with no tautologies or repeated literals
class Resolution:

    @staticmethod
    def applyStep(c1, c2):
        c = list()
        if isinstance(c1, list) or isinstance(c1, str): c.extend(c1)
        else: c.append(c1)
        if isinstance(c2, list) or isinstance(c2, str): c.extend(c2)
        else: c.append(c2)
        count = 0
        addStack = []
        while(c):
            element = c.pop(0)
            if element:
                negElement = Clause.negate(element)
                if negElement in c:
                    c.remove(negElement)
                    count += 1
                else: addStack.append(element)
        if not addStack and count == 1: return []
        elif count > 1: return c1
        else: c.extend(addStack)
        if isinstance(c, list):
            clauseSet = set(c)
            c = list(clauseSet)
        return c
