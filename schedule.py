import re

# intersection of 2 lists
def intersection(A, N):
    return [value for value in A if value in N]

# difference of 2 lists
def difference(A, N):
    return [value for value in A if value not in N]

# Bron-kerbosch algorithm with pivoting as a generator
def BronKerbosch(R, P, X, E):
    # base case: If P and X are empty then R is a maximal clique
    if not any((P, X)):
        yield R
    else:
        # choose the pivot vertex from P U X
        u = (P+X)[0]
        # iterating through u and its non-neighbors
        M = difference(P, E[u])
        for v in M:
            # vertices adjacent to v
            N = E[v]
            # explore the neighborhood of v for maximal cliques
            A = R + [v]
            B = intersection(P, N)
            C = intersection(X, N)
            yield from BronKerbosch(A, B, C, E)
            # transfer v from the candidate set P to the excluded set X
            P.remove(v)
            X.append(v)

# convert the time string to minutes after midnight
def get_time(time_string):
    hour, minute = time_string.split(':')
    return int(hour)*60 + int(minute)

# check if two classes have any conflict
def compatible(A, B):
    # if they are the same class type then they conflict
    if A[0]==B[0]:
        return False
    # if neither of the days of one class are equal either of the days of the other class then they don't conflict
    if not(A[1]==B[1] or A[1]==B[2] or A[2]==B[1] or (A[2]==B[2] and A[2]!="N")):
        return True
    # numerically compare the start and end times of both classes for compatibility
    startA = get_time(A[3])
    endA = get_time(A[4])
    startB = get_time(B[3])
    endB = get_time(B[4])
    return (startA < startB or startA > endB) and (endA < startB or endA > endB)

# creates a list of the index compatible elements for every element of V
def edge_generator(V):
    return [[j for j, v2 in enumerate(V) if compatible(v1, v2)] for v1 in V]

if __name__ == '__main__':
    # read the list of classes from a editable txt file and save it in V
    V = []
    with open('classes.txt') as f:
        for line in f:
            datum = []
            # Split each line using space and dash as delimiters
            values = re.split(r'[-\s]+', line)
            # Class type
            datum.append(values[0])
            # Class day schedule
            if len(values[1])==1:
                datum.append(values[1])
                datum.append("N")
            else:
                datum.append(values[1][0])
                datum.append(values[1][1])
            # Class time schedule
            datum.append(values[2])
            datum.append(values[3])
            V.append(datum)
    
    # counter for number of possible schedules
    n = 1
    # for loop to yield from generator
    # Bron-Kerbosch algorithm initialized with the vertice set and the edge set of V
    # represented as counting numbers
    for l in BronKerbosch([], list(range(len(V))), [], edge_generator(V)):
         # Assuming student needs to take all class types       
         if len(l)==len({v[0] for v in V}):
            # listing the classes chosen for proposed schedule n
            print("Schedule " + str(n) + ":")
            for i in l:
                # reconstructing the string from the list describing the chosen class
                if V[i][2]=="N":
                    print(V[i][0] + " " + V[i][1] + " " + V[i][3] + "-" + V[i][4])
                else:
                    print(V[i][0] + " " + V[i][1] + V[i][2] + " " + V[i][3] + "-" + V[i][4])
            print("")
            n = n+1