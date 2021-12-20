# Name: Shashank Karkada Holla
# Deductive Fault Simulator
# Usage: Follow the examples in the README.pdf file


from os import times
from typing import List, Tuple, Dict
import sys
import random, math
import argparse
import deductive_module

class colors: # You may need to change color settings
    RED = '\033[31m'
    ENDC = '\033[m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'

parser = argparse.ArgumentParser(description="Deductive fault simulator")
parser.add_argument("--cktFile", metavar="c", type=str, help="Input the circuit file")
parser.add_argument("--faultFile", metavar="ff", type=str, help="Faults file")
parser.add_argument("--dfs", action="store_true", help="Run Deductive Fault Simulator too.")
parser.add_argument("--fanout", action="store_true", help="Consider fan outs as different nodes.")
args = parser.parse_args()

cktFile = args.cktFile
faultFile = args.faultFile



# Gate Class
class Gate:
    def __init__(self, type, i, o):
        self.type = type
        self.i = i
        self.o = o
        self.faultList = []

    def __str__(self):
        return self.type + " " + str(self.i) + " " + str(self.o)

    def __repr__(self):
        return self.__str__()

gates: List[Gate] = []
inputs = []
outputs = []
outputGates = {}
wires = dict()
faultsToTest = []
DFrontier:List[Gate] = []
gateOutputMap = {}

