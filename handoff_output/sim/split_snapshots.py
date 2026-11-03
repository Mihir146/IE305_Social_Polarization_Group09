"""Separate repeated-measure application rows by cap before ordinary analysis."""
import csv
from pathlib import Path
from collections import defaultdict
from analyze import save,load_csv

ROOT=Path(__file__).resolve().parent
def main():
    with (ROOT/'application_snapshots.csv').open() as f:rows=list(csv.DictReader(f))
    groups=defaultdict(list)
    for r in rows:groups[int(r['cap'])].append(r)
    out=ROOT/'application_by_horizon';out.mkdir(exist_ok=True)
    for cap,sub in sorted(groups.items()):
        path=out/f'cap{cap}.csv';save(path,sub);load_csv(path)
        print(path.name,len(sub),'realizations')
if __name__=='__main__':main()
