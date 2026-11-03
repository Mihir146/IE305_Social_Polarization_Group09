"""Merge one-row AnyLogic CSVs and validate schema before analysis."""
from pathlib import Path
import argparse,csv
from analyze import load_csv,SCHEMA

def main():
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    paths=sorted(x for x in a.directory.glob('*.csv') if x.resolve()!=a.out.resolve())
    if not paths:raise ValueError('No CSV files in '+str(a.directory))
    rows=[];fields=None
    for path in paths:
        with path.open() as f:
            reader=csv.DictReader(f)
            if fields is None:fields=reader.fieldnames
            if fields!=reader.fieldnames:raise ValueError('Header mismatch: '+str(path))
            rows.extend(reader)
    # Validate before writing the requested output.
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w',suffix='.csv',delete=False) as f:
        tmp=Path(f.name);w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    try:load_csv(tmp)
    finally:tmp.unlink()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    print(len(rows),'valid runs ->',a.out)
if __name__=='__main__':main()
