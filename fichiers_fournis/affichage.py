#!/usr/bin/env python3
"""
display given segment files
"""
import sys
from geo.segment import load_segments
from geo.tycat import tycat

def display(filename):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    segments = load_segments(filename)
    print("{}: nous avons {} segments".format(filename, len(segments)))
    tycat(segments)

def main():
    """
    launch test on each file.
    """
    for filename in sys.argv[1:]:
        display(filename)

main()
