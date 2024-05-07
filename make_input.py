#!/usr/bin/env python
import sys,os
import flib

query = sys.argv[1]

with open(f"{query}.input","w") as ofp:
    i = flib.get_id(query)
    ofp.write(str(i))
    ofp.write("\n")
    ofp.write(query)
    ofp.write("\n")

print("Done")

