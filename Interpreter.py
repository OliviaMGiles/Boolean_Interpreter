# Olivia Giles
# Concepts of PRogramming Languages
# Interpereter Programming Project
#
# Prompt for input 
#   string containing Boolean expression     <--- Using this one
#   white spaces are optional delimiters
# Check if 
#   1. expression is valid syntax, 
#   2. no undefined variables (return error once per var and continue checking)
# Output: 
#   1. error messages
#   2. or message that gives the value of the expression

#global Variables
lex = ""
tokensList = []

varTable = {} #variables are stored as a key-value pair
sas = [] #semantic action stack

#tokenize input
#Throws exceptions for illegal characters and syntax errors involving := and ->
def tokenize(rawInput):
    tokens = list(rawInput) #list of characters
    i=0
    while i <len(tokens):
        if tokens[i] == " ":
            tokens.pop(i)   #remove the whitespace token
            continue        #restart the loop
        if tokens[i] in 'abcdefghijklmnopqrstuvwxyzV^()TF~.#;':
            pass         #leave the token alone and continue to the next token
        elif tokens[i] == ":":
            if tokens[i+1] == "=":
                tokens.pop(i+1)     #remove '='
                tokens[i] = ":="    #replace ':' with ':='
            else:
                raise Exception("Syntax Error: expected ':=' but got '"+tokens[i]+tokens[i+1]+"'")
        elif tokens[i] == "-":
            if tokens[i+1] == ">":
                tokens.pop(i+1)     #remove '>'
                tokens[i] = "->"    #replace '-' with '->'
            else:
                raise Exception("Syntax Error: expected '->' but got '"+tokens[i]+tokens[i+1]+"'")
        else:
            raise Exception("Syntax Error: unrecognized character '"+tokens[i]+"'")
        i+=1
    return tokens

#helper function. Returns the frontmost token from the tokensList
def getNext():
    global tokensList
    token = ""
    if len(tokensList) > 0: #don't pop from an empty list
        token = tokensList.pop(0)
    return token

#helper function. Returns true if the character is a variabe and false otherwise
def isVar(lex):
    if lex in 'abcdefghijklmnopqrstuvwxyz':
        return True
    else:
        return False

