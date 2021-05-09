#!/pkg/qct/software/python/2.7.6/bin/python
'''===------ CacheFileParser.py--------------------------------------------------===
   (c) 2020 Qualcomm Innovation Center, Inc. All rights reserved.

  ===----------------------------------------------------------------------='''

import argparse
import os
import sys
from CacheFilePyReader import CacheFileReader

cache_file_parser = argparse.ArgumentParser(
    description='Linker Cache File Parser')

# Add the arguments
cache_file_parser.add_argument('--cache-file',
                               metavar='cache_file',
                               required=True,
                               type=str,
                               help='Linker Cache File')

cache_file_parser.add_argument('--header',
                               help='Print File Header',
                               action='store_true')

cache_file_parser.add_argument('--sections',
                               help='Print all input sections',
                               action='store_true')
cache_file_parser.add_argument('--common_symbols',
                               help='Print all common symbols',
                               action='store_true')

# Execute the parse_args() method
args = cache_file_parser.parse_args()
cache_file = args.cache_file

if not os.path.exists(cache_file):
    print('The Cache file specified does not exist')
    sys.exit()

cache_file = CacheFileReader.CachingInfoDictReader(cache_file)
cache_file.readDictionary()

if args.header:
    dictionary_header = cache_file.getHeader()
    dictionary_header.printHeader()

objfiles = cache_file.getInputFiles()
out_sections = cache_file.getOutputSections()

sections = cache_file.getInputSections(out_sections, objfiles)
if args.sections:
    print('Input Section Name\t Output Section Name \t Input File')
    print('-' * 80)
    for x in sections:
        if x.getSectionName() != "":
            x.dump()

symbols = cache_file.getCommonSymbols(out_sections, objfiles)
if args.common_symbols:
    for x in symbols:
        x.dump()
