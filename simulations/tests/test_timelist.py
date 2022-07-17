from simulations.classes.TimeList import TimeList, TimeListEvent
import pytest

def test_bad_initialization_timelist_event():
    """
    Tests if the TimeList and TimeListEvent class is working properly with bad initialization.
    """
    
    with pytest.raises(TypeError):
        time = 1.131434
        object_type = "Button Press"
        person_info = [859,27000,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
        timelist_event = TimeListEvent(time, object_type, person_info)
    
    with pytest.raises(TypeError):
        time = 1
        object_type = 1
        person_info = [859,27000,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
        timelist_event = TimeListEvent(time, object_type, person_info)

def test_bad_add_timelist():
    """
    Tests a bad example of adding an event to a TimeList class.
    """

    with pytest.raises(TypeError):
        time = 27000
        object_type = "Button Press"
        person_info = [859,27000,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
        timelist_event = TimeListEvent(time, object_type, person_info)

        timelist = TimeList()
        timelist.add_event(timelist_event)

        bad_event = [1,1,1,1]
        timelist.add_event(bad_event)

def test_proper_timelist():
    """
    Tests a proper example of adding an event to a TimeList class and getting the current event.
    """
  
    time = 27005
    object_type = "Button Press"
    person_info = [859,27005,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
    timelist_event = TimeListEvent(time, object_type, person_info)

    timelist = TimeList()
    timelist.add_event(timelist_event)

    time = 27000
    object_type = "Button Press"
    person_info = [819,27000,1,4,69.41447472292165] # [person_id,time_in_seconds,start_floor,dest_floor,weight]
    timelist_event = TimeListEvent(time, object_type, person_info)

    timelist = TimeList()
    timelist.add_event(timelist_event)

    current_event = timelist.next_event()

    assert current_event.time == 27000
    assert current_event.object_type == "Button Press"
    assert current_event.object == [819,27000,1,4,69.41447472292165]