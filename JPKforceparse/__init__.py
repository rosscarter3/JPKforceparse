"""JPK-force-parse package."""
import os
import numpy as np
import matplotlib
from collections import OrderedDict

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

__version__ = "0.0.1"
__author__ = "Ross Carter"


class ForceCurve(object):
    """
    A Force Curve
    """

    def __init__(self, path):
        self.raw_path = path

        data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])

        raw_stream = file(self.raw_path, 'r')
        for num, line in enumerate(raw_stream):
            if line.startswith('# xPosition'):
                self.x_pos = float(line.split(": ")[1])
            elif line.startswith('# yPosition'):
                self.y_pos = float(line.split(": ")[1])
            elif line.startswith('# index'):
                self.index = int(line.split(": ")[1])
            elif line.startswith('# springConstant'):
                self.spring_constant = float(line.split(": ")[1])
            elif line[0] != '#':
                try:
                    data_row = line.split(" ")
                    data_row[8] = data_row[8][0:6]
                    data = np.append(data, np.array([map(float, data_row)]), axis=0)
                except IndexError:
                    pass

        data = np.delete(data, 0, axis=0)

        self.tipSampleSep = data[:, 0]          # [metres]
        self.vDeflection = data[:, 1]           # [Newtons]
        self.height = data[:, 2]                # [metres]
        self.error = data[:, 3]                 # [volts]
        self.smoothedMeasHeight = data[:, 4]    # [metres]
        self.measHeight = data[:, 5]            # [metres]
        self.hDeflection = data[:, 6]           # [volts]
        self.seriesTime = data[:, 7]            # [seconds]
        self.time = data[:, 8]                  # [seconds]

        self.calculate_contact_point()
        self.calculate_apparent_stiffness()

    def calculate_contact_point(self):
        """Contact point calculation"""
        # finds the contact point
        min_tssep_value = min(i for i in self.tipSampleSep if i > 0)
        self.contact_point_index = int(np.where(self.tipSampleSep == min_tssep_value)[0])
        self.contactpoint = self.height[self.contact_point_index]

    def calculate_apparent_stiffness(self, depth = 20e-9):
        """Instantaneous apparent stiffness calculation"""
        # fit polynomial, differentiate force indentation, report at fixed indentation depth
        indentation = self.smoothedMeasHeight[-1:len(self.smoothedMeasHeight)-self.contact_point_index]
        force = self.vDeflection[-1:len(self.smoothedMeasHeight)-self.contact_point_index]
        plt.plot(indentation, force)
        plt.show()

    def calculate_apparent_young_modulus(self):
        """Apparent Young's Modulus Calculation"""
        # see hertz sneddon stuff
        pass

    def plot_curve(self):
        """
        Plots a force curve of smoothed measured height vs. cantilever deflection
        """
        plt.plot(self.vDeflection)
        plt.show()


class ForceMap(object):
    """
    A Force Map, a collection of force curves
    """

    def __init__(self, directory):
        print "Loading Curves... "
        self.forcecurvedict = OrderedDict()

        for i, curve_file in enumerate(os.listdir(directory)):
            if i % 500 == 0:
                print i, " curves loaded"
            key = curve_file[-9:-4]
            value = ForceCurve(os.path.join(directory, curve_file))
            self.forcecurvedict[key] = value

    def plot_height_map(self):
        """
        plots a force map of contact height
        :return:
        """
        print "Plotting Height Map..."
        x, y, z = list(), list(), list()
        for curve in self.forcecurvedict.itervalues():
            x.append(curve.x_pos)
            y.append(curve.y_pos)
            z.append(curve.contactpoint)

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(x,y,z)
        #ax.plot_trisurf(x, y, z, color=z, cmap='Set1', vmin=min(z), vmax=max(z))
        # ax.plot_trisurf(x, y, z)
        plt.show()


def main():
    # path = "./example_data/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_00013.txt"
    # path2 = "/Users/carterr/Documents/afm_andy/LE Mannitol 010316 Sample 1/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_processed-2016.03.02-10.20.03/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_00256.txt"
    # point1 = ForceCurve(path2)
    # point1.plot_curve()
    directory = "/Users/carterr/Documents/afm_andy/LE Mannitol 010316 Sample 1/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_processed-2016.03.02-10.20.03"
    map1 = ForceMap(directory)
    map1.plot_height_map()


if __name__ == '__main__':
    main()
