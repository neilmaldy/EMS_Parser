__author__ = 'mneil'

import sys
import time
from xml.etree.cElementTree import *

def print_to_log(logString):
    """ Print to log file (stderr)
    Prints the logString to stderr, prepends date and time
    """
    print >> sys.stderr, (time.strftime("%Y%m%d-%H:%M:%S") + ":ems_to_csv: " + logString)

debug_it = 1

tree = parse('ems.xml')
root = tree.getroot()
xml_prefix = root.tag.split('}')[0] + '}'

for child in root.findall(xml_prefix + 'event-def'):
    try:
        if debug_it:
            print_to_log("Name: " + child.get('name') + " Severity: " + child.get('severity'))

        name = child.get('name')
        severity = child.get('severity')
        try:
            description = child.find(xml_prefix + 'description').text
        except AttributeError:
            description = ''

    except TypeError:
        if name:
            print_to_log("Missing essential field, skipping event-def " + name)
        else:
            print_to_log("Missing essential field, skipping event-def")