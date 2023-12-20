from __future__ import annotations
_EPSILON = 'ε'
class State():
    def __init__(self,accepting=False,name=None):
        self.accepting=accepting
        self.transmap = {}
        self.name=name
    
    def addTransForSymbol(self,symbol:str,state:State):
        if symbol not in self.transmap.keys():
            self.transmap[symbol]=[state]
        else:
            self.transmap[symbol].append(state)

    def getTransForSymbol(self,symbol:str):
        return {symbol:self.transmap[symbol]}
    
    def test():
        pass
    # wrong answer
    def getEpsionClosure(self):
        res = []
        res.append(self)
        if _EPSILON in self.transmap:
            res+=self.transmap[_EPSILON]
        return {_EPSILON:res}
        

class NFA():
    def __init__(self,inState:State,outState:State):
        self.inState =inState
        self.outState = outState
    
    def test(self,string:str):
        return self.inState.test(string)

    # iterate the NFA object groups and gen a table
    def _genNFA(self,stat:State,NfaTable=None):
        if NfaTable is None:
            NfaTable={}
        if stat not in NfaTable:
            # NfaTable.update({stat:stat.name})
            NfaTable.update({stat:stat.getEpsionClosure()})
            for k in stat.transmap:
                if k != _EPSILON:
                    NfaTable[stat].update({k:stat.transmap[k]})
        for stats in stat.transmap.values():
            for s in stats:
                # NfaTable.update({s.name:s})
                self._genNFA(s,NfaTable)
            
        return NfaTable

    def _genNFA_2(self,stat:State,NfaTable=None):
        pass

            
    def genNfaTable(self):
        return self._genNFA(self.inState)

    def genNFATable(self):
        pass
        
        
    
def char(symbol:str):
    inState = State(name=symbol+"->begin")
    outState = State(accepting=True,name=symbol+"->end")
    inState.addTransForSymbol(symbol,outState)
    return NFA(inState,outState)

def epsilon():
    return char('ε')

def concatPair(first:NFA,second:NFA):
    first.outState.accepting=False
    second.outState.accepting=True
    first.outState.addTransForSymbol('ε',second.inState)
    return NFA(first.inState,second.outState)


def concat(nfas:list[NFA]):
    first = nfas[0]
    for obj in nfas[1:]:
        first=concatPair(first,obj)

def orPair(first:NFA,second:NFA):
    starting = State(accepting=False,name="start")
    accepting = State(accepting=True,name="accept")
    starting.addTransForSymbol(_EPSILON,first.inState)
    starting.addTransForSymbol(_EPSILON,second.inState)
    first.outState.addTransForSymbol(_EPSILON,accepting)
    second.outState.addTransForSymbol(_EPSILON,accepting)
    first.outState.accepting=False
    second.outState.accepting=False
    return NFA(starting,accepting)

def orThem(nfas:list[NFA]):
    first = nfas[0]
    for obj in nfas[1:]:
        first=orPair(first,obj)
    return first

# repeat *
def rep(fragment:NFA):
    starting = State(name="rep_start")
    accepting = State(name="rep_end",accepting=True)
    starting.addTransForSymbol(_EPSILON,fragment.inState)
    starting.addTransForSymbol(_EPSILON,accepting)
    fragment.outState.accepting=False
    fragment.outState.addTransForSymbol(_EPSILON,accepting)
    accepting.addTransForSymbol(_EPSILON,fragment.inState)
    return NFA(starting,accepting)

if __name__ == '__main__':
    _A = char("A")
    _B = char("B")
    _C = char("C")
    
    pair1=orThem([_A,_B,_C])
    
    print(pair1.genNfaTable())
   # s1= State(name="s1")
    #s2=State(name="s2")
    #s1.test("haha")
    