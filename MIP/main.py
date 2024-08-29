from MIP import Courier_problem
while True:
    Input = input("select your instance: input \" all \" to run all the available instances or \" exit \" to terminate the program\n")
    if Input == "all":
        istanze_function = (["MIP/instance/inst0" + str(i) + ".dat" for i in range(1, 10)] +
                            ["MIP/instance/inst" + str(i) + ".dat" for i in [10, 13]])
        for istanza in istanze_function:
            Courier_problem(istanza)
            input("press enter for next instances\n")
        break

    if Input == "exit":
        break

    istanze_function = [str(i) for i in range(1, 11)] + ["13"]

    if Input not in istanze_function:
        print("instance not valid")
        continue
    else:
        istanza = "MIP/instance/inst" + ("0" if int(Input) < 10 else "") + Input + ".dat"
        Courier_problem(istanza)

