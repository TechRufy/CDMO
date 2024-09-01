#!/bin/bash
while :  
do
    echo "This is the project of CDMO, to run all the istances for all the models input \"all\""
    echo "To run a specific model input the name of it \" CP, MIP,SAT\" "
    read -p " " input 

    if [ "$input" = "all" ];
    then
        echo "CP instances with Gecode with SB"
        echo " "

        for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
        do
            echo "instance number $i"
            echo " "

            > "CP/temp_res/res_gecode_sb_$i.txt"

            echo "model : cp_${solver}_sb.mzn" >> "CP/temp_res/res_gecode_sb_$i.txt"
            echo "solver : $solver" >> "CP/temp_res/res_gecode_sb_$i.txt"
            echo "instance : $i" >> "CP/temp_res/res_gecode_sb_$i.txt"

            echo "--solver gecode ./CP/cp_gecode_sb.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time"

            minizinc --solver gecode ./CP/cp_gecode_sb.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_gecode_sb_$i.txt"
        done

        echo "CP instances with chuffed with SB"

        for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
        do
            echo "instance number $i"
            echo " "

            > "CP/temp_res/res_chuffed_sb_$i.txt"

            echo "model : cp_$solver_sb.mzn" >> "CP/temp_res/res_chuffed_sb_$i.txt"
            echo "solver : $solver" >> "CP/temp_res/res_chuffed_sb_$i.txt"
            echo "instance : $i" >> "CP/temp_res/res_chuffed_sb_$i.txt"

            echo "--solver chuffed ./CP/cp_chuffed_sb.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time"

            minizinc --solver chuffed ./CP/cp_chuffed_sb.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_chuffed_sb_$i.txt"

        done

        echo "CP instances with Gecode without SB"

        for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
        do
            echo "instance number $i"
            echo " "

            > "CP/temp_res/res_gecode_$i.txt"

            echo "model : cp_$solver.mzn" >> "CP/temp_res/res_gecode_$i.txt"
            echo "solver : $solver" >> "CP/temp_res/res_gecode_$i.txt"
            echo "instance : $i" >> "CP/temp_res/res_gecode_$i.txt"

            echo "--solver gecode ./CP/cp_gecode.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time"

            minizinc --solver gecode ./CP/cp_gecode.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_gecode_$i.txt"

        done

        echo "CP instances with chuffed without SB"

        for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
        do
            echo "instance number $i"
            echo " "

            > "CP/temp_res/res_chuffed_$i.txt"

            echo "model : cp_$solver.mzn" >> "CP/temp_res/res_chuffed_$i.txt"
            echo "solver : $solver" >> "CP/temp_res/res_chuffed_$i.txt"
            echo "instance : $i" >> "CP/temp_res/res_chuffed_$i.txt"

            echo "--solver chuffed ./CP/cp_chuffed.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time"

            minizinc --solver chuffed ./CP/cp_chuffed.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_chuffed_$i.txt"

        done


        echo "MIP instances"

        python3 ./MIP/main.py

        echo "SAT instances"

        python3 ./SAT/main.py

    fi

    if [ "$input" = "CP" ];
    then
        echo "to run all the istances for CP input \"all\" or the exact instance you want e.g \"01\" \n"
        read -p " " input 
        

        if [ "$input" = "all" ];
        then


            echo "which solver ? chuffed or gecode \n"
            read -p " " solver

            echo "with SB or without ? SB or NoSB  \n"
            read -p " " SB

            for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21
            do
                echo "instance number $i"
                echo " "

                if [ "$SB" = "SB" ]
                then

                    > "CP/temp_res/res_${solver}_sb_${i}.txt"

                    echo "model : cp_${solver}_sb.mzn" >> "CP/temp_res/res_${solver}_sb_${i}.txt"
                    echo "solver : $solver" >> "CP/temp_res/res_${solver}_sb_${i}.txt"
                    echo "instance : $i" >> "CP/temp_res/res_${solver}_sb_${i}.txt"

                    echo "minizinc --solver $solver ./CP/cp_${solver}_sb.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time"

                    minizinc --solver $solver ./CP/cp_${solver}_sb.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_${solver}_sb_${i}.txt"
                else  
                    > "CP/temp_res/res_${solver}_${i}.txt"

                    echo "model : cp_${solver}.mzn" >> "CP/temp_res/res_${solver}_${i}.txt"
                    echo "solver : $solver" >> "CP/temp_res/res_${solver}_${i}.txt"
                    echo "instance : $i" >> "CP/temp_res/res_${solver}_${i}.txt"

                    echo "minizinc --solver $solver ./CP/cp_$solver.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time"

                    minizinc --solver $solver ./CP/cp_$solver.mzn ./CP/Instances/inst$i.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_${solver}_${i}.txt"
                fi
            done
        else
            echo "which solver ? chuffed or gecode \n"
            read -p " " solver

            echo "with SB or without ? SB or NoSB  \n"
            read -p " " SB

            if [ "$SB" = "SB" ]
            then

                > "CP/temp_res/res_${solver}_sb_${input}.txt"

                echo "model : cp_${solver}_sb.mzn" >> "CP/temp_res/res_${solver}_sb_${input}.txt"
                echo "solver : $solver" >> "CP/temp_res/res_${solver}_sb_${input}.txt"
                echo "instance : $input" >> "CP/temp_res/res_${solver}_sb_${input}.txt"

                echo "minizinc --solver $solver ./CP/cp_${solver}_sb.mzn ./CP/Instances/inst$input.dzn --solver-time-limit 300000 --output-time"

                minizinc --solver $solver ./CP/cp_${solver}_sb.mzn ./CP/Instances/inst$input.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_${solver}_sb_${input}.txt"
            else  
                > "CP/temp_res/res_${solver}_${input}.txt"

                echo "model : cp_${solver}.mzn" >> "CP/temp_res/res_${solver}_${input}.txt"
                echo "solver : $solver" >> "CP/temp_res/res_${solver}_${input}.txt"
                echo "instance : $input" >> "CP/temp_res/res_${solver}_${input}.txt"

                echo "minizinc --solver $solver ./CP/cp_$solver.mzn ./CP/Instances/inst$input.dzn --solver-time-limit 300000 --output-time"

                minizinc --solver $solver ./CP/cp_$solver.mzn ./CP/Instances/inst$input.dzn --solver-time-limit 300000 --output-time >> "CP/temp_res/res_${solver}_${input}.txt"
            fi
        fi


    fi

    if [ "$input" = "MIP" ];
    then
        python3 ./MIP/main.py
    fi

    if [ "$input" = "SAT" ];
    then
        python3 ./SAT/main.py
    fi

    if [ "$input" = "CP_to_json" ]
    then
        python3 CP_to_json.py
    fi


done



