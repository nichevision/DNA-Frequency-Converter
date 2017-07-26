# Takes all .txt files in a specified directory with the format:
#
# Allele    Locus1  Locus2  Locus3
# 8 .02 .007    .084
#
# And transforms it into a format that is importable into ArmedXpert.
#
# 09/09/14

import os
import sys

def transform_frequencies(dir, sep='\t'):
    for path in os.listdir(dir):
        if os.path.splitext(path)[-1] == '.txt':
            # Make the whole path
            path = os.path.join(dir, path)
            print("Parsing %s..." % path)
            name = os.path.splitext(os.path.basename(path))[0]
            output_path = os.path.join(os.path.dirname(path), name +  '_axfrq.csv')
            out = open(output_path, 'w')
            try:
                with open(path) as f:
                    lines = f.readlines()
                    loci = lines[0].split(sep)[1:]
                    for line in lines[1:]:
                        columns = line.split(sep)
                        allele = columns[0].strip()
                        frequencies = columns[1:]
                        for i in range(0, len(frequencies)):
                            locus = loci[i].strip()
                            freq = frequencies[i].strip()
                            if freq:
                                out.write('{name}{sep}{locus}{sep}{allele}{sep}{freq}\n'.format(
                                    name=name,
                                    sep=sep,
                                    locus=locus,
                                    allele=allele,
                                    freq=freq
                                ))
            finally:
                out.close()
    print("Done.")

if __name__ == '__main__':
    dir_name = sys.argv[1]
    transform_frequencies(
        dir_name
    )
