"""
Takes all files in a specified directory (and its subdirectories) and
finds the format:

    Bin    Range (alleles)     Count      Fraction
     1       11-   11            0        0.0000
     2       12-   12            0        0.0000
     3       13-   13            0        0.0000
     4       14-   14           35        0.1716

And transforms it into a format that is importable into ArmedXpert.

Example usage:

python popstats_converter.py .\examples_for_popstats_converter > output.csv
"""
import re
import os
import sys
import logging

logging.basicConfig(level=logging.ERROR)

logger = logging.getLogger(__name__)


def parse_line(line):
    data = re.findall('[\d\-\.]+', line)
    return data


def parse_popstats_file(file_obj):
    for line in file_obj:
        line = line.decode('utf8')
        yield parse_line(line), line


def transform_frequencies(dirname):
    races = dict()
    for root, dirs, files in os.walk(dirname):
        # Make the whole path
        for path_name in files:
            path = os.path.join(root, path_name)
            with open(path, 'rb') as fileobj:
                logger.info("FILE: %s", path)
                
                locus = os.path.splitext(path_name)[0]
                race = os.path.splitext(path_name)[-1][1:]
                
                for freq_data, line in parse_popstats_file(fileobj):
                    if len(freq_data) == 5:
                        data_bin, data_range, alleles, count, fraction = freq_data
                        print('{race}{sep}{locus}{sep}{allele}{sep}{freq}'.format(
                            race=race,
                            locus=locus,
                            allele=alleles,
                            freq=fraction,
                            sep='\t'
                        ))
                    else:
                        logger.warn("Found line with missing data in %s: %s", path, line)
                    


if __name__ == '__main__':
    dir_name = sys.argv[1]
    transform_frequencies(
        dir_name
    )
