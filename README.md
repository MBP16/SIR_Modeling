# SIR_Modeling


### Dependencies to Install

- [matplotlib](https://matplotlib.org/) (for drawing SIR model Graph, require when using render_graph function)
  ```shell
  pip install matplotlib
  ```

### How to use

#### - Python version

- Just run the file [Pythonversion.py](sir_modeling_Pythonversion.py) then you will get output data into [file](data.csv) and get a graph drawn by matplotlib.pyplot

#### - C++ version

- First, run the following command
    ```shell
    python setup.py install
    ```
- Then run the file [C++version.py](sir_modeling_C++version.py) then you will get output data into [file](datacpp.csv) and get a graph drawn by matplotlib.pyplot

### Notices

- C++ version is faster than Python version when running with large data size.
- But C++ version needs buiding in each computer newly and it`s more complicated to use.

### Made by
- [Hyunwoo6321](https://github.com/hyunwoo6321)
- [Piop2(helped)](https://github.com/Piop2)