import ast, json, sys
src=open(sys.argv[1],encoding='utf-8').read()
tree=ast.parse(src)
def ev(n):
    if isinstance(n,ast.Constant): return n.value
    if isinstance(n,ast.List): return [ev(e) for e in n.elts]
    if isinstance(n,ast.Dict): return {ev(k):ev(v) for k,v in zip(n.keys,n.values)}
    if isinstance(n,ast.Call) and getattr(n.func,'id',None)=='dict': return {k.arg:ev(k.value) for k in n.keywords}
    if isinstance(n,ast.JoinedStr): return ''.join(str(ev(v)) if not isinstance(v,ast.FormattedValue) else '{...}' for v in n.values)
    if isinstance(n,ast.BinOp): return None
    return None
out={}
for node in tree.body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
        out[node.targets[0].id]=ev(node.value)
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print({k:(len(v) if hasattr(v,'__len__') else v) for k,v in out.items()})
