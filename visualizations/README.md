# Visualizations

### Quickstart:

* Setup the environment properly with the following:
```
pip install -r requirements.txt
```

* If you haven't already, make sure you are at the `/visualizations` directory with the following command:
```
cd visualizations
```

* Run the view data distribution code in python.
```
python view_data_dist.py --set_target_file data.csv  --set_width 15 --set_height 15
```
* We use `--set_target_file` to set the target file in `data/CSVs/..`, and `--set_width` and `--set_height` so set the width and height
of our Matplotlib plot.