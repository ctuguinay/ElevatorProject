# Data

### Quickstart:

* If you haven't already, make sure you are at the `/data` directory with the following command:
```
cd data
```

* Setup the environment properly with the following:
```
pip install -r requirements.txt
```

* Or you can just install `numpy` as that is the only dependency in the requirements folder:
```
pip install numpy
```

* Once you have setup the environment, run the code to create the CSV containing our data:
```
python create_csv.py --set_floors 8 --set_persons 10000
```
* You can use the `set_floors` and `set_persons` to simulate how many floors and people we want to generate within our data.

* If you are starting at the `./data` directory, you should find the CSV in `./CSVs/data.csv`.