#CDMO Project

This is a project realized for the exam of "Combinatorial Decision Making and Optimization".
The member of the group are:

1 - Alberto genovese
2 - Alessandro Tutone
3 - Elia Ceccolini

#Building the project

The project can be run through Docker, first download all the file of the project, than run the docker file in the directory with the comand:

```
docker compose up --build
```

Then run the container with :
```
docker run -it cdmo-app
```

After that you will be in the shell of the container.

#Running the project

After you enter the shell enter the comand

```
./runer.sh
```

After that you will enter a prompt sccript that will guide you through the running of the various instances for the various model.

MIP and SAT model will automatically create the json file , while CP, after running the istance, you will need to write

```
CP_to_json
```

in the shell program to run the script that will convert the CP result in the json.
