############################################################

from doubly_linked_list import DoublyLinkedList

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
        hasher="fnv1a",
    ):

        self.__bucket_count = bucket_count
        self.__min_bucket_count = min_bucket_count
        self.__max_bucket_count = max_bucket_count

        self.__default_value = default_value

        if hasher not in HashTable.hashers:
            raise Exception("UnknownHasherError")
        else:
            self.__hash = getattr(self, f"{hasher}_hash")

        self.__array = [None] * bucket_count

        return

    def __len__(self):

        return len(self.__array)

    ########################################
    #   hashing functions
    ########################################

    hashers = (
        "naive",
        "djb2",
        "fnv1",
        "fnv1a",
    )

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

        index = self.__hash(key) % self.__bucket_count

        # print(f"hash_index({repr(key)}) => {repr(index)}")

        return index

    @staticmethod
    def find_node_by_key(key, chain):

        node = None
        for ((k, v), n) in chain:
            if k == key:
                node = n

        return node

    ########################################
    #   table mutation
    ########################################

    def __setitem__(self, key, value):
        """
        Set the value stored with the given key.

        Hash collisions should be handled with Linked List Chaining.
        """

        index = self.hash_index(key)
        chain = self.__array[index]

        # if there's a chain at `index`, then...
        if chain is not None:

            # search it for `(key, value)`
            node = self.find_node_by_key(key, chain)

            # if found, update `value`
            if node is not None:
                node.value = (key, value)

            # else, append `(key, value)` to the chain
            else:
                chain.push_to_tail((key, value))

        # else, create a new chain
        else:
            self.__array[index] = DoublyLinkedList(value=(key, value))

        # print(f"array[{repr(index)}] := {repr(value)}")
        return

    def __getitem__(self, key):
        """
        Get the value stored with the given key.

        Returns `default_value` if the key is not found.
        """

        index = self.hash_index(key)
        chain = self.__array[index]
        value = self.__default_value

        # if there's a chain at `index`, then...
        if chain is not None:

            # search it for `(key, value)`
            node = self.find_node_by_key(key, chain)

            # if found, return its `value`
            if node is not None:
                (__, value) = node.value

            # else, return the default value (which we're already doing)

        # else, there's nothing to do

        # print(f"array[{repr(index)}] => {repr(value)}")
        return value

    def __delitem__(self, key):
        """
        Remove the value stored with the given key.
        """

        index = self.hash_index(key)
        chain = self.__array[index]

        # if there's a chain at `index`, then...
        if chain is not None:

            # search it for `(key, value)`
            node = self.find_node_by_key(key, chain)

            # if it exists, remove it
            if node is not None:
                chain.pop_node(node)

            # else, do nothing

        # else, do nothing

        # if the chain is now empty, remove it
        if len(chain) == 0:
            self.__array[index] = None

        # print(f"array[{repr(index)}] := {repr(value)}")
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
