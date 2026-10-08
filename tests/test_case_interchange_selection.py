"""真实 XMind ZIP 模板、字段裁剪和覆盖导入回归；全部为隔离合成用例。"""
import io
import json
import zipfile
import pytest
from test_case_features import features
from test_case_governance import governance
from services.case_interchange import read_xmind
from services.case_interchange import export_xmind
from models.module import Module
from models.test_case import TestCase as Case


def test_xmind_template_is_valid_and_preview_has_no_writes(features):
    g=features; c=g['client']; base=f"/api/v1/projects/{g['project'].id}/cases"
    template=c.get(base+'/template',params={'format':'xmind'})
    assert template.status_code==200,template.text
    assert 'case-template.xmind' in template.headers['content-disposition']
    row=read_xmind(template.content)[0]
    assert row['ID']=='' and row['用例名称'] and '填写操作步骤' in row['测试步骤']
    before=g['db'].query(Case).count()
    preview=c.post(base+'/import',params={'validate_only':True},files={'file':('template.xmind',template.content)})
    assert preview.json()['status']=='success',preview.text
    assert g['db'].query(Module).count()==0 and g['db'].query(Case).count()==before
    assert c.get(base+'/template',params={'format':'unsupported'}).status_code==422


def test_xmind_selected_fields_have_no_hidden_values_and_preserve_omitted_on_overwrite(features):
    g=features; c=g['client']; case=g['cases'][0]; base=f"/api/v1/projects/{g['project'].id}/cases"
    case.description='OMITTED-DESCRIPTION';case.precondition='OMITTED-PRECONDITION';case.tags=['OMITTED-TAG'];case.module_path='OMITTED-MODULE';case.priority='P0';g['db'].commit()
    exported=c.get(base+'/export',params={'format':'xmind','case_ids':case.id,'fields':'name,caseCode'})
    assert exported.status_code==200,exported.text
    with zipfile.ZipFile(io.BytesIO(exported.content)) as archive:
        text=archive.read('content.json').decode(); sheets=json.loads(text)
    assert 'OMITTED-' not in text and 'priority-1' not in text
    node=sheets[0]['rootTopic']['children']['attached'][0]
    assert node['atsCase']=={'case_code':case.case_code}
    assert set(read_xmind(exported.content)[0])=={'ID','用例名称'}
    node['title']='选择字段后更新名称'
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:archive.writestr('content.json',json.dumps(sheets,ensure_ascii=False))
    imported=c.post(base+'/import',params={'overwrite':True},files={'file':('selected.xmind',output.getvalue())})
    assert imported.json()['status']=='success',imported.text
    g['db'].refresh(case)
    assert case.name=='选择字段后更新名称'
    assert case.description=='OMITTED-DESCRIPTION' and case.precondition=='OMITTED-PRECONDITION' and case.tags==['OMITTED-TAG'] and case.priority=='P0'


def test_mixed_xmind_field_selections_preserve_each_nodes_omitted_values(features):
    g=features;first,second=g['cases'];base=f"/api/v1/projects/{g['project'].id}/cases"
    first.description='KEEP-OMITTED-A';first.priority='P0';first.tags=['KEEP-TAG'];first.module_path='';g['db'].commit()
    sheets=[]
    for case,fields in ((first,'name,caseCode'),(second,'name,caseCode,description,priority,tags,modulePath')):
        with zipfile.ZipFile(io.BytesIO(export_xmind([case],fields=fields))) as archive:sheets.extend(json.loads(archive.read('content.json')))
    sheets[0]['rootTopic']['children']['attached'][0]['title']='混合选择更新名称'
    output=io.BytesIO()
    with zipfile.ZipFile(output,'w') as archive:archive.writestr('content.json',json.dumps(sheets,ensure_ascii=False))
    response=g['client'].post(base+'/import',params={'overwrite':True},files={'file':('mixed.xmind',output.getvalue())})
    assert response.json()['status']=='success',response.text
    g['db'].refresh(first)
    assert first.name=='混合选择更新名称' and first.description=='KEEP-OMITTED-A' and first.priority=='P0' and first.tags==['KEEP-TAG']
    assert g['db'].query(Module).filter_by(name='nan').count()==0


@pytest.mark.parametrize('fields',['caseCode','name,unknown','name,createdBy',','.join(['name']*1000)])
def test_xmind_invalid_export_selection_is_rejected(features,fields):
    g=features
    response=g['client'].get(f"/api/v1/projects/{g['project'].id}/cases/export",params={'format':'xmind','fields':fields})
    assert response.status_code==422,response.text
