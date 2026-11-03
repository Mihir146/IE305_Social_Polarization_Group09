"""Exercise CSV ingestion on reference-data fixtures; NOT AnyLogic validation."""
from pathlib import Path
import csv,sys,subprocess,tempfile
from analyze import load_csv,save
ROOT=Path(__file__).resolve().parent

def main():
    with (ROOT/'results_primary.csv').open() as f:rows=list(csv.DictReader(f))[:3]
    checks=[]
    with tempfile.TemporaryDirectory(prefix='ie305_csv_fixture_') as td:
        tmp=Path(td);source=tmp/'source';source.mkdir()
        save(source/'one.csv',rows[:1]);save(source/'two.csv',rows[1:])
        target=tmp/'merged.csv'
        subprocess.run([sys.executable,str(ROOT/'ingest_anylogic.py'),str(source),'--out',str(target)],check=True,capture_output=True,text=True)
        assert len(load_csv(target))==3
        checks.append(dict(check='ingest_reference_fixture',status='PASS',scope='CSV plumbing only; no AnyLogic observations'))
        for name,change in [
            ('mixed_caps',lambda a:a[1].update(cap='3000')),
            ('duplicate_replication',lambda a:a[1].update(rep=a[0]['rep'])),
            ('duplicate_seed',lambda a:a[1].update(seed=a[0]['seed'])),
            ('invalid_isolate_rule',lambda a:a[1].update(allow_isolates='2')),
            ('edge_loss',lambda a:a[1].update(edges_end=str(int(a[1]['edges_end'])-1))),
            ('invalid_fraction',lambda a:a[1].update(giant_frac='1.1'))]:
            bad=[dict(r) for r in rows];change(bad);path=tmp/(name+'.csv');save(path,bad)
            try:load_csv(path)
            except ValueError:pass
            else:raise AssertionError('Accepted invalid fixture: '+name)
            checks.append(dict(check='reject_'+name,status='PASS',scope='CSV plumbing only; deliberate invalid fixture'))
        subprocess.run([sys.executable,str(ROOT/'analyze.py'),'--input',str(target),'--outdir',str(tmp/'analysis'),'--tables-only'],check=True,capture_output=True,text=True)
        checks.append(dict(check='analyze_partial_grid',status='PASS',scope='CSV plumbing only; reference fixture'))
        subprocess.run([sys.executable,str(ROOT/'compare_anylogic.py'),'--anylogic',str(target),'--reference',str(ROOT/'results_primary.csv'),'--out',str(tmp/'comparison.csv')],check=True,capture_output=True,text=True)
        checks.append(dict(check='comparison_command_reference_fixture',status='PASS',scope='Command plumbing only; NOT cross-implementation agreement'))
    save(ROOT/'pipeline_checks.csv',checks)
    print('PASS:',len(checks),'pipeline checks; NO AnyLogic comparison was performed')
if __name__=='__main__':main()
