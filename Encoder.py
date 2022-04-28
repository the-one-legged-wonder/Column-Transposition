import math
import numpy as np


def main(key, message):
    if len(key) > 9:
        raise Exception("Encryption key too long (key length < 9 please)")
    clean_message = message.replace(" ", "_")#.lower().replace("_","")

    sort_order = [k for k, v in sorted(
        list({k+1: v for k, v in enumerate(key)}.items()),
        key=lambda keyval: keyval[1]
    )]

    # create 2d array from clean_message
    pos = 0
    cols = math.ceil(len(clean_message) / len(key))
    rows = len(key)
    arr = np.zeros(shape=(cols, rows), dtype=str)

    for x in range(cols):
        for y in range(rows):
            if pos < len(clean_message):
                arr[x][y] = clean_message[pos]
            else:
                arr[x][y] = "_"
            pos += 1

    # sort each row of the array
    for x in range(cols):
        sorttttt = list(
            {k: v for k, v in sorted(list({k + 1: v for k, v in enumerate(arr[x])}.items()), key=lambda i: sort_order.index(i[0]))}.values())
        arr[x] = sorttttt

    return "".join([x for y in arr for x in y])