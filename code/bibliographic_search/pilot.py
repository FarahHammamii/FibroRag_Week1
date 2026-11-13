"""Pilot bibliographic search (PubMed, Europe PMC, OpenAlex). Metadata only, no patient data. Needs Internet."""
import argparse,csv,json,os,time,urllib.parse,urllib.request,urllib.error,datetime,pathlib,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[2]

def get(url,params,delay):
    target=url+'?'+urllib.parse.urlencode(params)
    for i in range(3):
        try:
            time.sleep(delay)
            req=urllib.request.Request(target,headers={'User-Agent':'FibroRAG-research/0.1 '+os.getenv('CONTACT_EMAIL','')})
            with urllib.request.urlopen(req,timeout=20) as r: return json.load(r)
        except (OSError,ValueError) as e:
            if i==2: raise
            time.sleep(2**i)

def run(row,limit,raw):
    base,q=row['base'],row['equation']; count=None; items=[]
    def save(x,n): (raw/f"{row['id']}_{n}.json").write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
    if base=='PubMed':
        u='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        common={'db':'pubmed','retmode':'json','tool':'fibro_rag','email':os.getenv('CONTACT_EMAIL','')}
        if os.getenv('NCBI_API_KEY'): common['api_key']=os.environ['NCBI_API_KEY']
        r=get(u+'esearch.fcgi',{**common,'term':q,'retmax':0},0.4);save(r,'count');count=int(r['esearchresult']['count'])
        for start in range(0,min(limit,count,9999),100):
            x=get(u+'esearch.fcgi',{**common,'term':q,'retstart':start,'retmax':min(100,limit-start,9999-start)},0.4);save(x,f'ids_{start}')
            ids=x['esearchresult']['idlist'];
            if not ids: break
            z=get(u+'esummary.fcgi',{**common,'id':','.join(ids)},0.4);save(z,f'meta_{start}')
            for i in ids:
                a=z['result'].get(i,{});doi=next((k['value'] for k in a.get('articleids',[]) if k['idtype']=='doi'),'');items.append({'pmid':i,'doi':doi,'title':a.get('title',''),'date':a.get('pubdate',''),'url':'https://pubmed.ncbi.nlm.nih.gov/'+i+'/'})
    elif base=='OpenAlex':
        u='https://api.openalex.org/works';cursor='*';page=0
        params={'search':q,'filter':'from_publication_date:2023-01-01,to_publication_date:2026-11-12','per_page':min(100,limit),'mailto':os.getenv('CONTACT_EMAIL','')}
        if os.getenv('OPENALEX_API_KEY'): params['api_key']=os.environ['OPENALEX_API_KEY']
        while cursor and len(items)<limit:
            x=get(u,{**params,'cursor':cursor},1);save(x,page);count=x['meta']['count'];cursor=x['meta'].get('next_cursor');page+=1
            if not x['results']:break
            for a in x['results'][:limit-len(items)]: items.append({'pmid':(a.get('ids',{}).get('pmid') or '').rsplit('/',1)[-1],'doi':a.get('doi') or '', 'title':a.get('display_name',''),'date':a.get('publication_date',''),'url':a.get('id','')})
    elif base=='Europe PMC':
        u='https://www.ebi.ac.uk/europepmc/webservices/rest/search';cursor='*';page=0
        while cursor and len(items)<limit:
            x=get(u,{'query':q,'format':'json','pageSize':min(100,limit-len(items)),'cursorMark':cursor,'resultType':'lite'},0.5);save(x,page);count=x['hitCount'];page+=1
            old=cursor;cursor=x.get('nextCursorMark');results=x.get('resultList',{}).get('result',[])
            for a in results: items.append({'pmid':a.get('pmid',''),'doi':a.get('doi',''),'title':a.get('title',''),'date':a.get('pubYear',''),'url':'https://europepmc.org/article/'+a.get('source','')+'/'+a.get('id','')})
            if not results or cursor==old:break
    else:raise ValueError(base)
    return count,items

def dedup(items):
    out=[]; by={}
    for a in items:
        doi=a['doi'].lower().removeprefix('https://doi.org/').strip();pmid=a['pmid'].strip();keys=[k for k in ('doi:'+doi if doi else '', 'pmid:'+pmid if pmid else '') if k]
        # Title fallback only if no strong ID, and retain manual review.
        if not keys:keys=['title:'+''.join(c for c in a['title'].lower() if c.isalnum())]
        match=next((by[k] for k in keys if k in by),None)
        if match is None: match=dict(a,query_ids=[a['query_id']]);out.append(match)
        else: match['query_ids']=sorted(set(match['query_ids']+[a['query_id']]))
        for k in keys:by[k]=match
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--ids',nargs='+',required=True);p.add_argument('--limit',type=int,default=30);p.add_argument('--out',type=pathlib.Path,required=True);args=p.parse_args()
    if args.limit<1 or args.limit>9999:p.error('pilot limit 1..9999')
    args.out.mkdir(parents=True,exist_ok=False);raw=args.out/'raw';raw.mkdir();logs=[];allitems=[]
    rows=list(csv.DictReader((ROOT/'review/search_queries.csv').open(encoding='utf-8-sig')))
    missing=set(args.ids)-{r['id'] for r in rows}
    if missing:p.error(str(missing))
    for r in rows:
        if r['id'] not in args.ids:continue
        log={'id':r['id'],'base':r['base'],'query':r['equation'],'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'count':None,'n_export':0,'status':'failed','error':''}
        try:
            count,items=run(r,args.limit,raw);log.update(count=count,n_export=len(items),status='ok');allitems.extend(dict(a,query_id=r['id']) for a in items)
        except Exception as e:log['error']=str(e)
        logs.append(log)
    unique=dedup(allitems)
    for name,data in [('log',logs),('results_raw_metadata',allitems),('results_dedup',unique)]: (args.out/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    with (args.out/'log.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(logs[0]));w.writeheader();w.writerows(logs)
    manifest={str(x.relative_to(args.out)):hashlib.sha256(x.read_bytes()).hexdigest() for x in args.out.rglob('*') if x.is_file()};(args.out/'sha256.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(logs,ensure_ascii=False,indent=2));return int(any(x['status']!='ok' for x in logs))
if __name__=='__main__':raise SystemExit(main())