def compute2(gate:Gate, wires, nodeStuck, stuckAt):

    retValue = None

    if(len(gate.i) == 2):
        if(gate.i[0] in inputs):
            a = wires[gate.i[0]]
        else:    
            a = compute2(gateOutputMap[gate.i[0]], wires, nodeStuck, stuckAt)
            if(not wires[gate.i[0]] in ['D','Dbar']):
                wires[gate.i[0]] = a
            else:
                # a = wires[gate.i[0]]
                wires[gate.i[0]] = a

            
        if(gate.i[1] in inputs):
            b = wires[gate.i[1]]
        else:    
            b = compute2(gateOutputMap[gate.i[1]], wires,  nodeStuck, stuckAt)
            if(not wires[gate.i[1]] in ['D','Dbar']):
                wires[gate.i[1]] = b
            else:
                # b = wires[gate.i[1]]
                wires[gate.i[1]] = b
            
    else:
        if(gate.i[0] in inputs):
            a = wires[gate.i[0]]
        else:
            a = compute2(gateOutputMap[gate.i[0]], wires, nodeStuck, stuckAt)
            wires[gate.i[0]] = a

    if gate.type == "AND":

        if(a in ['D','Dbar'] and (b == '1')):
            retValue = a
        elif(a in ['D','Dbar'] and (b == '0')):
            retValue = '0'
        elif(b in ['D','Dbar'] and (a == '0')):
            retValue = '0'
        elif(b in ['D','Dbar'] and (a == '1')):
            retValue = b

        elif('0' in [a,b]):
            retValue = '0'

        elif('X' in [a,b]):
            retValue = 'X'
        elif((a == 'D') and (b == 'Dbar')):
            retValue = '0'
        elif((b == 'D') and (a == 'Dbar')):
            retValue = '0'
        elif((a == 'D') and (b == 'D')):
            retValue = 'D'
        elif((a == 'Dbar') and (b == 'Dbar')):
            retValue = 'Dbar'
        else:
            res = int(a) & int(b)

            if(res == True):
                retValue = '1'
            else:
                retValue = '0'

        

    if gate.type == "NAND":
        if(a in ['D','Dbar'] and (b == '1')):
            if(a == 'D'):
                retValue = 'Dbar'
            else:
                retValue = 'D'

        elif(b in ['D','Dbar'] and (a == '1')):
            if(b == 'D'):
                retValue = 'Dbar'
            else:
                retValue = 'D'
        elif(a in ['D','Dbar'] and (b == '0')):
            retValue = '1'

        elif(b in ['D','Dbar'] and (a == '0')):
            retValue = '1'
        
        

        elif('0' in [a,b]):
            retValue = '1'

        elif('X' in [a,b]):
            retValue = 'X'
        elif((a == 'D') and (b == 'Dbar')):
            retValue = '1'
        elif((b == 'D') and (a == 'Dbar')):
            retValue = '1'
        elif((a == 'D') and (b == 'D')):
            retValue = 'Dbar'
        elif((a == 'Dbar') and (b == 'Dbar')):
            retValue = 'D'
        else:
            res = not(int(a) & int(b))

            if(res == True):
                retValue = '1'
            else:
                retValue = '0'

        

    if gate.type == "OR":

        if('1' in [a,b]):
            retValue = '1'
        elif('X' in [a,b]):
            retValue = 'X'
        elif(a in ['D','Dbar'] and (b == '0')):
            retValue = a
        elif(b in ['D','Dbar'] and (a == '0')):
            retValue = b
        elif((a == 'D') and (b == 'Dbar')):
            retValue = '1'
        elif((b == 'D') and (a == 'Dbar')):
            retValue = '1'
        elif((a == 'D') and (b == 'D')):
            retValue = 'D'
        elif((a == 'Dbar') and (b == 'Dbar')):
            retValue = 'Dbar'
        else:
            res = int(a) | int(b)

            if(res == True):
                retValue = '1'
            else:
                retValue = '0'

        

    if gate.type == "NOR":
        if(a in ['D','Dbar'] and (b == '0')):
            if(a == 'D'):
                retValue = 'Dbar'
            else:
                retValue = 'D'

        elif(b in ['D','Dbar'] and (a == '0')):
            if(b == 'D'):
                retValue = 'Dbar'
            else:
                retValue = 'D'
        elif('1' in [a,b]):
            retValue = '0'
        elif('X' in [a,b]):
            retValue = 'X' 
        elif((a == 'D') and (b == 'Dbar')):
            retValue =  '0'
        elif((b == 'D') and (a == 'Dbar')):
            retValue = '0'
        elif((a == 'D') and (b == 'D')):
            retValue = 'Dbar'
        elif((a == 'Dbar') and (b == 'Dbar')):
            retValue = 'D'
        else:
            res = not(int(a) | int(b))

            if(res == True):
                retValue = '1'
            else:
                retValue = '0'


    
    if gate.type == "INV":      
        if(a in ['X']):
            retValue = 'X'
        elif(a == 'D'):
            retValue = 'Dbar'
        elif(a == 'Dbar'):
            retValue = 'D'
        else:
            res = not(int(a))
            if(res == True):
                retValue = '1'
            else:
                retValue = '0'


    if gate.type == "BUF":  
        if(a in ['X']):
            retValue = 'X'
        elif(a in ['D','Dbar']):
            retValue = a
        else:
            res = int(a)
            if(res == True):
                retValue = '1'
            else:
                retValue = '0'

    if(gate.o == nodeStuck):
        if(retValue == '1' and stuckAt == '0'):
            return 'D'
        if(retValue == '0' and stuckAt == '1'):
            return 'Dbar'
    return retValue


