"""Keep native editable chart deck; make the primary deck use rendered plots.

All visible text remains editable. PNGs are rendered by standard JFreeChart
from the exact same chart data; native chart editing remains in the second file.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import xml.etree.ElementTree as ET
import shutil,json,copy
ROOT=Path(__file__).resolve().parent.parent
P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
C='http://schemas.openxmlformats.org/drawingml/2006/chart'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
NS={'p':P,'a':A,'r':R,'c':C}

def encoded(root):return ET.tostring(root,encoding='utf-8',xml_declaration=True)
def main():
    primary=ROOT/'Campus_Product_Launch.pptx';native=ROOT/'Campus_Product_Launch_EditableCharts.pptx';shutil.copyfile(primary,native)
    with ZipFile(primary) as z:entries={name:z.read(name) for name in z.namelist()}
    count=0
    for name in list(entries):
        if not name.startswith('ppt/slides/slide') or not name.endswith('.xml'):continue
        root=ET.fromstring(entries[name]);tree=root.find('p:cSld/p:spTree',NS)
        relname=name.replace('ppt/slides/','ppt/slides/_rels/')+'.rels';rr=ET.fromstring(entries[relname])
        for frame in list(tree):
            chart=frame.find('.//c:chart',NS)
            if chart is None:continue
            rid=chart.attrib['{'+R+'}id'];relationship=next(e for e in rr if e.attrib['Id']==rid)
            cid=int(relationship.attrib['Target'].split('chart')[-1].split('.')[0]);pic=ET.Element('{'+P+'}pic')
            nv=ET.SubElement(pic,'{'+P+'}nvPicPr');nv.append(copy.deepcopy(frame.find('p:nvGraphicFramePr/p:cNvPr',NS)))
            locks=ET.SubElement(nv,'{'+P+'}cNvPicPr');ET.SubElement(locks,'{'+A+'}picLocks',noChangeAspect='1');ET.SubElement(nv,'{'+P+'}nvPr')
            fill=ET.SubElement(pic,'{'+P+'}blipFill');ET.SubElement(fill,'{'+A+'}blip',{'{'+R+'}embed':rid});ET.SubElement(ET.SubElement(fill,'{'+A+'}stretch'),'{'+A+'}fillRect')
            sp=ET.SubElement(pic,'{'+P+'}spPr');transform=copy.deepcopy(frame.find('p:xfrm',NS));transform.tag='{'+A+'}xfrm';sp.append(transform)
            ET.SubElement(ET.SubElement(sp,'{'+A+'}prstGeom',prst='rect'),'{'+A+'}avLst')
            index=list(tree).index(frame);tree.remove(frame);tree.insert(index,pic)
            relationship.attrib.update(Type=R+'/image',Target=f'../media/chart{cid}.png');entries[f'ppt/media/chart{cid}.png']=(ROOT/f'figures/chart{cid}.png').read_bytes();count+=1
        entries[name]=encoded(root);entries[relname]=encoded(rr)
    for name in list(entries):
        if name.startswith(('ppt/charts/','ppt/embeddings/')):del entries[name]
    ct=ET.fromstring(entries['[Content_Types].xml'])
    for child in list(ct):
        if child.attrib.get('PartName','').startswith(('/ppt/charts/','/ppt/embeddings/')) or child.attrib.get('Extension')=='xlsx':ct.remove(child)
    ET.SubElement(ct,'{'+ct.tag.split('}')[0][1:]+'}Default',Extension='png',ContentType='image/png');entries['[Content_Types].xml']=encoded(ct)
    with ZipFile(primary,'w',ZIP_DEFLATED) as z:
        for name,value in entries.items():z.writestr(name,value)
    info=dict(primary=primary.name,native_editable_charts=native.name,visible_rendered_charts=count,
        chart_renderer='JFreeChart1.5.3 with exact bootstrap interval endpoints',
        text_and_shapes_editable=True,scope='Native chart data remain in the separate editable-chart deck')
    (ROOT/'sim/portable_deck_checks.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__':main()
