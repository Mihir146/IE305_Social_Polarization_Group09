"""Audit saved project evidence and write a reproducibility manifest.

Reads existing runs; does not manufacture engine data or rerun scenario searches.
"""
from pathlib import Path
import csv,json,hashlib,re,xml.etree.ElementTree as ET
from analyze import load_runs
from run_experiments import save
ROOT=Path(__file__).resolve().parent.parent
DESIGNS=[('pilot',540,30),('main',1800,100),('budget3',1800,100),('stress',2400,100),('behavior',2100,100),('quality_diagnostic',1200,100),('confirmation',400,100),('java_kernel',1080,30),('anylogic',None,None),('anylogic_network',None,None)]

def main():
    counts=[]
    for name,expected,markets in DESIGNS:
        path=ROOT/f'sim/results/{name}_runs.csv';rows=load_runs(path)
        if expected is not None:assert len(rows)==expected,(name,len(rows))
        if markets is not None:assert len({r['rep'] for r in rows})==markets
        else:assert rows and all(r['cohort']=='anylogic' for r in rows)
        counts.append(dict(dataset=name,policy_evaluation_rows=len(rows),market_labels=len({r['rep'] for r in rows}),
            implementation='Actual user engine export' if name.startswith('anylogic') else 'Standalone Java' if name=='java_kernel' else 'Python/NumPy initialization plus C++ dynamics',
            note='Markets reused across policies; do not pool datasets or generators as independent populations'))
    save(ROOT/'sim/analysis/experiment_inventory.csv',counts)
    original_hash='2762e98ce1b432139fcf5b896f8deb3f6b2a87718a9990b5f32bb1bf2b840759'
    assert hashlib.sha256((ROOT/'CampusProductLaunch.alp').read_bytes()).hexdigest()==original_hash
    kernel=(ROOT/'anylogic/ProductKernel.java').read_text().replace('public class ProductKernel {','public static class ProductKernel {',1)
    models=[]
    for name in ('CampusProductLaunch.alp','CampusProductLaunch_LiveNetwork.alp'):
        root=ET.parse(ROOT/name).getroot();ids=[e.text for e in root.iter('Id')];assert len(ids)==len(set(ids))
        main=root.find('.//ActiveObjectClass[Name="Main"]');assert kernel in main.findtext('AdditionalClassCode')
        assert main.findtext('.//EmbeddedObject[Name="consumers"]/Replication/Code')=='300'
        models.append(dict(model=name,sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),same_kernel=True,unique_ids=True))
    engine=list(csv.DictReader((ROOT/'sim/analysis/actual_anylogic_exact_comparison.csv').open()));net=list(csv.DictReader((ROOT/'sim/analysis/actual_anylogic_network_comparison.csv').open()));assert all(r['exact_match']=='1' for r in engine+net)
    for filename in ('deck_checks.json','portable_deck_checks.json','deck_poi_checks.json'):
        assert (ROOT/'sim'/filename).exists()
    assert json.loads((ROOT/'sim/deck_poi_checks.json').read_text())['schema_validation_passed']
    assert json.loads((ROOT/'sim/deck_checks.json').read_text())['planned_main_seconds']==735
    # Check local Markdown targets in selected-product documents; historical files keep their own scope.
    missing=[]
    for path in [*ROOT.glob('*.md'),ROOT.parent.parent/'RUN_ANYLOGIC.md',ROOT.parent.parent/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if target.startswith(('http:','https:','#','mailto:')):continue
            target=target.strip('<>').split('#')[0]
            if not (path.parent/target).exists():missing.append(dict(file=str(path.relative_to(ROOT.parent.parent)),target=target))
    assert not missing,missing
    info=dict(saved_dataset_checks_pass=True,reference_policy_evaluations=10240,standalone_java_evaluations=1080,
        actual_engine_summary_rows=sum(r['policy_evaluation_rows'] for r in counts if r['dataset'].startswith('anylogic')),
        actual_engine_independent_market_labels=len({r['rep'] for name,_,_ in DESIGNS if name.startswith('anylogic') for r in load_runs(ROOT/f'sim/results/{name}_runs.csv')}),
        engine_scope='Grid and earlier live-network default; same replication1000. White-layout visual check remains separate.',
        approved_grid_preserved=True,models=models,markdown_local_links_checked=True,
        primary_powerpoint_schema_valid=True,main_slides=12,backup_slides=4,main_seconds_including_demo=735,
        empirical_validation=False,paper_extraction_gaps='Explicit in parent/product literature read-status tables',
        remote_upload='Network/push now available; actual remote confirmation is recorded by Git, not inferred from local files')
    (ROOT/'sim/final_audit.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
    paths=[]
    for folder in ('sim','anylogic','data','figures'):
        for path in sorted((ROOT/folder).rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix in ('.so','.class','.pyc','.log'):continue
            if path.name in ('source_hashes.csv',):continue
            paths.append(dict(file=str(path.relative_to(ROOT)),bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    save(ROOT/'sim/source_hashes.csv',paths)
if __name__=='__main__':main()
