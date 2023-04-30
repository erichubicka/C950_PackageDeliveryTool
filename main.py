# Eric Hubicka
# Student ID: 010982699
# Data Structures and Algorithms II - C950
# NHP2 Project

import csv
from datetime import time
from Truck import Truck
from Package import Package
from HashTable import ChainingHashTable

#--------------------------------------- Space-Time Complexity---------------------------------------
# for the entire code, time complexity is O(n^2) and space complexity is O(n)
#-----------------------------------------------------------------------------------------

myHash = ChainingHashTable() # myHash will call the hashtable class

#--------------------------------------- Load Data ---------------------------------------

# create instances of packages using csv data and add them to a list
# Space-Time Complexities are O(n)
packageList = list()
def loadPackageData(filename):
    with open(filename) as packageInfo: # open the csv file and assign it to a variable
        packageData = csv.reader(packageInfo, delimiter=',') # read the csv file
        next(packageData) # go to the next line of the csv file
        for package in packageData: # add various parameters to a package object
            pPackageID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeliveryDeadline = package[5]
            pMass = package[6]
            pNotes = package[7]
            pStatus = "at the hub"
            pDeliveryTime = None
            # instantiate a new package object
            packageData = Package(pPackageID, pAddress, pCity, pState, pZip, pDeliveryDeadline, pMass, pNotes, pStatus, pDeliveryTime)
            myHash.insert(pPackageID, packageData) # insert the package into the hashtable
            packageList.append(package) # add the package into a list

# load the distances from csv data and add them to a list
# Space-Time Complexities are O(n)
distanceList = list()
def loadDistanceData(filename):
    with open(filename) as distanceInfo:
        distanceData = csv.reader(distanceInfo, delimiter=',')
        next(distanceData)
        for distance in distanceData: # for each distance
            distanceList.append(distance) # add the distance to the list

# load addresses from csv data and add them to a list
# Space-Time Complexities are O(n)
addressList = list()
def loadAddressData(filename):
    with open(filename) as distanceInfo:
        addressData = csv.reader(distanceInfo, delimiter=',')
        next(addressData)
        for address in addressData: # for each address
            addressList.append(address) # add the address to the list

# load in the csv files
loadPackageData('Package.csv')
loadDistanceData('Distance.csv')
loadAddressData('Address.csv')

#--------------------------------------- Various Methods ---------------------------------------

# input a packageID and return its associated delivery addressID
# time complexity is O(n) and space complexity is O(1)
def getAddressIDFromPackageID(packageID):
    addressReturned = None
    # for each package in the packageList
    for index, package in enumerate(packageList):  # enumerate makes the packageList iterable
        if packageID == index + 1: # if the packageID is found in the packageList
            addressReturned = package[1] # return its associated address name
    for address in addressList: # for each address in the addressList
        if addressReturned == address[2]: # if the packages address is found in the address list
            return int(address[0]) # return its associated addressID

# get the distance between two packages delivery Addresses
# Space-Time Complexities are O(1)
def getDistance(packageA, packageB): # pass in two address ID's
    return float(distanceList[packageA][packageB]) # return the distance as a float

#--------------------------------------- Algorithm ---------------------------------------

