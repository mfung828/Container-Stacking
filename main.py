'''
All Methods will be placed here. No need for classes.


'''

start=[[1,3,6],[2,4,5]]
end=[[1,2,5],[4,3,6]]
sampleA=[[1,0,0],[2,3,5]]
sampleB=[[0,0,0],[0,4,6]]




'''
Heuristic function immediately starts picking any container in the beginning configuration
and loads it into the ending configuration. This works despite being "greedy" because that touch is a minimal one touch 
by the crane. When there are no feasible/remaining containers at that stage (without reconfiguring), then
the algorithm looks at the dynamic programming tables that make use of the Bellman equation. 
If the dynamic programming tables have not been made yet, then only then will it start to make them.

By default, the algorithm will use the heuristic of grabbing whatever is feasible. Only with a "stuck"
situation will the algorithm then use dynamic programming. This is to save time from all the calculations
and looking up of policy. 

For notation purposes, we have the following:

1) startConfiguration- the configuration in matrix form at the very beginning of the problem. IMMUTABLE. 
2) configurationA- any of the configurations that the startConfiguration becomes. Ultimately becomes a zero matrix.
3) goalConfiguration- the end configuration. IMMUTABLE. 
4) configurationB- any of the configurations that the goalConfiguration becomes. Ultimately becomes the 
    goalConfiguration matrix.
'''
def heuristic(startConfiguration,goalConfiguration):

    #Instantiate the initial ConfigurationA and ConfigurationB matrices.
    configurationA = createConfiguration(startConfiguration,False)
    configurationB = createConfiguration(startConfiguration, True)
    history = ["Start Process"]
    score = 0

    # While there is still some container to put towards the goal, implement the algorithm.
    while (countContainers(configurationA)!=0):

        #Comb through configurationA to see if there are any containers ready to be grabbed immediately.
        vector = feasibleVector(configurationA,configurationB,goalConfiguration)
        print(vector)

        #What to do if there is a feasible container
        if (findTrueInVector(vector,False)):

            #Identify the row and column of where that container is in configurationA.
            locationColumn = findTrueInVector(vector,True)
            locationRow = findRow(locationColumn,configurationA)

            # add to history and score.
            addToHistory(configurationA[locationRow][locationColumn], history)
            score += 1

            #Alters the configurations.
            if (locationColumn<len(vector)/2):
                alterConfigurations(configurationA[locationRow][locationColumn],
                                configurationA,configurationB,goalConfiguration)
            else:
                alterConfigurations(configurationB[locationRow][locationColumn-(len(vector)/2)],
                                    configurationB, configurationB, goalConfiguration)

            print("Remaining containers left:" + str(countContainers(configurationA)))
            printConfiguration(configurationA)
            printConfiguration(configurationB)


        #What to do if there is no feasible container. ie look in dynamic programming tables, if already made.
        #else:


    return [history,score]


'''
Given a number k and configuration dimensions, width and length, 
return a list of possible arrangements of containers that are ALREADY STACKED. 
'''
def generateSubsets(k, width, length):

    numberContainers = width*length

    arrayContainers = []

    sampleArrangement=[0]*k
    #if k is less than or equal to width, then we can use for loops
    #to generate the possible combinations. Else, it's just 1,2,3...k for top row.
    if (k<=width):

    else:
        sampleArrangement=list(range(1,(width+1)))




    return True






'''
Given a configuration and a single container location, x, an element of [1,INF),
returns a tuple that describes the x and y of the container location.
'''
def containerPosition(configuration, position):

    widthConfiguration = len(configuration[0])

    x= (position %widthConfiguration)-1
    y= position//widthConfiguration

    return [x,y]

'''
Given n and k, return n choose k.
'''
def nChoosek(n,k):

    counter = 1
    for i in range(n,n-k,-1):
        counter*=i

    for j in range(k,0,-1):
        counter/=j

    return counter


'''
Looks in the COLUMN of configuration and returns the row of the first non-empty.
Returns -1 if all is empty. 
'''
def findRow(column,configuration):

    for i in range(len(configuration)):
        if configuration[i][column]!=0:
            return i

    return -1

'''
Takes both configurationA/configurationB and configurationB by reference and alters them
such that the container (named value) is taken from A/B, to be replaced by 0, and added to B in its proper B spot. 
'''
def alterConfigurations(value,configurationA,configurationB,goalConfiguration):

    #Location of where to place the value.
    locationB = findValue(value, goalConfiguration)
    rowLocationB = locationB[0]
    columnLocationB = locationB[1]

    # Location of where to remove the value.
    locationA= findValue(value, configurationA)
    rowLocationA = locationA[0]
    columnLocationA = locationA[1]

    configurationB[rowLocationB][columnLocationB] = value  # update configuration B
    configurationA[rowLocationA][columnLocationA] = 0  # update configuration A


