#!/usr/bin/env python3
'''
Scrape and reformat publication information for bulk upload to the BISB website
Niema Moshiri 2019
'''
COL_ORDER = ['PMID', 'PMCID', 'DOI', 'Source', 'FullJournalName', 'Year', 'Volume', 'Issue', 'Pages', 'Title', 'AuthorListStr']
NO_CAPITAL = {'and', 'in', 'of', 'the'}

def titlize(name):
    parts = name.split(' ')
    for i in range(len(parts)):
        if i == 0 or parts[i-1] == ':' or parts[i].lower() not in NO_CAPITAL:
            parts[i] = '%s%s' % (parts[i][0].upper(), parts[i][1:])
    return ' '.join(parts)

if __name__ == "__main__":
    # parse user arguments
    from sys import stderr; import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input PMID List (one per line)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output Publication Data File (TSV)")
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
    stderr.write("Parsing input PMIDs...\n")
    pmids = [l.strip() for l in infile]

    # prep Entrez
    stderr.write("Preparing Entrez...\n")
    from Bio import Entrez
    Entrez.email = args.email.strip()
    handle = Entrez.esummary(db="pubmed", id=','.join(pmids), retmode="xml")
    records = list(Entrez.parse(handle))

    # output publication data
    stderr.write("Outputting %d publication records...\n" % len(records))
    for i,record in enumerate(records):
        # prep record
        record['PMID'] = record['ArticleIds']['pubmed']            # get PMID
        if 'pmc' in record['ArticleIds']:
            record['PMCID'] = record['ArticleIds']['pmc']          # get PMCID
        else:
            record['PMCID'] = 'N/A'                                # specify N/A for missing PMCID
        for k in ['PMID','PMCID']:                                 # sometimes PMID is a list
            if isinstance(record[k], list):
                record[k] = record[k][0]
        record['Year'] = str(int(record['PubDate'].split(' ')[0])) # get year from publication date
        record['AuthorListStr'] = '|'.join(record['AuthorList'])   # pipe-separate authors
        for k in ['Source','FullJournalName']:                     # titlize journal name (abbreviated and full)
            record[k] = titlize(record[k])
        record['Title'] = record['Title'].rstrip('.')              # remove trailing period from title
        if record['Issue'].strip() == '':                          # specify N/A for missing issue
            record['Issue'] = 'N/A'
        if 'DOI' not in record:
            if 'doi' in record:                                    # sometimes DOI is key 'doi' instead of 'DOI'
                record['DOI'] = record['doi']
            else:
                record['DOI'] = 'N/A'                              # specify N/A for missing DOI

        # output record
        outfile.write('\t'.join(record[k] for k in COL_ORDER))
        outfile.write('\n')
        stderr.write("Completed record %d of %d\r" % (i+1,len(records)))
    stderr.write('\nDone\n')
