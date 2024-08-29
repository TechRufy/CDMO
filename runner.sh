
#!/bin/bash
while :  
do
    echo "This is the project of CDMO, to run all the istances for all the models input \"all\""
    echo "To run a specific model input the name of it \" CP, MIP,SAT\" "
    read -p " " input 

    if [ "$input" = "all" ];
    then
        echo "CP instances with Gecode"
        echo " "

        for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
        do
            echo "instance number $i"
            echo " "
            minizinc --solver gecode ./CP/cp_gecode.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time --json-stream >> "CP/temp_res/res_$i.json"
        done

        echo "CP instances with chuffed"

        for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
        do
            echo "instance number $i"
            echo " "
            minizinc --solver chuffed ./CP/cp_chuffed.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time --json-stream >> "CP/temp_res/res_$i.json"

        done

        echo "MIP instances"

        python3 ./MIP/main.py
    fi

    if [ "$input" = "CP" ];
    then
        echo "to run all the istances for CP input \"all\" or the exact instance you want e.g \"01\" \n"
        read -p " " input 
        

        if [ "$input" = "all" ];
        then
            echo "which solver ? chuffed or gecode \n"
            read -p " " solver

            for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
            do
                echo "instance number $i"
                echo " "
                minizinc --solver $solver ./CP/cp_$solver.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time --json-stream >> "CP/temp_res/res_$i.json"
            done
        else
            echo "which solver ? chuffed or gecode \n"
            read -p " " solver

            minizinc --solver $solver ./CP/cp_$solver.mzn ./CP/Instances/inst$input.dzn --solver-time-limit 300000  --output-time --json-stream >> "CP/temp_res/res_$i.json"
        fi


    fi

    if [ "$input" = "MIP" ];
    then
        python3 ./MIP/main.py
    fi

    if [ "$input" = "SAT" ];
    then
        echo not implemented, sorry UwU
    fi

done



