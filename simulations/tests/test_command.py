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

    command = Command()



def test_init_idle():
    """
    Test the initialization of Idle class
    """

    idle = Idle()


def test_init_openCloseDoors():
    """
    Test the OpenCloseDoors class
    """

    up_intention = True
    command = OpenCloseDoors(up_intention)
    assert command.going_up == True


def test_bad_init_move():
    """
    Test the bad initialization of Move class
    """

    with pytest.raises(TypeError):
        if_up = "yes"
        move = Move(if_up)
    
    with pytest.raises(TypeError):
        if_up = 1
        move = Move(if_up)
  

def test_good_init_move():
    """
    Test the good initialization of Move class
    """

    if_up = True
    move = Move(if_up)
    assert move.if_up == True

    if_up = False
    move = Move(if_up)
    assert move.if_up == False