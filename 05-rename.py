#!/usr/bin/env python

from pathlib import Path
import os
import re

indir = Path("CHELSA-nc-amazon/")
flist = sorted(indir.glob("*"))

def fix_date(fname):
    if re.match(r"(\d{4})_(\d{2})_(\d{2})", fname.name):
        print(f"Name already valid: {fname.name}")
        return fname
    m = re.findall(r"(.*)_(\d{2})_(\d{2})_(\d{4})_(.*)", fname.name)[0]
    outfile = f"{m[0]}_{m[3]}_{m[2]}_{m[1]}_{m[4]}"
    return fname.parent / outfile

for fname in flist:
    os.rename(fname, fix_date(fname))
