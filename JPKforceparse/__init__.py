"""JPK-force-parse package."""
import os
import numpy as np
import matplotlib
from collections import OrderedDict
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

__version__ = "0.0.1"
__author__ = "Ross Carter"


class ForceCurve(object):
    """
    A Force Curve
    """

    def __init__(self, path):
        self.raw_path = path

        data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype='float64')
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
            elif line.startswith('# force-settings.extend-k-length'):
                self.extend_length = int(line.split(": ")[1])
            elif line.startswith('# force-settings.retract-k-length'):
                self.retract_length = int(line.split(": ")[1])
            elif line.startswith('# force-settings.extended-pause-k-length'):
                self.extend_pause_length = int(line.split(": ")[1])
            elif line.startswith('# force-settings.retracted-pause-k-length'):
                self.retract_pause_length = int(line.split(": ")[1])
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
        self.calculate_apparent_young_modulus_hertz()

    def calculate_contact_point(self):
        """
        Contact point calculation
        """
        # finds the contact point
        min_tssep_value = min(i for i in self.tipSampleSep if i > 0)
        self.contact_point_index = int(np.where(self.tipSampleSep == min_tssep_value)[0])
        self.contactpoint = self.height[self.contact_point_index]

    def calculate_apparent_stiffness(self, depth=20e-9):
        """
        Instantaneous apparent stiffness calculation
        """
        # fit polynomial, differentiate force indentation, report at fixed indentation depth
        indentation = self.smoothedMeasHeight[0:self.extend_length-1][len(self.smoothedMeasHeight) - self.contact_point_index:-1]
        force = self.vDeflection[0:self.extend_length-1][len(self.vDeflection) - self.contact_point_index:-1]
        try:
            z = np.polyfit(indentation, force, 3)
            self.instantaneous_stiffness = 3*z[3]*depth**2 + 2*z[2]*depth + z[1]
        except TypeError:
            self.instantaneous_stiffness = 0

    def calculate_apparent_young_modulus_hertz(self, tip_radius=10e-9, poisson_ration=0.5):
        """
        Apparent Young's Modulus Calculation, Hertz Model, sphere
        """
        indentation = abs(self.smoothedMeasHeight[0:self.extend_length-1][len(self.smoothedMeasHeight) - self.contact_point_index:-1])
        force = np.power(self.vDeflection[0:self.extend_length-1][len(self.vDeflection) - self.contact_point_index:-1], 3)
        try:
            z = np.polyfit(indentation, force, 2)
        except TypeError:
            z = [0, 0]
        self.young_mod_hertz = (3./4) * z[0] * (1-poisson_ration**2) * (1/np.sqrt(tip_radius))

    def calculate_apparent_young_modulus_sneddon(self):
        """
        Apparent Young's Modulus Calculation, Sneddon Model, cone
        """
        # see hertz sneddon stuff
        indentation = self.smoothedMeasHeight[0:self.extend_length-1][len(self.vDeflection) - self.contact_point_index:-1]
        force = self.vDeflection[0:self.extend_length-1][len(self.vDeflection) - self.contact_point_index:-1]
        pass

    def plot_curve(self):
        """
        Plots a force curve of smoothed measured height vs. cantilever deflection
        """
        plt.plot(self.vDeflection)
        plt.show()

    def __repr__(self):
        return "I am a force curve at x = %f, y = %s \n \
        My contact point is at %f metres \n \
        My apparent stiffness is %f N/m \n \
        My Hertz modulus is %f Pascals" % (self.x_pos,
                                           self.y_pos,
                                           self.contactpoint,
                                           self.instantaneous_stiffness,
                                           self.young_mod_hertz)


class ForceMap(object):
    """
    A Force Map, a collection of force curves
    """

    def __init__(self, directory):
        print "Loading Curves... "
        self.force_curve_dictionary = OrderedDict()

        for i, curve_file in enumerate(os.listdir(directory)):
            if i % 500 == 0:
                print i, " curves loaded"
            key = curve_file[-9:-4]
            value = ForceCurve(os.path.join(directory, curve_file))
            self.force_curve_dictionary[key] = value

    def plot_height_map(self):
        """
        plots a force map of contact height
        """
        print "Plotting Height Map..."
        x, y, contact_point = list(), list(), list()
        for curve in self.force_curve_dictionary.itervalues():
            x.append(curve.x_pos)
            y.append(curve.y_pos)
            contact_point.append(curve.contactpoint)

        fig = plt.figure()
        ax = fig.gca()
        ax.scatter(x, y,
                   c=contact_point,
                   cmap='bone',
                   vmin=min(contact_point),
                   vmax=max(contact_point))
        plt.axis('equal')
        plt.xlim([min(x), max(x)])
        plt.ylim([min(y), max(y)])
        plt.show()

    def plot_stiffness_map(self):
        """
        plots a force map of instantaneous stiffness
        """
        print "Plotting Stiffness Map..."
        x, y, apparent_stiffness = list(), list(), list()
        for curve in self.force_curve_dictionary.itervalues():
            x.append(curve.x_pos)
            y.append(curve.y_pos)
            apparent_stiffness.append(curve.instantaneous_stiffness)

        fig = plt.figure()
        ax = fig.gca()
        ax.scatter(x, y,
                   c=apparent_stiffness,
                   cmap='bone',
                   vmin=min(apparent_stiffness),
                   vmax=max(apparent_stiffness))
        plt.axis('equal')
        plt.xlim([min(x), max(x)])
        plt.ylim([min(y), max(y)])
        plt.show()

    def plot_hertz_map(self):
        """
        plots a force map of instantaneous stiffness
        """
        print "Plotting Hertz Modulus Map..."
        x, y, hertz = list(), list(), list()
        for curve in self.force_curve_dictionary.itervalues():
            x.append(curve.x_pos)
            y.append(curve.y_pos)
            hertz.append(curve.young_mod_hertz)

        fig = plt.figure()
        ax = fig.gca()
        ax.scatter(x, y,
                   c=hertz,
                   cmap='bone',
                   vmin=min(hertz),
                   vmax=max(hertz))
        plt.axis('equal')
        plt.xlim([min(x), max(x)])
        plt.ylim([min(y), max(y)])
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
