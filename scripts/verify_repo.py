"""Validate the public learner repository without executing Spark or Delta."""
from pathlib import Path
from decimal import Decimal
import ast, argparse, csv, hashlib, json, re

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'retailflow-v1.0.0'
def rows(path):
    with path.open(encoding='utf-8',newline='') as stream:
        reader=csv.DictReader(stream);result=list(reader)
        assert len(reader.fieldnames)==len(set(reader.fieldnames))
        assert all(None not in r and None not in r.values() for r in result)
        return result
def verify_manifest(root):
    manifest=root/'manifest.json';entries=json.loads(manifest.read_text(encoding='utf-8'))['files']
    for e in entries:
        content=(root/e['path']).read_bytes()
        assert len(content)==e['bytes'] and hashlib.sha256(content).hexdigest()==e['sha256'],e['path']
        if 'data_rows' in e:assert len(rows(root/e['path']))==e['data_rows']
    return len(entries)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--starter',action='store_true',help='Also require baseline file hashes and all exercise cells empty, before starting work.')
    args=parser.parse_args()
    pinned_files=verify_manifest(DATA)
    notebooks=sorted((ROOT/'notebooks').glob('*.ipynb'));assert len(notebooks)==7
    code_cells=0;exercises=0
    for path in notebooks:
        nb=json.loads(path.read_text(encoding='utf-8'));assert (nb['nbformat'],nb['nbformat_minor'])==(4,5)
        ids=[c['id'] for c in nb['cells']];assert len(ids)==len(set(ids))
        assert nb['metadata']['retailflow']['starter_repository_version']=='1.0.0'
        for cell in nb['cells']:
            assert 'instructor/expected/' not in cell['source']
            if cell['cell_type']!='code':continue
            compile(cell['source'],f'{path.name}:{cell["id"]}','exec');code_cells+=1
            if path.name.startswith('00_'):continue
            if cell['metadata']['retailflow']['role']=='lesson':
                exercises+=1
                if args.starter:
                    assert not ast.parse(cell['source']).body,cell['id']
                    assert cell['execution_count'] is None and cell['outputs']==[]
    assert exercises==32
    expected_counts={'stores':10,'products':12,'customers':20,'sales_batch_01':60,'sales_batch_02':23,'sales_dirty':68,'returns':6}
    for name,count in expected_counts.items():assert len(rows(DATA/'data'/f'{name}.csv'))==count
    for name,key in [('stores','store_id'),('products','product_id'),('customers','customer_id')]:
        rr=rows(DATA/'data'/f'{name}.csv');assert len({r[key] for r in rr})==len(rr)
    # Exercise the exact supplied Python cleaning utility, without importing Spark.
    cleaner_nb=json.loads((ROOT/'notebooks/03_clean_bronze_and_silver.ipynb').read_text(encoding='utf-8'))
    support=next(c['source'] for c in cleaner_nb['cells'] if c['id']=='python-utilities')
    namespace={'DATASET_ROOT':str(DATA)};exec(compile(support,'supplied-python-utilities','exec'),namespace)
    accepted,rejected,duplicates,repairs=namespace['clean_sales'](rows(DATA/'data/sales_dirty.csv'))
    assert (len(accepted),len(rejected),len(duplicates),len(repairs))==(60,6,2,6)
    assert rejected==rows(DATA/'checks/expected/quarantine.csv')
    business=namespace['business_records']
    initial=rows(DATA/'data/sales_batch_01.csv')
    assert business(accepted)==business(initial)
    assert business(initial)==business(rows(DATA/'checks/expected/initial_sales.csv'))
    # Reference snapshot cardinality/version validation; expected outputs remain checks only.
    incoming,rejected2,duplicate2,repairs2=namespace['clean_sales'](rows(DATA/'data/sales_batch_02.csv'))
    assert not rejected2 and not duplicate2 and not repairs2
    final=namespace['current_versions'](accepted+incoming)
    assert business(final)==business(rows(DATA/'checks/expected/final_sales.csv'))
    assert len(final)==80
    for stage,sales in [('initial',initial),('final',final)]:
        returns=namespace['visible_returns'](stage,sales)
        expected={r['metric']:r['value'] for r in rows(DATA/'checks/expected'/f'{stage}_metrics.csv')}
        amount=sum((Decimal(r['quantity'])*Decimal(r['unit_price'])*(1-Decimal(r['discount_pct'])/100) for r in sales),Decimal(0))
        refunds=sum((Decimal(r['refund_amount']) for r in returns),Decimal(0))
        assert Decimal(expected['net_sales'])==amount
        assert Decimal(expected['refund_amount'])==refunds
        assert Decimal(expected['net_revenue'])==amount-refunds
    # Check relative Markdown links in public documentation.
    for path in list(ROOT.glob('*.md'))+list((ROOT/'docs').glob('*.md')):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if not target.startswith(('https://','http://','#')):assert (path.parent/target.split('#')[0]).exists(),(path,target)
    if args.starter:
        baseline_files=verify_manifest(ROOT)
        assert not (ROOT/'instructor').exists()
        assert not list(ROOT.rglob('ANSWER_KEY.md'))
        assert not list(ROOT.rglob('*.env'))
        print(f'PASS: untouched starter inventory ({baseline_files} files plus root manifest); 32 exercise cells empty.')
    print(f'PASS: {pinned_files} pinned dataset/check files; 7 notebooks; {code_cells} code cells compile; source counts, cleaning, snapshots, returns and metrics agree.')
    print('Local verification only: Spark/Delta execution and public GitHub access still require their own checks.')
if __name__=='__main__':main()
