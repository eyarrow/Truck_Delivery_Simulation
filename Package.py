# Module to manage individual package and packages
import DataStructures
import csv


class Package:
    def __init__(self, id, address, deadline, city, zip, weight, status='at the hub', location_code=0):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip = zip
        self.weight = weight
        self.status = status
        self.location_code = location_code

    # Updates the delivery status of a package
    def updateDeliveryStatus(self, status):
        self.status = status

    # print the info for a single package
    def printPackageInfo(self):
        print(
            f"{self.id} | {self.address} | {self.city} | {self.zip} | {self.weight} | {self.deadline} | {self.status}")

    def returnAddress(self):
        return self.address

    def returnLocationCode(self):
        return self.location_code

    def updateAddress(self, new_address, new_city, new_zip):
        self.address = new_address
        self.city = new_city
        self.zip = new_zip



# Class to manage data related to a distance between points
class Distance:
    def __init__(self, locationCode, distance):
        self.location = locationCode
        self.distance = distance

    def printDistance(self):
        print(f"Location: {self.location}")
        print(f"Distance: {self.distance}")


# Class to manage the group of packages to be delivered. Parameters: filename_packages = file name that contains the
# packages to be loaded. filename_distances = a csv that includes the distances between addresses. filename_addresslist:
# A list of all the addresses that will be delivered to in that day. Used to create a mapping between the addresses
# number (order on the list) and the full physical address. Upon creation this class loads the packages, and addresses.
# It creates a mapping between the addresses and the packages, storing the address index to the package record. A
# lookup matrix is created so that distances between any two points can be easily determined.
class PackagesToBeDelivered:
    def __init__(self, filename_packages, filename_distances, filename_addresslist, num_addresses):
        self.packageHash = DataStructures.HashTable()
        self.file = filename_packages
        self.file_distances = filename_distances
        self.file_addresslist = filename_addresslist
        self.location_index = {}
        self.address_matrix = DataStructures.DistanceMatrix(num_addresses)
        self.loadPackageFile()
        self.createLocationIndex()
        self.loadDistanceFile()
        self.populateLocationCodes(self.location_index)

    # Prints all packages in the given hash table
    def printAllPackages(self):
        for i in range(len(self.packageHash.array)):
            if self.packageHash.array[i].returnLinkedListData() is None:
                i = i + 1
            else:
                temp = self.packageHash.array[i]
                temp.returnLinkedListData().printPackageInfo()
                # iterate through the list if there are other values
                while temp.returnLinkedListNext() is not None:
                    temp = temp.next
                    temp.data.printPackageInfo()

    # Populate all the data members of the hash table with a location code. This is reliant on a key dictionary to be
    # present
    def populateLocationCodes(self, key_dictionary):
        for i in range(len(self.packageHash.array)):
            if self.packageHash.array[i].returnLinkedListData() is None:
                i = i + 1
            else:
                street_address = self.packageHash.array[i].returnLinkedListData().returnAddress()
                index = key_dictionary[street_address]
                self.packageHash.array[i].returnLinkedListData().location_code = index


    # Return the package numbers of all the packages
    def returnPackageIndices(self):
        package_list = []
        for i in range(len(self.packageHash.array)):
            if self.packageHash.array[i].returnLinkedListData() is None:
                i = i + 1
            else:
                package_list.append(self.packageHash.array[i].returnLinkedListData().id)
        return package_list

    # Returns a list of all the packages in the table
    def returnAllPackages(self):
        package_list = []
        for i in range(len(self.packageHash.array)):
            if self.packageHash.array[i].returnLinkedListData() is None:
                i = i + 1
            else:
                package_list.append(self.packageHash.array[i].returnLinkedListData())
        return package_list

    # return a package object. Look up uses the package id which is passed by parameter
    def returnPackageByID(self, id):
        return self.packageHash.findDataInHashTable(id)

    # Return location Code
    def returnLocationCode(self, index):
        package_data = self.packageHash.findDataInHashTable(index)
        return package_data.location_code


    # Load the packages in from a CSV file
    def loadPackageFile(self):
        with open(self.file, newline='', encoding='utf-8-sig') as reader:
            package_file = csv.reader(reader, delimiter=',')
            for row in package_file:
                newPackage = Package(int(row[0]), row[1], row[5], row[2], row[4], row[6])
                self.packageHash.addToHashTable(int(row[0]), newPackage)


    # Load the distances between points from a CSV file
    def loadDistanceFile(self):
        with open(self.file_distances, newline='', encoding='utf-8-sig') as reader:
            distance_file = csv.reader(reader, delimiter=',')
            index = 0
            row_index = 0
            for row in distance_file:
                for cell in row:
                    # represents the "destination", x axis of the matrix
                    position = row.index(cell)
                    distance_num = float(cell)
                    new_distance = Distance(position, distance_num)
                    self.address_matrix.addToMatrix(row_index, new_distance)
                row_index = row_index + 1
                index = index+1

    # Load the location index. This is used to map addresses to their numerical values used for the distance matrix
    def createLocationIndex(self):
        with open(self.file_addresslist, newline='', encoding='utf-8-sig') as reader:
            location_file = csv.reader(reader, delimiter=',')
            index = 0
            for row in location_file:
                self.location_index[row[0]] = index
                index = index + 1

    # Update the status string for a given package id
    def updateStatusByPackageID(self, package_id, status_string):
        key = self.packageHash.calculateIndex(package_id)
        self.packageHash.array[key].head.data.updateDeliveryStatus(status_string)
