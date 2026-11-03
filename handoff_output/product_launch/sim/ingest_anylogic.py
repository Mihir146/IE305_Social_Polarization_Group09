"""Collect real AnyLogic summary exports; refuse duplicate reruns.

Usage: python sim/ingest_anylogic.py path/to/product_output
This never manufactures engine observations from Java or reference outputs.
"""
from pathlib import Path
import argparse,csv,json
from analyze import load_runs
from run_experiments import save
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path)
    ap.add_argument('--out',type=Path,default=ROOT/'results/anylogic_runs.csv');a=ap.parse_args()
    rows=[];seen=set()
    for path in sorted((a.directory/'summary').glob('*.csv')):
        with path.open(encoding='utf-8-sig',newline='') as f:sub=list(csv.DictReader(f))
        if len(sub)!=1:raise ValueError(f'Expected one summary row: {path}')
        row=sub[0]
        if row['cohort']!='anylogic':raise ValueError(f'Not labeled as an AnyLogic export: {path}')
        key=tuple(row[k] for k in ('scenario','strategy','price','h','rep'))
        if key in seen:raise ValueError(f'Duplicate policy/market: {path}')
        seen.add(key);rows.append(row)
    if not rows:raise ValueError('No summary/*.csv files found; use the folder printed by the engine console')
    a.out.parent.mkdir(parents=True,exist_ok=True);save(a.out,rows);checked=load_runs(a.out)
    info=dict(source_directory=str(a.directory.resolve()),summary_files=len(rows),
        independently_reported_market_labels=len({r['rep'] for r in checked}),
        origin='Files supplied by user as engine exports; cohort label alone does not cryptographically attest origin',
        accounting_and_schema_checked=True)
    a.out.with_suffix('.manifest.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__':main()
