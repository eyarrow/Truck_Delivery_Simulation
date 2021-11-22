# Module for displaying the main menu, and managing it's functionality.
import Sim


# class for displaying the main menu, and providing functionality that allows the user to control the simulation
class MainMenu:
    def __init__(self):
        self.title = "Welcome to the WGUPS Delivery Program!"
        self.divider = "---------------------------------------------------------------------------------------------" \
                       "-----------"
        self.option_1 = "[1] Run the simulation until all packages are delivered"
        self.option_2 = "[2] Pause the simulation at a given time"
        self.option_3 = "[3] View statistics"
        self.option_4 = "[4] Exit the program "

    # prints the main menu to the screen
    def printMainMenu(self):
        print(self.divider)
        print(self.option_1)
        print(self.option_2)
        print(self.option_3)
        print(self.option_4)
        print(self.divider)

    # runs a simulation. Prints out the Results to the screen
    def runSimulation(self, time='19:00'):
        sim = Sim.Simulation('packages.csv', 'distances.csv', 'addresslist.csv', 27, 16)
        sim.loadAndDeliver(time)

        # If simulation had a pause, print that info
        if time != '19:00':
            print(f"Simulation paused at {time}")

        print("Current Status of All Packages:")
        print(self.divider)
        sim.new_packages.printAllPackages()
        print("\n")
        print(f"Total Miles traveled: {sim.total_distance_traveled}")

    def showStats(self):
        sim = Sim.Simulation('packages.csv', 'distances.csv', 'addresslist.csv', 27, 16)
        sim.loadAndDeliver()
        print("Simulation Statistics: ")
        print(self.divider)
        print(f"Total number of miles traveled by both trucks: {sim.total_distance_traveled}")
        print(f"Total miles driven by Truck 1: {sim.truck1.miles}")
        print(f"Total miles driven by Truck 2: {sim.truck2.miles}")
        print(f"Truck 1 finished delivering packages at: {sim.truck1.truck_time}")
        print(f"Truck 2 finished delivering packages at: {sim.truck2.truck_time}")
        print(self.divider)


