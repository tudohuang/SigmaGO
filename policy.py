import numpy as np


def get_idx(result, invalid):
    steps = np.argsort(result)[0,::-1]
   
    got_idx = -1

    for idx in steps:
        if invalid[idx] == 0:
            got_idx = idx
            break
    if got_idx == -1:
        got_idx = 81
    return got_idx

def xy_to_go_coord(x, y):
    columns = "ABCDEFGHJKLMNOPQRSTUVWXYZ"  # I is omitted in Go
    coord = columns[x] + str(y + 1)
    return coord

def go_coord_to_xy(coord):
    columns = "ABCDEFGHJKLMNOPQRSTUVWXYZ"  # I is omitted in Go
    x = columns.index(coord[0].upper())
    y = int(coord[1:]) - 1
    return (x, y)