# Updating Publications on the BISB Website
Publications can now be easily updated semi-frequently using Niema's [BISB Publication Database](https://docs.google.com/spreadsheets/d/1RbLJXoj9RzbB1eTLc1yQyk25iXGIti0L-YVYxv1E4Ws).

1. Download Niema's [BISB Publication Database](https://docs.google.com/spreadsheets/d/1RbLJXoj9RzbB1eTLc1yQyk25iXGIti0L-YVYxv1E4Ws) as a TSV file
2. Run [publications_to_drupal_CSV.py](scripts/publications_to_drupal_CSV.py) to convert it to a CSV file compatible with Drupal's "Import CSV" function
3. On the BISB website, delete all "Biblio" content nodes (e.g. via [this page](https://bioinformatics.ucsd.edu/admin/biblio-delete))
4. On the BISB website, go to "Configuration", then "Development", then "CSV importer", specify "Content", then specify "Biblio", and upload the CSV you created

# Updating the BISB Publication Database from PMIDs
If you want to generate your own database in the same format as Niema's [BISB Publication Database](https://docs.google.com/spreadsheets/d/1RbLJXoj9RzbB1eTLc1yQyk25iXGIti0L-YVYxv1E4Ws) (e.g. to add to Niema's database), you can do so easily from a list of PMIDs.

1. Create a file containing your list of PMIDs (one per line)
2. Run [PMIDs_to_publications.py](scripts/PMIDs_to_publications.py) to query PubMed for the metadata and output as a database in the same format as Niema's [BISB Publication Database](https://docs.google.com/spreadsheets/d/1RbLJXoj9RzbB1eTLc1yQyk25iXGIti0L-YVYxv1E4Ws)
