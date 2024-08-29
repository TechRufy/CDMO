# syntax=docker/dockerfile:1
# Pulls an image endowed with minizinc
FROM minizinc/mznc2022:latest AS builder

# Installing python and its required libraries
RUN apt-get update -y \
    && apt-get install -y apt-transport-https \
    && apt-get install -y python3 \
    && apt-get install -y python3-pip 

# Setting the base folder for the container 


RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y bison build-essential cmake flex git

# Coping all the content of this folder into the container
WORKDIR /src

RUN git clone https://github.com/gecode/gecode . && \
    git checkout develop

# Build gecode and install it into /install.
RUN mkdir /install && mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/install .. && \
    cmake --build . --config Release && \
    cmake --build . --config Release --target install



FROM minizinc/mznc2022:latest AS final

RUN apt-get update -y \
    && apt-get install -y apt-transport-https \
    && apt-get install -y python3 \
    && apt-get install -y python3-pip 


COPY . .

COPY MIP/requirements.txt /requirements.txt

COPY --from=builder /install /gecode

RUN python3 -m pip install -r /requirements.txt


# Add gecode to the MiniZinc search path and set it as the default solver.
#
# See https://www.minizinc.org/doc-2.6.3/en/command_line.html#user-configuration-files
RUN echo '{"mzn_solver_path": ["/gecode/share/minizinc/solvers"],' > $HOME/.minizinc/Preferences.json && \
    echo '"tagDefaults": [["", "org.gecode.gecode"]]}'           >> $HOME/.minizinc/Preferences.json

# Use this command to keep the container up and use the terminal inside of it
# CMD python3 -m http.server 


# Use this command to run the instances and generate the results automatically
#CMD minizinc --solver gecode ./CP/cp.mzn ./CP/Instances/inst01.dzn && python3 ./MIP/main.py && python3 -m http.server
RUN chmod +rx runner.sh
#CMD python3 -m http.server