#!/usr/bin/env python2
"""Parses ems xml file into csv
Default input file is ems.xml
Specify input file with -i or --input==
Outputs to screen so redirect with > outfile.csv
"""

__author__ = 'mneil'

import sys
import time
from xml.etree.cElementTree import *
import getopt


def usage():
    print __doc__


def print_to_log(logString):
    """ Print to log file (stderr)
    Prints the logString to stderr, prepends date and time
    """
    print >> sys.stderr, (time.strftime("%Y%m%d-%H:%M:%S") + ":ems_to_csv: " + logString)


def remove_non_ascii(s):
    if s:
        return ("".join(i for i in s if ord(i) < 128)).replace(",", "")
    else:
        return ""

debug_it = 0
input_file = "ems.xml"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "input="])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit()
    elif opt in ("-i", "--input"):
        input_file = arg

tree = parse(input_file)
root = tree.getroot()
xml_prefix = root.tag.split('}')[0] + '}'
print("Name,Deprecated,Severity,Description,Corrective Action,SNMP Trap,ASUP Reason,Asup Msg")
started_count = 0
finished_count = 0
for child in root.findall(xml_prefix + 'event-def'):
    started_count += 1
    name = ''
    severity = ''
    description = ''
    corrective_action = ''
    snmp_trap = 'N'
    reason = ''
    msgno = ''
    deprecated = 'N'

    name = child.get('name')
    if debug_it:
        print_to_log(name)
    severity = child.get('severity')
    if debug_it:
        print_to_log(severity)

    if debug_it:
        print_to_log("Name: " + child.get('name') + " Severity: " + child.get('severity'))
    try:
        if '\n' in child.find(xml_prefix + 'description').text:
            lines = child.find(xml_prefix + 'description').text.splitlines()
            for line in lines:
                temp_line = line.strip().replace(',', ';')
                if debug_it:
                    print_to_log(temp_line)
                if description:
                    description += ' ' + temp_line
                else:
                    description = temp_line
        else:
            description = child.find(xml_prefix + 'description').text.strip().replace(',', ';')
        if debug_it:
            print_to_log(description)
        # description = child.find(xml_prefix + 'description').text.strip('\n').strip('\t').strip()
    except AttributeError:
        description = ''

    try:
        if child.find(xml_prefix + 'corrective-action').get('type') == "TEXT":
            if '\n' in child.find(xml_prefix + 'corrective-action').text:
                lines = child.find(xml_prefix + 'corrective-action').text.splitlines()
                for line in lines:
                    temp_line = line.strip().replace(',', ';')
                    if debug_it:
                        print_to_log(temp_line)
                    if corrective_action:
                        corrective_action += ' ' + temp_line
                    else:
                        corrective_action = temp_line
            else:
                corrective_action = child.find(xml_prefix + 'corrective-action').text.strip().replace(',', ';')
        elif child.find(xml_prefix + 'corrective-action').get('type'):
            corrective_action = child.find(xml_prefix + 'corrective-action').get('type')
        else:
            corrective_action = "NONE"
        if debug_it:
            print_to_log(corrective_action)
    except AttributeError:
        corrective_action = ''

    try:
        if child.find(xml_prefix + 'snmp') is not None:
            snmp_trap = 'Y'
    except AttributeError:
        pass
    if debug_it:
        print_to_log(snmp_trap)

    try:
        # print_to_log("Checking deprecated")
        if child.find(xml_prefix + 'deprecated') is not None:
            # print_to_log("Found deprecated")
            deprecated = 'Y'
    except AttributeError:
        print_to_log("Problem checking deprecated for " + name)

    if debug_it:
        print_to_log(deprecated)

    try:
        asup = child.find(xml_prefix + 'asup')
    except AttributeError:
        reason = ''
        msgno = ''

    if asup:
        try:
            reason = asup.find(xml_prefix + 'reason').text.strip()
            if debug_it:
                print_to_log("asup reason: " + reason)
        except AttributeError:
            reason = ''
        try:
            msgno = asup.find(xml_prefix + 'msgno').text.strip()
            if debug_it:
                print_to_log("asup msgno: " + msgno)
        except AttributeError:
            msgno = ''
    if debug_it:
        print_to_log(reason)
        print_to_log(msgno)

    print ','.join([remove_non_ascii(name),
                    remove_non_ascii(deprecated),
                    remove_non_ascii(severity),
                    remove_non_ascii(description), remove_non_ascii(corrective_action),
                    remove_non_ascii(snmp_trap),
                    remove_non_ascii(reason),
                    remove_non_ascii(msgno)])
    finished_count +=1

print "Processed " + str(finished_count) + " of " + str(started_count) + " events"
