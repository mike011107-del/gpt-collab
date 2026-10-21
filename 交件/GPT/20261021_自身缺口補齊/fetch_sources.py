from pathlib import Path
import urllib.request,hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'source_manifest.json').read_text(encoding='utf-8'))
rows=[]
for f in m['files']:
 url=f"https://raw.githubusercontent.com/{m['repository']}/{m['commit']}/{f['path']}"
 request=urllib.request.Request(url,headers={'User-Agent':'Codex-CIS-research'})
 b=urllib.request.urlopen(request,timeout=25).read()
 actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert actual==f['sha'] and len(b)==f['size'],f['path']
 p=root/'sources'/f['path'];p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(b)
 rows.append(dict(f,url=url,sha256=hashlib.sha256(b).hexdigest(),verified=True))
(root/'source_readback.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'downloaded':len(rows),'all_git_blobs_verified':all(x['verified'] for x in rows)}))
