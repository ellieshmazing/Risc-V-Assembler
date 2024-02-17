def assembleFile(source):
    for line in source: #Iterate through each line in source file
        parser = line.split()   #Split line into individual elements
        instructionTokens = []  #Empty array to hold elements

        for token in parser:    #Iterate through each element of the instruction line
            if (token[0] == '#'):   #Stop processing of comments
                break
            
            instructionTokens.append(token) #Add token to element array

        if (len(instructionTokens) == 0):   #Stop processing for lines only containing a comment
            continue

        if (len(instructionTokens) == 1):   #Handles labels
            continue

        print(len(instructionTokens))

        

def main():
    while (True):   #Open file from user input
        try:
            filename = input("Enter file containing Risc-V assembly code to convert: ")
            source = open(filename)
        except IOError:
            print("File failed to open.")
        else:
            break

    assembleFile(source)

if __name__ == "__main__":
    main()