"""Package project files without Git metadata, caches or installed software."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,csv,hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'handoff_output/IE305_Group09_Submission.zip'

def selected():
    files=[]
    for folder in ('handoff_output','handoff'):
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts or p.name=='SUBMISSION_ARCHIVE.json':continue
            if p.suffix in ('.zip','.so','.class','.pyc','.log','.tmp') or p.name.endswith('.alp.autosave'):continue
            files.append(p)
    for name in ('README.md','PROJECT_JOURNAL.md','RUN_ANYLOGIC.md'):
        files.append(ROOT/name)
    return sorted(set(files))

def main():
    files=selected();manifest=ROOT/'handoff_output/SUBMISSION_MANIFEST.csv'
    files=[p for p in files if p!=manifest]
    with manifest.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['file','bytes','sha256']);w.writeheader()
        for p in files:w.writerow(dict(file=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    files.append(manifest)
    with ZipFile(OUT,'w',ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:z.write(p,'IE305_Group09/'+str(p.relative_to(ROOT)))
    with ZipFile(OUT) as z:
        assert z.testzip() is None
        for name in ('CampusProductLaunch.alp','CampusProductLaunch_LiveNetwork.alp','Campus_Product_Launch.pptx','Campus_Product_Launch.pdf'):
            assert 'IE305_Group09/handoff_output/product_launch/'+name in z.namelist()
        assert 'IE305_Group09/handoff_output/sim/native.cpp' in z.namelist()
    info=dict(archive=str(OUT.relative_to(ROOT)),files=len(files),bytes=OUT.stat().st_size,sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),crc_test_pass=True,
        includes='Models, presentation, data, scripts, literature, validation and archived mechanism evidence',excludes='Git metadata, caches, regenerable binaries, logs, application autosaves and other ZIPs',
        uploaded_to_moodle=False,remote_push_performed_by_user=True)
    (ROOT/'handoff_output/SUBMISSION_ARCHIVE.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__':main()
