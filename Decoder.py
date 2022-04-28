import math
import string
import numpy as np


def main(key, message):
    if len(key) > 9:
        raise Exception("Encryption key too long (key length < 9 please)")

    header = {k: v for k, v in sorted(
        list({k+1: v for k, v in enumerate(key)}.items()),
        key=lambda keyval: keyval[1]
    )}
    sort_order = [x for x in header]
    wanted_sort_order = [x for x in range(1, len(key)+1)]

    # create 2d array from message
    pos = 0
    cols = math.ceil(len(message) / len(key))
    rows = len(key)
    arr = np.zeros(shape=(cols, rows), dtype=str)

    for x in range(cols):
        for y in range(rows):
            if pos < len(message):
                arr[x][y] = message[pos]
            pos += 1

    # sort each row of the array
    for x in range(cols):
        sorttttt = list(
            {k: v for k, v in sorted(list({k + 1: v for k, v in enumerate(arr[x])}.items()), key=lambda i: sort_order[i[0]-1])}.values())

        arr[x] = sorttttt

    return "".join([x for y in arr for x in y]).replace("_", " ").strip()
