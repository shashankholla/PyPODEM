
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


# Compute Function for circuit simulator
def compute(gate, wires, table):
    if wires.get(gate.o, -1) != -1:
        return wires[gate.o]

    if gate.type == "AND":
        if gate.i[0] in wires:
            a = wires[gate.i[0]]
        else:
            a = compute(table[gate.i[0]], wires, table)
            wires[gate.i[0]] = a
        if gate.i[1] in wires:
            b = wires[gate.i[1]]
        else:
            b = compute(table[gate.i[1]], wires, table)
            wires[gate.i[1]] = b

        return a & b

    if gate.type == "NAND":
        if gate.i[0] in wires:
            a = wires[gate.i[0]]
        else:
            a = compute(table[gate.i[0]], wires, table)
            wires[gate.i[0]] = a
        if gate.i[1] in wires:
            b = wires[gate.i[1]]
        else:
            b = compute(table[gate.i[1]], wires, table)
            wires[gate.i[1]] = b

        return not (a & b)

    if gate.type == "OR":
        if gate.i[0] in wires:
            a = wires[gate.i[0]]
        else:
            a = compute(table[gate.i[0]], wires, table)
            wires[gate.i[0]] = a
        if gate.i[1] in wires:
            b = wires[gate.i[1]]
        else:
            b = compute(table[gate.i[1]], wires, table)
            wires[gate.i[1]] = b

        return a | b

    if gate.type == "NOR":
        if gate.i[0] in wires:
            a = wires[gate.i[0]]

        else:
            a = compute(table[gate.i[0]], wires, table)
            wires[gate.i[0]] = a
        if gate.i[1] in wires:
            b = wires[gate.i[1]]
        else:
            b = compute(table[gate.i[1]], wires, table)
            wires[gate.i[1]] = b

        return not (a | b)

    if gate.type == "INV":
        if gate.i[0] in wires:
            a = wires[gate.i[0]]
        else:
            a = compute(table[gate.i[0]], wires, table)
            wires[gate.i[0]] = a

        return not a

    if gate.type == "BUF":
        if gate.i[0] in wires:
            a = wires[gate.i[0]]
        else:
            a = compute(table[gate.i[0]], wires, table)
            wires[gate.i[0]] = a

        return a


def deduce(gate, faultMap, inputs, wires, table):

    if gate.type in ["AND", "NAND", "OR", "NOR"]:
        if not gate.i[0] in inputs:
            deduce(table[gate.i[0]], faultMap, inputs, wires, table)
        if not gate.i[1] in inputs:
            deduce(table[gate.i[1]], faultMap, inputs, wires, table)

        faultListA = set(faultMap.get(gate.i[0], set()))
        faultListB = set(faultMap.get(gate.i[1], set()))

        ip1 = wires[gate.i[0]]
        ip2 = wires[gate.i[1]]
        if gate.type in ["AND", "NAND"]:
            if ip1 == 0:
                if ip2 == 0:  # A -> 0 , B -> 0
                    faultMap[gate.o] = (
                        set(faultListA)
                        .intersection(set(faultListB))
                        .union(faultMap.get(gate.o, set()))
                    )
                else:  # A -> 0, B -> 1
                    faultMap[gate.o] = (set(faultListA) - set(faultListB)).union(
                        faultMap.get(gate.o, set())
                    )

            if ip1 == 1:
                if ip2 == 0:  # A -> 1 , B -> 0
                    faultMap[gate.o] = (set(faultListB) - set(faultListA)).union(
                        faultMap.get(gate.o, set())
                    )
                else:  # A -> 1, B -> 1
                    faultMap[gate.o] = (
                        set(faultListA)
                        .union(set(faultListB))
                        .union(faultMap.get(gate.o, set()))
                    )

            # return a & b

        if gate.type in ["OR", "NOR"]:
            if ip1 == 0:
                if ip2 == 0:  # A -> 0 , B -> 0
                    faultMap[gate.o] = (
                        set(faultListA)
                        .union(set(faultListB))
                        .union(faultMap.get(gate.o, set()))
                    )
                else:  # A -> 0, B -> 1
                    faultMap[gate.o] = (set(faultListB) - set(faultListA)).union(
                        faultMap.get(gate.o, set())
                    )

            if ip1 == 1:
                if ip2 == 0:  # A -> 1 , B -> 0
                    faultMap[gate.o] = (set(faultListA) - set(faultListB)).union(
                        faultMap.get(gate.o, set())
                    )
                else:  # A -> 1, B -> 1
                    faultMap[gate.o] = (
                        set(faultListA)
                        .intersection(set(faultListB))
                        .union(faultMap.get(gate.o, set()))
                    )

    if gate.type in ["INV", "BUF"]:
        if not gate.i[0] in inputs:
            deduce(table[gate.i[0]], faultMap, inputs, wires, table)
        faultListA = set(faultMap.get(gate.i[0], set()))
        faultMap[gate.o] = faultListA.union(faultMap.get(gate.o, set()))


def faultDeduction(cktFile, cktInput, fault, node):
    with open(cktFile, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.split()[0] == "INPUT":
                inpLen = len(line[5:].strip().split()) - 1
                break

        inpVec = cktInput.strip()

        gates: List[Gate] = []
        inputs = []
        outputs = []
        wires = dict()
        table = dict()
        faultMap = dict()
        f.seek(0)
        while True:
            newLine = f.readline()
            if newLine == None:
                break
            newLine = newLine.split()
            if len(newLine) != 0:
                newLine = [newLine[0]] + list(map(int, newLine[1:]))
                if newLine[0] == "INPUT":
                    inputs = newLine[1:-1]
                    for ip in inputs:
                        wires[ip] = int(cktInput[0])
                        cktInput = cktInput[1:]
                elif newLine[0] == "OUTPUT":
                    outputs = newLine[1:-1]

                else:
                    gates.append(Gate(newLine[0], newLine[1:-1], newLine[-1]))
            else:
                break

        for g in gates:
            table[g.o] = g

        opTxt = ""

        for o in outputs:
            wires[o] = compute(table[o], wires, table)
            opTxt += str(int(wires[o]))



        
        fault = int(fault)
        node = int(node)
        if wires[node] != fault:
            faultMap[node] = faultMap.get(node, []) + [
                str(node) + "_" + str(fault)
            ]
        for i in inputs:
            faultMap[i] = faultMap.get(i, [])

        ll = list(faultMap.keys()).sort()
        # ll.sort()

        for o in outputs:
            deduce(table[o], faultMap, inputs, wires, table)

        allFaults = list()
        for o in outputs:
            allFaults = allFaults + list(faultMap[o])

        allFaults = list(set(allFaults))
        allFaults.sort(key=lambda x: int(x.split("_")[0]))
        return list(map(int,allFaults[0].split("_")))

