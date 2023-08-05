from __future__ import unicode_literals
from datetime import datetime


EPOCH = datetime.utcfromtimestamp(0)


def datetime_to_timestamp(dt):
    '''
    Source:
    http://stackoverflow.com/questions/6999726/how-can-i-convert-a-datetime-object-to-milliseconds-since-epoch-unix-time-in-p
    '''
    return int((dt - EPOCH).total_seconds())


def now_timestamp():
    '''
    Return timestamp representing the current time.
    '''
    return datetime_to_timestamp(datetime.now())


def get_index_of_tool(lst_of_conc, tool):
    """Return the index of the object in the provided list
    whose tool name matches tool.

    If tool is None, return the first valid index into `lst_of_conc`.

    This returns -1 if:
      * `lst_of_conc` is None, or
      * `lst_of_conc` has no entries, or
      * no object in `lst_of_conc` matches `tool`.

    Args:

    - `lst_of_conc`: A list of Concrete objects, each of which
      has a `.metadata` field.
    - `tool`: A tool name to match.
    """
    idx = -1
    if lst_of_conc is not None and len(lst_of_conc) > 0:
        if tool is not None:
            for (cidx, obj) in enumerate(lst_of_conc):
                if obj.metadata.tool == tool:
                    idx = cidx
                    break
        else:
            idx = 0
    return idx
