from __future__ import annotations
from ilib import stat_list
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
            NfaTable.update({stat:stat.getEpsionClosure()}) # every state at least had a ep closure
            for k in stat.transmap:
                if k != _EPSILON: # iterate each trans symbol
                    NfaTable[stat].update({k:stat.transmap[k]})
        for stats in stat.transmap.values():
            for s in stats: # iterate all states in current state transmap 
                # NfaTable.update({s.name:s})
                self._genNFA(s,NfaTable)
            
        return NfaTable

            
    def genNfaTable(self):
        return self._genNFA(self.inState)
    

    def genNFATable2(self):
        s_a_map = dict()
        raw_table = self._genNFA(self.inState)
        new_table = {}
        for state in raw_table:
            s_a_map.update({state:stat_list.pop()})
        for state in raw_table:
            new_table.update({s_a_map[state]:{}})
            for trans_sym in raw_table[state]:
                trans_list = raw_table[state][trans_sym]
                trans_st_sym_list = [s_a_map[st] for st in trans_list]
                st_sym = s_a_map[state]
                new_table[st_sym].update({trans_sym:trans_st_sym_list})
        return new_table

def epsilon_closure(epsilon_nfa,states):
    ep_closure_set = set(states)
    stack = list(states)
    while stack:
        current_state = stack.pop()
        epsilon_transitions = epsilon_nfa.get(current_state,{}).get(_EPSILON,[])
        for state in epsilon_transitions:
            if state not in ep_closure_set:
                ep_closure_set.add(state)
                stack.append(state)
    return ep_closure_set

def convert_epsilon_NFA_2_NFA(epsilon_nfa):
    nfa = {}
    for state in epsilon_nfa:
        nfa[state]={}
        ep_closure_set = epsilon_closure(epsilon_nfa,[state])
        for symbol in epsilon_nfa[state]:
            if symbol != _EPSILON:
                nfa[state][symbol] = epsilon_nfa[state][symbol]
                
        for ep_state in ep_closure_set:
            for symbol in epsilon_nfa[ep_state].get(ep_state,{}):
                if symbol != _EPSILON:
                    nfa[state].setdefault(symbol,[]).extend(epsilon_nfa[ep_state][symbol])
    return nfa

def convert_epsilon_nfa_to_nfa(epsilon_nfa):
    nfa = {}

    for state in epsilon_nfa:
        nfa[state] = {}

        # Step 1: Find epsilon closure of each state
        epsilon_closure_set = epsilon_closure(epsilon_nfa, [state])

        for symbol in epsilon_nfa[state]:
            if symbol != _EPSILON:
                nfa[state][symbol] = epsilon_nfa[state][symbol]

        # Step 2: Add transitions for epsilon closure
        for epsilon_state in epsilon_closure_set:
            for symbol in epsilon_nfa.get(epsilon_state, {}):
                if symbol != _EPSILON:
                    # nfa[state].setdefault(symbol, []).extend(epsilon_nfa[epsilon_state][symbol])
                    nfa[state].setdefault(symbol,[])
                    for add_state in epsilon_nfa[epsilon_state][symbol]:
                        if add_state not in nfa[state][symbol]:
                            nfa[state][symbol].append(add_state)
                        


    return nfa    
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
    return first

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

def check(input_str,nfa):
    i=0
    current_state='Z9'
    while i<len(input_str):
        symbol = input_str[i]
        if( nfa[current_state].get(symbol) == None):
            return False
        current_state = nfa[current_state].get(symbol).pop()
        i+=1
    if nfa[current_state] == {}:
        return True
    else:
        return False
if __name__ == '__main__':
    _A = char("A")
    _B = char("B")
    _C = char("C")
    
    # pair1=concat([_C,orThem([_A,_B])])
    # pair1 =orThem([_A,_B,_C])
    pair1 =concat([_A,_B,_C])

    e_NFA_table = pair1.genNFATable2()
    print(e_NFA_table)
    NFA_table =convert_epsilon_nfa_to_nfa(e_NFA_table)
    print(NFA_table)
    # print(NFA_table['Z9'].get('D'))
    print(check('ABCD',NFA_table))
   # s1= State(name="s1")
    #s2=State(name="s2")
    #s1.test("haha")
    