from simulations.classes.Commands import Command, Idle, OpenCloseDoors, Move
import pytest

def test_bad_command():
    """
    Tests if the Command class is working properly with bad initialization
    """
    with pytest.raises(TypeError):
        intended_dest = "hi"
        command = Command(intended_dest)
    
    with pytest.raises(TypeError):
        intended_dest = 1.2
        command = Command(intended_dest)

def test_good_command():
    intended_dest = 3
    command = Command(intended_dest)
    assert command.intended_destination == 3

    intended_dest = None
    command = Command(intended_dest)
    assert command.intended_destination == None


def test_idle():
    intended_dest = 3
    command = Command(intended_dest)
    idle = Idle(command.intended_destination)
    assert idle.intended_destination == 3


def test_openCloseDoors():
    intended_dest = 3
    command = Command(intended_dest)
    ocd = OpenCloseDoors(command.intended_destination)
    assert ocd.intended_destination == 3

def test_bad_move():
    with pytest.raises(TypeError):
        if_up = 123
        intended_dest = 3
        move = Move(intended_dest, if_up)

def test_good_move():
    if_up = True
    intended_dest = 3
    move = Move(intended_dest, if_up)
    assert move.intended_destination == 3
    assert move.if_up == True
