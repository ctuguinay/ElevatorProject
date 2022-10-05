# Simulations

### Disclaimer:

* Results found on the paper may not exactly be replicable for either `base_case_simulation.py` or `dqn_training.py`.

### Quickstart:

* If you haven't already, make sure you are at the `/simulations` directory with the following command:
```
cd simulations
```

* Run the base case simulation in Python:
```
python base_case_simulation.py --python_command python3
```
* Use ``--python_command (insert command)`` to use the command your device uses to run Python.

* `base_case_simulation.py` correlates to section 4.5 of the paper: Naive Approach to Elevator Control.

* Run the RL Training Model in Python:
```
python dqn_training.py --python_command python3
```
* Again, use the ``--python_command (insert command)`` to use the command your device uses to run Python.

* Explore the classes we will be using for Simulations at `classes`.