# use the nearest neighbor algorithm to sort the trucks packages in an improved order to be delivered
# time complexity is O(n^2) where n is the number of packages in the truck
# space complexity is O(n) where n is the number of packages in the truck
def nearestNeighbor(truck):
    packageNNRoute = []
    currentRoute = []
    for package in truck.packages: # add packages to the current Route (to be improved)
        currentRoute.append(package.PackageID) # add the packages to the route list

    nearestInitialDistance = float('inf') # set the nearest distance initially to infinite
    nearestPackage = None # set the nearest package delivery address initially to none
    # get the initial closest package delivery address from the hub using the NN algorithm
    for package in currentRoute: # find distances for each package delivery address to the hub
        distance = getDistance(0, getAddressIDFromPackageID(package)) # get the distance
        if distance < nearestInitialDistance: # if the distance is the closest to the hub so far
            nearestInitialDistance = distance # overwrite the nearest distance
            nearestPackage = package # overwrite the package with the nearest delivery address to the hub
    packageNNRoute.append(nearestPackage) # add a package to the NN route
    currentRoute.remove(nearestPackage) # remove a package from the current route

    while len(currentRoute) > 0:  # while currentRoute is not empty
        nearestDistance = float('inf')  # set the nearest distance initially to infinite
        # after the initial closest package, compile a route list using the NN algorithm
        for package in currentRoute:
            if package == 9: # packageID 9 is a special case that the address changes
                Package.updateAddress(myHash.search(9), "410 S State St") # wrong address changed for package 9
            # get the package distance between the package and the last package in the final route list
            distance = getDistance(getAddressIDFromPackageID(packageNNRoute[-1]), getAddressIDFromPackageID(package))
            if distance < nearestDistance:
                nearestDistance = distance
                nearestPackage = package
        packageNNRoute.append(nearestPackage)
        currentRoute.remove(nearestPackage)
    return packageNNRoute # return the package route determined by the algorithm

#--------------------------------------- Trucks ---------------------------------------

# instantiate two trucks from the Truck class and load them with packages
truck1 = Truck(1, 0, 0, set()) # id 1, location starting 0 (WGU Hub), no mileage yet, no associated packages yet
truck2 = Truck(2, 0, 0, set())
truck3 = Truck(3, 0, 0, set())

# load the trucks manually
packageTruck1_ids = [14, 15, 16, 34, 20, 21, 13, 39, 4, 40, 19, 27, 35, 12, 23, 11] # add package IDs to a list
for package_id in packageTruck1_ids: # for each packageID in the list
    truck1.add(myHash.search(package_id)) # add the package to truck1
truck1nnRoute = nearestNeighbor(truck1) # compile an optimal delivery route for truck 1 using the nearest neighbor algorithm
packageTruck2_ids = [6, 31, 32, 25, 26, 3, 18, 36, 38, 28, 9, 10, 2, 33, 17, 22]
for package_id in packageTruck2_ids:
    truck2.add(myHash.search(package_id))
truck2nnRoute = nearestNeighbor(truck2)
packageTruck3_ids = [37, 5, 30, 8, 7, 29, 1, 24]
for package_id in packageTruck3_ids:
    truck3.add(myHash.search(package_id))
truck3nnRoute = nearestNeighbor(truck3)

#--------------------------------------- Menu Methods ---------------------------------------

# return a list of miles travelled for a truck after each delivery, and an equivalent delivery time list
# Space-Time Complexities are O(n)
def getTimeAndMileage(truckNNRoute):
    #mileage
    totalMileage = 0
    truckLocation = 0
    mileageList = []
    for i in truckNNRoute: # for each package in the truck route, add its delivery mileage to a list
        totalMileage = totalMileage + getDistance(truckLocation, getAddressIDFromPackageID(i))
        mileageList.append(totalMileage)
        truckLocation = getAddressIDFromPackageID(i)
    #time
    if truckNNRoute == truck2nnRoute: # for truck 2
        startTime = (9 * 60) + 15 # 9:15am start time in minutes
    else: # for trucks 1 and 3
        startTime = 8 * 60  # 8:00am start time in minutes
    lastTravelDistance = 0
    travelTimeMinutes = []
    deliveryTimeList = []
    for i in mileageList: # use the mileage List to create another list of equivalent travel minutes per delivery
        travelTimeMinutes.append(round((i - lastTravelDistance) / 0.3)) # 0.3 is the avg miles per minutes
        lastTravelDistance = i
    for i in travelTimeMinutes: # add delivery times to a list for the truck route
        startTime += i
        hours, minutes = divmod(startTime, 60)
        deliveryTimeList.append(f"{hours:02d}:{minutes:02d}")
    return mileageList, deliveryTimeList

