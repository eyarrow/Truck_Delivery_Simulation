# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Package
import Truck
import Simulation

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load the package data for the simulation, including packages to be delivered, addresses, and their distance
    # information
    simulation = Simulation.Simulation([1, 2], 'packages.csv', 'distances.csv', 'addresslist.csv', 27, 16)

    # Load packages that need to be on specific trucks
    simulation.truckSpecificDelivery(2, [3, 18, 36, 38])  # requirement: loaded on truck 2
    simulation.truckSpecificDelivery(1, [13, 14, 15, 16, 19, 20])  # req: must be delivered together

    # Load parameters for time sensitive deliveries
    simulation.setTimeSensitiveDeliveryTimes('10:30', 0, [13, 14, 16, 20, 29, 30, 31, 34, 37, 40])
    simulation.setTimeSensitiveDeliveryTimes('09:00', 0, [15])
    # simulation.setTimeSensitiveDeliveryTimes('09:05', 1, [6, 25, 28, 32])  # Not at depo until 9:05, 25
        # will need to be loaded first has a deadline of 10:30
    simulation.setTimeSensitiveDeliveryTimes('10:20', 1, [9])  # needs delivery address updated

    # Load any time sensitive packages onto trucks that have not been loaded already
    simulation.loadRemainingTimedDeliveries()
    simulation.loadTrucksToMaxCapacity()
    simulation.runTruckSimulation()
    print(simulation.clock)
    print(simulation.total_distance_traveled)


    simulation.printPackagesCurrentStatus()
    print(f"Total Miles Traveled: {simulation.total_distance_traveled}")
    myList = simulation.experimentingWithLists()
    print(myList)









    print("There is something about Mary")
