import types
import pprint


def is_array(var):
    return isinstance(var, (list, tuple, dict))


def search_dicts(key, val, targets):
    for item in targets:
        if item[key] == val:
            return item

    return None


def var_dump(obj):
    pprint(dump(obj))


def dump(obj):
    '''return a printable representation of an object for debugging'''
    newobj = obj
    if isinstance(obj, list):
        newobj = []
        for item in obj:
            newobj.append(dump(item))
    elif isinstance(obj, tuple):
        temp = []
        for item in obj:
            temp.append(dump(item))
        newobj = tuple(temp)
    elif isinstance(obj, set):
        temp = []
        for item in obj:
            temp.append(str(dump(item)))
        newobj = set(temp)
    elif isinstance(obj, dict):
        newobj = {}
        for key, value in obj.items():
            newobj[str(dump(key))] = dump(value)
    elif isinstance(obj, types.FunctionType):
        newobj = repr(obj)
    elif '__dict__' in dir(obj):
        newobj = obj.__dict__.copy()
        if ' object at ' in str(obj) and not '__type__' in newobj:
            newobj['__type__']=str(obj).replace(" object at ", " #").replace("__main__.", "")
        for attr in newobj:
            newobj[attr]=dump(newobj[attr])
    return newobj
