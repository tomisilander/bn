#!/usr/bin/python

"""Caching dictionary that uses access times to decide which objects to
flush from the cache.

When instantiating, you can set the maximum number of key/value pairs
to maintain in the cache:

    c = Cache(size=1000)

When the maximum size of the cache is reached, it will be resized
automatically to 95% of its maximum size the next time a new key is added to
the dictionary.  The least recently accessed items will be the ones that are
flushed.
"""

import UserDict, time

class Cache(UserDict.UserDict):
    """simple cache that uses least recently accessed time to trim size"""
    def __init__(self,data=None,size=100):
        UserDict.UserDict.__init__(self,data)
        self.size = size

    def resize(self):
        """trim cache to no more than 95% of desired size"""
        trim = max(0, int(len(self.data)-0.95*self.size))
        if trim:
            # don't want self.items() because we must sort list by access time
            values = map(None, self.data.values(), self.data.keys())
            values.sort()
            for val,k in values[0:trim]:
                del self.data[k]

    def __setitem__(self,key,val):
        if (not self.data.has_key(key) and
	    len(self.data) >= self.size):
            self.resize()
        self.data[key] = (time.time(), val)

    def __getitem__(self,key):
	"""like normal __getitem__ but updates time of fetched entry"""
        val = self.data[key][1]
        self.data[key] = (time.time(),val)
        return val

    def get(self,key,default=None):
	"""like normal __getitem__ but updates time of fetched entry"""
        try:
            return self[key]
        except KeyError:
            return default

    def values(self):
	"""return values, but eliminate access times first"""
        vals = list(self.data.values())
        for i in range(len(vals)):
            vals[i] = vals[i][1]
        return tuple(vals)

    def items(self):
        return map(None, self.keys(), self.values())

    def copy(self):
	return self.__class__(self.data, self.size)

    def update(self, dict):
	for k in dict.keys():
	    self[k] = dict[k]

def _test(size=100):
    c = Cache(size=size)
    for i in range(120):
	c[i] = i
	if i > 5:
	    x = c[5]
	time.sleep(0.01)
    x = c.keys()
    x.sort()
    assert x == [5]+range(21,120), x
    c.update({1:1})
    x = c.keys()
    x.sort()
    assert x == [1,5]+range(26,120), x

    print "all cache tests passed"

if __name__ == "__main__":
    _test()

