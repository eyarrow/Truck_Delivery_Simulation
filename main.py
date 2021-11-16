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


    # create simulation object
    simulation = Simulation.Simulation([1, 2], 'packages.csv', 'distances.csv', 'addresslist.csv', 27, 16)

    # Load packages that need to be on specific trucks
    simulation.truckSpecificDelivery(2, [3, 18, 36, 38])  # requirement: loaded on truck 2
    simulation.truckSpecificDelivery(1, [13, 14, 15, 16, 19, 20])  # req: must be delivered together

    # Load parameters for time sensitive deliveries
    simulation.setTimeSensitiveDeliveryTimes('10:30', 0, [13, 14, 16, 20, 29, 30, 31, 34, 37, 40])
    simulation.setTimeSensitiveDeliveryTimes('09:00', 0, [15])
    simulation.setTimeSensitiveDeliveryTimes('10:20', 1, [9])  # needs delivery address updated

    # Load any time sensitive packages onto trucks that have not been loaded already
    simulation.loadRemainingTimedDeliveries()
    simulation.removePackagesThatAreNotReadyAtDepo([6, 25, 28, 32])
    simulation.loadTrucksToMaxCapacity()
    simulation.runTruckSimulation()


    print("Current Delivery Status: ")
    print("_______________________________________________________________________________")
    simulation.printPackagesCurrentStatus()
    print("_______________________________________________________________________________")
    print(f"Total Miles Traveled: {simulation.total_distance_traveled}")

    simulation.setTimeSensitiveDeliveryTimes('10:30', 0, [6])  # Not at depo until 9:05, 25
    simulation.newPackagesAtDepot([25, 28, 32])


    simulation.reloadTrucks()

    print("After Second Round: ")
    print("_______________________________________________________________________________")
    simulation.printPackagesCurrentStatus()
    print("_______________________________________________________________________________")
    print(f"Total Miles Traveled: {simulation.total_distance_traveled}")

    simulation.deliverSubsequentRounds()

    print("After Last Delivery: ")
    print("_______________________________________________________________________________")
    simulation.printPackagesCurrentStatus()
    print("_______________________________________________________________________________")
    print(f"Total Miles Traveled: {simulation.total_distance_traveled}")
