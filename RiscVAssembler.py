#Possible instructions for each format
rInstructions = ('add', 'mult', 'sub', 'sll', 'slt', 'multu', 'xor', 'div', 'srl', 'divu', 'sra', 'or', 'and')
iLoadInstructions = ('lb', 'lh', 'lw')
iImmInstructions = ('addi', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai')
sInstructions = ('sb', 'sh', 'sw')
jalrInstructions = ('jr', 'jalr')
bInstructions = ('beq', 'bne', 'bgtz', 'bltz', 'blt', 'blez', 'bge', 'bgez', 'beq')
jInstructions = ('j', 'jal')
uInstructions = ('lui')

#Alternate register names
regNames = {
    '0': '0',
    'zero': '0',
    'ra': '1',
    'sp': '2',
    'gp': '3',
    'tp': '4',
    't0': '5',
    't1': '6',
    't2': '7',
    'fp': '8',
    's1': '9',
    'a0': '10',
    'a1': '11',
    'a2': '12',
    'a3': '13',
    'a4': '14',
    'a5': '15',
    'a6': '16',
    'a7': '17',
    's2': '18',
    's3': '19',
    's4': '20',
    's5': '21',
    's6': '22',
    's7': '23',
    's8': '24',
    's9': '25',
    's10': '26',
    's11': '27',
    't3': '28',
    't4': '29',
    't5': '30',
    't6': '31'
}

#Dictionary for labels
labels = {}

#Function to convert number to binary value of a certain length
def convertToBinary(num, digits):
    negFlag = False
    binaryNum = bin(int(num)).replace('0b', '')

    #Set flag to introduce correct sign bit if negative
    if (binaryNum[0] == '-'):
        negFlag = True
        binaryNum = binaryNum[1:]

    if (negFlag):
        while(len(binaryNum) < digits - 1):
            binaryNum = '0' + binaryNum

        binaryNum = '1' + binaryNum
    else:
        while(len(binaryNum) < digits):
            binaryNum = '0' + binaryNum

    return binaryNum

#Function to convert binary number to hexadecimal
def convertToHex(binaryNum):
    num = int(binaryNum, 2) #Convert to an integer
    hexNum = format(num, 'x')   #Convert to hex

    #Pad 0s until the number is the correct length
    while (len(hexNum) < 8):
        hexNum = '0' + hexNum

    return hexNum

def rAssembler(instructionTokens, idx):
    #Initialize instruction components
    opcode = 51
    f3 = None
    f7 = None
    rs1 = instructionTokens[2]
    rs2 = instructionTokens[3]
    rd = instructionTokens[1]

    #Assign f3 and f7 values according to instruction
    match instructionTokens[0]:
        case 'add':
            f3 = 0
            f7 = 0
        case 'mult':
            f3 = 0
            f7 = 1
        case 'sub':
            f3 = 0
            f7 = 32
        case 'sll':
            f3 = 1
            f7 = 0
        case 'slt':
            f3 = 2
            f7 = 0
        case 'multu':
            f3 = 3
            f7 = 0
        case 'xor':
            f3 = 4
            f7 = 0
        case 'div':
            f3 = 4
            f7 = 1
        case 'srl':
            f3 = 5
            f7 = 0
        case 'divu':
            f3 = 5
            f7 = 1
        case 'sra':
            f3 = 5
            f7 = 32
        case 'or':
            f3 = 6
            f7 = 0
        case 'and':
            f3 = 7
            f7 = 0

    #Reduce rd to register number
    if (rd in regNames):
        rd = regNames[rd]
    elif (rd[0] == 'x'):
        rd = rd[1:]

    #Reduce rs1 to register number
    if (rs1 in regNames):
        rs1 = regNames[rs1]
    elif (rs1[0] == 'x'):
        rs1 = rs1[1:]

    #Reduce rs2 to register number
    if (rs2 in regNames):
        rs2 = regNames[rs2]
    elif (rs2[0] == 'x'):
        rs2 = rs2[1:]
    
    #Convert machine parameters to binary strings of correct length
    opcode = convertToBinary(opcode, 7)
    f3 = convertToBinary(f3, 3)
    f7 = convertToBinary(f7, 7)
    rd = convertToBinary(rd, 5)
    rs1 = convertToBinary(rs1, 5)
    rs2 = convertToBinary(rs2, 5)

    #Concatenate binary values
    assembledLine = f7 + rs2 + rs1 + f3 + rd + opcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'

def iLoadAssembler(instructionTokens, idx):
    #Initialize instruction parameters
    opcode = 3
    f3 = None
    rd = instructionTokens[1]
    rs1 = None
    imm = None

    #Split imm and rs1 from instruction input
    imm, delimiter, rs1 = instructionTokens[2].partition('(')
    rs1 = rs1[:-1]  #Remove closing parenthesis

    #Assign f3 based on instruction
    match instructionTokens[0]:
        case 'lb':
            f3 = 0
        case 'lh':
            f3 = 1
        case 'lw':
            f3 = 2

    #Reduce rd to register number
    if (rd in regNames):
        rd = regNames[rd]
    elif (rd[0] == 'x'):
        rd = rd[1:]

    #Reduce rs1 to register number
    if (rs1 in regNames):
        rs1 = regNames[rs1]
    elif (rs1[0] == 'x'):
        rs1 = rs1[1:]
    
    #Convert machine parameters to binary strings of correct length
    opcode = convertToBinary(opcode, 7)
    f3 = convertToBinary(f3, 3)
    rd = convertToBinary(rd, 5)
    rs1 = convertToBinary(rs1, 5)
    imm = convertToBinary(imm, 12)

    #Concatenate binary values
    assembledLine = imm + rs1 + f3 + rd + opcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'

def iImmAssembler(instructionTokens, idx):
    #Initialize instruction parameters
    opcode = 19
    f3 = None
    rd = instructionTokens[1]
    rs1 = instructionTokens[2]
    imm = instructionTokens[3]

    #Assign f3 based on instruction
    match instructionTokens[0]:
        case 'addi':
            f3 = 0
        case 'xori':
            f3 = 4
        case 'ori':
            f3 = 6
        case 'andi':
            f3 = 7
        case 'slli':
            f3 = 1
        case 'srli':
            f3 = 5
            imm5_11 = 0
        case 'srai':
            f3 = 5
            imm5_11 = 32

    #Reduce rd to register number
    if (rd in regNames):
        rd = regNames[rd]
    elif (rd[0] == 'x'):
        rd = rd[1:]

    #Reduce rs1 to register number
    if (rs1 in regNames):
        rs1 = regNames[rs1]
    elif (rs1[0] == 'x'):
        rs1 = rs1[1:]
    
    #Convert machine parameters to binary strings of correct length, with special case when imm5_11 is used as f7
    if (f3 != 5):
        opcode = convertToBinary(opcode, 7)
        f3 = convertToBinary(f3, 3)
        rd = convertToBinary(rd, 5)
        rs1 = convertToBinary(rs1, 5)
        imm = convertToBinary(imm, 12)

        #Concatenate binary values
        assembledLine = imm + rs1 + f3 + rd + opcode
    else:
        opcode = convertToBinary(opcode, 7)
        f3 = convertToBinary(f3, 3)
        rd = convertToBinary(rd, 5)
        rs1 = convertToBinary(rs1, 5)
        imm = convertToBinary(imm, 5)
        imm5_11 = convertToBinary(imm5_11, 7)

        #Concatenate binary values
        assembledLine = imm5_11 + imm + rs1 + f3 + rd + opcode

    #Convert to hexcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'

def jalrAssembler(instructionTokens, idx):
    #Initialize instruction parameters
    opcode = 103
    f3 = None
    rd = None
    rs1 = None
    imm = None

    #Assign f3 based on instruction
    match instructionTokens[0]:
        case 'jalr':
            f3 = 0
            rd = instructionTokens[1]
            rs1 = instructionTokens[2]
            imm = instructionTokens[3]
        case 'jr':
            f3 = 0
            rd = 'x0'
            rs1 = instructionTokens[1]
            imm = 0

    #Reduce rd to register number
    if (rd in regNames):
        rd = regNames[rd]
    elif (rd[0] == 'x'):
        rd = rd[1:]

    #Reduce rs1 to register number
    if (rs1 in regNames):
        rs1 = regNames[rs1]
    elif (rs1[0] == 'x'):
        rs1 = rs1[1:]
    
    #Convert machine parameters to binary strings of correct length
    opcode = convertToBinary(opcode, 7)
    f3 = convertToBinary(f3, 3)
    rd = convertToBinary(rd, 5)
    rs1 = convertToBinary(rs1, 5)
    imm = convertToBinary(imm, 12)

    #Concatenate binary values
    assembledLine = imm + rs1 + f3 + rd + opcode

    #Convert to hexcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'

def sAssembler(instructionTokens, idx):
    #Initialize instruction parameters
    opcode = 35
    f3 = None
    rs1 = None
    rs2 = instructionTokens[1]
    imm = None

    #Split imm and rs1 from instruction input
    imm, delimiter, rs1 = instructionTokens[2].partition('(')
    rs1 = rs1[:-1]  #Remove closing parenthesis

    #Assign f3 based on instruction
    match instructionTokens[0]:
        case 'sb':
            f3 = 0
        case 'sh':
            f3 = 1
        case 'sw':
            f3 = 2

    #Reduce rs1 to register number
    if (rs1 in regNames):
        rs1 = regNames[rs1]
    elif (rs1[0] == 'x'):
        rs1 = rs1[1:]

    #Reduce rs2 to register number
    if (rs2 in regNames):
        rs2 = regNames[rs2]
    elif (rs2[0] == 'x'):
        rs2 = rs2[1:]
    
    #Convert machine parameters to binary strings of correct length
    opcode = convertToBinary(opcode, 7)
    f3 = convertToBinary(f3, 3)
    rs1 = convertToBinary(rs1, 5)
    rs2 = convertToBinary(rs2, 5)
    imm = convertToBinary(imm, 12)

    #Concatenate binary values
    assembledLine = imm[0:7] + rs2 + rs1 + f3 + imm[7:12] + opcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'

def bAssembler(instructionTokens, idx):
    #Initialize instruction components
    opcode = 99
    f3 = None
    rs1 = None
    rs2 = None
    imm = None

    #Assign f3 and f7 values according to instruction
    match instructionTokens[0]:
        case 'beq':
            f3 = 0
            rs1 = instructionTokens[1]
            rs2 = instructionTokens[2]
            imm = instructionTokens[3]
        case 'bne':
            f3 = 1
            rs1 = instructionTokens[1]
            rs2 = instructionTokens[2]
            imm = instructionTokens[3]
        case 'blt':
            f3 = 4
            rs1 = instructionTokens[1]
            rs2 = instructionTokens[2]
            imm = instructionTokens[3]
        case 'bgtz':
            f3 = 4
            rs1 = 'x0'
            rs2 = instructionTokens[1]
            imm = instructionTokens[2]
        case 'bltz':
            f3 = 4
            rs1 = instructionTokens[1]
            rs2 = 'x0'
            imm = instructionTokens[2]
        case 'bge':
            f3 = 5
            rs1 = instructionTokens[1]
            rs2 = instructionTokens[2]
            imm = instructionTokens[3]
        case 'blez':
            f3 = 5
            rs1 = 'x0'
            rs2 = instructionTokens[1]
            imm = instructionTokens[2]
        case 'bgez':
            f3 = 5
            rs1 = instructionTokens[1]
            rs2 = 'x0'
            imm = instructionTokens[2]

    #Reduce rs1 to register number
    if (rs1 in regNames):
        rs1 = regNames[rs1]
    elif (rs1[0] == 'x'):
        rs1 = rs1[1:]

    #Reduce rs2 to register number
    if (rs2 in regNames):
        rs2 = regNames[rs2]
    elif (rs2[0] == 'x'):
        rs2 = rs2[1:]

    #Calculate imm value based on instructions from label
    imm = (labels[imm] - idx) * 4
    
    #Convert machine parameters to binary strings of correct length
    opcode = convertToBinary(opcode, 7)
    f3 = convertToBinary(f3, 3)
    rs1 = convertToBinary(rs1, 5)
    rs2 = convertToBinary(rs2, 5)
    imm = convertToBinary(imm, 12)

    #Concatenate binary values
    assembledLine = imm[0:7] + rs2 + rs1 + f3 + imm[7:12] + opcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'

def uAssembler(instructionTokens, idx):
    #Initialize instruction components
    opcode = 55
    rd = instructionTokens[1]
    imm = instructionTokens[2]

    #Reduce rd to register number
    if (rd in regNames):
        rd = regNames[rd]
    elif (rd[0] == 'x'):
        rd = rd[1:]
    
    #Convert machine parameters to binary strings of correct length
    opcode = convertToBinary(opcode, 7)
    rd = convertToBinary(rd, 5)
    imm = convertToBinary(imm, 20)

    #Concatenate binary values
    assembledLine = imm + rd + opcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'


def jAssembler(instructionTokens, idx):
    #Initialize instruction components
    opcode = 111
    rd = None
    imm = None

    #Assign f3 and f7 values according to instruction
    match instructionTokens[0]:
        case 'jal':
            rd = instructionTokens[1]
            imm = instructionTokens[2]
        case 'j':
            rd = 'x0'
            imm = instructionTokens[1]

    if (imm in labels):
        imm = (labels[imm] - idx) * 4

    #Reduce rd to register number
    if (rd in regNames):
        rd = regNames[rd]
    elif (rd[0] == 'x'):
        rd = rd[1:]
    
    #Convert machine parameters to binary strings of correct length
    opcode = convertToBinary(opcode, 7)
    rd = convertToBinary(rd, 5)
    imm = convertToBinary(imm, 20)

    #Concatenate binary values
    assembledLine = imm + rd + opcode
    assembledLine = convertToHex(assembledLine)

    return assembledLine + '\n'

def assembleFile(source, destination):
    #Initialize instruction counter
    numInstructions = 0

    #Iterate through each line in source file to find labels
    for idx, line in enumerate(source):
        parser = line.split()   #Split line into individual elements
        instructionTokens = []  #Empty array to hold elements

        #Iterate through each element of the instruction line
        for token in parser:
            if (token[0] == '#'):   #Skip processing of comments
                break

            token = token.replace(',', '')  #Remove commas
            
            instructionTokens.append(token) #Add token to element array

        if (len(instructionTokens) == 0):   #Skip processing of lines only containing a comment
            continue

        if (len(instructionTokens) == 1):   #Adds labels to dictionary
            if (instructionTokens[0][-1] != ':'):   #Ensure single element is label
                print("Invalid instruction at line " + str(idx + 1) + ". Assembly failed.")
                return
            
            labels[instructionTokens[0][:-1]] = numInstructions + 1
            continue

        numInstructions += 1

    #Reset instruction counter and file position
    numInstructions = 0
    source.seek(0)

    #Iterate through each line in source file for assembling
    for idx, line in enumerate(source):
        parser = line.split()   #Split line into individual elements
        instructionTokens = []  #Empty array to hold elements

        #Iterate through each element of the instruction line
        for token in parser:
            if (token[0] == '#'):   #Skip processing of comments
                break

            token = token.replace(',', '')  #Remove commas
            
            instructionTokens.append(token) #Add token to element array

        if (len(instructionTokens) == 0 or len(instructionTokens) == 1):   #Skip processing of lines only containing a comment or label
            continue

        numInstructions += 1

        #Determine instruction format and route to appropriate assembler function
        assembledLine = None   #Variable to hold assembled line
        if (instructionTokens[0] in rInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = rAssembler(instructionTokens, numInstructions)
        elif (instructionTokens[0] in iLoadInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = iLoadAssembler(instructionTokens, numInstructions)
        elif (instructionTokens[0] in iImmInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = iImmAssembler(instructionTokens, numInstructions)
        elif (instructionTokens[0] in sInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = sAssembler(instructionTokens, numInstructions)
        elif (instructionTokens[0] in jalrInstructions):
            if (len(instructionTokens) != 4 & len(instructionTokens) != 2):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = jalrAssembler(instructionTokens, numInstructions)
        elif (instructionTokens[0] in bInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = bAssembler(instructionTokens, numInstructions)
        elif (instructionTokens[0] in jInstructions):
            if (len(instructionTokens) != 2 & len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = jAssembler(instructionTokens, numInstructions)
        elif (instructionTokens[0] in uInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = uAssembler(instructionTokens, numInstructions)
        else:
            print(instructionTokens[0])
            print("Invalid instruction at line " + str(idx + 1) + ". Assembly failed.")
            return
        
        destination.write(assembledLine)
        

def main():
    #Open source file from user input
    while (True):
        try:
            sourceFilename = input("Enter file containing Risc-V assembly code to convert: ")
            source = open(sourceFilename)
        except IOError:
            print("File failed to open.")
        else:
            break

    #Create destination file
    identifierIndex = sourceFilename.find('.')
    destinationFilename = sourceFilename[:identifierIndex] + 'Assembled' + sourceFilename[identifierIndex:]
    destination = open(destinationFilename, 'w')

    #Call assembler function
    assembleFile(source, destination)

    print("Assembly successful. Result in " + destinationFilename)

if __name__ == "__main__":
    main()