# coding=utf-8

import os
import glob
import subprocess
import shutil
import ctypes
import sys
import math
import time

import numpy as np

try:
    ModuleNotFoundError
except NameError:
    # python 2 does not have ModuleNotFoundError
    ModuleNotFoundError = ImportError

try:
    from hall_reader import HallReader
except ModuleNotFoundError:
    from hall_tools.hall_reader import HallReader


TOEPLITZ_PATH = "D:/Codes/Main/Inversion/toeplitz"

if not os.path.isabs(TOEPLITZ_PATH):
    TOEPLITZ_PATH = os.path.join(os.path.dirname(__file__), TOEPLITZ_PATH)


class InversionWriter(HallReader):

    @classmethod
    def from_reader(cls, reader, **kwargs):

        return InversionWriter(
            **dict(kwargs,
                file=reader.file,
                hallconst=reader.hallconst,
                hall_offset_v=reader.hall_offset_v,
                bussibaer_factor=reader.bussibaer_factor,
                mayscanner=reader.mayscanner,
                flip_x=reader.flip_x,
                flip_y=reader.flip_y,
                neg_x=reader.neg_x,
                neg_y=reader.neg_y,
                xy_unit=reader.xy_unit,
                center=reader.center,
                get_new_val=reader.get_new_val,
            )
        )

    def __init__(self,
                 thickness=None,
                 distance=None,
                 stepsize=None,
                 pixelx=None, pixely=None,
                 offset=None,
                 result_path=None,
                 result_prefix=None,
                 grid_point_factor=None,
                 toeplitz_path=None,
                 x_cushion=False, y_cushion=False,
                 **kwargs):

        HallReader.__init__(self, **dict(kwargs, hall_unit="T"))

        self.thickness = thickness
        self.distance = distance
        self.stepsize = stepsize
        self.pixelx = pixelx
        self.pixely = pixely
        self.offset = offset
        self.result_path = result_path
        self.result_prefix = result_prefix
        self.grid_point_factor = grid_point_factor
        self.x_cushion = x_cushion
        self.y_cushion = y_cushion
        self.toeplitz_path = toeplitz_path

        if self.file is not None and not self.file.endswith(".mat"):

            missing = []

            if self.file is None:
                missing.append("file")
            if thickness is None:
                missing.append("thickness")
            if distance is None:
                missing.append("distance")
            if stepsize is None:
                missing.append("stepsize")
            if self.hallconst is None:
                missing.append("hall constant")

            if len(missing) > 0:
                print("Warning, missing parameters: {}".format(
                    ", ".join(missing)))

    def save_for_inversion(self, filename=None, pad_grid_size=None):

        if filename is None:
            filename = join_path(self._get_toeplitz_path(), "B.mat")

        stepsizex, stepsizey = self._get_stepsize()
        
        if self.mayscanner:
            x, y, B = self.load_values(self.data_cols(["x", "y", "hall_v"]))
        else:
            x, y, B = self.load_values(self.data_cols("xyB"))
        x_anz, y_anz = self.read_counts()

        if self.grid_point_factor is not None:
            gpf = self._get_xy_list(self.grid_point_factor)
            x_anz *= gpf[0]
            y_anz *= gpf[1]

        grid, xi, yi = self._calc_map_grid(x, y, B, x_anz, y_anz)

        if self.x_cushion:
            g2 = np.flip(grid, axis=1)

            if self.x_cushion == "both" or self.x_cushion == True:
                conc = (g2, grid, g2)
            elif self.x_cushion == "left":
                conc = (g2, grid)
            elif self.x_cushion == "right":
                conc = (grid, g2)
            else:
                raise ValueError("Unknown value for x_cushion")

            grid = np.concatenate(conc, axis=1)

        if self.y_cushion:
            g2 = np.flip(grid, axis=0)

            if self.y_cushion == "both" or self.y_cushion == True:
                conc = (g2, grid, g2)
            elif self.y_cushion == "top":
                conc = (grid, g2)
            elif self.y_cushion == "bottom":
                conc = (g2, grid)
            else:
                raise ValueError("Unknonw value for y_cushion")

            grid = np.concatenate(conc, axis=0)

        sh = np.flip(np.shape(grid), 0)
        print("Datafile:     {} x {} = {} points\n"
              "converted to: {} x {} = {} points".format(
              x_anz, y_anz, x_anz * y_anz,
              sh[0], sh[1], sh[0] * sh[1],
        ))

        if pad_grid_size is not None:
            pgs = self._get_xy_list(pad_grid_size, "pad_grid_size")

            if sh[0] < pgs[0] or sh[1] < pgs[1]:
                grid = pad_grid(grid, *pgs)

        pixelx = self.pixelx
        pixely = self.pixely

        if pixelx is None:
            pixelx = np.size(grid, axis=1)
        if pixely is None:
            pixely = np.size(grid, axis=0)

        s = "# %u %u %.4e %.4e %.4e %.4e" % (
            pixelx, pixely, self.thickness * 1e-6, self.distance * 1e-6, stepsizex * 1e-6, stepsizey * 1e-6
        )

        if self.offset is not None:
            s += " %5.4e" % self.offset

        s += "\n\n"

        if self._get_flip_x():
            grid = np.flip(grid, 1)
        if self._get_flip_y():
            grid = np.flip(grid, 0)

        with open(filename, "w") as file:
            file.write(s)

            for line in grid:
                s = ""
                for B in line:
                    s += "%e " % B
                s += "\n"
                file.write(s)

        print("saved file {!r}".format(filename))

    def perform_inversion(self, pad_grid_size=None, show_memory_usage=False):

        clean_B_after = True

        if self.file is None:
            print("No filename given, assuming 'B.mat' is already in the toeplitz folder")
            clean_toeplitz_folder(path=self._get_toeplitz_path(), clean_B=False)
            clean_B_after = False

        elif self.file.endswith(".mat"):
            print("Filename ends in '.mat'. Assuming it is the right format for the toeplitz program")
            clean_toeplitz_folder(path=self._get_toeplitz_path(), clean_B=True)
            target = join_path(self._get_toeplitz_path(), "B.mat")
            shutil.copy2(self.file, target)
            print("copied {!r} into the toeplitz folder".format(self.file))

        else:
            clean_toeplitz_folder(path=self._get_toeplitz_path(), clean_B=True)
            self.save_for_inversion(
                filename=join_path(self._get_toeplitz_path(), "B.mat"),
                pad_grid_size=pad_grid_size,
            )

        res = start_inversion(
            clean=False,
            result_path=self._get_result_path(),
            result_prefix=self._get_result_prefix(),
            clean_B_after=clean_B_after,
            show_memory_usage=show_memory_usage,
            toeplitz_path=self._get_toeplitz_path(),
        )

        if res is None:
            return False
        else:
            return True

    def _get_stepsize(self):
        s = self._get_xy_list(self.stepsize, name="stepsize", allow_None=False)

        s = self._recalc_xy(
            *s,
            is_bf=False, is_neg=True, is_center=True
        )

        if self.grid_point_factor is not None:
            gpf = self._get_xy_list(self.grid_point_factor)
            s = np.divide(s, gpf)

        return s

    def _get_xy_list(self, value, name="value", allow_None=True):

        if value is None:
            if allow_None:
                return None
            else:
                raise ValueError("{!r} can not be None".format(name))
        elif isinstance(value, (list, tuple, np.ndarray)):
            if not len(value) == 2:
                if name is None:
                    return None
                else:
                    raise ValueError("{!r} must be a number or a list of lenght 2".format(name))

            return value
        else:
            return [value, value]

    def _get_result_prefix(self):

        res = self.result_prefix

        if self.file is None or self.file.endswith(".mat"):
            if res is None:
                res = ""

            res = res.format("")
        else:
            fname = os.path.splitext(os.path.basename(self.file))[0]

            if res is None:
                res = "{}_"

            res = res.format(fname)

        return res

    def _get_result_path(self):
        return self.result_path.format(self._get_result_prefix())

    def _get_toeplitz_path(self):
        if self.toeplitz_path is None:
            return TOEPLITZ_PATH
        else:
            return self.toeplitz_path


