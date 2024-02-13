#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import groupby
from numpy import asarray, shape

def iHall(filetoread):
    # open file
    f = open(filetoread, 'r')
    # read data from file
    # * all lines are read except those starting with "#"
    # * the data in a line is split at whitespaces
    # * [ [ []*values_in_line ]*lines ]
    s = [[float(i) for i in line.split()] for line in f if line[0] != '#']
    # regroup data
    # * read data into a list as long as the elements are not empty
    # * if an empty element is present a new list begins
    # * [ [ []*values_in_point ]*points_in_linescan ]*number_of linescans ]
    s = [list(group) for i, group in groupby(s, bool) if i]
    # assign data
    # * reshape nested list
    # * [ [ [ ]*points_in_linescan ]*number_of linescans ]*values_in_point ]
    d = [asarray([asarray([p[i] for p in l]) for l in s])
         for i in range(len(s[0][0]))]
    # close file
    f.close()
    # return data
    return asarray(d)


def oHall(filetowrite, data, **kwds):
    # open file
    f = open(filetowrite, 'w')
    # write header
    if "offset" in kwds:
        s = "# %u %u %.4e %.4e %.4e %.4e %.4e\n" % (kwds["pixelx"],
                                                    kwds["pixely"],
                                                    kwds["thickness"],
                                                    kwds["distance"],
                                                    kwds["stepwidthx"],
                                                    kwds["stepwidthy"],
                                                    kwds["offset"])
    else:
        s = "# %u %u %.4e %.4e %.4e %.4e\n" % (kwds["pixelx"],
                                               kwds["pixely"],
                                               kwds["thickness"],
                                               kwds["distance"],
                                               kwds["stepwidthx"],
                                               kwds["stepwidthy"])
    f.write(s)
    # write matrix into file
    for line in data:
        s = ""
        for B in line:
            s += "%e " % B
        s += "\n"
        f.write(s)

    f.close()
