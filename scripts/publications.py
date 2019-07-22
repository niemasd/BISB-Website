#!/usr/bin/env python3
'''
Scrape and reformat publication information for bulk upload to the BISB website
Niema Moshiri 2019
'''

if __name__ == "__main__":
    # parse user arguments
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input Publication Info (CSV)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    parser.add_argument('-e', '--email', required=True, type=str, help="Email Address (for Entrez)")
    args = parser.parse_args()
    if args.input == 'stdin':
        from sys import stdin as infile
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')

    # parse input publications
    pmids = [l.split(',')[0].strip() for l in infile]

    # prep Entrez
    from Bio import Entrez
    Entrez.email = args.email.strip()
    handle = Entrez.esummary(db="pubmed", id=pmids, retmode="xml")
    records = Entrez.parse(handle)

    # output publication data
    for record in records:
        outfile.write('%s\t' % record['Title'])
        outfile.write('%s\t' % record['DOI'])
        outfile.write('%s\t' % record['PubDate'])
        outfile.write('%s\t' % record['AuthorList'])
        outfile.write('\n')