def start_inversion(clean=True, result_path=None, result_prefix=None,
                    clean_B_after=True, show_memory_usage=False,
                    toeplitz_path=None):

    error = False

    if toeplitz_path is None:
        toeplitz_path = TOEPLITZ_PATH

    if clean:
        print("cleaning toeplitz folder...")
        clean_toeplitz_folder(path=toeplitz_path)
        print()

    params = [join_path(toeplitz_path, "toeplitz_r3")]
    if show_memory_usage:
        params.append("-m")

    if sys.platform.startswith("win"):
        # Don't display the Windows GPF dialog if the invoked program dies.
        # See comp.os.ms-windows.programmer.win32
        #  How to suppress crash notification dialog?, Jan 14,2004 -
        #     Raymond Chen's response [1]

        SEM_NOGPFAULTERRORBOX = 0x0002  # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)
        # CREATE_NO_WINDOW = 0x08000000   # From Windows API
        # flags = CREATE_NO_WINDOW

    start_time = time.time()

    try:
        res = subprocess.run(params, cwd=toeplitz_path)
        returncode = res.returncode
    except AttributeError:
        # python 2
        res = subprocess.call(params, cwd=toeplitz_path)
        returncode = res

    duration = time.time() - start_time

    print("--------------------\n")
    print("Duration: {:.2f} min".format(duration / 60))

    if returncode == 1:
        print("warning, the toeplitz program was aborted forcefully, if that was deliberate, everything could be fine...")
    elif returncode != 0:
        print("error with the toeplitz_program: {!r}".format(res))
        error = True

    if not _check_toeplitz_files_exist(toeplitz_path):
        error = True

    if result_path is not None:
        if not copy_toeplitz_results(result_path, result_prefix,
                                     clean_B_after=clean_B_after,
                                     toeplitz_path=toeplitz_path):
            error = True

    if not error:
        print_res_path = result_path
        if print_res_path is None:
            print_res_path = toeplitz_path

        print_res_path = os.path.abspath(print_res_path).replace("\\", "/")
        print("The results are here: {!r}".format(print_res_path))

    if error:
        return None
    elif result_path or result_prefix:
        return (result_path, result_prefix)
    else:
        return (toeplitz_path, "")


