# Filename: synonymsfetch.py
# Author: Thomas H. Smith 2017

from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import xml.dom.minidom
import urllib2
from urllib2 import HTTPError, URLError
#from operator import itemgetter
from requests.exceptions import ReadTimeout


## TODO add functionality for db saving
def build_syns_df(_df):
    """
    Retrieve synonyms associated with a given protein. Synonyms
    db was retrieved from Uniprot.org. Option to save the db or
    begin with a db generated from a previous analysis.

    Parameters
    ----------
    _df : pandas.DataFrame
        Input df containing protein IDs

    save_db : str
        String arguments for creation ('new') a saved local database
        of synonyms or expansation ('expand') or a previously saved
        database pickle, saved in package's /data directory

    Returns
    -------
    df_syns : pandas.DataFrame
        Output df containing synonyms associated with input
        df unique protein IDs

    """
    df_in = _df.copy()
    uniprot_ids = list(df_in.Protein.unique())
    print 'Getting synonyms from Uniprot for %d unique proteins.' % len(uniprot_ids)
    print 'This may take several minutes...'
    pool = ThreadPool(32)
    results = pool.map(_fetchUniprotSynonyms, uniprot_ids)
    pool.close()
    pool.join()
    df_syns = pd.DataFrame(results)
    #df_syns['Synonyms'] = df_syns['Synonyms'].apply(lambda x: _conv_syns(x))
    df_syns.set_index('UniprotID', inplace=True)
    print 'Finished building synonyms table.'
    return df_syns

def _conv_syns(syns):
    syns = ','.join([str(x) for x in syns])
    return syns


def _fetchUniprotSynonyms(uniprot_ID):
    url = 'http://www.uniprot.org/uniprot/%s.xml' % uniprot_ID
    try:
        fp = urllib2.urlopen(url)
        doc = xml.dom.minidom.parse(fp)
        fp.close()
    except HTTPError:
        print 'Caught HTTPError for %s' % uniprot_ID
        return [0]
    syns = []
    protein_elements = doc.getElementsByTagName('protein')
    if len(protein_elements) > 0:
        for prot_elem in protein_elements:
            full_names = prot_elem.getElementsByTagName('fullName')
            short_names = prot_elem.getElementsByTagName('shortName')
            if len(full_names) > 0:
                for node in full_names:
                    syns.append(node.childNodes[0].data)
            if len(short_names) > 0:
                for node in short_names:
                    syns.append(node.childNodes[0].data)
    gene_elements = doc.getElementsByTagName('gene')
    if len(gene_elements) > 0:
        for gene_elem in gene_elements:
            names = gene_elem.getElementsByTagName('name')
            if len(names) > 0:
                for node in names:
                    syns.append(node.childNodes[0].data)
    syns = set(syns)
    syns = list(syns)
    return {'UniprotID':uniprot_ID, 'Synonyms':syns}

