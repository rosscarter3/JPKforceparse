"""JPK-force-parse package test script"""

import JPKforceparse as JPK


def main():
    curve_path = "/Users/carterr/Documents/afm_andy/LE Mannitol 010316 Sample 1/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_processed-2016.03.02-10.20.03/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_00345.txt"
    forcemap_path1 = "/Users/carterr/Documents/afm_andy/LE Mannitol 010316 Sample 1/Le Mannitol 010316 sample 1 map-data-2016.03.01-15.09.41.098_processed-2016.03.02-10.20.03"
    forcemap_path2 = "/Users/carterr/Documents/afm_andy/LE Mannitol 030216 S1/map LE mannitol 030216 s1-data-2016.02.03-10.15.00.814_processed-2016.02.04-08.47.17"
    forcemap_path3 = "/Users/carterr/Documents/afm_andy/LE Mannitol 030216 S2/map LE mannitol 030216 s2-data-2016.02.03-11.22.40.361_processed-2016.02.04-09.02.06"

    # map1 = JPK.ForceMap(forcemap_path1)
    # map1.plot_stiffness_map()
    # map1.plot_height_map()
    # map1.plot_hertz_map()

    curve1 = JPK.ForceCurve(curve_path)
    # curve1.plot_curve()
    # curve1.calculate_apparent_young_modulus_hertz()
    print curve1

if __name__ == '__main__':
    main()