def _check_toeplitz_files_exist(toeplitz_path):

    files = get_toeplitz_files(include_B=False)

    missing = []

    for f in files:
        ff = join_path(toeplitz_path, f)
        if not os.path.exists(ff):
            missing.append(f)

    if len(missing) > 0:
        print("Error, the toeplitz program did not create the following files:")

        for f in missing:
            print(f)

        return False

    return True


def copy_toeplitz_results(result_path, result_prefix=None, clean_after=True,
                          clean_B_after=True, verbose=False,
                          toeplitz_path=None):

    success = True

    files = get_toeplitz_files()

    try:
        os.makedirs(result_path, exist_ok=True)
    except TypeError:
        # python 2 has no exist_ok parameter

        try:
            os.makedirs(result_path)
        except BaseException as err:
            print(err)

    copycount = 0
    failcount = 0

    if toeplitz_path is None:
        toeplitz_path = TOEPLITZ_PATH

    for f in files:
        source = join_path(toeplitz_path, f)

        dest = f
        if result_prefix is not None:
            dest = result_prefix + dest

        dest = join_path(result_path, dest)

        try:
            shutil.copy2(source, dest)
            copycount += 1
            if verbose:
                print("copied to {!r}".format(dest))

        except BaseException as err:
            success = False
            failcount += 1
            print(err)
            continue

    total = copycount + failcount

    if failcount == 0:
        multi = "" if copycount == 1 else "s"
        print("Successfully copied all {} file{} to {!r}".format(
            copycount, multi, result_path))
    else:
        multi = "" if total == 1 else "s"
        print("Warning, only {} of {} file{} were copied to {!r}".format(
            copycount, total, multi, result_path))

    if success and clean_after:
        clean_toeplitz_folder(path=toeplitz_path, clean_B=clean_B_after, verbose=verbose)

    return success


def clean_toeplitz_folder(path=None, clean_data=True, clean_B=False, clean_o=False, verbose=False):

    if path is None:
        path = TOEPLITZ_PATH

    del_files = []

    if clean_data:
        del_files.extend(get_toeplitz_files(include_B=False))

    if clean_B:
        del_files.append("B.mat")

    for i, f in enumerate(del_files):
        del_files[i] = join_path(path, f)

    if clean_o:
        p = os.path.join(path, "*.o")
        files = glob.glob(p)

        for f in files:
            del_files.append(norm_path(f))

    delcount = 0
    failcount = 0
    max_tries = 2

    for f in del_files:

        for i in range(max_tries):
            if os.path.exists(f):
                try:
                    os.remove(f)
                    delcount += 1
                    if verbose:
                        print("deleted {!r}".format(f))

                    break

                except BaseException as err:
                    if i < max_tries - 1:
                        time.sleep(1)
                    else:
                        failcount += 1
                        print(err)

    total = delcount + failcount

    if total > 0:
        if failcount == 0:
            multi = "" if delcount == 1 else "s"
            print("Successfully cleaned {} file{} from the toeplitz folder".format(delcount, multi))
        else:
            multi = "" if total == 1 else "s"
            print("Warning, only {} of {} file{} were deleted from the toeplitz folder".format(
                delcount, total, multi))


def get_toeplitz_files(include_B=True, include_log=False):
    res = [
            "Bi.mat",
            "Bo.mat",
            "Bs.mat",
            "J.mat",
            "JB.dat",
            "Jx.mat",
            "Jy.mat",
            "M.mat",
            "P.mat",
            "res.mat",
    ]

    if include_B:
        res.insert(0, "B.mat")

    if include_log:
        res.append("logfile")

    return res


def pad_grid(grid, x_anz, y_anz, pad_with=0):

    sh = np.flip(np.shape(grid))

    left, right, top, bottom = 0, 0, 0, 0

    if x_anz > sh[0]:
        left = math.ceil((x_anz - sh[0]) / 2)
        right = left

    if y_anz > sh[1]:
        top = math.ceil((y_anz - sh[1]) / 2)
        bottom = top

    if left > 0 or top > 0:
        print("padding the grid with {}".format((left, top)))

    res = np.pad(grid, ((top, bottom), (left, right)), 'constant', constant_values=pad_with)
    return res


def get_toeplitz_file(filename, path="", prefix=""):
    return join_path(path, prefix + filename)


def norm_path(path):
    return os.path.normpath(path).replace("\\", "/")


def join_path(*paths):
    return norm_path(os.path.join(*paths))