# Compute Function for circuit simulator
def compute(gate:Gate, wires, nodeStuck, stuckAt):
    if(len(gate.i) == 2):
        if(gate.i[0] in inputs):
            a = wires[gate.i[0]]
        else:    
            a = compute(gateOutputMap[gate.i[0]], wires, nodeStuck, stuckAt)
            if(not wires[gate.i[0]] in ['D','Dbar']):
                wires[gate.i[0]] = a
            else:
                # a = wires[gate.i[0]]
                wires[gate.i[0]] = a

            
        if(gate.i[1] in inputs):
            b = wires[gate.i[1]]
        else:    
            b = compute(gateOutputMap[gate.i[1]], wires,  nodeStuck, stuckAt)
            if(not wires[gate.i[1]] in ['D','Dbar']):
                wires[gate.i[1]] = b
            else:
                # b = wires[gate.i[1]]
                wires[gate.i[1]] = b
            
    else:
        b = 'X'
        if(gate.i[0] in inputs):
            a = wires[gate.i[0]]
        else:
            a = compute(gateOutputMap[gate.i[0]], wires, nodeStuck, stuckAt)
            wires[gate.i[0]] = a

    
            # A     B       AND     NAND     OR     NOR     INV     BUF
    op = [  ['0',   '0',   '0',     '1',    '0',    '1',    '1',    '0'],
            ['0',   '1',   '0',     '1',    '1',    '0',    '1',    '0'],
            ['0',   'D',   '0',     '1',    'D',    'Dbar', '1',    '0'],
            ['0',   'Dbar','0',     '1',    'Dbar', 'D',    '1',    '0'],
            ['0',   'X',   '0',     '1',    'X',    'X',    '1',    '0'],
            ['1',   '0',   '0',     '1',    '1',    '0',    '0',    '1'],
            ['1',   '1',   '1',     '0',    '1',    '0',    '0',    '1'],
            ['1',   'D',   'D',     'Dbar', 'D',    '0',    '0',    '1'],
            ['1',   'Dbar','Dbar',  'D',    'Dbar', '0',    '0',    '1'],
            ['1',   'X',   'X',     'X',    '1',    '0',    '0',    '1'],
            ['D',   '0',   '0',     '1',    'D',    'Dbar', 'Dbar', 'D'],
            ['D',   '1',   'D',     'Dbar', '1',    '0',    'Dbar', 'D'],
            ['D',   'D',   'D',     'Dbar', 'D',    'Dbar', 'Dbar', 'D'],
            ['D',   'Dbar','0',     '1',    'Dbar', '0',    'Dbar', 'D'],
            ['D',   'X',   'X',     'X',    'X',    'X',    'Dbar', 'D'],
            ['Dbar','0',   '0',     '1',    'Dbar', 'D',    'D',    'Dbar'],
            ['Dbar','1',   'Dbar',  'D',    '1',    '0',    'D',    'Dbar'],
            ['Dbar','D',   '0',     '1',    '1',    '0',    'D',    'Dbar'],
            ['Dbar','Dbar','Dbar',  'D',    'Dbar', 'D',    'D',    'Dbar'],
            ['Dbar','X',   'X',     'X',    'X',    'X',    'D',    'Dbar'],
            ['X',   '0',   '0',     '1',    'X',    'X',    'X',    'X'],
            ['X',   '1',   'X',     'X',    '1',    '0',    'X',    'X'],
            ['X',   'D',   'X',     'X',    'X',    'X',    'X',    'X'],
            ['X',   'Dbar','X',     'X',    'X',    'X',    'X',    'X'],
            ['X',   'X',   'X',     'X',    'X',    'X',    'X',    'X']]

    maps = {
        "AND" : 2,
        "NAND": 3,
        "OR"  : 4,
        "NOR" : 5,
        "INV" : 6,
        "BUF" : 7
    }

    for row in op:
        if((row[0] == a) and (row[1] == b)):
            ret = row[maps[gate.type]]
    
    if(gate.o == nodeStuck):
        if(ret == '1' and stuckAt == '0'):
            return 'D'
        if(ret == '0' and stuckAt == '1'):
            return 'Dbar'
    return ret

        

def getObjective(faultNode, stuckAtVal):
    # Check if faultNode is at X or not excited yet
    if wires[faultNode] in ['X', stuckAtVal]:
        if(stuckAtVal == '1'):
            return [faultNode,'0']
        else:
            return [faultNode,'1']
    #Fault node is at correct value, now find next objective
    else:
        i = 0
        theGate = None
        nextNode = 0
        while i < len(DFrontier):
            theGate = DFrontier[i]
            if(wires[theGate.i[0]] == 'X'):
                nextNode = theGate.i[0]
                break
            if(wires[theGate.i[1]] == 'X'):
                nextNode = theGate.i[1]
                break
            i = i+1
        
        if(nextNode == 0):
            print("Failed")
            return ['-1','-1']
        else:
            if(theGate.type in ["AND","NAND"]):
                return [nextNode, '1']
            elif(theGate.type in ["OR","NOR"]):
                return [nextNode, '0']
            else:
                print("Buf or INV")
                return ['-1','-1']

