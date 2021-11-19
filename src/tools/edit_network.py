#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function


import os
from subprocess import call
import sys

try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  # noqa
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME'")

netedit = checkBinary('netedit')

if len(sys.argv) <= 1:
    sys.exit('Error: A network file must be provided.')

file = sys.argv[1]
call([netedit, file])
