"""JPK-force-parse package test script"""

import JPKforceparse as JPK

def main():
    curve_path = "/Users/carterr/Documents/afm_andy/LE Mannitol 010316 Sample 1/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_processed-2016.03.02-10.20.03/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_00256.txt"
    forcemap_path = "/Users/carterr/Documents/afm_andy/LE Mannitol 010316 Sample 1/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_processed-2016.03.02-10.20.03"

    # map1 = JPK.ForceMap(directory)
    # map1.plot_height_map()

    curve1 = JPK.ForceCurve(curve_path)
    curve1.plot_curve()


if __name__ == '__main__':
    main()
