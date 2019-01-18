import pandas as pd
constants={'⊤':1,'⊥':0}


"""
This program creates the truth tables for a well formed formula and verifies
the equivalence of the formula.
Example of such an equation : (P∧Q) ≡ (P∨Q)

To create the truth table I used the pandas library and I had to create
a dictionary that has as keys the head of the tables and as values a list
with the values I want to display on that column
Ecample: For (P∧Q) ≡ (P∨Q) we have the dictionary:
            {
            'P': [0, 1, 0, 1],
            'Q': [0, 0, 1, 1],
            '(P∧Q)': [0, 0, 0, 1],
            '(P∨Q)': [0, 1, 1, 1]
            }

For an easier writing of the formulas I took the folowing symbols from the keyboard as:
 '&' = '∧'
 '|' = '∨'
 '!' = '¬'
 '-' = '⇒'
 '=' = '⇔'
but the origina symblos still can be used
"""

#============================================================CHECKING AND STUFF============================================
"""
This function deletes the spaces betwen the elements of a proposition
Exemple: "(P∧    Q)   ≡ (P  ∨Q)" will become "(P∧Q)≡(P∨Q)"

"""
def delete_spaces(l):
    n=len(l)
    i=0
    while i<n:
        if l[i]==' ':
            l=l[:i]+l[i+1:]
            i-=1
            n-=1
        i+=1
    return l

#============================================================TABLE AND THINGS==============================================

"""
This function adds a new value to the table
Head is the name of the column(the key of the dict)
Resul is the value that is going to be add
lv is the level, this helps so that it doesn't add
the same thing two times
"""
def add_result(table,head,result,lv):
    if head in table.keys():
        if len(table[head]) < lv:
            table[head].append(result)
    else:
        table[head]=[result]
    return table
        


#============================================================CREATING THE VALUES==============================================
"""
This function detects the atoms from the equation l
!!!I assumed that all the atoms are only one big letter!!!
"""

def detect_formulas(l): #detects the letter Q P R etc...
    atoms=dict()
    for i in l:
        if i.isalpha():
            atoms[i]=0
    return atoms


"""
This function creates all the possibilites of values a atom can take.
To create this I used the binary representation of a number instead of
backtracking.
X is the 2**(number of atoms)

Example for 3 atoms
we will have the list:
[
[0, 0, 0],
[1, 0, 0],
[0, 1, 0],
[1, 1, 0],
[0, 0, 1],
[1, 0, 1],
[0, 1, 1],
[1, 1, 1]
]
"""
def create_values(x):
    values = list()
    i=0
    max=list(bin(x))[2:] #I use this to know the length of the list
                         #becouse for example 2 in banary is 10
                         #but I need to fill the rest of the spaces with 0
                         #so the list will look [0,0,0] (for 3 atoms)
    while i<x:
        b=bin(i)
        b=b[2:] 
        b=list(map(int,b))  #convert str to int
        b=b[::-1]
        while len(b) < len(max)-1: #fills with 0 the rest of the space
            b.append(0)
        values.append(b)
        i+=1
    return values


"""
This function copyes the elements from a list a to the
values of a ductionary atoms

I used this function to copy the values from the matrix with all
the possibilities to the dict atoms, where I memoriezed
the value for each atom
"""
def copy_values(atoms,a):  
    i=0
    for key in atoms.keys(): 
            atoms[key]=a[i]
            i+=1
    return atoms
    



#+==============================================================LOGICAL PART==================================================


"""
This function gets the connector for the first pair of parentheses
For example for (P∧Q) will return the index of ∧ (2)
This function uses parantheses to detect the connector that is
why is very important that the proposition is written correct
"""
def predominant(l):     # Gets the predominant sign of the eq
    b=0
    for i in range(len(l)):
        if l[i] == '(':
            b+=1
            continue
        if l[i]== ')':
            b-=1
            continue
        if not(l[i].isalpha()) and l[i]!=' ' and b==1:
            return i


"""
This is a function with returns the result
of each logical connector for truth values A and B
"""
def determine_value(A,cn,B=None): #does the logical equation between A and B
    if cn=='!' or cn=='¬': #not
        return not A
    if cn=='&' or cn=='∧': #and
        return A and B
    if cn=='|' or cn=='∨': #or
        return A or B
    if cn == '=' or cn=='⇔':  #<=>
        return A==B
    if cn == '-' or cn=='⇒': #=>
        if A==1 and B==0:
            return False
        return True


"""
This is the function that check each proposition. Every time
this function gets a formula will try to "break" it such that will
get an atom  that is memorized in the atoms dictionary

I think is easier to explain this on an example:
check((A&(B|C))) will first detect the connector & and will
call the function for the left side and the right side of it.
So now we have:
check(A) that will detect it is an atom and returns its value
check((B|C)) that will detect the connector | and call :
check(B) that will give the value of B
check(C) that will give the value of C

As it is going up in the 'tree' the program will execute the
equation for each connector

I am sorry that my comments may not be the best but I hope
the concept is not that hard to understand.
"""
def check(l,table,constants,atoms,lv):
    if l[0]=='(':                                                   #checks if there si another formula or just an atom
        pred=predominant(l)                                         #gets the connector
        if l[pred]=='!' or l[pred]=='¬':                            #id the connector is not we have a special case with only one value
            B=None
            A=check(l[pred+1:-1],table,constants,atoms,lv)
            
        else:                                                       #the general case with (P cn Q) where P,Q atoms and cn any connector besides of not
            A=check(l[1:pred],table,constants,atoms,lv)
            B=check(l[pred+1:-1],table,constants,atoms,lv)   
        result=determine_value(A,l[pred],B)                         #the logical result between the left side and right side of the connector 
        head=l
        add_result(table,head,result,lv)                            #adds the result to the table 
        return result
    
    if l[0] in constants.keys():                                    #search if the lement is an constant '⊤' or '⊥'
        add_result(table,l[0],constants[l[0]],lv)
        return constants[l[0]]
    add_result(table,l[0],atoms[l[0]],lv)                      #gets the elemt from the atoms dictionary where the values of the atoms are 
    return atoms[l[0]]


#--------------------------------------------------------------------------------------------
try:
    l=input()                                       
    l=delete_spaces(l) #deletes the spaces between the elemts  
    ok=1               # this will tell if the equation is equivalent or not 
    table=dict()
    atoms=detect_formulas(l)   #gets the names of the atoms 
    values=create_values(2**len(atoms)) #creates all the possibilities 
    l=l.split("≡")          #split all the equation in 2 wffs
    result_first=0              
    result_second=0
    step=0                  #index used to know the 'level' in the table 
    while step < 2**len(atoms):
        atoms=copy_values(atoms,values[step]) #gets a new set of values for the atoms
        result_first=check(l[0],table,constants,atoms,step+1) #gets the result from the left side
        result_secound=check(l[1],table,constants,atoms,step+1) #gets the result from the right side
        if result_first != result_secound:                      #if the results are different it stops 
            ok=0
        step+=1

    if ok==0:                                               
        print("The expressions are not equivalent!!!")
    else:
        print("The expressions are equivalent!!!")
        
    
except:
    print("Invalid syntax")

    
new_dataframe2 = pd.DataFrame(    #draws the table 
        table
    )

new_dataframe2





    
