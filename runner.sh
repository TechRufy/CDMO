
#!/bin/bash
while :  
do
    echo "This is the project of CDMO, to run all the istances for all the models input \"all\" \n"
    echo "To run a specific model input the name of it \" CP, MIP,SAT\" "
    read -p " " input 



    if [ "$input" = "all" ];
    then
        for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
        do
            minizinc --solver gecode ./CP/cp.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000
        done
        python3 ./MIP/main.py
    fi

    if [ "$input" = "CP" ];
    then
        echo "to run all the istances for CP input \"all\" or the exact instance you want e.g \"01\" \n"
        read -p " " input 
        
        if [ "$input" = "all" ];
        then
            for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
            do
                minizinc --solver gecode ./CP/cp.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000
            done
        else
            minizinc --solver gecode ./CP/cp.mzn ./CP/Instances/inst$input.dzn --solver-time-limit 300000
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



