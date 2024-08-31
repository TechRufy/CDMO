FROM minizinc/minizinc:2.8.3 AS final

RUN apt-get update -y \
    && apt-get install -y apt-transport-https \
    && apt-get install -y python3 \
    && apt-get install -y python3-pip 


COPY . .


RUN python3 -m pip install -r ./MIP/requirements.txt
RUN python3 -m pip install -r ./SAT/requirements.txt
# Use this command to run the instances and generate the results automatically
#CMD minizinc --solver gecode ./CP/cp.mzn ./CP/Instances/inst01.dzn && python3 ./MIP/main.py && python3 -m http.server
RUN chmod +rx runner.sh
#CMD python3 -m http.server