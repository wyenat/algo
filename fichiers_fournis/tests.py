#!/usr/bin/env python3
"""
Enable  to run various tests to ensure we get enough points to pass
"""
from time import time
import argparse
from geo.segment import load_segments
from geo.graph import Graph
from geo.tycat import tycat

def compute_path(filename, chrono, hash_points,  nbsegment, fichier):
    """
    load segment file, get back connexity, get even degrees, display eulerian path.
    """
    segments = load_segments(filename)

    graph = Graph(segments)

    fichier.write(filename[5:] + "\n")
    if nbsegment:
        fichier.write(str(graph.nb_segment)+"\n")
    if chrono:
        temps_reconnect = time()
    graph.reconnect(hash_points)
    if chrono:
        fichier.write(str(time()-temps_reconnect) + "\n")


    temps_even_degrees = time()
    graph.even_degrees(hash_points)
    if chrono:
        fichier.write(str(time()-temps_even_degrees) + "\n")

    temps_cycle = time()
    cycle = graph.eulerian_cycle()
    if chrono:
        fichier.write(str(time()-temps_cycle) + "\n")

def main():
    """
    parse arguments and work on each file.
    """
    fichier = open("tests_hash.txt", 'w')
    parser = argparse.ArgumentParser(
        description="Permet de testers les différents algorithmes",
        epilog="loads a set of segments, add some, find eulerian cycle and animate\
                results in terminology"
    )
    parser.add_argument("--chrono", action="store_true", help="crée une table qui affiche le temps pour faire chaque algo ")
    parser.add_argument("--hash", action="store_true", help="use hash tables")
    parser.add_argument("--nbsegment", action="store_true", help="affiche le nombre de segments")
    parser.add_argument("filenames", metavar="filename", nargs="+",
                        type=str, help="files to process")
    args = parser.parse_args()

    for filename in args.filenames:
        compute_path(filename, args.chrono, args.hash, args.nbsegment, fichier)


main()
