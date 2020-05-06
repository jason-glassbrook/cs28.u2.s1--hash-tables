############################################################

from doubly_linked_list import DoublyLinkedList
from math_tools import int_min, int_max

############################################################
#   hash table
############################################################


class HashTable:
    """
    A hash table with `bucket_count` buckets
    that accepts string keys

    Implement this.
    """

    DEFAULT_BUCKET_COUNT = 128
    DEFAULT_MIN_BUCKET_COUNT = None
    DEFAULT_MAX_BUCKET_COUNT = None
    DEFAULT_RESIZE_FACTOR = 2
    DEFAULT_RESIZE_UP_FACTOR = DEFAULT_RESIZE_FACTOR
    DEFAULT_RESIZE_DOWN_FACTOR = DEFAULT_RESIZE_FACTOR
    DEFAULT_LOAD_BEFORE_RESIZE_UP = 3 / 4
    DEFAULT_LOAD_BEFORE_RESIZE_DOWN = 1 / 4
    DEFAULT_DEFAULT_VALUE = None
    DEFAULT_HASHER = "fnv1a"

    def __init__(
        self,
        bucket_count=DEFAULT_BUCKET_COUNT,
        min_bucket_count=DEFAULT_MIN_BUCKET_COUNT,
        max_bucket_count=DEFAULT_MAX_BUCKET_COUNT,
        resize_factor=DEFAULT_RESIZE_FACTOR,
        resize_up_factor=DEFAULT_RESIZE_UP_FACTOR,
        resize_down_factor=DEFAULT_RESIZE_DOWN_FACTOR,
        load_before_resize_up=DEFAULT_LOAD_BEFORE_RESIZE_UP,
        load_before_resize_down=DEFAULT_LOAD_BEFORE_RESIZE_DOWN,
        default_value=DEFAULT_DEFAULT_VALUE,
        hasher=DEFAULT_HASHER,
    ):

        self.__bucket_count = bucket_count
        self.__min_bucket_count = min_bucket_count
        self.__max_bucket_count = max_bucket_count

        self.__item_count = 0
        self.__array = [None] * bucket_count

        self.__resize_factor = resize_factor
        self.__resize_up_factor = resize_up_factor
        self.__resize_down_factor = resize_down_factor
        self.__load_before_resize_up = load_before_resize_up
        self.__load_before_resize_down = load_before_resize_down

        self.__default_value = default_value

        if hasher not in HashTable.hashers:
            raise Exception("UnknownHasherError")
        else:
            self.__hash = getattr(self, f"{hasher}_hash")

        return

    def __len__(self):
        return self.item_count

    @property
    def item_count(self):
        return self.__item_count

    @property
    def bucket_count(self):
        return self.__bucket_count

    @property
    def min_bucket_count(self):
        return self.__min_bucket_count

    @property
    def max_bucket_count(self):
        return self.__max_bucket_count

    @property
    def resize_factor(self):
        return self.__resize_factor

    @property
    def resize_up_factor(self):
        return self.__resize_up_factor

    @property
    def resize_down_factor(self):
        return self.__resize_down_factor

    @property
    def load_before_resize_up(self):
        return self.__load_before_resize_up

    @property
    def load_before_resize_down(self):
        return self.__load_before_resize_down

    @property
    def default_value(self):
        return self.__default_value

    @property
    def hash(self):
        return self.__hash

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
                break

        return node

    ########################################
    #   table mutation
    ########################################

    @property
    def load_factor(self):
        """
        The load factor of the hash table.
        """
        return (self.__item_count / self.__bucket_count)

    @property
    def bucket_count_after_resize_up(self):
        """
        The new `bucket_count` when up-sizing the hash table's internal array.
        """

        return int_min(
            self.__max_bucket_count,
            self.__bucket_count * self.__resize_up_factor,
        )

    @property
    def bucket_count_after_resize_down(self):
        """
        The new `bucket_count` when down-sizing the hash table's internal array.
        """

        return int_max(
            self.__min_bucket_count,
            self.__bucket_count / self.__resize_down_factor,
        )

    def resize(self):
        """
        Resize the hash table's internal array based on the current load factor.
        Rehash all key-value pairs.
        Returns the final `bucket_count`.
        """

        if self.load_factor >= self.load_before_resize_up:
            return self.resize_up()

        if self.load_factor <= self.load_before_resize_down:
            return self.resize_down()

        return self.bucket_count

    def resize_up(self):
        """
        Up-size the hash-table's internal array.
        Rehash all key-value pairs.
        Returns the final `bucket_count`.
        """

        return self.bucket_count

    def resize_down(self):
        """
        Down-size the hash-table's internal array.
        Rehash all key-value pairs.
        Returns the final `bucket_count`.
        """

        return self.bucket_count

    ########################################
    #   item access
    ########################################

    def push_item(self, key, value):
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

    def find_item(self, key):
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

    def pop_item(self, key):
        """
        Remove the value stored with the given key.
        """

        index = self.hash_index(key)
        chain = self.__array[index]
        value = None

        # if there's a chain at `index`, then...
        if chain is not None:

            # search it for `(key, value)`
            node = self.find_node_by_key(key, chain)

            # if it exists, remove it
            if node is not None:
                (__, value) = chain.pop_node(node)

            # else, do nothing

        # else, do nothing

        # if the chain is now empty, remove it
        if len(chain) == 0:
            self.__array[index] = None

        # print(f"array[{repr(index)}] := {repr(value)}")
        return value

    ####################
    #   other names
    ####################

    #-------------------
    #   push_item
    #-------------------

    def __setitem__(self, key, value):
        self.push_item(key, value)
        return

    def set(self, key, value):
        self.push_item(key, value)
        return

    def put(self, key, value):
        self.push_item(key, value)
        return

    def push(self, key, value):
        self.push_item(key, value)
        return

    #-------------------
    #   find_item
    #-------------------

    def __getitem__(self, key):
        return self.find_item(key)

    def get(self, key):
        return self.find_item(key)

    def find(self, key):
        return self.find_item(key)

    #-------------------
    #   pop_item
    #-------------------

    def __delitem__(self, key):
        self.pop_item(key)
        return

    def delete(self, key):
        self.pop_item(key)
        return

    def pop(self, key):
        return self.pop_item(key)


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
