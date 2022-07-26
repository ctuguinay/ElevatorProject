import pytest
from simulations.classes.EventObjects import HallCall, Arrival
# A quick note, we also have a Hall_Call class under the general Person.py file. Since it doesn't
# seem like that's integrated into the class structure at all, I'm working with the HallCall class.


HALLCALL_ORDER = ['person_id', 'time', 'start_floor', 'dest_floor', 'weight']
    # The attributes of a HallCall, also the arguments of its initialization.


def test_csv_initialization_hallcall():
    """
    Tests if the HallCall class initialization functions properly for several good initializations,
    using various data points from the CSV.
    """

    person1 = [5192, 27570.33890162208, 1, 5, 74.21924393885755]
    person2 = [5016, 28111.65820004999, 1, 6, 72.41407647871662]
    person3 = [9637, 28361.307956435645, 1, 6, 62.53834224858009]
    person4 = [1119, 28361.685953126092, 1, 5, 69.40820321618097]
    person5 = [2383, 28395.968621072745, 1, 2, 71.36470902648905]

    for person in [person1, person2, person3, person4, person5]:
        call = HallCall(*person)
        for characteristic, label in zip(person, HALLCALL_ORDER):
            assert vars(call)[label] == characteristic


def test_general_initialization_hallcall():
    """
    Tests general initializations for the HallCall class with unrealistic values.
    """
    person1 = [0, 20, 10, 1, 0.0]
    person2 = [-1, -100, -10, 4, 1.0 * 10 ** 10]
    person3 = [250000, 864001, 6, 7, -30.1312]
    person4 = [-100, 2864000, 1, -3, -500.0]
    person5 = [400, 864001.0, 10000, 24, 10.0]

    for person in [person1, person2, person3, person4, person5]:
        call = HallCall(*person)
        for characteristic, label in zip(person, HALLCALL_ORDER):
            assert vars(call)[label] == characteristic


def test_bad_initialization_hallcall():
    """
    Tests if the HallCall class initialization functions properly for several bad initializations.
    """
    
    person1 = ['5192', 27570.33890162208, 1, 5, 74.21924393885755] # Person id should be an int
    person2 = [5016, 28111.65820004999, 1.0, 6, 72.41407647871662] # Start should be an int
    person3 = [9637, 28361.307956435645, 1, 6.0, 62.53834224858009] # Destination should be an int
    person4 = [1119, None, 1, 5, 69.40820321618097] # Time should be numeric
    person5 = [2383, 28395.968621072745, 1, 2, 71] # Weight should be a float
    for person in [person1, person2, person3, person4, person5]:
        with pytest.raises(TypeError):
            call = HallCall(*person)


def test_good_initialization_arrival():
    """
    Tests if the Arrival class initialization functions properly for several good initializations.
    """
    floor1 = Arrival(1)
    floor2 = Arrival(2)
    floor3 = Arrival(0)
    floor4 = Arrival(-1)
    floor5 = Arrival(2 ** 32)
    assert floor1.floor == 1
    assert floor2.floor == 2
    assert floor3.floor == 0
    assert floor4.floor == -1
    assert floor5.floor == 2 ** 32


def test_bad_initialization_arrival():
    """
    Tests if the Arrival class initialization fun(ctions properly for several bad initializations.
    """
    with pytest.raises(TypeError):
        floor1 = Arrival('1')
    with pytest.raises(TypeError):
        floor2 = Arrival(1.0)
    with pytest.raises(TypeError):
        floor3 = Arrival(None)
