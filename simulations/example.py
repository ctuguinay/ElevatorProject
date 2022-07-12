from classes.controller import Controller

if __name__ == "__main__":
    
    # Initialize the Controller.
    controller = Controller(3, 10) # 3 Elevators and 10 Floors.

    # Assign a elevator to go up to floor 3.
    controller.assign_elevator(3, "up")

    # Call Elevator to go up
    controller.call_elevator(3, "up")

    # Run the simulation.
    controller.run()