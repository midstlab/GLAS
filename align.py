import pandas as pd
from os.path import join
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import os
import warnings
import re

def findseq(id, protname):
    seq = ""

    idlst = id.split()
    if len(idlst)==1:
        url = "https://www.uniprot.org/uniprot/" + idlst[0] + ".fasta"

        context = ssl._create_unverified_context()
        html = urlopen(url, context=context)
        soup = BeautifulSoup(html, 'lxml')

        rows = soup.find('p')
        if rows is None:
            seq = "problem"
            return seq

        fasta = rows.string
        fas_seq = fasta.split('\n')

        for k in range(1, len(fas_seq) - 1):
            seq = seq + str(fas_seq[k])
    else:
        for i in idlst:
            url = "https://www.uniprot.org/uniprot/" + i + ".fasta"
            context = ssl._create_unverified_context()
            html = urlopen(url, context=context)
            soup = BeautifulSoup(html, 'lxml')

            rows = soup.find('p')
            if rows is None:
                seq = "problem"
                return seq

            fasta = rows.string
            fas_seq = fasta.split('\n')
            
            if str(protname).lower() in str(fas_seq[0]).lower():
                #print(protname)
                #print(fas_seq[0])
                for k in range(1, len(fas_seq) - 1):
                    seq = seq + str(fas_seq[k])

    return seq


def align(item, folderpath):
    
    folderpath = folderpath + "/ResultFiles" 
    dest = folderpath + "/AlignedResults"
    notfound = []
    #print(os.environ.get('PYTHONWARNINGS'))

    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore")
    df1 = pd.read_excel(join(folderpath, item), engine='openpyxl')
    colnames = list(df1.columns)
    uniprotID = df1['UniProt ID'].tolist()
    protnames = df1['Protein Name'].tolist()
    orig_protein = findseq(uniprotID[0], protnames[0])
    if orig_protein == "problem":
        notfound.append(item)
    else:
        bind_sites = [orig_protein]

        pdbID = df1['PDB ID'].tolist()
        res = df1[colnames[-1]].tolist()

        for k in range(len(pdbID)):
            stri = ""
            if pd.isna(res[k]):
                bind_sites.append(stri)
            else:
                for i in range(len(orig_protein)):
                    stri = stri + "-"
                lst1 = res[k].split(",")
                for m in range(len(lst1)):
                    str1 = lst1[m]
                    idx = str1.rfind("_")
                    aa = str1[idx + 1]
                    idx_ = str1.find("_")
                    idxline = str1.find("-")
                    location_string = re.sub(r'[^\d\n]+','',str1[idx_ + 2:idxline])
                    if location_string:
                        loc = int(location_string)
                    else:
                        loc = -1
                    stri = stri[:loc - 1] + aa + stri[loc:]

                bind_sites.append(stri)
        #print("Length of df1:", len(df1))
        #print("Length of bind_sites[1:]:", len(bind_sites[1:]))
        df1['Binding Site Alignment'] = bind_sites[1:]

        with open(dest + "/" + item.strip(".xlsx") + ".txt", "w", encoding='utf-8') as w:
            w.write(">" + item.strip(".xlsx") + "\n" + orig_protein + "\n")
            for key in range(len(bind_sites[1:])):
                w.write(">" + pdbID[key] + "\n" + bind_sites[key + 1] + "\n")

    if len(notfound) > 0:
        print("Uniprot ID could not be found for: \n")
        for id in notfound:
            print(id)
            print('\n')

    return dest
