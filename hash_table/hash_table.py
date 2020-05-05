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
    A hash table with `bucket_count` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, bucket_count=128, default_value=None):

        self.__bucket_count = bucket_count
        self.__default_value = default_value
        self.__array = [default_value] * bucket_count

        return

    def __len__(self):

        return len(self.__array)

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

        Implement this and/or FNV-1.
        """
        pass

    def fnv1_hash(self, string):
        """
        FNV-1 64-bit hash function

        Implement this and/or DJB2.
        """
        pass

    ########################################
    #   indexing
    ########################################

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage `bucket_count` of the hash table.
        """

        index = self.naive_hash(key) % self.__bucket_count
        # index = self.fnv1_hash(key) % self.__bucket_count
        # index = self.djb2_hash(key) % self.__bucket_count

        print(f"hash_index({repr(key)}) => {repr(index)}")
        return index

    ########################################
    #   table mutation
    ########################################

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """

        index = self.hash_index(key)
        self.__array[index] = value

        print(f"array[{repr(index)}] := {repr(value)}")
        return

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """

        index = self.hash_index(key)
        self.__array[index] = self.__default_value

        print(f"array[{repr(index)}] := {repr(self.__default_value)}")
        return

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """

        index = self.hash_index(key)
        value = self.__array[index]

        print(f"array[{repr(index)}] => {repr(value)}")
        return

    def resize(self):
        """
        Doubles the `bucket_count` of the hash table and
        rehash all key/value pairs.

        Implement this.
        """


############################################################

if __name__ == "__main__":

    ht = HashTable(bucket_count=2)

    ht.put("line_1", "Tiny hash table!")
    ht.put("line_2", "Filled beyond capacity!")
    ht.put("line_3", "Linked list saves the day!")

    print()

    # Test storing beyond bucket_count
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    # Test resizing
    old_bucket_count = len(ht)
    ht.resize()
    new_bucket_count = len(ht)

    print(f"\nResized from {old_bucket_count} to {new_bucket_count}.\n")

    # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print()
