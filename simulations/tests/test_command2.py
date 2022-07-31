from simulations.classes.Commands import Command, Idle, OpenCloseDoors, Move
import pytest

def test_bad_command():
    """
    Tests if the Command class is working properly with bad initialization
    """
    with pytest.raises(TypeError):
        intended_dest = "hi"
        command = Command(intended_dest)

def test_good_command():
    
    command = Command()


def test_idle():

    idle = Idle()


def test_openCloseDoors():
    if_going_up = False
    ocd = OpenCloseDoors(if_going_up)
    assert ocd.going_up == if_going_up

def test_bad_move():
    with pytest.raises(TypeError):
        if_up = 123
        intended_dest = 3
        move = Move(intended_dest, if_up)

def test_good_move():
    if_up = True
    move = Move(if_up)
    assert move.if_up == True