def backtrace(node,value):
    if node in inputs:
        return [node, value]
    n = node
    invParity = 0
    cnt = 0
    while not (n in inputs):
        cnt += 1
        for g in gates:
            if (g.o == n) and (wires[g.i[0]] == 'X') : 
                n = g.i[0]
                if(g.type in ["NOR","NAND","INV"]):
                    invParity += 1
                break
            
            elif(not g.type in ["INV","BUF"]):
                if (g.o == n) and (wires[g.i[1]] == 'X') : 
                    n = g.i[1]
                    if(g.type in ["NOR","NAND","INV"]):
                        invParity += 1
                    break
        if(cnt == 100):
            print("Failed")
            return ['-1','-1']

            
    # Odd invParity
    if invParity % 2 :
        if value == '1':
            return [n, '0']
        else:
            return [n, '1']
    else:
        if value == '1':
            return [n, '1']
        else:
            return [n, '0']
 
def logicSimulate(faultNode, stuckAt, wires):
    for g in outputGates:
        a = compute(outputGates[g],wires, faultNode, stuckAt) 
        # b = compute2(outputGates[g],wires, faultNode, stuckAt) 
        wires[outputGates[g].o] = a

def updateDFrontiers():
    global DFrontier
    DFrontier = []
    for g in gates:
        if(not g.type in ["INV","BUF"]):
            if(wires[g.o] == 'X'):
                #Changed here
                if((wires[g.i[0]] in ['D','Dbar']) and (wires[g.i[1]] == 'X') ):
                    DFrontier.append(g)
                elif((wires[g.i[1]] in ['D','Dbar']) and (wires[g.i[0]] == 'X')):
                    DFrontier.append(g)
    
def XPathCheck(faultNode):
    # If fault is at Input as is X
    if(faultNode in inputs):
        if(wires[faultNode] != 'X'):
            return 0
        else:
            return 1

    while True:
        for gt in DFrontier:
            g = gates[gt]
            if g.o == faultNode:
                if(g.type in ["BUF","INV"]):
                    if(wires[g.i[0]] == 'X'):
                        faultNode = g.i[0]
                        return 1
                    else:
                        return 0
                else:
                    if(wires[g.i[0]] == 'X'):
                        faultNode = g.i[0]
                        return 1
                    elif(wires[g.i[1]] == 'X'):
                        faultNode = g.i[1]
                        return 1
                    else:
                        return 0
        return 1

def PODEMRecursion(faultNode, stuckAt):
    updateDFrontiers()

    # If D or Dbar is at PO
    for i in outputs:
        if(wires[i] in ['D','Dbar']):
            return True


    # Check failure state to terminate
    if (len(DFrontier) < 1) and (XPathCheck(faultNode) == False):
        return False

    #[node, value]
    [g,v] = getObjective(faultNode, stuckAt)
    if [g,v] == ['-1','-1']:
        return False
    [pi,u] = backtrace(g,v)
    if [pi,u] == ['-1','-1']:
        return False

    wires[pi] = u
    
    if(pi == faultNode):
        if(u == '1' and stuckAt == '0'):
            wires[pi] = 'D'
        if(u == '0' and stuckAt == '1'):
            wires[pi] = 'Dbar'

    logicSimulate(faultNode, stuckAt, wires)

    result = PODEMRecursion(faultNode, stuckAt)

    if(result):
        return True

    if(u == '1'):
        u = '0'
    else:
        u = '1'

    wires[pi] = u

    logicSimulate(faultNode, stuckAt, wires)

    result = PODEMRecursion(faultNode, stuckAt)

    if(result):
        return True

    u = 'X'
    wires[pi] = u

    return False

def resetState():
    for w in wires.keys():
        wires[w] = 'X'