TimeMileageListsTruck1 = getTimeAndMileage(truck1nnRoute)
TimeMileageListsTruck2 = getTimeAndMileage(truck2nnRoute)
TimeMileageListsTruck3 = getTimeAndMileage(truck3nnRoute)

# calculate travel miles by the trucks
# Space-Time Complexities are O(1)
def totalMileageCalculation():
    truck3ReturnTrip = getDistance(12, 0) # truck 3 will need to return to the hub from address ID 12
    # total miles travelled by all three trucks including trucks 3 return trip back to the hub
    totalMileage = TimeMileageListsTruck1[0][-1] + TimeMileageListsTruck2[0][-1] + truck3ReturnTrip + TimeMileageListsTruck3[0][-1]
    truck1Mileage = TimeMileageListsTruck1[0][-1] # total miles travelled by truck 1
    truck2Mileage = TimeMileageListsTruck2[0][-1]
    truck3Mileage = TimeMileageListsTruck3[0][-1] + truck3ReturnTrip
    return totalMileage, truck1Mileage, truck2Mileage, truck3Mileage

# add delivery times to each package in a particular truck route
# Space-Time Complexities are O(n)
def addDeliveryTimesToPackages(truckNNRoute, TimeMileageList):
    timeNum = 0
    for package_id in truckNNRoute:  # put the delivery times into the truck packages
        Package.updateDeliveryTime(myHash.search(package_id), TimeMileageList[1][timeNum])
        timeNum = timeNum + 1

addDeliveryTimesToPackages(truck1nnRoute, TimeMileageListsTruck1)
addDeliveryTimesToPackages(truck2nnRoute, TimeMileageListsTruck2)
addDeliveryTimesToPackages(truck3nnRoute, TimeMileageListsTruck3)

# user pass in a single packageID and time and see that packages status at that time
# Space-Time Complexities are O(1)
def getSinglePackageStatusWithTime(userPackageInput, userTimeInput):
    packageDeliveryTime = time.fromisoformat(myHash.search(userPackageInput).DeliveryTime)
    truck1and3DepartTime = time(8, 0) # time truck 1 and 3 will depart the hub
    truck2DepartTime = time(9, 15) # time truck 2 will depart the hub

    # change the package status depending on which trucks its associated with and the time the user passed in
    if userPackageInput in packageTruck1_ids or userPackageInput in packageTruck3_ids:
        if userTimeInput < truck1and3DepartTime:
            Package.updateStatus(myHash.search(userPackageInput), "at hub")
        else:
            if packageDeliveryTime > userTimeInput:
                Package.updateStatus(myHash.search(userPackageInput), "en route")
            else:
                Package.updateStatus(myHash.search(userPackageInput), "delivered")
    else:
        if userTimeInput < truck2DepartTime:
            Package.updateStatus(myHash.search(userPackageInput), "at hub")
        else:
            if packageDeliveryTime > userTimeInput:
                Package.updateStatus(myHash.search(userPackageInput), "en route")
            else:
                Package.updateStatus(myHash.search(userPackageInput), "delivered")

    # if the package does not have a delivered status, display the delivery time a N/A
    if myHash.search(userPackageInput).Status != "delivered":
        Package.updateDeliveryTime(myHash.search(userPackageInput), "N/A")

    print("----------------------------------------------")
    print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
    print(myHash.search(userPackageInput)) # print the package

