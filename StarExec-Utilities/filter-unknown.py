#!/usr/bin/env python

# filter_unknown.py
#
# A utility to process XML descriptions of Star-Exec spaces
# reads a XML file from standard input and outputs a new XML file
# without undesirable benchmarks 
#
# A benchmark is considered undesirable if:
# - its id is listed in a file named "remove.txt" in the current directory
# - the value of its 'status' attribute is 'unknown'
# - the value of its 'contains-bv-partial-func' attribute is 'true'
#
# David Deharbe - Universidade Federal do Rio Grande do Norte (c) 2015

import optparse
import os
import sys
import xml.etree.ElementTree as ET

removed = 0 # how many benchmarks have been removed
kept = 0    # how many benchmarks have been kept
removable = [] # list of benchmarks id found in file 'remove.txt'
# mapping of XML attribute pairs name-value characterizing benchmarks that
# shall be removed
filters = dict({'status': 'unknown', 'contains-bv-partial-func': 'true'})

def remove_unknown_rec(node):
    global removed, kept, removable
    for bench in node.findall('Benchmark'):
	remove = False
	if int(bench.attrib['id']) in removable:
	    remove = True
	else:
            for a in bench.findall('Attribute'):
                name, value = a.attrib['name'], a.attrib['value']
                if name in filters and filters[name] == value:
                    remove = True
        if remove:
            removed = removed + 1
            node.remove(bench)
            sys.stderr.write('removing,' + bench.attrib['name'] +',' + bench.attrib['id'] + '\n')
        else:
            sys.stderr.write('keeping,' + bench.attrib['name'] +',' + bench.attrib['id'] + '\n')
            kept = kept + 1
    for child in node:
        remove_unknown_rec(child)


def main():
    global removed, kept, removable
    p = optparse.OptionParser(description='removes benchmarks with status unknown from StarExec space XML',
                              prog='filter-unknown',
                              usage='%prog < input > output')
    options, arguments = p.parse_args()
    if len(arguments) == 0:
	if os.path.exists('remove.txt'):
	    removable = set([ int(line) for line in open('remove.txt').readlines() ])
        else:
            removable = set([])
        xml = ET.parse(sys.stdin)
        root = xml.getroot()
        remove_unknown_rec(root)
        xml.write(sys.stdout)
        sys.stderr.write(str(removed) + ' removed, ' + str(kept) + ' kept\n')
    else:
        p.print_help()

if __name__ == '__main__':
    main()