if __name__ == "__main__":
    inpLen = 0
    
    with open(cktFile, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.split()[0] == "INPUT":
                inpLen = len(line[5:].strip().split()) - 1
                break    
        
        f.seek(0)

        while True:
            newLine = f.readline()
            if newLine == None:
                break
            newLine = newLine.split()
            if len(newLine) != 0:
                
                if newLine[0] == "INPUT":
                    inputs = newLine[1:-1]
                    for ip in inputs:
                        wires[ip] = "X"        
                elif newLine[0] == "OUTPUT":
                    outputs = newLine[1:-1]

                else:
                    gates.append(Gate(newLine[0], newLine[1:-1], newLine[-1]))
                    for node in newLine[1:]:
                        wires[node] = "X"
            else:
                break


        # Map the output gates
        for o in outputs:
            for g in gates:
                if(g.o == o):
                    outputGates[o] = g

        for g in gates:
            gateOutputMap[g.o] = g

   
    if(args.fanout):
        for c in gates:
            opX = str(c.o)
            newOutput = c.o + 'FO'
            FI = 0
            opFo = None
            ipFo = []
            
            for ci in gates:       
                if (ci.i[0] == opX) or ((not ci.type in ["BUF","INV"]) and ci.i[1] == opX):
                    ipFo.append(ci)

            if(len(ipFo) > 1):
                
                for ci in ipFo:
                    newCI = c.o+"_"+str(FI)
                    gates.append(Gate("BUF", [newOutput], newCI ))
                    wires[newCI] = "X"
                    if(ci.i[0] == opX):
                        ci.i[0] = newCI
                    else:
                        ci.i[1] = newCI
                    FI +=1
                wires.pop(c.o)
                wires[newOutput] = "X"
                c.o = newOutput

        for x in range(len(inputs)):
            i = inputs[x]
            opX = str(i)
            newOutput = i + 'FO'
            FI = 0
            opFo = None
            ipFo = []
            
            for ci in gates:       
                if (ci.i[0] == opX) or ((not ci.type in ["BUF","INV"]) and ci.i[1] == opX):
                    ipFo.append(ci)

            if(len(ipFo) > 1):
                
                for ci in ipFo:
                    newCI = i+"_"+str(FI)
                    gates.append(Gate("BUF", [newOutput], newCI ))
                    wires[newCI] = "X"
                    if(ci.i[0] == opX):
                        ci.i[0] = newCI
                    else:
                        ci.i[1] = newCI
                    FI +=1
                wires.pop(i)
                wires[newOutput] = "X"
                inputs[x] = newOutput
                

    for g in gates:
            gateOutputMap[g.o] = g
        
    
    with open(faultFile, "r") as f:   
        lines = f.readlines()

        for line in lines:
            thisLine = line.split()
            faultsToTest.append([thisLine[1],thisLine[-1][-1]])

    text = f"{cktFile}\n"
    text = text.encode('utf8')
    sys.stdout.buffer.write(text)
    for fault in faultsToTest:
        resetState()
        
        faultNode = fault[0]
        stuckAt = fault[1]
        
        result = PODEMRecursion(faultNode, stuckAt)
        
        if(result):
            for c in wires.keys():
                if(wires[c] == 'D'):
                    wires[c] = '1'
                elif(wires[c] == 'Dbar'):
                    wires[c] = '0'

            
            inpVec = ""
            for i in inputs:
                inpVec += wires[i]
            
            text = f"Net {faultNode} s-a-{stuckAt} - {inpVec}\n"
            text = text.encode('utf8')
            sys.stdout.buffer.write(text)
            if(args.dfs):
                ded_faultNode,ded_stuckAt = deductive_module.faultDeduction(cktFile, inpVec.replace('X','0'),stuckAt,faultNode)
        
                if((ded_stuckAt != int(stuckAt)) or (ded_faultNode != int(faultNode))):
                    text = "❌ Deductive Fault Simulator Failed.\n"
                else:
                    text= "✅ Deductive Fault Simulator Passed.\n"
                text = text.encode('utf8')
                sys.stdout.buffer.write(text)
                sys.stdout.buffer.flush()
                
        else:
            text = f"Net {faultNode} s-a-{stuckAt} - No Test\n\n"    
            text = text.encode('utf8')
            sys.stdout.buffer.write(text)
    print()