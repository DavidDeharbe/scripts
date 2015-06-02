#!/usr/bin/env python

# filter_unknown.py
#
# a utility to process XML descriptions of Star-Exec spaces
# reads a XML file from standard input and outputs a new XML file
# without the benchmarks with status unknown removed.
#
# David Deharbe - Universidade Federal do Rio Grande do Norte (c) 2015

import optparse
import os
import sys
import xml.etree.ElementTree as ET

removed = 0
kept = 0
removable = []

def remove_unknown_rec(node):
    global removed, kept, removable
    for bench in node.findall('Benchmark'):
	remove = False
	if int(bench.attrib['id']) in removable:
	    remove = True
	else:
            for attribute in bench.findall('Attribute'):
                if attribute.attrib['name'] == 'status' and attribute.attrib['value'] == 'unknown':
                    remove = True
        if remove:
            removed = removed + 1
            node.remove(bench)
            sys.stderr.write(bench.attrib['name'] +'(' + bench.attrib['id'] + ') removed\n')
        else:
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
