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
    outfile.write("title,field_biblio_authors_field,field_doi,field_isbn_number,field_issn_number,field_issue,field_number_of_volumes,field_custom7,field_publisher,field_pubmed_id,field_tracks,field_biblio_type,field_volume,field_biblio_year,field_journal,field_pages\n")
    for l in infile:
        if l.startswith('PMID\t'):
            continue
        pmid,pmcid,doi_isbn_url,journal_abbr,journal_full,issn,year,volume,issue,pages,title,authors = l.strip().split('\t')
        entry = dict()
        entry['title'] = title.strip()
        entry['authors'] = authors.replace('|', ', ')
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
        entry['num_volumes'] = ''
        entry['pmcid'] = pmcid
        entry['publisher'] = ''
        if pmid.strip() == NA:
            entry['pmid'] = ''
        else:
            entry['pmid'] = pmid
            entry['pub_type'] = PUB_TYPE['journal'] # override
        entry['bisb_tracks'] = ''
        entry['volume'] = volume.strip()
        entry['year'] = year.strip()
        entry['journal'] = journal_abbr.strip()
        entry['pages'] = pages.strip()
        for k in entry:
            if entry[k].strip() == NA:
                entry[k] = ''
        outfile.write('%s\n' % (','.join(('"%s"' % entry[k].replace('"',"'")) for k in ['title','authors','doi','isbn','issn','issue','num_volumes','pmcid','publisher','pmid','bisb_tracks','pub_type','volume','year','journal','pages'])))
