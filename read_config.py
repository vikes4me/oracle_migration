from __future__ import print_function
from ConfigParser import SafeConfigParser
import sys


def read_config(config_file):
    parser = SafeConfigParser()
    parser.read(config_file)

    dictionary = {}
    for section in parser.sections():
        dictionary[section] = {}
        for option in parser.options(section):
            dictionary[section][option] = parser.get(section, option)

    return dictionary


if __name__ == '__main__':

    print("This module can not be run as a stand-alone.")
    sys.exit()
