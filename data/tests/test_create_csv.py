import pytest
import sys
from create_csv import argparse_create

def test_default_argparse_create():

    # Parse arguments.
    args = argparse_create([])

    # Check argument types.
    assert type(args.set_persons) is int
    assert type(args.set_target_file) is str
    assert type(args.set_floors) is int
    assert type(args.set_no_stop_prob) is float
    assert type(args.set_max_non_standard_hall_calls) is int
    assert type(args.set_mean_entry) is int
    assert type(args.set_mean_lunch) is int
    assert type(args.set_mean_exit) is int
    assert type(args.set_stdev) is int
    assert type(args.set_cutoff) is int
    assert type(args.set_mean_lunch_len) is int
    assert type(args.set_lunch_stdev) is int
    assert type(args.set_lunch_cutoff) is int
    assert type(args.set_standard_call_buffer) is int