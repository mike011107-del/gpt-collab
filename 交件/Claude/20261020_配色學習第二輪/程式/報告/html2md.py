# 把報告 HTML 轉成文字版 Markdown（給 GPT 與專案資料夾）。圖改成「〔圖〕說明」。
import re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.buf=''; s.stack=[]; s.row=[]; s.rows=[]; s.cell=''; s.in_cell=False; s.ol=[]; s.skip=0; s.cls=[]
    def flush(s, prefix=''):
        t=re.sub(r'\s+',' ',s.buf).strip()
        if t: s.out.append(prefix+t)
        s.buf=''
    def handle_starttag(s, tag, a):
        a=dict(a); c=a.get('class','') or ''
        if tag in ('img','br','hr','meta','link','input'):
            if s.skip: return
            if tag=='img': s.flush(); s.out.append(f"〔圖：{a.get('src','').split('/')[-1]}〕")
            elif s.in_cell: s.cell+=' '
            else: s.buf+=' '
            return
        s.cls.append(c)
        cs=c.split()
        if any(k in cs for k in ('stripes','gps','irs','chips','nr','arw')):
            s.flush(); s.out.append('〔色塊圖，見 PDF；數據見文末附錄〕') if not (s.out and s.out[-1].startswith('〔色塊圖')) else None
            s.skip+=1; s.stack.append((tag,True)); return
        if tag in ('style','script') or 'foot' in cs or c in ('sb','gpc','icc','strip','arb','pr','bar'): s.skip+=1; s.stack.append((tag,True)); return
        s.stack.append((tag,False))
        if s.skip: return
        if tag in ('h1','h2','h3','p','li','div','figcaption') and not s.in_cell: s.flush(s._pre())
        if tag=='ol': s.ol.append(0)
        if tag=='ul': s.ol.append(None)
        if tag=='li' and s.ol and s.ol[-1] is not None: s.ol[-1]+=1
        if tag=='tr': s.row=[]
        if tag in ('td','th'): s.in_cell=True; s.cell=''
        if tag=='img':
            s.out.append(f"〔圖：{a.get('src','').split('/')[-1]}〕")
        if tag=='br':
            if s.in_cell: s.cell+=' '
            else: s.buf+=' '
        if tag=='b' or tag=='strong':
            if s.in_cell: s.cell+='**'
            else: s.buf+='**'
    def _pre(s):
        return ''
    def handle_endtag(s, tag):
        if not s.stack: return
        t,sk=s.stack.pop(); c=s.cls.pop() if s.cls else ''
        if sk: s.skip-=1; return
        if s.skip: return
        if tag in ('b','strong'):
            if s.in_cell: s.cell+='**'
            else: s.buf+='**'
        if tag in ('td','th'):
            s.in_cell=False; s.row.append(re.sub(r'\s+',' ',s.cell).strip().replace('|','／'))
        elif tag=='tr':
            s.rows.append(s.row)
        elif tag=='table':
            if s.rows:
                n=max(len(r) for r in s.rows)
                rs=[r+['']*(n-len(r)) for r in s.rows]
                s.out.append('| '+' | '.join(rs[0])+' |'); s.out.append('|'+'---|'*n)
                for r in rs[1:]: s.out.append('| '+' | '.join(r)+' |')
                s.out.append('')
            s.rows=[]
        elif tag=='h1': s.flush('# ')
        elif tag=='h2': s.out.append(''); s.flush('## ')
        elif tag=='h3': s.out.append(''); s.flush('### ')
        elif tag=='li':
            pre = f"{s.ol[-1]}. " if s.ol and s.ol[-1] is not None else '- '
            s.flush(pre)
        elif tag in ('ol','ul'):
            s.ol.pop(); s.out.append('')
        elif tag=='figcaption': s.flush('　說明：')
        elif tag in ('p','div'):
            if 'learn' in c.split(): s.flush('> ')
            elif 'part' in c.split(): s.out.append(''); s.flush('# ')
            else: s.flush()
    def handle_data(s, d):
        if s.skip: return
        if s.in_cell: s.cell+=d
        else: s.buf+=d

html=open(sys.argv[1]).read()
pages=html.split('<section class="page')
p=P(); p.feed(html); p.flush()
txt='\n'.join(p.out)
txt=re.sub(r'\n{3,}','\n\n',txt)
open(sys.argv[2],'w').write(txt)
print(len(txt))
