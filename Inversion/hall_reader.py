# coding=utf-8

import os
import math

import numpy as np
import scipy.interpolate


DEFAULT_BB_FACTOR = [1.4, 1.4]


class HallReader:

    def __init__(self, file=None, hallconst=None, hall_offset_v=0, calc_hall_const=None,
                 bussibaer_factor=False, neg_x=None, neg_y=None,
                 flip_x=None, flip_y=None, center=None, get_new_val=None,
                 mayscanner=False, xy_unit=None, hall_unit=None):

        self.file = file
        self.hallconst = hallconst
        self.hall_offset_v = hall_offset_v
        self.bussibaer_factor = bussibaer_factor
        self.center = center
        self.get_new_val = get_new_val
        self.neg_x = neg_x
        self.neg_y = neg_y
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.mayscanner = mayscanner
        self.xy_unit = xy_unit
        self.hall_unit = hall_unit

        if mayscanner and bussibaer_factor:
            print("Warning, bussibaer_factor set for mayscanner")

        if calc_hall_const is not None:
            if hallconst is not None or hall_offset_v != 0:
                print("Warning, given hallconst and hall_offset_v will be overwritten")

            self.calc_hall_const(*calc_hall_const)

    def data_cols(self, values):
        return get_data_columns(values, mayscanner=self.mayscanner)

    def load_values(self, data_columns=None):

        if isinstance(data_columns, int):
            data_columns = [data_columns]

        if self.file is None or not os.path.exists(self.file):
            print("Error, the file does not exist: {!r}".format(self.file))

            if data_columns is None:
                return None
            else:
                return [None] * len(data_columns)

        values = np.loadtxt(self.file, unpack=True)

        fac = self._get_xy_factor()

        if self.mayscanner:
            fac *= 10

        if fac != 1:
            values[self.data_cols("x")] *= fac  # µm -> unit
            values[self.data_cols("y")] *= fac

        values[self.data_cols("x")], values[self.data_cols("y")] = self._recalc_xy(
            values[self.data_cols("x")], values[self.data_cols("y")]
        )

        fac = self._get_hall_factor()

        if self._get_hall_unit().endswith("V"):
            values[self.data_cols("hall_v")] *= fac  # V -> hall_unit
        else:
            # V -> T via hallconst and hall_offset
            values[self.data_cols("hall_v")] = (values[self.data_cols("hall_v")] + self.hall_offset_v) * self.hallconst
            values[self.data_cols("hall_v")] *= fac  # T -> hall_unit

        if self.get_new_val is not None:
            self.get_new_val(self, values)

        return self.get_from_values(values, data_columns)

    def read_counts(self):
        out_count, in_count = read_counts(self.file)

        if self.mayscanner:
            x_count, y_count = in_count, out_count
        else:
            x_count, y_count = out_count, in_count

        return x_count, y_count

    def get_from_values(self, values, data_columns):

        if data_columns is None:
            return values
        else:
            if isinstance(data_columns, int):
                return values[data_columns]
            else:
                res = []
                for c in data_columns:
                    res.append(values[c])

                return res

    # region Helper Functions

    def calc_hall_const(self, start_f, end_f, start_v, end_v, print_res=False):
        self.hallconst, self.hall_offset_v = calc_hall_const(
            start_f, end_f, start_v, end_v, print_res,
        )

    def _recalc_xy(self, x, y, is_bf=False, is_center=False, is_neg=False, is_all=False):

        if is_all:
            is_center = True
            is_neg = True
            is_bf = True

        if not is_center and self.center is not None:
            x = np.subtract(x, self.center[0])
            y = np.subtract(y, self.center[1])

        if not is_neg:
            if self._get_neg_x():
                x = np.multiply(x, -1)
            if self._get_neg_y():
                y = np.multiply(y, -1)

        if not is_bf and self.bussibaer_factor is not None:

            if self.bussibaer_factor == True:
                self.bussibaer_factor = DEFAULT_BB_FACTOR
            elif self.bussibaer_factor == False:
                self.bussibaer_factor = [1, 1]
            elif isinstance(self.bussibaer_factor, (float, int)):
                self.bussibaer_factor = [1, self.bussibaer_factor]

            x = np.multiply(x, self.bussibaer_factor[0])
            y = np.multiply(y, self.bussibaer_factor[1])

        return x, y

    def _calc_map_grid(self, x, y, v, x_anz=None, y_anz=None):

        if x_anz is None and y_anz is None:
            x_anz, y_anz = self.read_counts()

        xi = np.linspace(x.min(), x.max(), x_anz)
        yi = np.linspace(y.max(), y.min(), y_anz)

        # print("x =", x.min(), x.max())
        # print("y =", y.min(), y.max())

        # print("size(xi) =", np.size(xi))
        # print("size(yi) =", np.size(yi))
        # print("xi =", xi)
        # print("yi =", yi)
        # print(np.diff(yi))
        # print(np.diff(xi))

        xi, yi = np.meshgrid(xi, yi)

        grid = scipy.interpolate.griddata(
            (x, y), v, (xi, yi), method="linear"
        )

        # remove all 'NaN'
        while np.isnan(grid).sum() != 0:
            ax_0 = np.isnan(grid).sum(axis=0)
            ax_1 = np.isnan(grid).sum(axis=1)
            if ax_0.max() > ax_1.max():
                grid = np.delete(grid, np.argmax(ax_0), axis=1)
                xi = np.delete(xi, np.argmax(ax_0), axis=1)
                yi = np.delete(yi, np.argmax(ax_0), axis=1)
            else:
                grid = np.delete(grid, np.argmax(ax_1), axis=0)
                xi = np.delete(xi, np.argmax(ax_1), axis=0)
                yi = np.delete(yi, np.argmax(ax_1), axis=0)

        return grid, xi, yi

    def _get_neg_x(self):
        if self.neg_x is None:
            if not self.mayscanner and self.center is not None:
                return True
            else:
                return False
        else:
            return self.neg_x

    def _get_neg_y(self):
        if self.neg_y is None:
            return False
        else:
            return self.neg_y

    def _get_flip_x(self):
        return self._get_flip_xy()[0]

    def _get_flip_y(self):
        return self._get_flip_xy()[1]

    def _get_flip_xy(self):
        if self.mayscanner:
            flip_x = False if self.flip_x is None else self.flip_x
            flip_y = True if self.flip_y is None else self.flip_y
        else:
            flip_x = True if self.flip_x is None else self.flip_x
            flip_y = False if self.flip_y is None else self.flip_y

        if self._get_neg_x():
            flip_x = not flip_x
        if self._get_neg_y():
            flip_y = not flip_y

        return flip_x, flip_y

    def _get_xy_unit(self):
        if self.xy_unit is None or self.xy_unit == "":
            return "µm"
        else:
            return self.xy_unit

    def _get_hall_unit(self):
        if self.hall_unit is None or self.hall_unit == "":
            if self.hallconst is None:
                return "µV"
            else:
                return "mT"
        else:
            if not self.hall_unit.endswith("T") and not self.hall_unit.endswith("V"):
                raise ValueError("wrong hall unit")

            if self.hallconst is None and self.hall_unit.endswith("T"):
                raise ValueError("hall constant needed for field calculation")

            return self.hall_unit

    def _get_hall_factor(self):

        unit = self._get_hall_unit()
        if unit == "T" or unit == "V":
            return 1
        else:
            return 1 / get_si_factor(unit[0])

    def _get_xy_factor(self):

        if not self._get_xy_unit().endswith("m"):
            raise ValueError("xy_unit must be a valid length unit")

        fac = 1e-6  # data file unit is µm
        if self.xy_unit == "m":
            return fac
        else:
            return fac / get_si_factor(self._get_xy_unit()[0])

    # endregion