# user pass in a time and see all the package statuses at that time
# Space-Time Complexities are O(n)
def getAllPackageStatusWithTime(userTimeInput):
    print("----------------------------------------------")
    print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
    truck1and3DepartTime = time(8, 0) # time truck 1 and 3 will depart the hub
    truck2DepartTime = time(9, 15) # time truck 2 will depart the hub

    for packageID in range(1, 41): # for all 40 packages
        packageDeliveryTime = time.fromisoformat(myHash.search(packageID).DeliveryTime)
        # change the package status depending on which trucks its associated with and the time the user passed in
        if packageID in packageTruck1_ids or packageID in packageTruck3_ids:
            if userTimeInput < truck1and3DepartTime:
                Package.updateStatus(myHash.search(packageID), "at hub")
            else:
                if packageDeliveryTime > userTimeInput:
                    Package.updateStatus(myHash.search(packageID), "en route")
                else:
                    Package.updateStatus(myHash.search(packageID), "delivered")
        else:
            if userTimeInput < truck2DepartTime:
                Package.updateStatus(myHash.search(packageID), "at hub")
            else:
                if packageDeliveryTime > userTimeInput:
                    Package.updateStatus(myHash.search(packageID), "en route")
                else:
                    Package.updateStatus(myHash.search(packageID), "delivered")

        # if the package does not have a delivered status, display the delivery time a N/A
        if myHash.search(packageID).Status != "delivered":
            Package.updateDeliveryTime(myHash.search(packageID), "N/A")

        print(myHash.search(packageID)) #  print the package

#--------------------------------------- Menu ---------------------------------------

def menu(): # command line interface which the user can interact with
    print("----------------------------------------------")
    print("Main Menu, please type an option 1, 2, 3, or 4")
    print("----------------------------------------------")
    print("1. Print All Package Status and Total Mileage")
    print("2. Get a Single Package Status with a Time")
    print("3. Get All Package Status with a Time")
    print("4. Exit the Program")
    menuOptionSelect = input("Selection: ")  # get user input to select a menu option
    if menuOptionSelect == "1": # if menu option 1 is selected
        option1() # run the method for option 1
    elif menuOptionSelect == "2":
        option2()
    elif menuOptionSelect == "3":
        option3()
    else:
        option4()

def option1(): # print all package status and total mileage
    print("----------------------------------------------")
    print("Truck 1 travelled " + str(round(totalMileageCalculation()[1], 1)) + " miles.")
    print("Truck 2 travelled " + str(round(totalMileageCalculation()[2], 1)) + " miles.")
    print("Truck 3 travelled " + str(round(totalMileageCalculation()[3], 1)) + " miles.")
    print("The total distance travelled to deliver all the packages is " + str(round(totalMileageCalculation()[0], 1)) + " miles.")
    print("----------------------------------------------")
    print("Here is a list of all the packages:")
    print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
    for packageID in range(1, 41): # for each package set the status to delivered and print it
        Package.updateStatus(myHash.search(packageID), "delivered")
        print(myHash.search(packageID))

def option2(): # get a single package status with a time
    print("----------------------------------------------")
    userPackageInput = ""
    timeInput = ""
    while userPackageInput == "":
        try: # get the packageID input from the user
            userPackageInputString = input("Enter a package ID: ")
            userPackageInput = int(userPackageInputString)
        except ValueError:
            print("Invalid input. Please enter a number.")
    while timeInput == "":
        try: # get the time input from the user
            userTimeInputString = input("Enter a time in the format 'hh:mm': ") # get user input
            hours, minutes = map(int, userTimeInputString.split(":"))  # split the string into hours and minutes
            timeInput = time(hours, minutes)  # create a new time with the hours and minutes values
        except:
            print("Invalid input. Please enter a valid time in the format 'hh:mm'.")

    getSinglePackageStatusWithTime(userPackageInput, timeInput) # call the function to get a package status

def option3(): # get all package status with a time
    print("----------------------------------------------")
    timeInput = ""
    while timeInput == "":
        try:
            userTimeInputString = input("Enter a time in the format 'hh:mm': ") # get user input
            hours, minutes = map(int, userTimeInputString.split(":"))  # split the string into hours and minutes
            timeInput = time(hours, minutes)  # create a new time with the hours and minutes values
        except:
            print("Invalid input. Please enter a valid time in the format 'hh:mm'.")

    getAllPackageStatusWithTime(timeInput) # call the function to get all the packages statuses

def option4(): # exit the program
    print("----------------------------------------------")
    print("You have exited the program. Goodbye!")

menu() # call the menu function which acts as the command line interface

