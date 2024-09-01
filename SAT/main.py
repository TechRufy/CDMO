from SAT import SAT_courier

while True:
    Input = input(
        'select your instance e.g "01", input " all " to run all the available instances or " exit " to terminate the program\n'
    )
    if Input == "all":
        istanze_function = [
            "MIP/instance/inst0" + str(i) + ".dat" for i in range(1, 10)
        ] + ["MIP/instance/inst" + str(i) + ".dat" for i in [10, 13]]

        for encoding in ["np", "bw", "seq"]:
            for istanza in istanze_function:
                SAT_courier(istanza, encoding)

        break

    if Input == "exit":
        break

    istanze_function = ["0" + str(i) for i in range(1, 10)] + ["13", "10"]

    if Input not in istanze_function:
        print("instance not valid")
        continue
    else:
        istanza = "MIP/instance/inst" + Input + ".dat"
        encoding = input(
            "select wich encoding between: naive = np , bitwise = bw, sequential = seq \n"
        )
        SAT_courier(istanza, encoding)
