# SIR_Modeling


### Dependencies to Install

- [matplotlib](https://matplotlib.org/) (for drawing SIR model Graph, require when using render_graph function)
  ```shell
  pip install matplotlib
  ```

### How to use

#### - Python version

- First, change the values in [config file](config.json) to your own
- Then, run the file [Pythonversion.py](sir_modeling_Pythonversion.py) then you will get output data into [file](data.csv) and get a graph drawn by matplotlib.pyplot

#### - C++ version

- First, change the values in [config file](config.json) to your own
- Next, run the following command
    ```shell
    python setup.py install
    ```
- Finally, run the file [C++version.py](sir_modeling_C++version.py) then you will get output data into [file](datacpp.csv) and get a graph drawn by matplotlib.pyplot

#### - Config changing help

###### Essential Values

- DT: Time step to calculate S, I, R values
- λ: Infection Rate
- γ: Recovery Rate
- S: Initial Susceptible number

###### Optional Values

- FLOAT_TYPE: Select fixed/floating points, True: fixed points/False: floating points(False is default)
- T: Starting time(0 is default)
- I: Initial Infected(1 is default)
- R: Initial Recovery(0 is default)
- END_TIME: Use when you want to End modeling in specific time.(0 is default, it means no end until S0+I0+R0 = LastR)

### Notices

- γ and λ value in config is allowed to use in expression with string type.(ex. "1/200")
- Without END_TIME, the program doesn`t end especially when DT value is low.(Python only, c++ version has an exit method)
- C++ version is faster than Python version when running with large data size.
- But C++ version needs buiding in each computer newly and it`s more complicated to use.

### Made by
- [Hyunwoo6321](https://github.com/hyunwoo6321)
- [Piop2(helped)](https://github.com/Piop2)
