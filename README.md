![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

# Optimizing automotive inbound logistics: A mixed-integer linear programming approach

Final project for the exam of Mathematical Optimisation course @ University of Trieste, carried out
with [Lorenzo Elia](https://github.com/lorenzoelia).
This repository contains the implementation of the model
described [here](https://www.sciencedirect.com/science/article/abs/pii/S1366554522001259).

## Setup

To clone this repository, you need to have `git` installed. After that you can open a terminal window and run

```
git clone https://github.com/damianoravalico/optimizing_automotive_inbound_logistics
```

Move to the project folder

```
cd optimizing_automotive_inbound_logistics
```

Now you need to install the dependencies. Make sure you have `pip` installed and then run

```
pip install -r requirements.txt
```

To run the program, do the following

```
cd src
```

and finally

```
python main.py
```

## Directories

- The `results` directory contains all the data needed for the analysis. Thanks to git, the only file in it is the file
  csv,
  named [`collected_data.csv`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/blob/master/results/collected_data.csv),
  used for analysis done and written within the presentation. When you run
  the [`main.py`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/blob/master/src/main.py),
  all new data is saved inside this directory, with the name `data_` + datetime + `.csv`
- [`src`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/tree/master/src) is the basis
  package containing all Python code. Inside there are:
    - [`model.py`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/blob/master/src/model.py)
      files, which represent the model used for optimization (variables and constraints)
    - [`main.py`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/blob/master/src/main.py),
      the entry point
    - Package [`anal`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/tree/master/anal),
      which contains all the scripts to do the analysis. Note that these scripts are based
      at [`collected_data.csv`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/blob/master/results/collected_data.csv)
    - [`dataset`](https://github.com/damianoravalico/optimizing_automotive_inbound_logistics/tree/master/dataset)
      package, which contains the scripts and a class, used within the model and for generating the dataset