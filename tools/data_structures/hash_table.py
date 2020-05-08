############################################################

from tools.math_tools import int_min, int_max
from tools.data_structures.doubly_linked_list import DoublyLinkedList

############################################################
#   hash table
############################################################


class HashTable:
    """
    A hash table with `bucket_count` buckets
    that accepts string keys.

    Implement this.
    """

    DEFAULT_BUCKET_COUNT = 0o100
    DEFAULT_MIN_BUCKET_COUNT = 0o10
    DEFAULT_MAX_BUCKET_COUNT = 0o100000
    DEFAULT_RESIZE_FACTOR = 2
    DEFAULT_RESIZE_UP_FACTOR = DEFAULT_RESIZE_FACTOR
    DEFAULT_RESIZE_DOWN_FACTOR = DEFAULT_RESIZE_FACTOR
    DEFAULT_LOAD_BEFORE_RESIZE_UP = 3 / 4
    DEFAULT_LOAD_BEFORE_RESIZE_DOWN = 1 / 4
    DEFAULT_DEFAULT_VALUE = None
    DEFAULT_HASHER = "fnv1a"
    DEFAULT_DEBUG = False

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
        debug=DEFAULT_DEBUG,
    ):

        self.debug = debug

        self.__bucket_count = bucket_count
        self.min_bucket_count = int_min(bucket_count, min_bucket_count)
        self.max_bucket_count = int_max(bucket_count, max_bucket_count)

        self.__item_count = 0
        self.__array = [None] * bucket_count

        self.resize_factor = resize_factor
        self.resize_up_factor = resize_up_factor
        self.resize_down_factor = resize_down_factor
        self.load_before_resize_up = load_before_resize_up
        self.load_before_resize_down = load_before_resize_down

        self.default_value = default_value

        if hasher not in HashTable.hashers:
            raise Exception("UnknownHasherError")
        else:
            self.__hash = getattr(self, f"{hasher}_hash")

        return

    #-----------------------------------------------------------

    def __len__(self):
        return self.item_count

    #-----------------------------------------------------------

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, value):
        self.__debug = bool(value)
        return

    @debug.deleter
    def debug(self):
        setattr(self, "debug", self.DEFAULT_DEBUG)
        return

    def should_debug_print(self, local_debug=None):
        if local_debug is not None:
            return bool(local_debug)
        else:
            return self.debug

    def debug_print(self, *messages, local_debug=None):
        if self.should_debug_print(local_debug=local_debug):
            print(*messages)
        return

    #-----------------------------------------------------------

    @property
    def item_count(self):
        return self.__item_count

    #-----------------------------------------------------------

    @property
    def bucket_count(self):
        return self.__bucket_count

    #-----------------------------------------------------------

    @property
    def min_bucket_count(self):
        return self.__min_bucket_count

    @min_bucket_count.setter
    def min_bucket_count(self, value):
        self.__min_bucket_count = value
        return

    @min_bucket_count.deleter
    def min_bucket_count(self):
        setattr(self, "min_bucket_count", self.DEFAULT_MIN_BUCKET_COUNT)
        return

    #-----------------------------------------------------------

    @property
    def max_bucket_count(self):
        return self.__max_bucket_count

    @max_bucket_count.setter
    def max_bucket_count(self, value):
        self.__max_bucket_count = value
        return

    @max_bucket_count.deleter
    def max_bucket_count(self):
        setattr(self, "max_bucket_count", self.DEFAULT_MAX_BUCKET_COUNT)
        return

    #-----------------------------------------------------------

    @property
    def resize_factor(self):
        return self.__resize_factor

    @resize_factor.setter
    def resize_factor(self, value):
        self.__resize_factor = value
        setattr(self, "resize_up_factor", value)
        setattr(self, "resize_down_factor", value)
        return

    @resize_factor.deleter
    def resize_factor(self):
        setattr(self, "resize_factor", self.DEFAULT_RESIZE_FACTOR)
        delattr(self, "resize_up_factor")
        delattr(self, "resize_down_factor")
        return

    #-----------------------------------------------------------

    @property
    def resize_up_factor(self):
        return self.__resize_up_factor

    @resize_up_factor.setter
    def resize_up_factor(self, value):
        self.__resize_up_factor = value
        return

    @resize_up_factor.deleter
    def resize_up_factor(self):
        setattr(self, "resize_up_factor", self.DEFAULT_RESIZE_UP_FACTOR)
        return

    #-----------------------------------------------------------

    @property
    def resize_down_factor(self):
        return self.__resize_down_factor

    @resize_down_factor.setter
    def resize_down_factor(self, value):
        self.__resize_down_factor = value
        return

    @resize_down_factor.deleter
    def resize_down_factor(self):
        setattr(self, "resize_down_factor", self.DEFAULT_RESIZE_DOWN_FACTOR)
        return

    #-----------------------------------------------------------

    @property
    def load_before_resize_up(self):
        return self.__load_before_resize_up

    @load_before_resize_up.setter
    def load_before_resize_up(self, value):
        self.__load_before_resize_up = value
        return

    @load_before_resize_up.deleter
    def load_before_resize_up(self):
        setattr(self, "load_before_resize_up", self.DEFAULT_LOAD_BEFORE_RESIZE_UP)
        return

    #-----------------------------------------------------------

    @property
    def load_before_resize_down(self):
        return self.__load_before_resize_down

    @load_before_resize_down.setter
    def load_before_resize_down(self, value):
        self.__load_before_resize_down = value
        return

    @load_before_resize_down.deleter
    def load_before_resize_down(self):
        setattr(self, "load_before_resize_down", self.DEFAULT_LOAD_BEFORE_RESIZE_DOWN)
        return

    #-----------------------------------------------------------

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        self.__default_value = value
        return

    @default_value.deleter
    def default_value(self):
        setattr(self, "default_value", self.DEFAULT_DEFAULT_VALUE)
        return

    #-----------------------------------------------------------

    @property
    def hash(self):
        return self.__hash

    ############################################################
    #   hashing functions
    ############################################################

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

    ############################################################
    #   indexing
    ############################################################

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

    ############################################################
    #   table mutation
    ############################################################

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

    def resize(self, local_debug=None):
        """
        Resize the hash table's internal array based on the current load factor.
        Rehash all key-value pairs.
        Returns the final `bucket_count`.
        """

        def debug_print(*messages):
            self.debug_print(
                f"resize()",
                *messages,
                local_debug=local_debug,
            )
            return

        debug_print()
        debug_print(f"... load_factor = {self.load_factor}",)

        new_bucket_count = self.__bucket_count

        if self.load_factor >= self.__load_before_resize_up:

            debug_print(f"... resizing up",)

            new_bucket_count = self.resize_up()

        elif self.load_factor <= self.__load_before_resize_down:

            debug_print(f"... resizing down",)

            new_bucket_count = self.resize_down()

        else:

            debug_print(f"... not resizing",)

            pass

        debug_print(f"... new_bucket_count = {new_bucket_count}",)

        return new_bucket_count

    def resize_up(self, local_debug=None):
        """
        Up-size the hash-table's internal array.
        Rehash all key-value pairs.
        Returns the final `bucket_count`.
        """

        def debug_print(*messages):
            self.debug_print(
                f"resize_up()",
                *messages,
                local_debug=local_debug,
            )
            return

        debug_print()

        old_bucket_count = self.__bucket_count
        new_bucket_count = self.bucket_count_after_resize_up

        if new_bucket_count > old_bucket_count:

            debug_print(f"... resizing",)

            old_array = self.__array

            self.__bucket_count = new_bucket_count
            self.__array = [None] * new_bucket_count

            self.rehash_from_array(old_array)

        # else, no need to rehash
        else:

            debug_print(f"... not resizing",)

            pass

        return new_bucket_count    # ... == old_bucket_count if resize skipped

    def resize_down(self, local_debug=None):
        """
        Down-size the hash-table's internal array.
        Rehash all key-value pairs.
        Returns the final `bucket_count`.
        """

        def debug_print(*messages):
            self.debug_print(
                f"resize_down()",
                *messages,
                local_debug=local_debug,
            )
            return

        debug_print()

        old_bucket_count = self.__bucket_count
        new_bucket_count = self.bucket_count_after_resize_down

        if new_bucket_count < old_bucket_count:

            debug_print(f"... resizing",)

            old_array = self.__array

            self.__bucket_count = new_bucket_count
            self.__array = [None] * new_bucket_count

            self.rehash_from_array(old_array)

        # else, no need to rehash
        else:

            debug_print(f"... not resizing",)

            pass

        return new_bucket_count    # ... == old_bucket_count if resize skipped

    def rehash_from_array(self, from_array):
        """
        Rehash the items in `from_array` to the hash table's internal array.
        """

        for chain in from_array:
            if chain is not None:
                for ((key, value), node) in chain:
                    self.push_item(key, value, should_resize=False)

        return

    ############################################################
    #   item access
    ############################################################

    def push_item(self, key, value, should_resize=True, local_debug=None):
        """
        Set `key`'s value to `value` in the hash table.
        Hash collisions are handled with linked list chaining.
        Returns the hash table's new item count.
        """

        def debug_print(*messages):
            self.debug_print(
                f"push_item({repr(key)}, {repr(value)})",
                *messages,
                local_debug=local_debug,
            )
            return

        debug_print()

        index = self.hash_index(key)
        chain = self.__array[index]

        # if there's a chain at `index`, then...
        if chain is not None:

            debug_print(f"... there is a chain",)

            # search it for `(key, value)`
            node = self.find_node_by_key(key, chain)

            # if found, update `value`
            if node is not None:

                debug_print(
                    f"... key found",
                    f"... updating value",
                )

                node.value = (key, value)

            # else, insert it
            else:

                debug_print(
                    f"... key not found",
                    f"... inserting (key, value)",
                )

                self.__item_count += 1
                chain.push_to_tail((key, value))

        # else, create a new chain
        else:

            debug_print(
                f"... there is no chain",
                f"... inserting new chain with (key, value)",
            )

            self.__item_count += 1
            self.__array[index] = DoublyLinkedList(value=(key, value))

        # maybe resize
        if should_resize:
            self.resize()

        # print(f"array[{repr(index)}] := {repr(value)}")
        return self.__item_count

    def find_item(self, key, local_debug=None):
        """
        Get `key`'s value in the hash table.
        Returns the key's value or `default_value` if the key is not found.
        """

        def debug_print(*messages):
            self.debug_print(
                f"find_item({repr(key)})",
                *messages,
                local_debug=local_debug,
            )
            return

        debug_print()

        index = self.hash_index(key)
        chain = self.__array[index]
        value = self.__default_value

        # if there's a chain at `index`, then...
        if chain is not None:

            debug_print(f"... there is a chain",)

            # search it for `(key, value)`
            node = self.find_node_by_key(key, chain)

            # if found, return its `value`
            if node is not None:

                debug_print(
                    f"... key found",
                    f"... getting value",
                )

                (__, value) = node.value

            # else, return the default value (which we're already doing)
            else:

                debug_print(
                    f"... key not found",
                    f"... passing",
                )

                pass

        # else, do nothing
        else:

            debug_print(
                f"... there is no chain",
                f"... passing",
            )

            pass

        # else, there's nothing to do

        # print(f"array[{repr(index)}] => {repr(value)}")
        return value

    def pop_item(self, key, should_resize=True, local_debug=None):
        """
        Remove `key`'s value in the hash table.
        Returns the removed value and the hash table's new item count.
        """

        def debug_print(*messages):
            self.debug_print(
                f"pop_item({repr(key)})",
                *messages,
                local_debug=local_debug,
            )
            return

        debug_print()

        index = self.hash_index(key)
        chain = self.__array[index]
        value = None

        # if there's a chain at `index`, then...
        if chain is not None:

            debug_print(f"... there is a chain",)

            # search it for `(key, value)`
            node = self.find_node_by_key(key, chain)

            # if it exists, remove it
            if node is not None:

                debug_print(
                    f"... key found",
                    f"... deleting (key, value)",
                )

                self.__item_count -= 1
                (__, value) = chain.pop_node(node)

                # if the chain is now empty, remove it
                if len(chain) == 0:

                    debug_print(
                        f"... chain is empty",
                        f"... deleting",
                    )

                    self.__array[index] = None

            # else, do nothing
            else:

                debug_print(
                    f"... key not found",
                    f"... passing",
                )

                pass

        # else, do nothing
        else:

            debug_print(
                f"... there is no chain",
                f"... passing",
            )

            pass

        # maybe resize
        if should_resize:
            self.resize()

        # print(f"array[{repr(index)}] := {repr(value)}")
        return (value, self.__item_count)

    ########################################
    #   other names
    ########################################

    #---------------------------------------
    #   push_item
    #---------------------------------------

    def __setitem__(self, key, value, **kwargs):
        self.push_item(key, value, **kwargs)
        return

    def set(self, key, value, **kwargs):
        return self.push_item(key, value, **kwargs)

    def put(self, key, value, **kwargs):
        return self.push_item(key, value, **kwargs)

    def push(self, key, value, **kwargs):
        return self.push_item(key, value, **kwargs)

    #---------------------------------------
    #   find_item
    #---------------------------------------

    def __getitem__(self, key, **kwargs):
        return self.find_item(key, **kwargs)

    def get(self, key, **kwargs):
        return self.find_item(key, **kwargs)

    def find(self, key, **kwargs):
        return self.find_item(key, **kwargs)

    #---------------------------------------
    #   pop_item
    #---------------------------------------

    def __delitem__(self, key, **kwargs):
        self.pop_item(key, **kwargs)
        return

    def delete(self, key, **kwargs):
        self.pop_item(key, **kwargs)
        return

    def pop(self, key, **kwargs):
        return self.pop_item(key, **kwargs)


############################################################

if __name__ == "__main__":

    ht = HashTable(bucket_count=2, debug=True)

    ht.put("line_1", "Tiny hash table!")
    ht.put("line_2", "Filled beyond capacity!")
    ht.put("line_3", "Linked list saves the day!")

    print()

    # Test storing beyond bucket_count
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    # Test resizing
    old_bucket_count = ht.bucket_count
    ht.resize()
    new_bucket_count = ht.bucket_count

    print(f"\nResized from {old_bucket_count} to {new_bucket_count}.\n")

    # Test if data intact after resizing
    print(ht.get("line_1"))
    print(ht.get("line_2"))
    print(ht.get("line_3"))

    print()
