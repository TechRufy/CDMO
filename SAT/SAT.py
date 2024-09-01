# imports
import json
import time
from z3 import *
from itertools import combinations
from math import ceil


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


def sol_to_json(solver, solution, istance, time, distance):

    if time >= 300:
        optimal = False
    else:
        optimal = True

    diz = {
        solver: {
            "time": int(time),
            "optimal": optimal,
            "obj": distance,
            "sol": solution,
        }
    }

    print(os.listdir("res/SAT"))

    if os.listdir("res/SAT").__contains__(str(int(istance.strip())) + ".json"):
        with open("res/SAT/" + str(int(istance.strip())) + ".json", "r+") as outfile:
            dic = json.load(outfile)
            dic[solver] = {
                "time": int(time),
                "optimal": optimal,
                "obj": distance,
                "sol": solution,
            }
            outfile.seek(0)
            json.dump(dic, outfile)
        print(f"\n result added successfully")
    else:
        with open("res/SAT/" + str(int(istance.strip())) + ".json", "w") as outfile:
            json.dump(diz, outfile)
            name = istance + ".json"
            print(f"\nJSON file {name} created successfully")

    pass


# ENCODINGS
# naive encoding
def at_least_one_np(bool_vars):
    return Or(bool_vars)


def at_most_one_np(bool_vars, name=""):
    return [Not(And(pair[0], pair[1])) for pair in combinations(bool_vars, 2)]


def exactly_one_np(bool_vars, name=""):
    return at_most_one_np(bool_vars) + [at_least_one_np(bool_vars)]


# sequential encoding
def at_least_one_seq(bool_vars):
    return at_least_one_np(bool_vars)


def at_most_one_seq(bool_vars, name):
    constraints = []
    n = len(bool_vars)
    s = [
        Bool(f"s_{name}_{i}") for i in range(n - 1)
    ]  # the trick to distinguish variables is using index numbers
    constraints.append(Or(Not(bool_vars[0]), s[0]))  # implication
    constraints.append(Or(Not(bool_vars[n - 1]), Not(s[n - 2])))  # s has length n-1
    for i in range(1, n - 1):
        constraints.append(Or(Not(bool_vars[i]), s[i]))
        constraints.append(Or(Not(bool_vars[i]), Not(s[i - 1])))
        constraints.append(Or(Not(s[i - 1]), s[i]))
    return And(constraints)  # CNF


def exactly_one_seq(bool_vars, name):
    return And(at_least_one_seq(bool_vars), at_most_one_seq(bool_vars, name))


# bitwise encoding
def toBinary(num, length=None):
    num_bin = bin(num).split("b")[-1]
    if length:
        return "0" * (length - len(num_bin)) + num_bin
    return num_bin


def at_least_one_bw(bool_vars):
    return at_least_one_np(bool_vars)


def at_most_one_bw(bool_vars, name):
    constraints = []
    n = len(bool_vars)
    m = math.ceil(math.log2(n))
    r = [Bool(f"r_{name}_{i}") for i in range(m)]
    binaries = [toBinary(i, m) for i in range(n)]
    for i in range(n):
        for j in range(m):
            phi = Not(r[j])
            if binaries[i][j] == "1":
                phi = r[j]
            constraints.append(Or(Not(bool_vars[i]), phi))
    return And(constraints)


def exactly_one_bw(bool_vars, name):
    return And(at_least_one_bw(bool_vars), at_most_one_bw(bool_vars, name))


# heule encoding
def at_least_one_he(bool_vars):
    return at_least_one_np(bool_vars)


def at_most_one_he(bool_vars, name):
    if len(bool_vars) <= 4:
        return And(at_most_one_np(bool_vars))
    y = Bool(f"y_{name}")
    return And(
        And(at_most_one_np(bool_vars[:3] + [y])),
        And(at_most_one_he(bool_vars[3:] + [Not(y)], name + "_")),
    )


def exactly_one_he(bool_vars, name):
    return And(at_most_one_he(bool_vars, name), at_least_one_he(bool_vars))


def symMax(l):
    m = l[0]
    for v in l[1:]:
        m = If(v > m, v, m)
    return m


# import instances
def import_instance(path):
    with open(path, "r") as f:
        lines = f.readlines()

        m = int(lines[0].strip())
        n = int(lines[1].strip())
        l = [int(x) for x in lines[2].strip().split()]
        s = [int(x) for x in lines[3].strip().split()]

        dist_data = [line.strip().split() for line in lines][4:]
        D = [[int(x) for x in row] for row in dist_data]
    return m, n, l, s, D


