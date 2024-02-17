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
    binaryNum = bin(int(num)).replace('0b', '')

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
    opcode = 51
    f3 = None
    f7 = None
    rs1 = instructionTokens[2]
    rs2 = instructionTokens[3]
    rd = instructionTokens[1]

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
    return 'iLoad'

def iImmAssembler(instructionTokens, idx):
    return 'iImm'

def jalrAssembler(instructionTokens, idx):
    return 'jalr'

def sAssembler(instructionTokens, idx):
    return 's'

def bAssembler(instructionTokens, idx):
    return 'b'

def uAssembler(instructionTokens, idx):
    return 'u'

def jAssembler(instructionTokens, idx):
    return 'j'

def assembleFile(source, destination):
    #Iterate through each line in source file
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
            
            labels[instructionTokens[0][:-1]] = idx
            continue

        #Determine instruction format and route to appropriate assembler function
        assembledLine = None   #Variable to hold assembled line
        if (instructionTokens[0] in rInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = rAssembler(instructionTokens, idx)
        elif (instructionTokens[0] in iLoadInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = iLoadAssembler(instructionTokens, idx)
        elif (instructionTokens[0] in iImmInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = iImmAssembler(instructionTokens, idx)
        elif (instructionTokens[0] in sInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = sAssembler(instructionTokens, idx)
        elif (instructionTokens[0] in jalrInstructions):
            if (len(instructionTokens) != 4 & len(instructionTokens) != 2):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = jalrAssembler(instructionTokens, idx)
        elif (instructionTokens[0] in bInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = bAssembler(instructionTokens, idx)
        elif (instructionTokens[0] in jInstructions):
            if (len(instructionTokens) != 2 & len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = jAssembler(instructionTokens, idx)
        elif (instructionTokens[0] in uInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = uAssembler(instructionTokens, idx)
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

if __name__ == "__main__":
    main()