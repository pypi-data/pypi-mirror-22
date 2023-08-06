import re
from random import shuffle, choice

re_nests  = r"\((.*?)\)"
re_square = r"\[.*?\]"
re_curly  = r"\{.*?\}"
re_chars  = r"[^[\](){}]"
br_pairs = {"(":")",
            ")":"(",
            "[":"]",
            "]":"[",
            "{":"}",
            "}":"{"}

class PlayString:
    """ Container for PCHAR objects """
    contains_nest = False
    def __init__(self, string):
        self.string   = list(string)
        self.original = str(string)
    def __repr__(self):
        return repr(self.string)
    def __len__(self):
        return len(self.string)
    def __getitem__(self, key):
        return self.string[key]
    def __setitem__(self, key, value):
        self.string[key] = value
    def get_dur(self):
        """ Returns a list of durations """
        return [char.get_dur() for char in self.string]
    def multiply(self, value):
        for char in self.string:
            char.multiply(value)
        return
    def append(self, item):
        self.string.append(item)
    def extend(self, items):
        self.string.extend(items)
    def index(self, sub, start=0):
        """ Returns the index of the closing bracket """
        br = "([{"[")]}".index(sub)]
        count = 0
        for i in range(start, len(self.string)):
            char = self.string[i]
            if char == br:
                count += 1
            elif char == sub:
                if count > 0:
                    count -= 1
                else:
                    return i
        raise ParseError("Closing bracket '%s' missing in string '%s'" % (sub, self.original))

    # Return strings
    
    def shuffle(self):
        """ Proper method of shuffling playstrings as opposed to shuffle() """

        # 1. Get all the characters out in order

        chars = re.findall(re_chars, self.original)

        string = re.sub(re_chars, "%s", self.original)

        # 2. Shuffle

        shuffle(chars)

        # 3. replace

        return string % tuple(chars)

    def mirror(self):
        l = list(self.original)
        l.reverse()
        for i, char in enumerate(l):
            if char in br_pairs.keys():
                l[i] = br_pairs[char]
        return "".join(l)

    def rotate(self, n=1):
        # 1. Get all the characters out in order

        chars = re.findall(re_chars, self.original)

        string = re.sub(re_chars, "%s", self.original)

        # 2. Rotate
    
        n = int(n)

        chars = chars[n:] + chars[:n]

        return string % tuple(chars)


##class PlayGroup(tuple):
##    def __init__(self, seq=[]):
##        data = []
##        for item in seq:
##            if isinstance(item, self.__class__):
##                data.extend(item)
##            else:
##                data.append(item)
##        tuple.__init__(self, data)
##        self.data = data
##    def __repr__(self):
##        return "<" + tuple.__repr__(self)[1:-1] + ">"
##    def string(self):
##        """ Returns the form a PlayGroup takes in a PlayString """
##        return "[" + "".join([(s.string() if hasattr(s, "string") else str(s)) for s in self]) + "]"
##    def __len__(self):
##        return 1
##    def __eq__(self, other):
##        # Can do "[xx]" == PlayGroup(x,x)
##        if type(other) == str:
##            if other[0] == "[" and other[-1] == "]":
##                new_data = other[1:-1]
##                if len(new_data) == len(self.data):
##                    return all([new_data[i] == self.data[i] for i in range(len(new_data))])
##        else:
##            return tuple.__eq__(self, other)
##        return False
##    def divide(self, value):
##        for item in self:
##            item.divide(value)
##        return self
##    def mirror(self):
##        return self.__class__(list(reversed(self.data)))

##class RandomPlayGroup(object):
##    def __init__(self, seq, dur=1):
##        self.data = []
##        self.dur  = dur
##        for item in seq:
##            if type(item) is list:
##                self.data.extend(item)
##            else:
##                self.data.append(item)
##    def now(self):
##        return choice(self.data)
##    def string(self):
##        """ Returns the form a PlayGroup takes in a PlayString """
##        return "{" + "".join([(s.string() if hasattr(s, "string") else str(s)) for s in self.data]) + "}"
##    def __len__(self):
##        return 1
##    def __repr__(self):
##        return "<?" + repr(self.data)[1:-1] + ">"
##    def divide(self, value):
##        self.dur /= float(value)
##        return self
            
class PCHAR:
    def __init__(self, char, dur=1):
        self.char = char
        self.dur  = dur
    def __len__(self):
        return 1
    def __str__(self):
        return self.char
    def __repr__(self):
        return repr(self.char)
    def __eq__(self, other):
        return str(self.char) == str(other)
    def __ne__(self, other):
        return str(self.char) != str(other)
    def get_dur(self):
        return self.dur
    def multiply(self, val):
        self.dur *= float(val)
        return
    def divide(self, value):
        self.dur /= float(value)


class ParseError(Exception):
    pass
