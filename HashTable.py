class ChainingHashTable: # hashtable class
    # initialize an empty hash table, Space-Time Complexities are O(1)
    def __init__(self, initial_capacity=40): # capacity will be for 40 packages
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # time complexity is O(n) and space complexity is O(1)
    def insert(self, key, item): # insert an item into the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Part F lookup function
    # time complexity is O(n) and space complexity is O(1)
    def search(self, key): # lookup an item in the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # time complexity is O(n) and space complexity is O(1)
    def remove(self, key): # remove an item from the hash table
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