def multiple_couriers_problem_sat(m, n, l, s, D, encoding):
    # choice of an encoding
    if encoding == "np":
        exactly_one = exactly_one_np
        at_least_one = at_least_one_np
        at_most_one = at_most_one_np
    elif encoding == "bw":
        exactly_one = exactly_one_bw
        at_least_one = at_least_one_bw
        at_most_one = at_most_one_bw
    elif encoding == "seq":
        exactly_one = exactly_one_seq
        at_least_one = at_least_one_seq
        at_most_one = at_most_one_seq

    # three-dimensional array to keep trace of courier paths - Arc from j to k is travelled by courier i
    arcs = [[Bool(f"arcs_{j}_{k}") for k in range(n + 1)] for j in range(n + 1)]
    # matrix to keep track of the ordering of the items
    b = [[Bool(f"b_{j}_{i}") for i in range(m)] for j in range(n)]

    c = [[Int(f"c_{j}_{i}") for i in range(m)] for j in range(n + 1)]

    # definition of the solver
    opt = Optimize()
    opt.set("timeout", 300000)

    # channeling b and arcs
    for j in range(n):
        for k in range(n):
            opt.add(
                Implies(
                    arcs[j][k],
                    And(
                        exactly_one([And(b[j][i], b[k][i]) for i in range(m)], f"a_{j}")
                    ),
                )
            )

    for j in range(n):
        for i in range(m):
            opt.add(Implies(b[j][i], at_least_one([arcs[j][k] for k in range(n + 1)])))

    # computation of the distance for each courier
    d = [
        Sum(
            [
                If(And(arcs[j][k], b[j][i]), D[j][k], 0)
                for j in range(n)
                for k in range(n + 1)
            ]
        )
        for i in range(m)
    ]

    for i in range(m):
        for j in range(n):
            d[i] += If(And(b[j][i], arcs[n][j]), D[n][j], 0)

    # ensure that there is only one edge starting from an item
    for j in range(n):
        opt.add(
            And(
                exactly_one(
                    [And(arcs[j][k], b[j][i]) for k in range(n + 1) for i in range(m)],
                    f"c_{j}",
                )
            )
        )

    # ensure that there is only one edge going in an item
    for j in range(n):
        opt.add(
            And(
                exactly_one(
                    [And(arcs[k][j], b[j][i]) for k in range(n + 1) for i in range(m)],
                    f"d_{j}",
                )
            )
        )

    # ensure that each courier start only one time from the origin
    for i in range(m):
        opt.add(
            And(exactly_one([And(arcs[n][j], b[j][i]) for j in range(n)], f"e_{i}"))
        )

    # ensure that each courier ends only one time in the origin
    for i in range(m):
        opt.add(
            And(exactly_one([And(arcs[j][n], b[j][i]) for j in range(n)], f"f_{i}"))
        )

    # no arc between the same item
    for i in range(n + 1):
        opt.add(Not(Or(arcs[i][i])))

    # ensure that the item are below the load limit
    for i in range(m):
        opt.add(Sum([s[j] * b[j][i] for j in range(n)]) <= l[i])

    # ensures that paths are connected
    for i in range(m):
        for k in range(n + 1):
            for j in range(n):
                if k != j:
                    if k == n:
                        # opt.add(Implies(arcs[k][j][i],at_least_one([arcs[j][h][i] for h in range(n+1) if h != j])))
                        opt.add(
                            Implies(
                                And(arcs[k][j], b[j][i]),
                                at_least_one(
                                    [arcs[j][h] for h in range(n + 1) if h != j]
                                ),
                            )
                        )
                    else:
                        opt.add(
                            Implies(
                                And(arcs[k][j], b[j][i]),
                                at_least_one(
                                    [
                                        arcs[j][h]
                                        for h in range(n + 1)
                                        if h != j and h != k
                                    ]
                                ),
                            )
                        )

    # subtour elimination
    for i in range(m):
        for j in range(n):
            for k in range(n):
                if j != k:
                    opt.add(Implies(arcs[j][k], c[j][i] < c[k][i]))

    # minimizing the objctive function
    max_d = Int("max_d")
    max_d = symMax(d)

    opt.minimize(max_d)

    if opt.check() != unsat:
        return opt.model()
    else:
        return "unsat"


def SAT_courier(istance, encoding):
    # import of the instance
    m, n, l, s, D = import_instance(istance)

    # solve the problem
    start_time = time.time()

    model = multiple_couriers_problem_sat(m, n, l, s, D, encoding)

    elapsed_time = time.time() - start_time

    if model != "unsat":
        solution = sorted(
            [(str(i), model[i]) for i in model], key=lambda x: str(x[0][-1])
        )
        sol_arcs = [
            solution[i][0]
            for i in range(len(solution))
            if solution[i][0].startswith(f"arcs_") and solution[i][1]
        ]
        sol_b = [
            [
                solution[i][0]
                for i in range(len(solution))
                if solution[i][0].startswith(f"b_")
                and solution[i][1]
                and solution[i][0].endswith(f"{j}")
            ]
            for j in range(m)
        ]

        sol = []
        for i in range(m):
            sol_courier = []
            for elem1 in sol_b[i]:
                for elem2 in sol_arcs:
                    if (
                        elem1.split("_")[1] == elem2.split("_")[1]
                        or elem1.split("_")[1] == elem2.split("_")[2]
                    ) and elem2 not in sol_courier:
                        sol_courier.append(elem2)
            sol.append(sol_courier)

        paths = []
        for i in range(m):
            courier_path = []
            next = n
            while sol[i]:
                if int(sol[i][0].split("_")[1]) == next:
                    courier_path.append(sol[i][0])
                    next = int(sol[i][0].split("_")[2])
                    sol[i] = sol[i][1:]
                else:
                    sol[i].append(sol[i][0])
                    sol[i] = sol[i][1:]
            paths.append(courier_path)

        d = [0 for i in range(m)]
        for i in range(m):
            for j in range(len(paths[i])):
                d[i] += D[int(paths[i][j].split("_")[1])][
                    int(paths[i][j].split("_")[2])
                ]

        print(max(d))

        sol = [
            [
                (int(element.split("_")[-2]), int(element.split("_")[-1]))
                for element in lista
            ]
            for lista in paths
        ]

        sol_to_json(
            "SAT_" + encoding,
            ordinamento(sol),
            istance[17:19],
            elapsed_time,
            max(d),
        )

        return

    else:
        print("unsat")
