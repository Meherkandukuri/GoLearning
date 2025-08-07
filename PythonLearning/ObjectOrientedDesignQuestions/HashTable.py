class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, initial_capacity=8, load_factor_threshold=0.75):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor_threshold = load_factor_threshold
        self.table = [[] for _ in range(self.capacity)]

    def _hash_function(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        old_table = self.table
        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0  # Will be recalculated during reinsertion

        for bucket in old_table:
            for item in bucket:
                self.set(item.key, item.value)

    def set(self, key, value):
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

        hash_index = self._hash_function(key)
        bucket = self.table[hash_index]

        for item in bucket:
            if item.key == key:
                item.value = value
                return

        bucket.append(Item(key, value))
        self.size += 1

    def get(self, key):
        hash_index = self._hash_function(key)
        bucket = self.table[hash_index]

        for item in bucket:
            if item.key == key:
                return item.value

        raise KeyError(f'Key {key!r} not found')

    def remove(self, key):
        hash_index = self._hash_function(key)
        bucket = self.table[hash_index]

        for index, item in enumerate(bucket):
            if item.key == key:
                del bucket[index]
                self.size -= 1
                return

        raise KeyError(f'Key {key!r} not found')

    # Pythonic enhancements
    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def __len__(self):
        return self.size

    def __str__(self):
        items = []
        for bucket in self.table:
            for item in bucket:
                items.append(f"{repr(item.key)}: {repr(item.value)}")
        return "{" + ", ".join(items) + "}"