'''
Adds what happened to the history/ policy array
'''
def addToHistory(value,historyArray):

    historyArray.append(str(value) + " moved to Configuration B heuristically.")



'''
Takes two matrix configurations and compares them to see if they are the same. 
At the sight of a discrepancy, it immediately terminates and returns False. 
Otherwise, returns True. 
'''
def compareConfigurations(configurationA,configurationB):

    configurationLength = len(configurationA)
    configurationWidth = len(configurationA[0])

    for i in range(0, configurationLength):
        for j in range(0, configurationWidth):
            if configurationA[i][j]!=configurationB[i][j]:
                return False

    return True


'''
Creates a matrix the same size as the starting or ending matrix. 
If empty is True, then the resulting matrix is one of zeros. Otherwise, it takes the configuration
given and copies it. 
Tested
'''
def createConfiguration(configuration,empty):

    configurationLength = len(configuration)
    configurationWidth = len(configuration[0])
    newMatrix = [0]*configurationLength

    for i in range(configurationLength):
        newMatrix[i] = [0]* configurationWidth

    if empty:
        return newMatrix
    else:

        for i in range(0, configurationLength):
            for j in range(0, configurationWidth):
                newMatrix[i][j]= configuration[i][j]

        return newMatrix

'''
Given a configuration in matrix form, it counts the number of containers inside and returns the total.
Tested.
'''
def countContainers(configuration):

    configurationLength=len(configuration)
    configurationWidth= len(configuration[0])
    counter=0

    for i in range(0, configurationLength):
        for j in range(0, configurationWidth):
            if (configuration[i][j]!=0):
                counter+=1

    return counter

'''
Sub function that finds a specific value in a matrix configuration. 
Returns a vector of size: [a,b]
'''
def findValue (value,configuration):

    configurationLength = len(configuration)
    configurationWidth = len(configuration[0])

    for i in range(0, configurationLength):
        for j in range(0, configurationWidth):
            if (configuration[i][j] == value):
                return [i,j]



'''
Sub function that takes a value, looks for that value in a matrix and 
returns if it is feasible to place value in a matrix configurationB. 
Tested. 
'''
def feasibleValue (value, configurationB, goalConfiguration):

    location = findValue(value,goalConfiguration)
    rowLocation= location[0]
    columnLocation=location[1]

    if (configurationB[rowLocation][columnLocation]==value):
        return False

    if (configurationB[rowLocation][columnLocation]==0):
        if (rowLocation == len(configurationB) - 1):  # means that that container is in the bottom of a stack
            return True
        else:
            if ((configurationB[rowLocation+1][columnLocation]==goalConfiguration[rowLocation+1][columnLocation])):
                return True
            else:
                return False

    return False


'''
Function prints out the matrix in the console in a rectangular and tabular format. 
Tested.
'''
def printConfiguration(configuration):

    configurationLength = len(configuration)
    configurationWidth = len(configuration[0])
    string=""

    for i in range(0,configurationLength):
        for j in range(0, configurationWidth):
            string +=str(configuration[i][j]) + " "
        string +="\n"

    print (string)

'''
Looks at the current matrix configuration and the goal configuration. 
Then evaluates for the highest row, which container may be put directly into
place in the goal configuration. 

Returns a vector describing this. 
Tested.
'''
def feasibleVector(configurationA, configurationB, goalConfiguration):

    configurationLength = len(configurationA)
    configurationWidth = len(configurationA[0])*2
    returnVector = [False]*configurationWidth

    for i in range(0,configurationWidth):
        for j in range(0, configurationLength):

            if (i<len(configurationA[0])):
                if (configurationA[j][i]!=0):   #We start from the top and we found a non-empty spot, ie a container exists
                                                #there.

                    #Looks into the goal configuration to see if it is feasible to insert
                    if (feasibleValue(configurationA[j][i],configurationB,goalConfiguration)):
                        returnVector[i]=True    #Yes, it's feasible
                        break
                    break
            else:
                if (configurationB[j][i-len(configurationA[0])] != 0):

                    # Looks into the goal configuration to see if it is feasible to insert
                    if (feasibleValue(configurationB[j][i-len(configurationA[0])], configurationB, goalConfiguration)):
                        returnVector[i] = True  # Yes, it's feasible
                        break
                    break

    return returnVector

'''
Takes a 1D vector. If location is True, then it spits out an index of the first True. Otherwise, spits out
True if there is a True inside the vector. 
Tested.
'''
def findTrueInVector(vector,location):

    for i in range(len(vector)):
        if vector[i]==True:
            if location== True:
                return i
            else:
                return True

    return False

print(heuristic(start,end))
