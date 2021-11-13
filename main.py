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
    simulation = Simulation.Simulation([1, 2], 'packages.csv', 'distances.csv', 'addresslist.csv', 27)
    simulation.truckSpecificDelivery(2, [3, 18, 36, 38])  # requirement: loaded on truck 2
    simulation.truckSpecificDelivery(1, [13, 14, 15, 16, 19, 20])  # req: must be delivered together

    print("There is something about Mary")
