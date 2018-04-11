#!/usr/bin/env python3
"""
run tests on given segments files
"""
import argparse
from geo.segment import load_segments
from geo.graph import Graph
from geo.tycat import tycat

def animate_cycle(cycle):
    """
    graphical animation of eulerian cycle
    """
    edges = []
    while cycle:
        next_edge = cycle.pop()
        tycat(edges, next_edge)
        edges.append(next_edge)

def compute_path(filename, hash_points, animate, display):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    segments = load_segments(filename)

    graph = Graph(segments)
    if display:
        print("loaded graph")
        tycat(graph)

    graph.reconnect(hash_points)
    if display:
        print("reconnected graph")
        tycat(graph)

    graph.even_degrees(hash_points)
    if display:
        print("graph has even degrees")
        tycat(graph)

    cycle = graph.eulerian_cycle()
    if display:
        print("found eulerian cycle")
        tycat(cycle)

    if animate:
        animate_cycle(cycle)

def main():
    """
    parse arguments and work on each file.
    """
    parser = argparse.ArgumentParser(
        description="eulerian cycles for 3d printing",
        epilog="loads a set of segments, add some, find eulerian cycle and animate\
                results in terminology"
    )
    parser.add_argument("--hash", action="store_true", help="use hash tables")
    parser.add_argument("--animate", action="store_true", help="animate found cycle")
    parser.add_argument("--display", action="store_true", help="display all intermediate steps")
    parser.add_argument("filenames", metavar="filename", nargs="+",
                        type=str, help="files to process")
    args = parser.parse_args()

    for filename in args.filenames:
        compute_path(filename, args.hash, args.animate, args.display)

main()
