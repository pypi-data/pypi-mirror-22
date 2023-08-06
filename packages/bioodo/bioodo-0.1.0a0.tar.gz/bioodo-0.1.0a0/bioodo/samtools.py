# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
from bioodo import resource, annotate_by_uri, DataFrame, utils
import bioodo

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['samtools']


SECTION_NAMES = ['SN', 'FFQ', 'LFQ', 'GCF', 'GCL', 'GCC', 'IS', 'RL', 'ID', 'IC', 'COV', 'GCD']
COLUMNS = {
    'SN': ['statistic', 'value'],
    'FFQ': None,
    'LFQ': None,
    'GCF': ['percent', 'count'],
    'GCL': ['percent', 'count'],
    'GCC': ['cycle', 'A', 'C', 'G', 'T', 'ACGT_PCT', 'NO_PCT'],
    'IS': ['insert_size', 'pairs_total', 'inward_oriented_pairs',
           'outward_oriented_pairs', 'other_pairs'],
    'RL': ['length', 'count'],
    'ID': ['length', 'insertions', 'deletions'],
    'IC': ['cycle', 'insertions_fwd', 'insertions_rev',
           'deletions_fwd', 'deletions_rev'],
    'COV': ['bin', 'coverage', 'count'],
    'GCD': ['percent', 'unique', 'p10', 'p25', 'p50', 'p75', 'p90'],
}


@resource.register(config['stats']['pattern'],
                   priority=config['stats']['priority'])
@annotate_by_uri
def resource_samtools_stats(uri, key="SN", **kwargs):
    """Parse samtools stats text output file.

    Args:
      uri (str): filename
      key (str): result section to return

    Returns:
      DataFrame: DataFrame for requested section
    """
    if key not in SECTION_NAMES:
        raise KeyError("Not in allowed section names; allowed values are {}".format(", ".join(SECTION_NAMES + ["Summary"])))
    with open(uri) as fh:
        data = [[y for y in x.replace(":", "").strip().split("\t")[1:] if not y.startswith("#")] for x in fh.readlines() if x.startswith(key)]
    if key in ['FFQ', 'LFQ']:
        df = DataFrame.from_records(data)
        df = df.apply(pd.to_numeric, errors='ignore')
        df.columns = ['cycle'] + [str(x) for x in range(len(df.columns) - 1)]
        df = df.set_index('cycle')
    else:
        n = len(data[0])
        df = DataFrame.from_records(data, columns=COLUMNS[key][0:n])
        df = df.apply(pd.to_numeric, errors='ignore')
        df = df.set_index(df[COLUMNS[key][0]])
        del df[COLUMNS[key][0]]
    return df


# Aggregation function
def aggregate(infiles, outfile=None, regex=None, **kwargs):
    """Aggregate individual samtools reports to one output file

    Args:
      infiles (list): list of input files
      outfile (str): csv output file name
      regex (str): regular expression pattern to parse input file names
      kwargs (dict): keyword arguments

    """
    logger.debug("Aggregating samtools infiles {} in samtools aggregate".format(",".join(infiles)))
    df = utils.aggregate(infiles, regex=regex, **kwargs)
    if outfile:
        df.to_csv(outfile)
    else:
        return df
