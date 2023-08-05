# functions.py
## classless utility functions

import string

# function decorators

## updateClient
### updates client if expired
def updateClient(func):
    def func_wrapper(self, *args, **kwargs):
        if (self.client.auth.access_token_expired):
            self.client.login()
        return func(self, *args, **kwargs)
    return func_wrapper

## arrayedCheck
### expands typechecking to accommodate arrays
def arrayedCheck(func):
    def func_wrapper(value):
        if isinstance(value, list):
            for val in value:
                if not func(val):
                    return False
            return True
        return func(value)
    return func_wrapper

# classless functions

## trim
### removes leading/trailing spaces/newlines or other
### characters in trimSet
def trim(data, trimSet=None):
    if trimSet is None: trimSet = set([" ", "\n"])
    begin = 0
    while (len(data) > begin and data[begin] in trimSet):
        begin += 1
    data = data[begin:]
    end = len(data) - 1
    while (end >= 0 and data[end] in trimSet):
        end -= 1
    data = data[:(end+1)]
    return data

## reverseDict
### reverses a dictionary
### only works for 1:1 mappings
def reverseDict(dictToReverse):
    result = dict()
    for key in dictToReverse:
        result[dictToReverse[key]] = key
    return result

## dropIndices
### given a list of elements
### and a set of indices to drop
### returns a new list with the values
### at those indices removed from the list
def dropIndices(data, indices):
    result = list()
    for i in xrange(len(data)):
        if i not in indices:
            result.append(data[i])
    return result

## isType
### given a string and a constraintString
### returns whether all elements of the
### value string are also elements
### of the constraint string
def isType(value, constraintString):
    value = str(value)
    if (len(value) == 0): return False
    constraintSet = set(list(constraintString))
    for i in value:
        if i not in constraintSet:
            return False
    return True

## isInteger
@arrayedCheck
def isInteger(value):
    if (isinstance(value, int)): return True
    value = str(value)
    if (len(value) > 0 and value[0] in "-+"):
        value = value[1:]
    return isType(value, string.digits)

## isNumeric
@arrayedCheck
def isNumeric(value):
    if (isinstance(value, int) or isinstance(value, float)):
        return True
    value = str(value)
    if (len(value) > 0 and value[0] in "-+"):
        value = value[1:]
    return (isType(value, (string.digits + "."))
            and value.count(".") <= 1)

## isAlpha
@arrayedCheck
def isAlpha(value):
    return isType(value, string.ascii_letters)

## is Alphanumeric
@arrayedCheck
def isAlphanumeric(value):
    return isType(value,
                  (string.ascii_letters + string.digits))

## isString
@arrayedCheck
def isString(value):
    return isinstance(value, str)

## isBoolean
@arrayedCheck
def isBoolean(value):
    return (isinstance(value, bool) or
            str(value) in {'TRUE', 'FALSE'})

## is Array
def isArray(value):
    return (isinstance(value, list) or isinstance(value, str)
            or isinstance(value, int))

## isPositive
@arrayedCheck
def isPositive(value):
    if (isinstance(value, int) or isinstance(value, float)):
        return (value > 0)
    value = str(value)
    if (len(value) > 0 and value[0] == "-"):
        return False
    valSet = set(list(value))
    if "+" in valSet: valSet.remove("+")
    if "0" in valSet: valSet.remove("0")
    if "." in valSet: valSet.remove(".")
    return (len(valSet) > 0)

## isNonnegative
@arrayedCheck
def isNonnegative(value):
    if (isinstance(value, int) or isinstance(value, float)):
        return (value >= 0)
    value = str(value)
    return (len(value) == 0 or value[0] != "-")

## convertToKeyed
### given a list of dicts and a parameter to convert to a key
### returns a dictionary that uses said parameter as key
### ignoring all members that don't have said parameter
### if allowDuplicates is True, the result will map
### from values of the parameter to lists containing
### record dictionaries
###
### NOTE: make sure all values that the param can take
### are hashable
def convertToKeyed(data, param, allowDuplicates=False):
    result = dict()
    for item in data: # item is a dictionary
        if param in item:
            if allowDuplicates:
                if item[param] not in result:
                    result[item[param]] = list()
                result[item[param]].append(item)
            else:
                result[item[param]] = item
    return result

## flattenList
### given a list that may contain other lists,
### flattens said list
def flattenList(data):
    result = list()
    for item in data:
        if (isinstance(item, list) or
            isinstance(item, tuple)):
            result += flattenList(item)
        else:
            result.append(item)
    return result
