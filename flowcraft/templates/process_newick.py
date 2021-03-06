#!/usr/bin/env python3

import os
import json
import dendropy

from flowcraft_utils.flowcraft_base import get_logger, MainWrapper



"""
Purpose
-------

This module is intended to process the newick generated by
 a proces to generate a report. The newick tree will be 
 rooted (midpoint). 
 
 
Expected input
--------------

The following variables are expected whether using NextFlow or the
:py:func:`main` executor.

- ``newick``: phylogenetic tree in newick format.

Generated output
----------------
- ``.report.jason``: Data structure for the report

Code documentation
------------------

"""

__version__ = "1.0.1"
__build__ = "20.09.2018"
__template__ = "raxml-nf"

logger = get_logger(__file__)


if __file__.endswith(".command.sh"):
    NEWICK = '$newick'
    logger.debug("Running {} with parameters:".format(
        os.path.basename(__file__)))
    logger.debug("NEWICK: {}".format(NEWICK))



@MainWrapper
def main(newick):
    """Main executor of the process_newick template.

    Parameters
    ----------
    newick : str
        path to the newick file.

    """

    logger.info("Starting newick file processing")

    print(newick)

    tree = dendropy.Tree.get(file=open(newick, 'r'), schema="newick")

    tree.reroot_at_midpoint()

    to_write=tree.as_string("newick").strip().replace("[&R] ", '').replace(' ', '_').replace("'", "")

    with open(".report.json", "w") as json_report:
        json_dic = {
            "treeData": [{
                "trees": [
                    to_write
                ]
            }],
        }

        json_report.write(json.dumps(json_dic, separators=(",", ":")))

    with open(".status", "w") as status_fh:
        status_fh.write("pass")


if __name__ == '__main__':

    main(NEWICK)

