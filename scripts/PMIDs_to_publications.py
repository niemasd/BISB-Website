#!/usr/bin/env python3
'''
Scrape and reformat publication information for bulk upload to the BISB website
Niema Moshiri 2019
'''
COL_ORDER = ['PMID', 'PMCID', 'DOI', 'Source', 'FullJournalName', 'Year', 'Volume', 'Issue', 'Pages', 'Title', 'AuthorListStr']

def titlize(name):
    return name.title().replace(' And ',' and ').replace(' Of ',' of ').replace(' The ',' the ')

if __name__ == "__main__":
    # parse user arguments
    import argparse
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
    pmids = [l.strip() for l in infile]

    # prep Entrez
    from Bio import Entrez
    Entrez.email = args.email.strip()
    handle = Entrez.esummary(db="pubmed", id=','.join(pmids), retmode="xml")
    records = Entrez.parse(handle)

    # output publication data
    for record in records:
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
