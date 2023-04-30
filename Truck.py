class Truck: # truck class
    # Space-Time Complexities are O(1)
    def __init__(self, id, location, mileage,  packages):
        self.id = id # a unique identifier for the truck
        self.location = location # current location of a truck
        self.mileage = mileage # mileage of the truck
        self.packages = packages # associated packages with the truck

    # Space-Time Complexities are O(1)
    def add(self, packageId): # add a package to a truck
        self.packages.add(packageId)

    def __str__(self):
        return "%s, %s, %s, %s" % (self.id, self.location, self.mileage, self.packages)