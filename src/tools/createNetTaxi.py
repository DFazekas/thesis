"""
Create the XML input files for the generation of the SUMO network.
"""

from __future__ import absolute_import
from __future__ import print_function
import random
import subprocess
import os
import sys

# Import constants
from constants import PREFIX, DOUBLE_ROWS, ROW_DIST

# Modify system path to use the sumolib
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib

# Network building
nodes = open("%s.nod.xml" % PREFIX, "w")
sumolib.xml.writeHeader(nodes, root="nodes")
edges = open("%s.edg.xml" % PREFIX, "w")
sumolib.xml.writeHeader(edges, root="edges")

# Generate Main street (nodes & edges)
nodeID = "main0"
print('<node id="in" x="-100" y="0" />', file=nodes)
print('<edge id="mainin" from="in" to="%s" numLanes="2" />' % nodeID, file=edges)
for row in range(DOUBLE_ROWS):
    nextNodeID = "main%s" % row
    x = row * ROW_DIST
    print('<node id="%s" x="%s" y="0" />' % (nextNodeID, x), file=nodes)
    if row > 0:
        print('<node id="out" x="%s" y="0" />' % (x + 100), file=nodes)
    nodeID = nextNodeID
print('<node id="out" x="%s" y="0" />' % (x + 100), file=nodes)
print('<edge id="mainout" from="%s" to="out" numLanes="2" />' %
      nodeID, file=edges)

# Close nodes and edges files
print('</nodes>', file=nodes)
nodes.close()
print('</edges>', file=edges)
edges.close()

# Generate network file
subprocess.call([sumolib.checkBinary('netconvert'),
                 '-n', '%s.nod.xml' % PREFIX,
                 '-e', '%s.edg.xml' % PREFIX,
                 '-o', '%s.net.xml' % PREFIX])
