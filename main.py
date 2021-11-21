# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Package
import Truck
import Simulation
import Sim

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load the package data for the simulation, including packages to be delivered, addresses, and their distance
    # information


    # create simulation object


    sim2 = Sim.Simulation('packages.csv', 'distances.csv', 'addresslist.csv', 27, 16)
    sim2.loadAndDeliver('19:00')

    sim2.new_packages.printAllPackages()
    print(f"Total Miles traveled: {sim2.total_distance_traveled}")



    print("there is something about mary")

