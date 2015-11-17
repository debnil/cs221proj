import operator

# Handles clearing the cache when it gets too large
class TranspositionTable():
    def __init__(self):
        self.cache_ = {}
        # Keep track of the number of times key has been queried
        self.accessCount_ = {} 
        self.MAX_CACHE_SIZE = 500000 # Cache up to 500,000 entries
        self.PRUNE_RATE = 0.2

    def containsKey(self, key):
        if key in self.cache_:
            return True
        return False

    def value(self, key):
        if not self.containsKey(key):
            raise ValueError("Invalid key: %s" % str(key))
        self.accessCount_[key] += 1
        return self.cache_[key]

    def addKey(self, key, value):
        if self.containsKey(key):
            raise ValueError("Key %s already exists." % str(key))
        self.cache_[key] = value
        self.accessCount_[key] = 0
        if len(self.cache_) > self.MAX_CACHE_SIZE:
            self.__pruneTable()

    def updateTable(self, key, value):
        self.cache_[key] = value

    def __pruneTable(self):
        # Prune entries that aren't used frequently
        toDelete = []
        for key in sorted(self.accessCount_, key=self.accessCount_.get):
            toDelete.append(key)
            if len(toDelete) > (self.PRUNE_RATE * self.MAX_CACHE_SIZE):
                break

        for key in toDelete:
            del self.cache_[key]
            del self.accessCount_[key]
