#!/usr/bin/env python3
'''
Convert my scraped and reformatted publication information to a Drupal-compatible CSV for bulk upload to the BISB website
Niema Moshiri 2019
'''
from PMIDs_to_publications import NA
DOI_URL_PREFIX = "https://doi.org"
ISBN_URL_PREFIX = "https://isbnsearch.org/isbn"
PUBMED_URL_PREFIX = "http://www.ncbi.nlm.nih.gov/pubmed"

# publication types
PUB_TYPE = {'book':'Book Chapter', 'journal':'Journal Article', 'other':''}

if __name__ == "__main__":
    # parse user arguments
    from sys import stderr; import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input Publication Information TSV")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output Drupal CSV")
    args = parser.parse_args()
    if args.input == 'stdin':
        from sys import stdin as infile
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output,'w')

    # parse publication info list and reformat output
    outfile.write("title,field_authors,field_doi,field_isbn_number,field_issn_number,field_issue,field_journal,field_pages,field_pmc_id,field_pubmed_id,field_bisb_training_grant,field_type,field_volume,field_year\n")
    for l in infile:
        if l.startswith('PMID\t'):
            continue
        try:
            pmid,pmcid,doi_isbn_url,journal_abbr,journal_full,issn,year,volume,issue,pages,title,authors,training_grant = l.strip().split('\t')
        except Exception as e:
            print("ERROR WITH LINE: %s" % l.strip())
            raise e
        entry = dict()
        entry['title'] = title.strip()
        entry['authors'] = authors.replace('|', ', ')
        entry['training_grant'] = {'Yes':'1', 'No':'0'}[training_grant.strip()]
        if doi_isbn_url.lower().startswith('doi:'):    # parse DOI
            entry['doi'] = ':'.join(doi_isbn_url.split(':')[1:]).strip()
            entry['isbn'] = ''
            entry['pub_type'] = PUB_TYPE['journal']
        elif doi_isbn_url.lower().startswith('isbn:'): # parse ISBN
            entry['doi'] = ''
            entry['isbn'] = ':'.join(doi_isbn_url.split(':')[1:]).strip(); url = '%s/%s' % (ISBN_URL_PREFIX, entry['isbn'])
            entry['pub_type'] = PUB_TYPE['book']
        elif doi_isbn_url.lower().startswith('url:'):  # parse URL
            entry['doi'] = ''
            entry['isbn'] = ''
            entry['pub_type'] = PUB_TYPE['other']
        elif doi_isbn_url.strip() == NA:
            entry['doi'] = ''
            entry['isbn'] = ''
            entry['pub_type'] = ''
        else:
            raise ValueError("Unrecognized DOI/ISBN/URL: %s" % doi_isbn_url.strip())
        entry['issn'] = issn.strip()
        entry['issue'] = issue.strip()
        entry['pmcid'] = pmcid
        if pmid.strip() == NA:
            entry['pmid'] = ''
        else:
            entry['pmid'] = pmid
            entry['pub_type'] = PUB_TYPE['journal'] # override
        entry['volume'] = volume.strip()
        entry['year'] = year.strip()
        entry['journal'] = journal_abbr.strip()
        entry['pages'] = pages.strip()
        for k in entry:
            if entry[k].strip() == NA:
                entry[k] = ''
        outfile.write('%s\n' % (','.join(('"%s"' % entry[k].replace('"',"'")) for k in ['title','authors','doi','isbn','issn','issue','journal','pages','pmcid','pmid','training_grant','pub_type','volume','year'])))
