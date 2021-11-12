# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import Package
import Truck

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Load the package data for the simulation, including packages to be delivered, addresses, and their distance
    # information
    new_packages = Package.PackagesToBeDelivered('packages.csv', 'distances.csv', 'addresslist.csv', 27)
    new_packages.printAllPackages()



    print("There is something about Mary")



