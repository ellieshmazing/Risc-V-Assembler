#Possible instructions for each format
rInstructions = ('add', 'mult', 'sub', 'sll', 'slt', 'multu', 'xor', 'div', 'srl', 'divu', 'sra', 'or', 'and')
iLoadInstructions = ('lb', 'lh', 'lw')
iImmInstructions = ('addi', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai')
sInstructions = ('sb', 'sh', 'sw')
jalrInstructions = ('jr', 'jalr')
bInstructions = ('beq', 'bne', 'bgtz', 'bltz', 'blt', 'blez', 'bge', 'bgez', 'beq')
jInstructions = ('j', 'jal')
uInstructions = ('lui')

def rAssembler(instructionTokens):
    print("r")

def iLoadAssembler(instructionTokens):
    print("i")

def iImmAssembler(instructionTokens):
    print("i")

def jalrAssembler(instructionTokens):
    print("i")

def sAssembler(instructionTokens):
    print("s")

def bAssembler(instructionTokens):
    print("b")

def uAssembler(instructionTokens):
    print("u")

def jAssembler(instructionTokens):
    print("j")

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

        if (len(instructionTokens) == 1):   #Handles labels
            continue

        #Determine instruction format and route to appropriate assembler function
        assembledLine = None   #Variable to hold assembled line
        if (instructionTokens[0] in rInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = rAssembler(instructionTokens)
        elif (instructionTokens[0] in iLoadInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = iLoadAssembler(instructionTokens)
        elif (instructionTokens[0] in iImmInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = iImmAssembler(instructionTokens)
        elif (instructionTokens[0] in sInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = sAssembler(instructionTokens)
        elif (instructionTokens[0] in jalrInstructions):
            if (len(instructionTokens) != 4 & len(instructionTokens) != 2):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = jalrAssembler(instructionTokens)
        elif (instructionTokens[0] in bInstructions):
            if (len(instructionTokens) != 4):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = bAssembler(instructionTokens)
        elif (instructionTokens[0] in jInstructions):
            if (len(instructionTokens) != 2 & len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = jAssembler(instructionTokens)
        elif (instructionTokens[0] in uInstructions):
            if (len(instructionTokens) != 3):
                print("Invalid number of arguments at line " + str(idx + 1) + ". Assembly failed.")
                return
            assembledLine = uAssembler(instructionTokens)
        else:
            print(instructionTokens[0])
            print("Invalid instruction at line " + str(idx + 1) + ". Assembly failed.")
            return
        
        #destination.write(assembledLine)
        

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