from simulations.classes.Commands import Command, Idle, OpenCloseDoors, Move
import pytest


def test_bad_init_command():
    """
    Test the bad initialization of command class
    """

    with pytest.raises(TypeError):
        intended_destination = 2.234
        command = Command(intended_destination)
    
    
    with pytest.raises(TypeError):
        intended_destination = {}
        command = Command(intended_destination)


def test_good_init_command():
    """
    Test the good initialization of command class
    """

    intended_destination = 5
    command = Command(intended_destination)
    assert command.intended_destination == 5


    intended_destination = None
    command = Command(intended_destination)
    assert command.intended_destination == None



def test_init_idle():
    """
    Test the initialization of Idle class
    """

    intended_destination = 15
    command = Command(intended_destination)
    idle = Idle(command.intended_destination)
    assert idle.intended_destination == 15

    intended_destination = 105
    command = Command(intended_destination)
    idle = Idle(command.intended_destination)
    assert idle.intended_destination == 105


def test_init_openCloseDoors():
    """
    Test the OpenCloseDoors class
    """

    intended_destination = 56
    command = Command(intended_destination)
    door = OpenCloseDoors(command.intended_destination)
    assert door.intended_destination == 56


def test_bad_init_move():
    """
    Test the bad initialization of Move class
    """

    with pytest.raises(TypeError):
        if_up = "yes"
        intended_destination = 3
        move = Move(intended_destination, if_up)
    
    with pytest.raises(TypeError):
        if_up = 1
        intended_destination = 5
        move = Move(intended_destination, if_up)

    with pytest.raises(TypeError):
        if_up = True
        intended_destination = 2.1234
        move = Move(intended_destination, if_up)
  

def test_good_init_move():
    """
    Test the good initialization of Move class
    """

    intended_destination = 10
    if_up = True
    move = Move(intended_destination, if_up)
    assert move.if_up == True

    if_up = False
    move = Move(intended_destination, if_up)
    assert move.if_up == False