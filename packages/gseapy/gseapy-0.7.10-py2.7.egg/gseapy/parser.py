# -*- coding: utf-8 -*-
from numpy import in1d
from pandas import read_table, DataFrame
from .utils import unique, DEFAULT_LIBRARY
import sys, logging, json

logger = logging.getLogger(__name__)

def gsea_cls_parser(cls):
    """Extact class(phenotype) name from .cls file.
    
    :param cls: the a class list instance or .cls file which is identical to GSEA input .
    :return: phenotype name and a list of class vector. 
    """

    if isinstance(cls, list) :
        classes = cls
        sample_name= unique(classes)
    elif isinstance(cls, str) :    
        with open(cls) as c:
            file = c.readlines()
        classes = file[2].strip('\n').split(" ")
        sample_name = file[1].lstrip("# ").strip('\n').split(" ")
    else:
        raise Exception('Error parsing sample name!')
  
    return sample_name[0], sample_name[1], classes

def gsea_edb_parser(results_path, index=0):
    """Parse results.edb file stored under **edb** file folder.            

    :param results_path: the .results file where lcoated inside edb folder.
    :param index: gene_set index of gmt database, used for iterating items.   
    :return: enrichment_term, hit_index,nes, pval, fdr.
    """
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(open(results_path), features='xml')
    tag = soup.findAll('DTG')   
    term = dict(tag[index].attrs)
    # dict_keys(['RANKED_LIST', 'GENESET', 'FWER', 'ES_PROFILE', 
    # 'HIT_INDICES', 'ES', 'NES', 'TEMPLATE', 'RND_ES', 'RANK_SCORE_AT_ES',
    #'NP', 'RANK_AT_ES', 'FDR'])         
    enrich_term = term.get('GENESET').split("#")[1]
    es_profile = term.get('ES_PROFILE').split(" ")
    #rank_es = term.get('RND_ES').split(" ")
    hit_ind =term.get('HIT_INDICES').split(" ")
    es_profile = [float(i) for i in es_profile ]
    hit_ind = [float(i) for i in hit_ind ]
    #rank_es = [float(i) for i in rank_es ]
    nes = term.get('NES')
    pval = term.get('NP')
    fdr =  term.get('FDR')
    #fwer = term.get('FWER')   
    #index_range = len(tag)-1
    logger.debug("Enriched Gene set is: "+ enrich_term)

    return enrich_term, hit_ind, nes, pval, fdr
    

def gsea_rank_metric(rnk):
    """Parse .rnk file. This file contains ranking correlation vector and gene names or ids. 
    
    :param rnk: the .rnk file of GSEA input or a ranked pandas DataFrame instance.
    :return: a pandas DataFrame with 3 columns names are:
             
                 'gene_name','rank',rank2'
                 
    """
    if isinstance(rnk, DataFrame) :
        rank_metric = rnk.copy()
    elif isinstance(rnk, str) :
        rank_metric = read_table(rnk,header=None)
    else:
        raise Exception('Error parsing gene list!')
        
    rank_metric.columns = ['gene_name','rank']
    rank_metric['rank2'] = rank_metric['rank']
           
    return rank_metric
    
def gsea_gmt_parser(gmt, min_size = 3, max_size = 1000, gene_list=None):
    """Parse gene_sets.gmt(gene set database) file or download from enrichr server.  
    
    :param gmt: the gene_sets.gmt file of GSEA input or an enrichr libary name.
                checkout full enrichr library name here: http://amp.pharm.mssm.edu/Enrichr/#stats
                
    :param min_size: Minimum allowed number of genes from gene set also the data set. Default: 3. 
    :param max_size: Maximum allowed number of genes from gene set also the data set. Default: 5000.
    :param gene_list: Used for filtering gene set. Only used this argument for :func:`call` method.
    :return: Return a new filtered gene set database dictionary. 

    **DO NOT** filter gene sets, when use :func:`replot`. Because ``GSEA`` Desktop have already
    do this for you.
            
    """

    if gmt.lower().endswith(".gmt"):
        logger.info("User Defined gene sets is given.......continue..........") 
        with open(gmt) as genesets:    
             genesets_dict = { line.strip("\n").split("\t")[0]: line.strip("\n").split("\t")[2:] 
                              for line in genesets.readlines()}    
    else:
        logger.info("Downloading and generating Enrichr library gene sets...") 
        if gmt in DEFAULT_LIBRARY:
            names = DEFAULT_LIBRARY
        else:
            names = get_library_name()
        if gmt in names:
            import requests
            ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/geneSetLibrary'
            query_string = '?mode=text&libraryName=%s'
            response = requests.get( ENRICHR_URL + query_string % gmt)
        else: 
            raise Exception("gene_set files(.gmt) not found")
        if not response.ok:
            raise Exception('Error fetching enrichment results, check internet connection first.')
                     
        genesets_dict = { line.split("\t")[0]: 
                          [gene.strip("\n").split(",")[0] for gene in line.split("\t")[2:-1]] 
                          for line in response.iter_lines(chunk_size=1024, decode_unicode='utf-8')}    
 
    

    #filtering dict
    if sys.version_info[0] == 3 :
        genesets_filter =  {k: v for k, v in genesets_dict.items() if len(v) >= min_size and len(v) <= max_size}
    elif sys.version_info[0] == 2:
        genesets_filter =  {k: v for k, v in genesets_dict.iteritems() if len(v) >= min_size and len(v) <= max_size}
    else:
        sys.stderr.write("System failure. Please Provide correct input files")
        sys.exit(1)    
    if gene_list is not None:
        subsets = sorted(genesets_filter.keys())             
        for subset in subsets:            
            tag_indicator = in1d(gene_list, genesets_filter.get(subset), assume_unique=True)
            tag_len = sum(tag_indicator)      
            if tag_len <= min_size or tag_len >= max_size:                    
                del genesets_filter[subset]
            else:
                continue
    #some_dict = {key: value for key, value in some_dict.items() if value != value_to_remove}
    #use np.intersect1d() may be faster???    
    filsets_num = len(genesets_dict) - len(genesets_filter)
    logging.info("{a} gene_sets have been filtered out when max_size={b} and min_size={c}".format(a=filsets_num,b=max_size,c=min_size))
    
    if filsets_num == len(genesets_dict):
        sys.stderr.write("No gene sets passed throught filtering condition!!!, try new paramters again!\n" +\
                         "Note: Gene names for gseapy is case sensitive." )
        sys.exit(1)
    else:
        return genesets_filter
    
def get_library_name():
    """return enrichr active enrichr library name. """

    # make a get request to get the gmt names and meta data from Enrichr
    #python 2
    if sys.version_info[0] == 2 :
        import urllib2
        x = urllib2.urlopen('http://amp.pharm.mssm.edu/Enrichr/geneSetLibrary?mode=meta')
        response = x.read()
        gmt_data = json.loads(response)

    # python 3
    elif sys.version_info[0] == 3:
        import urllib
        x = urllib.request.urlopen('http://amp.pharm.mssm.edu/Enrichr/geneSetLibrary?mode=meta')
        response = x.read()
        gmt_data = json.loads(response.decode('utf-8'))
    else:
        sys.stderr.write("System failure. Please Provide correct input files")
        sys.exit(1) 
    # generate list of gmts 
    gmt_names = []

    # get library names 
    for inst_gmt in gmt_data['libraries']:

        # only include active gmts 
        if inst_gmt['isActive'] == True:
            gmt_names.append(inst_gmt['libraryName'])
    
    return sorted(gmt_names)