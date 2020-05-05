############################################################
#   hash table entry
############################################################


class HashTableEntry:
    """
    Hash Table entry, as a linked list node.
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


############################################################
#   hash table
############################################################


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    ########################################
    #   hashing functions
    ########################################

    def naive_hash(self, string):
        """
        Naïve hash from string to integer.
        """

        string_bytes = str(string).encode()

        total = 0

        for b in string_bytes:
            total += b
            total &= 0xffffffff

        return total

    def djb2_hash(self, string):
        """
        DJB2 32-bit hash function

        Implement this, and/or FNV-1.
        """
        pass

    def fnv1_hash(self, string):
        """
        FNV-1 64-bit hash function

        Implement this, and/or DJB2.
        """
        pass

    ########################################
    #   indexing
    ########################################

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.naive_hash(key) % self.capacity
        # return self.fnv1(key) % self.capacity
        # return self.djb2(key) % self.capacity

    ########################################
    #   table mutation
    ########################################

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """

    def resize(self):
        """
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Implement this.
        """


############################################################

if __name__ == "__main__":

    ht = HashTable(2)

    ht.put("line_1", "Tiny hash table")
    ht.put("line_2", "Filled beyond capacity")
    ht.put("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print("")