# rule functions
#<B> ::= <VA><IT>.
def B():
    global lex
    if lex in '#~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <VA>
        if VA():
            if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <IT>
                if IT():
                    if lex == ".":
                        lex = getNext()
                        return True
                    else: print("Error: Expected '.'  but got '"+lex+"'"); return False      
                else: return False
            else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False        
        else: return False
    else: print("Error: Expected '#', '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False
        
#<VA> ::= #var:=<IT>;<VA>
#<VA> ::= {empty}
def VA():
    global lex
    global varTable
    if lex == "#": #<VA> ::= #var:=<IT>;<VA>
        lex = getNext()
        if isVar(lex): #check to make sure lex is a var
            tempVar = lex
            lex= getNext()
            if lex == ':=':
                lex = getNext()
                if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <IT>
                    if IT():
                        #semantics to define var
                        varTable[tempVar] = sas.pop(0) #store the value of <IT> into the var table
                        if lex == ";":
                            lex = getNext()
                            if lex in '#~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <VA>
                                if VA():
                                    return True
                                else: return False
                            else: print("Error: Expected '#', '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False # not in selection set of <VA>
                        else: print("Error: Expected ';'  but got '"+lex+"'"); return False
                    else: return False
                else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'");return False # not in selection set of <IT>
            else: print("Error: Expected ':=' but got '"+lex+"'");return False
        else: print("Error: Expected a lowercase letter but got '"+lex+"'");return False #not var
    else: #<VA> ::= {empty}
        return True

#<IT> ::= <CT><IT_Tail>
def IT():
    global lex
    if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #Selection set of <CT>
        if CT():
            if lex in '->.;)': #Selection set of <IT_Tail>
                if IT_Tail():
                    return True
                else: return False
            else: print("Error: Expected '->', '.', ';', or ')' but got '"+lex+"'"); return False # not in selection set of <IT_Tail>
        else: return False
    else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False # not in selection set of <CT>

#<IT_Tail> ::= -> <CT><IT_Tail>
#<IT_Tail> ::= {empty}
def IT_Tail():
    global lex
    if lex == '->': #<IT_Tail> ::= -> <CT><IT_Tail>
        lex = getNext()
        if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #Selection set of <CT>
            if CT():
                #semantics of op2 -> op1
                op1 = sas.pop(0)
                op2 = sas.pop(0)
                if isinstance(op1, bool) and isinstance(op2, bool):
                    result = (not op2) or op1 #p->q == not(p) or q
                    sas.insert(0, result)
                else:
                    sas.insert(0, "E")
                if lex in '->.;)': #Selection set of <IT_Tail>
                    if IT_Tail():
                        return True
                    else: return False
                else: print("Error: Expected '->', '.', ';', or ')' but got '"+lex+"'"); return False # not in selection set of <IT_Tail>
            else: return False
        else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False # not in selection set of <CT>
    else: #<IT_Tail> ::= {empty}
        return True

#<CT> ::= <L><CT_Tail>
def CT():
    global lex
    if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <L>
        if L():
            if lex in 'V^->.;)': #selection set of <CT_Tail>
                if CT_Tail():
                    return True
                else: return False
            else: print("Error: Expected 'V', '^', '->', '.', ';', or ')' but got '"+lex+"'"); return False # not in selection set of <CT_Tail>
        else: return False
    else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False # not in selection set of <L>

#<CT_Tail> ::= V <L><CT_Tail>
#<CT_Tail> ::= ^ <L><CT_Tail>
#<CT_Tail> ::= {empty}
def CT_Tail():
    global lex
    if lex == "V": #<CT_Tail> ::= V <L><CT_Tail>
        lex = getNext()
        if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <L>
            if L():
                #semantics for <CT_Tail> ::= V <L><CT_Tail>
                op1 = sas.pop(0)
                op2 = sas.pop(0)
                if isinstance(op1, bool) and isinstance(op2, bool):
                    result = op1 or op2
                    sas.insert(0, result)
                else:
                    sas.insert(0, "E")
                if lex in 'V^->.;)': #selection set of <CT_Tail>
                    if CT_Tail():
                        return True
                    else: return False
                else: print("Error: Expected 'V', '^', '->', '.', ';', or ')' but got '"+lex+"'"); return False # not in selection set of <CT_Tail>
            else: return False
        else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False # not in selection set of <L>
    elif lex =="^": #<CT_Tail> ::= ^ <L><CT_Tail>
        lex = getNext()
        if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <L>
            if L():
                #semantics for <CT_Tail> ::= ^ <L><CT_Tail>
                op1 = sas.pop(0)
                op2 = sas.pop(0)
                if isinstance(op1, bool) and isinstance(op2, bool):
                    result = op1 and op2
                    sas.insert(0, result)
                else:
                    sas.insert(0, "E")
                if lex in 'V^->.;)': #selection set of <CT_Tail>
                    if CT_Tail():
                        return True
                    else: return False
                else: print("Error: Expected 'V', '^', '->', '.', ';', or ')' but got '"+lex+"'"); return False # not in selection set of <CT_Tail>
            else: return False
        else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False # not in selection set of <L>
    else: #<CT_Tail> ::= {empty}
        return True

#<L> ::= <A>
#<L> ::= ~<L>
def L():
    global lex
    global sas
    if lex in 'TFabcdefghijklmnopqrstuvwxyz(': #Selection set of <A>
        if A(): 
            return True #Don't need to do any semantic operations
        else: print("Error: expected <A>"); return False
    elif lex == "~": #<L> ::= ~<L>
        lex = getNext()
        if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <L>
            if L():
                #semantics: if (L,state) != error, then invert (L, state) else error
                if sas[0] != "E": # if the value isn't an error
                   sas[0] = not sas[0] #invert the boolean value
                return True
            else: return False
        else: print("Error: Expected '~', 'T', 'F', var, or '(' but got '"+lex+"'"); return False # not in selection set of <L>
    else: return False

#<A> ::= T
#<A> ::= F
#<A> ::= var
#<A> ::= (<IT>)
def A():
    global lex
    global sas
    global varTable
    if lex == "T": #<A> ::= T
        lex = getNext()
        sas.insert(0, True) #push T on the stack
        return True
    elif lex == "F": #<A> ::= F
        lex = getNext()
        sas.insert(0, False) #push F on the stack
        return True
    elif isVar(lex): #<A> ::= var
        #Semantics: push the value of the variable on the stack
        if lex in varTable.keys(): # if the variable is defined in the table
            sas.insert(0, varTable[lex]) #push the value of the variable onto the stack
        else:   #variable is not defined before being referenced. give an error
            print("Error: variable '"+lex+"' is undefined")
            sas.insert(0, "E") #store E on the stack for error 
        lex = getNext()
        return True
    elif lex == "(": #<A> ::= (<IT>)
        lex = getNext()
        if lex in '~TFabcdefghijklmnopqrstuvwxyz(': #selection set of <IT>
            if IT():
                if lex ==")":
                    lex = getNext()
                    return True
                else: print("Error: Expected ')' but got '"+lex+"'");return False
            else: return False
        else: print("Error: Expected char in'~TFabcdefghijklmnopqrstuvwxyz(' but got '"+lex+"'");return False
    else: return False

def main():
    myOutput = "output"
    #input boolean expression
    myInput = input("Enter a boolean expression: ")        

    #tokenize the input
    try: 
        global tokensList
        tokensList = tokenize(myInput)
        # myOutput = tokensList
    
        #Syntax anylysis, recursive descent
        global lex 
        lex = getNext()
        if B():
            print("Syntax correct")
            #Recursive descent evaluates the expression. The result is on the sas 
            if isinstance(sas[0], bool):
                myOutput = sas[0]
            else: myOutput = "Error: undefined variable was used."
        else:
            print("Syntax incorrect")
            myOutput = ""
        
        sas.clear()
    
    except Exception as error:
        myOutput = error

    return myOutput

while True:
    print(main())
