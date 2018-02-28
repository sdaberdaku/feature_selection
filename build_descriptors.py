#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''This script loads all AAIndex1 features and builds descriptors for each amino acid in the given protein chains.
Each amino acid is assigned a descriptor of 553 features. The total list of AA indices is comprised of 566 entries, 
but 13 of them assign 'NA' values to one or more amino acid, so the script skips them. 

The script computes the set of descriptors for each entry in the DB5sel.fa protein database, and saves the results
in the './descriptors/' folder.'''

import re
from Bio.SeqUtils import seq3
import os

s="\s+-?(\d+\.\d*|\.\d+|\d+)"
AAIndex1 = {}
with open("aaindex1.txt", "r") as aaindex1_file :
    content = aaindex1_file.read()
    aa_indices = content.split("//\n")[:-1]
    for aa_index in aa_indices :
        m=re.search(r"H (.+)\n", aa_index)
        accession_number = m.group(1)
        i=re.search(r"%s\n%s\n" %(s*10, s*10), aa_index)
        if i : # the regex match fails if 'NA' is assigned to one or more amino acids, so we simply skip those entries
            AAIndex1[accession_number] = {"Ala": float(i.group(1)), "Arg": float(i.group(2)), "Asn": float(i.group(3)), "Asp": float(i.group(4)), "Cys": float(i.group(5)),
                                          "Gln": float(i.group(6)), "Glu": float(i.group(7)), "Gly": float(i.group(8)), "His": float(i.group(9)), "Ile": float(i.group(10)), 
                                          "Leu": float(i.group(11)),"Lys": float(i.group(12)),"Met": float(i.group(13)),"Phe": float(i.group(14)),"Pro": float(i.group(15)),
                                          "Ser": float(i.group(16)),"Thr": float(i.group(17)),"Trp": float(i.group(18)),"Tyr": float(i.group(19)),"Val": float(i.group(20))}
    print len(aa_indices)
    print len(AAIndex1)

# Save the list of extracted indices to file for later use
with open("total_indices_list.txt", "w") as id_list :
    id_list.write("\n".join(sorted(AAIndex1)))     
# Compute the descriptors
if not os.path.exists("./descriptors/"): os.makedirs("./descriptors/")
with open("DB5Sel.fa", "r") as in_DB5 :
    content = in_DB5.read()
    for entry in content.split(">")[1:] :
        fields = entry.split("\n")
        chainID = fields[0]
        aa_chain = fields[1]
        prediction = fields[2]
        print chainID
        with open("./descriptors/%s_descriptors.txt" % chainID, "w") as out_descriptors :
            descriptors = []
            for ii in range(len(aa_chain)) :
                if prediction[ii] == "I" :
                    y = "+1"
                else :
                    y = "-1"
                aa_name = seq3(aa_chain[ii])
                descriptor = y
                count = 1
                for aa_index in sorted(AAIndex1) : 
                    descriptor += "\t%d:%f" %(count, AAIndex1[aa_index][aa_name])
                    count += 1
                descriptors.append(descriptor)
            out_descriptors.write("\n".join(descriptors))
        