def calc_hall_const(start_f, end_f, start_v, end_v, print_res=False):

    hall_const = (end_f - start_f) / (end_v - start_v)
    hall_offs = 0

    if abs(start_f) <= 1e-4:
        hall_offs = start_v
    elif abs(end_f) <= 1e-4:
        hall_offs = end_v

    if print_res:
        print("hall_const = {:0.2f} T/V, offset_v = {:0.4e} V".format(hall_const, hall_offs))

    return hall_const, hall_offs


def read_counts(filename):

    # todo: implement this as my own reading function
    inner_counts = [0]
    cur_index = 0

    with open(filename, "r") as f:
        for line in f:
            if not line.startswith("#"):
                line = line.strip()
                if line == "":
                    if inner_counts[cur_index] > 0:
                        inner_counts.append(0)
                        cur_index += 1
                else:
                    inner_counts[cur_index] += 1

    if inner_counts[-1] == 0:
        inner_counts = inner_counts[:-1]

    in_count = max(inner_counts)
    out_count = len(inner_counts)

    return out_count, in_count


_DATA_NAMES = dict(x=0, y=1, z=2)
_BB_DATA_NAMES = dict(hall_v=3, cant_v=4, temp=5, time=6, **_DATA_NAMES)
_MAY_DATA_NAMES = dict(field=3, hall_v=4, **_DATA_NAMES)

_COMBO_DATA_NAMES = dict(xy=["x", "y"], xyz=["x", "y", "z"], xyB=["x", "y", "hall_v"])
_COMBO_BB_DATA_NAMES = dict(xycant=["x", "y", "cant_v"], **_COMBO_DATA_NAMES)
_COMBO_MAY_DATA_NAMES = dict(**_COMBO_DATA_NAMES)


def get_data_columns(values, scanner=None, mayscanner=None):

    if scanner is None:
        if mayscanner:
            scanner = "may"
        else:
            scanner = "bb"

    scanner = scanner.lower()

    if scanner == "may":
        names = _MAY_DATA_NAMES
        combo = _COMBO_MAY_DATA_NAMES
    elif scanner in ["bb", "bussi", "bussibaer", "bussibär", "baer", "bär"]:
        names = _BB_DATA_NAMES
        combo = _COMBO_BB_DATA_NAMES
    else:
        names = _DATA_NAMES
        combo = _COMBO_DATA_NAMES

    is_list = True
    is_combo = False
    if not isinstance(values, (list, tuple, np.ndarray)):
        is_list = False
        values = [values]

    res = []

    for v in values:
        if v in combo:
            is_combo = True
            for n in combo[v]:
                res.append(names[n])
        else:
            res.append(names[v])

    if is_list or is_combo:
        return res
    else:
        return res[0]


def get_si_factor(prefix):

    # python 2 has problems with the encoding
    if prefix == "µ" or prefix == "\xc2":
        prefix = "u"

    factors = dict(
        Y=1e24, Z=1e21, E=1e18, P=1e15, T=1e12, G=1e9, M=1e6, k=1e3, h=100, da=10,
        d=1e-1, c=1e-2, m=1e-3, u=1e-6, n=1e-9, p=1e-12, f=1e-15, a=1e-18, z=1e-21, y=1e-24,
    )

    return factors[prefix]
