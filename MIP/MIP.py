from functools import cmp_to_key

from pulp import *


def ordinamento(l: list):
    copia = l.copy()
    for i in range(len(copia)):
        copia[i].sort(reverse=True)
        for j in range(len(copia[i]) - 1):
            for k in range(j + 2, len(copia[i])):
                if copia[i][j][1] != copia[i][j + 1][0]:
                    copia[i][j + 1], copia[i][k] = copia[i][k], copia[i][j + 1]
    copia = [[lista[i][1] + 1 for i in range(len(lista) - 1)] for lista in copia]
    return copia


# import of an instance
def import_instance(path):
    with open(path, 'r') as f:
        lines = f.readlines()

        m = int(lines[0].strip())
        n = int(lines[1].strip())
        l = [int(x) for x in lines[2].strip().split()]
        s = [int(x) for x in lines[3].strip().split()]

        dist_data = [line.strip().split() for line in lines][4:]
        D = [[int(x) for x in row] for row in dist_data]
    return m, n, l, s, D


# Define problem parameters

def Courier_problem(istanza):
    m, n, l, s, D = import_instance(istanza)

    # Create decision variables
    choices = LpVariable.dicts("choices", (range(n + 1), range(n + 1), range(m)), cat=LpBinary, lowBound=0)
    longest = LpVariable("longest", lowBound=0, cat=LpInteger)
    c = LpVariable.dicts("c", (range(n + 1), range(m)), lowBound=0, upBound=n, cat=LpInteger)
    # Create problem instance
    prob = LpProblem("MCP", LpMinimize)

    # objective function
    prob += longest

    # ensure that longest is the max of all the distance
    d = [lpSum([D[i][j] * choices[i][j][k] for i in range(n + 1) for j in range(n + 1)]) for k in range(m)]

    # ensure that longest is the maximum of the distance
    for k in range(m):
        prob += longest >= d[k]

    # ensure that there is only one edge starting from an item by limiting to 1 the number of 1 in a rows
    for i in range(n):
        prob += lpSum([choices[i][j] for j in range(n + 1) if i != j]) == 1

    # ensure that there is only one edge going in an item by limiting to 1 the number of 1 in a columns
    for i in range(n):
        prob += lpSum([choices[j][i] for j in range(n + 1) if i != j]) == 1

    # ensure that each courier start only one time from the origin
    for k in range(m):
        prob += lpSum([choices[n][j][k] for j in range(n)]) == 1

    # ensure that each courier ends only one time in the origin
    for k in range(m):
        prob += lpSum([choices[j][n][k] for j in range(n)]) == 1

    # no arc between the same item
    for i in range(n + 1):
        prob += lpSum(choices[i][i]) == 0

    # Ensures that paths are connected
    for k in range(m):
        for i in range(n + 1):
            for j in range(n):
                if i != j:
                    if i == n:
                        prob += choices[i][j][k] <= lpSum([choices[j][h][k] for h in range(n + 1) if h != j])
                    else:
                        prob += choices[i][j][k] <= lpSum([choices[j][h][k] for h in range(n + 1) if h != j and h != i])

    # ensure that the item are below the load limit
    for k in range(m):
        prob += lpSum([s[i] * choices[i][j][k] for i in range(n) for j in range(n + 1)]) <= l[k]

    # subtour elimination
    for k in range(m):
        for i in range(n):
            for j in range(n):
                if i != j:
                    prob += c[i][k] + choices[i][j][k] <= c[j][k] + (n - 1) * (1 - choices[i][j][k])

    time_limit_in_seconds = 60 * 5

    prob.solve(PULP_CBC_CMD(msg=True, timeLimit=time_limit_in_seconds))

    # Solve the problem

    solution = [[] for i in range(m)]

    # Print the solution
    for k in range(m):
        for i in range(n + 1):
            for j in range(n + 1):
                if choices[i][j][k].varValue > 0:
                    solution[k].append((i, j))
                else:
                    pass
    print("instance number : ", istanza[18:20])
    print(LpStatus[prob.status])
    print("Optimal Solution: ", ordinamento(solution))
    print("Total distance:", value(prob.objective))
