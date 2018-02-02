#!/usr/bin/env python
from __future__ import print_function
import argparse
import sys
import poagraph
import seqgraphalignment
import simplefasta

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-g', '--globalAlign', action='store_true', help='Global alignment, or (default) local alignment')
    parser.add_argument('-O', '--gapopen', type=int, default=-2, help='Gap opening score')
    parser.add_argument('-E', '--gapextend', type=int, default=-1, help='Gap extension score')
    parser.add_argument('-s', '--simple', action='store_true', help='Simple method')
    parser.add_argument('-m', '--match', type=int, default=2, help='Match score')
    parser.add_argument('-M', '--mismatch', type=int, default=-2, help='Mismatch score')
    parser.add_argument('-H', '--html', nargs='?', type=argparse.FileType('w'), default='poa.html', help='html output')
    args = parser.parse_args()

    seqNo = 0
    fasta = simplefasta.readfasta(args.infile)
    graph = poagraph.POAGraph(fasta[0][1], fasta[0][0])
    for label, sequence in fasta[1:]:
        alignment = seqgraphalignment.SeqGraphAlignment(sequence, graph, fastMethod=not args.simple,
                                                        globalAlign=args.globalAlign,
                                                        matchscore=args.match, mismatchscore=args.mismatch,
                                                        opengapscore=args.gapopen, extendgapscore=args.gapextend)
        graph.incorporateSeqAlignment(alignment, sequence, label)

    alignments = graph.generateAlignmentStrings()
    for label, alignstring in alignments:
        print("{0:15s} {1:s}".format(label, alignstring))

    if args.html is not None:
        graph.htmlOutput(args.html)
