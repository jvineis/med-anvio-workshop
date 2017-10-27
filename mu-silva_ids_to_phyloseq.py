#!/usr/bin/env python
 
import sys
import csv
 
### ~~~~ This script is built to convert the hits from vsearch to the silva taxonomy db to a Phyloseq taxonomy table ~~~~~ ####
 
# it is run like this 
 
###   python mu-silva_ids_to_phyloseq.py "~/scripts/databas/silva119.tax" "table_of_hits_from_search" "table_of_all_node_ids"
## Note that the hits from vsearch and node ids are manipulated prior to running this script.  
 
## Created a file containing the node Ids
#grep ">" NODE-REPRESENTATIVES.fasta | cut -f 1 -d "|" | sed 's/>//g' > NODE-IDs.txt
 
## fix the vsearch output
#cut -f 1 -d "|" NODE-HITS.txt > NODE-HITS-1.txt
#cut -f 2 NODE-HITS.txt > NODE-HITS-2.txt
#paste NODE-HITS-1.txt NODE-HITS-2.txt > NODE-HITS-1-2.txt
#rm NODE-HITS-1.txt
#rm NODE-HITS-2.txt
#mv NODE-HITS-1-2.txt NODE-HITS.txt
 
## Input taxonomy ID to taxonomy string - this should be a two column table with col 1 = tax id and col2 = taxonomy string
tax_source = sys.argv[1]
 
# output from vsearch 
# eg "vsearch --usearch_global NODE-REPRESENTATIVES.fasta --db /groups/g454/blastdbs/gast_distributions/silva119.fa --blast6out NODE-HITS.txt --id 0.6"
node_hits = sys.argv[2]
 
#The name of the table containg all the node ids - some recd no hits from the silva db and are therefore not in the "node_hits"
node_ids = sys.argv[3]
# The name of the output file where the silva ids are converted to taxonomy strings
 
def open_input_to_dict(sample_name):
    sample_dict = {}
    with open(sample_name, 'rU') as f:
        for line in f:
            x = line.strip().split("\t")
            sample_dict[x[0]] = x[1]
    return sample_dict
 
def open_silva_database(db_name):
    db_name_dict = {}
    with open(db_name, 'rU') as f:
        for line in f:
            x = line.rstrip().split("\t")
            newkey = x[0]
            db_name_dict[newkey] = x[1]
    return db_name_dict
 
def open_node_id_to_list(node_ids_file):
    node_id_list = {}
    with open(node_ids_file, 'rU') as f:
        for line in f:
            x = line.rstrip()
            node_id_list[x] = x
    return node_id_list
 
# Create each of the dictionaries using the defined functions above
 
out_silvaid_table = open_input_to_dict(node_hits)
db_lookup = open_silva_database(tax_source)
node_ids_dict = open_node_id_to_list(node_ids)
     
#  Open and output file
output = open('PHYLOSEQ-TAX-OBJECT.txt', 'w')
 
# Add header to output file
output.write('node'+";"+'Domain'+";"+'Phylum'+";"+'Class'+";"+'Order'+";"+'Family'+";"+'Genus'+";"+'Species'+";"+'Subsp'+"\n")
 
# Add the node and taxonomy string to the output file
for key in out_silvaid_table.keys():
    x = out_silvaid_table[key]
    output.write(str(key)+";"+db_lookup[x]+"\n")
 
#  Add the nodes that rec'd no hit in the  silva db to the output.
for key in node_ids_dict.keys():
    if key not in out_silvaid_table.keys():
        output.write(str(key)+"\n")
 
 
output.close()
