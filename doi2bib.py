#!/usr/bin/env python
# read doi from a file or a single doi entry
# and spits out a bibtex entry onto stdout
# dependencies: python3, argparse, textwrap, wget, unix-like environment. 
# for a quick help:
# python doi2bib.py --help
#
# (c) Peter Beerli, Tallahassee FL 32311 July 2021
import sys
import os
# I have a large folder with PDF files and used this to generate a raw doi file
# grep -h -a -E "prism:doi" /path/to/your/pdfsfolder/*.pdf | sed 's/prism:doi//g;s/<>//g' > doitemp
# you will need manually clean the list and if it looks something like this:
# 10.1080/01621459.2013.866565
# 10.1016/j.tree.2014.03.002
# 10.1016/j.matcom.2014.02.005
# 10.1016/j.compbiolchem.2010.09.001
# 10.1371/journal.pcbi.1003537
# 10.1371/journal.pcbi.1003537
# 10.1016/j.jmps.2019.04.005
# 10.1186/1748-7188-7-13
# it should work
#
# with a single doi code you can do this:
#> python ~/bin/doi2bib.py 10.1073/pnas.1810239116 
#
#@article{Mashayekhi_2019,
#	doi = {10.1073/pnas.1810239116},
#	url = {https://doi.org/10.1073%2Fpnas.1810239116},
#	year = 2019,
#	month = {mar},
#	publisher = {Proceedings of the National Academy of Sciences},
#	volume = {116},
#	number = {13},
#	pages = {6244--6249},
#	author = {Somayeh Mashayekhi and Peter Beerli},
#	title = {Fractional coalescent},
#	journal = {Proceedings of the National Academy of Sciences}
#} 




def read_doicodes(arg):
    ''' 
    reads from a text file with doi codes or then falls back 
    to a single doi code
    '''
    doifile = []
    try:
        f = open(arg)
        for line in f:
    	    doifile.append(line.rstrip())
    	    #print(line.rstrip())
        f.close()
    except:
        doifile.append(arg)
    return doifile

def convert_doi_bib(doifile):
    ''' converts doi codes to bib entries'''
    for doi in doifile:
        #print(doi)
        os.system("sleep 1")
        os.system(f"wget -o doi2bib.log -O - http://api.crossref.org/works/{doi}/transform/application/x-bibtex")
        os.system('echo " "')
    return 'done'

def myparser():
    ''' parses command arguments'''
    import argparse
    import textwrap
    from argparse import ArgumentParser, HelpFormatter

    program_description= f'''
           Convert DOI codes to bibtex entries. 
           For example, try this

           python ~/bin/doi2bib.py 10.1073/pnas.1810239116

           This will return a single bibtext entry. 
           With a filename as argument, it is assumed that the 
           content consists of doi addresses one on each line.
           '''
    class RawFormatter(HelpFormatter):
        def _fill_text(self, text, width, indent):
            return "\n".join([textwrap.fill(line, width) for line in textwrap.indent(textwrap.dedent(text), indent).splitlines()])

    
    parser = argparse.ArgumentParser(description=program_description, formatter_class=RawFormatter)
    parser.add_argument('DOI', 
                        help='input file with doi codes or then a single doi code')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = myparser() # parses the commandline arguments
    doiarg = args.DOI
    doifile = read_doicodes(doiarg)
    done = convert_doi_bib(doifile)
