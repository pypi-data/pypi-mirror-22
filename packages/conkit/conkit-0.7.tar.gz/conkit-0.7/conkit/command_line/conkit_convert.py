#!/usr/bin/env python
"""This script provides direct access to ConKit's conversion algorithms.

This script can convert either contact prediction files or sequence files.
In case of the latter, a file with a single or multiple sequences can be
converted.

!!! IMPORTANT
=============
Do not attempt to mix formats, i.e. convert from a contact file format
to a sequence file format.

"""

__author__ = "Felix Simkovic"
__date__ = "01 Oct 2016"
__version__ = "0.1"

import argparse
import sys

import conkit.command_line
import conkit.io

_OPTIONS = sorted(
    conkit.io.CONTACT_FILE_PARSERS.keys() 
    + conkit.io.SEQUENCE_FILE_PARSERS.keys()
)

logger = conkit.command_line.get_logger('converter', level='info')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile')
    parser.add_argument('informat')
    parser.add_argument('outfile')
    parser.add_argument('outformat')
    args = parser.parse_args()
    
    # Perform the conversion
    logger.info("Converting file\n\t%s of format %s\nto file\n\t%s of format %s", 
                args.infile, args.informat, args.outfile, args.outformat)
    conkit.io.convert(args.infile, args.informat, args.outfile, args.outformat)

    return


if __name__ == "__main__":
    sys.exit(main())
