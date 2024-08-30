import json
import os


megadict = {i: {} for i in range(1, 22)}


for filename in os.listdir("CP/temp_res"):
    if filename.endswith(".txt"):
        with open("CP/temp_res/" + filename) as file:
            sol = []
            solver = ""
            instance = ""
            distance = 0
            time = 0
            for line in file.readlines():
                if line.startswith("solver"):
                    solver = line.split(":")[-1].strip()
                    continue
                if line.startswith("instance"):
                    instance = line.split(":")[-1]
                    continue
                if line.startswith("Paths"):
                    temp = line[line.find("[|") + 2 :].split(",")
                    sol.append([int(numb) for numb in temp])
                    continue
                if line.startswith(" ") and not line.endswith("|]\n"):
                    sol.append([int(numb) for numb in line[2:].split(",")])
                    continue
                if line.startswith("Max"):
                    distance = line.split("=")[-1]
                    continue
                if line.startswith("% time"):
                    time = int(float(line[1:-3].split(":")[-1]))
                    continue
            megadict[int(instance)][solver] = {
                "time": time if time <= 300 else 300,
                "optimal": True if time < 300 else False,
                "obj": int(distance),
                "sol": sol if len(sol) > 0 else "UNKNOW",
            }

for keys in megadict.keys():
    with open("res/CP/" + str(keys) + ".json", "w") as file:
        json.dump(megadict[keys], file)
