# coding=utf-8
import sys
sys.path.append('D:/Codes/Main/Inversion')
import hall_inversion


def calc_inversion():

    # all length units are µm, everything else is SI
    c = hall_inversion.InversionWriter(
        file="D:/Data/Inversion Data/R192-5/coarse_30_30_50_5K.dat",
        hallconst=43.91,
        bussibaer_factor=[1.4, 1.4],
        mayscanner=False,

        thickness=2.7,
        distance=50,
        stepsize=30,

        # {} will be replaced by the filename of the scan file
        # if None, "{}_" will be used
        result_prefix=None,

        # {} will be replaced by the result_prefix
        result_path="D:/Data/Inversion Data/R192-5/coarse_30_30_50_5K",
    )

    c.perform_inversion()


if __name__ == "__main__":
    calc_inversion()
