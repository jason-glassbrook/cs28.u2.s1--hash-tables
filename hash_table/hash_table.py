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

    def __init__(
        self,
        bucket_count=128,
        min_bucket_count=None,
        max_bucket_count=None,
        default_value=None,
    ):

        self.__bucket_count = bucket_count
        self.__min_bucket_count = min_bucket_count
        self.__max_bucket_count = max_bucket_count

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

        s_bytes = str(string).encode()
        s_hash = 0

        for b in s_bytes:
            s_hash += b
            s_hash &= 0xFFFFFFFF

        return s_hash

    def djb2_hash(self, string):
        """
        DJB2 32-bit hash function
        """

        s_bytes = str(string).encode()
        s_hash = 5381

        for b in s_bytes:
            s_hash *= 0x21
            s_hash += b
            s_hash &= 0xFFFFFFFF

        return s_hash

    def fnv1_hash(self, string):
        """
        FNV-1 64-bit hash function
        """

        s_bytes = str(string).encode()
        s_hash = 0xCBF29CE484222325

        for b in s_bytes:
            s_hash *= 0x100000001B3
            s_hash += b
            s_hash &= 0xFFFFFFFFFFFFFFFF

        return s_hash

    def fnv1a_hash(self, string):
        """
        FNV-1a 64-bit hash function
        """

        s_bytes = str(string).encode()
        s_hash = 0xCBF29CE484222325

        for b in s_bytes:
            s_hash += b
            s_hash *= 0x100000001B3
            s_hash &= 0xFFFFFFFFFFFFFFFF

        return s_hash

    ########################################
    #   indexing
    ########################################

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage `bucket_count` of the hash table.
        """

        # index = self.naive_hash(key) % self.__bucket_count
        # index = self.djb2_hash(key) % self.__bucket_count
        # index = self.fnv1_hash(key) % self.__bucket_count
        index = self.fnv1a_hash(key) % self.__bucket_count

        print(f"hash_index({repr(key)}) => {repr(index)}")

        return index

    ########################################
    #   table mutation
    ########################################

    def __setitem__(self, key, value):
        """
        Set the value stored with the given key.

        Hash collisions should be handled with Linked List Chaining.
        """

        index = self.hash_index(key)
        self.__array[index] = value

        print(f"array[{repr(index)}] := {repr(value)}")

        return

    def __getitem__(self, key):
        """
        Get the value stored with the given key.

        Returns `default_value` if the key is not found.
        """

        index = self.hash_index(key)
        value = self.__array[index]

        print(f"array[{repr(index)}] => {repr(value)}")

        return value

    def __delitem__(self, key):
        """
        Remove the value stored with the given key.
        """

        self[key] = self.__default_value

        return

    def resize(self):
        """
        Doubles the `bucket_count` of the hash table and
        rehash all key/value pairs.

        Implement this.
        """
        pass

    ####################
    #   other names
    ####################

    def set(self, key, value):
        self[key] = value
        return

    def put(self, key, value):
        self[key] = value
        return

    def get(self, key):
        return self[key]

    def delete(self, key):
        del self[key]
        return


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
