#!/usr/bin/env python3
"""Build matchup_database.html (Finalist Matchup Database).
Self-contained: reads post_rows_0.jsonl + proto_decks.json + card_icons/, writes matchup_database.html.
Runnable standalone or imported (call main()). Designed to run inside the dashboard build so the
matchup DB regenerates automatically on every new data fetch.
Features: multi-select win-cons, spell layer, Coverage Optimizer, and a per-player filter.
"""
import json, base64, os, io, re
from collections import defaultdict, Counter

D = os.environ.get("CRL_DIR", ".")

FIN = {"#GPPYR9JYR":"Clown","#898Y8PGJ9":"evolve","#9RQ8YRYQL":"Batan","#2LJ0ULYCC":"Guriko",
"#C88VYCJC":"EGW","#9CPCC890":"Adriel","#U890Q9UQ":"Sub","#290UQY8C":"Soudy",
"#G9YV9GR8R":"Mohamed Light","#J0VU9CGP":"SK Dominik","#RP0L2Y8C9":"Ardentoas","#C0V0UQ9UY":"Ryley",
"#RJ88Y8U08":"Pedro","#RUQ0JU2P":"Asaf","#2VGG29RJ2":"Coco","#2CLV2RP0":"Mugi"}


def build_data():
    proto = json.load(open(f"{D}/proto_decks.json"))
    WC = set(proto["wincons"]); SP = set(proto["spells"])
    rows = [json.loads(l) for l in open(f"{D}/post_rows_0.jsonl")]

    def wc(d): return [c for c in d if c in WC]
    def sp(d): return [c for c in d if c in SP]
    def won(cf, ca): return None if cf is None or ca is None else cf > ca

    def build(pred):
        M1 = defaultdict(lambda:[0,0]); M2 = defaultdict(lambda:[0,0]); n = 0
        for r in rows:
            if r[0] not in FIN or not pred(r): continue
            wv = won(r[4], r[5])
            if wv is None: continue
            aw = wc(r[2]); asp = sp(r[2]); bw = wc(r[3])
            if not aw or not bw: continue
            n += 1
            for a in aw:
                for b in bw:
                    c = M1[(a,b)]; c[0]+=1; c[1]+=(1 if wv else 0)
                    for s in asp:
                        c2 = M2[(a,s,b)]; c2[0]+=1; c2[1]+=(1 if wv else 0)
        return M1, M2, n

    def pack(M1, M2, minc1=4, minc2=4):
        m1 = defaultdict(dict); m2 = defaultdict(lambda: defaultdict(dict))
        for (a,b), v in M1.items():
            if v[0] >= minc1: m1[a][b] = [v[0], round(100*v[1]/v[0],1)]
        for (a,s,b), v in M2.items():
            if v[0] >= minc2: m2[a][s][b] = [v[0], round(100*v[1]/v[0],1)]
        return {k:dict(v) for k,v in m1.items()}, {k:{s:dict(bb) for s,bb in v.items()} for k,v in m2.items()}

    M1a, M2a, na = build(lambda r: True)
    M1c, M2c, nc = build(lambda r: r[7] == "Official CRL")
    m1_all, m2_all = pack(M1a, M2a)
    m1_crl, m2_crl = pack(M1c, M2c)

    # per-player matrices (lower storage threshold since samples are thinner)
    by_player = {}
    for tag, name in FIN.items():
        M1p, M2p, npg = build(lambda r, t=tag: r[0] == t)
        m1p, m2p = pack(M1p, M2p, minc1=3, minc2=3)
        if m1p:
            by_player[name] = {"m1": m1p, "m2": m2p, "n": npg}

    freq = Counter()
    for (a,b), v in M1a.items(): freq[a] += v[0]
    wc_order = [w for w,_ in freq.most_common()]
    spf = Counter()
    for (a,s,b), v in M2a.items(): spf[s] += v[0]
    sp_order = [s for s,_ in spf.most_common()]

    players_with_data = [FIN[t] for t in FIN if FIN[t] in by_player]

    return {"wincons": wc_order, "spells": sp_order,
            "m1_all": m1_all, "m2_all": m2_all, "m1_crl": m1_crl, "m2_crl": m2_crl,
            "by_player": by_player, "players": players_with_data,
            "n_all": na, "n_crl": nc}


def build_icons(dt):
    from PIL import Image
    man = json.load(open(f"{D}/card_icons/manifest.json"))
    def fn(n):
        v = man.get(n); return v.get("base") if isinstance(v, dict) else v
    def slug(n): return "c" + re.sub(r"[^A-Za-z0-9]", "", n)
    need = set(dt["wincons"]) | set(dt["spells"])
    css = ""; have = set()
    for n in sorted(need):
        f = fn(n); p = f"{D}/card_icons/{f}" if f else None
        if p and os.path.exists(p):
            im = Image.open(p).convert("RGBA"); w0 = 64; h0 = int(im.height*w0/im.width)
            im = im.resize((w0, h0), Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
            css += f".{slug(n)}{{background-image:url(data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()})}}\n"
            have.add(n)
    dt["slug"] = {n: slug(n) for n in need}; dt["have"] = sorted(have)
    return css, len(have)


JS = r"""
const DATA=D0;
const SLUG=DATA.slug,HAVE=new Set(DATA.have),WCL=DATA.wincons,SPL=DATA.spells,BYP=DATA.by_player||{},PLAYERS=DATA.players||[];
const esc=s=>(s+"").replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function ci(n,cls){cls=cls||'cs';return HAVE.has(n)?'<span class="'+cls+' '+SLUG[n]+'" title="'+esc(n)+'"></span>':'<span class="'+cls+' noi" title="'+esc(n)+'">'+esc(n.slice(0,3))+'</span>';}
let src='all', minG=8, player='', expanded={};
function m1(){if(player)return (BYP[player]||{}).m1||{};return DATA['m1_'+src]||{};}
function m2(){if(player)return (BYP[player]||{}).m2||{};return DATA['m2_'+src]||{};}
function colr(p){if(p==null)return '#5b6478';if(p>=60)return '#22c55e';if(p>=55)return '#a3e635';if(p>=50)return '#eab308';if(p>=45)return '#f59e0b';return '#ef4444';}
function conf(g){return g>=25?['●●●','#22c55e']:(g>=12?['●●○','#f59e0b']:['●○○','#ef4444']);}

class Field{
 constructor(id,opts,o){this.el=document.getElementById(id);this.opts=opts;this.ph=o.placeholder||'';this.onChange=o.onChange||(()=>{});this.sel=[];
  this.el.classList.add('tf');this.el.innerHTML='<div class="tfbox"><span class="chips"></span><input class="tfin" placeholder="'+esc(this.ph)+'"></div><div class="tfdrop"></div>';
  this.box=this.el.querySelector('.tfbox');this.chips=this.el.querySelector('.chips');this.input=this.el.querySelector('.tfin');this.drop=this.el.querySelector('.tfdrop');
  this.input.addEventListener('input',()=>this.open());this.input.addEventListener('focus',()=>this.open());
  this.input.addEventListener('keydown',e=>{if(e.key==='Enter'){const f=this.drop.querySelector('.opt');if(f){this.pick(f.dataset.v);e.preventDefault();}}else if(e.key==='Backspace'&&!this.input.value&&this.sel.length){this.sel.pop();this.render();this.onChange();}else if(e.key==='Escape')this.close();});
  document.addEventListener('click',e=>{if(!this.el.contains(e.target))this.close();});this.render();}
 pick(v){if(!this.sel.includes(v))this.sel.push(v);this.input.value='';this.close();this.render();this.onChange();}
 remove(v){this.sel=this.sel.filter(x=>x!==v);this.render();this.onChange();}
 render(){this.chips.innerHTML=this.sel.map((v,i)=>'<span class="chip">'+(this.rank?('<span class="rk">'+(i+1)+'</span>'):'')+ci(v,'csT')+esc(v)+'<b data-rm="'+esc(v)+'">×</b></span>').join('');
  this.chips.querySelectorAll('b[data-rm]').forEach(b=>b.onclick=e=>{e.stopPropagation();this.remove(b.dataset.rm);});this.input.placeholder=this.sel.length?'':this.ph;this.box.onclick=()=>this.input.focus();}
 open(){const q=this.input.value.toLowerCase();let l=this.opts.filter(o=>!this.sel.includes(o)&&(!q||o.toLowerCase().includes(q))).slice(0,14);if(!l.length){this.close();return;}
  this.drop.innerHTML=l.map(o=>'<div class="opt" data-v="'+esc(o)+'">'+ci(o,'csT')+esc(o)+'</div>').join('');this.drop.querySelectorAll('.opt').forEach(d=>d.onclick=()=>this.pick(d.dataset.v));this.drop.style.display='block';}
 close(){this.drop.style.display='none';}
}
const F={};

function comboRate(wcs,B){let tg=0,tw=0;for(const A of wcs){const c=m1()[A]&&m1()[A][B];if(c&&c[0]>0){tg+=c[0];tw+=c[1]*c[0];}}return tg?[tw/tg,tg]:[null,0];}
function comboSpell(wcs,B,s){let tg=0,tw=0;for(const A of wcs){const c=m2()[A]&&m2()[A][s]&&m2()[A][s][B];if(c&&c[0]>0){tg+=c[0];tw+=c[1]*c[0];}}return tg?[tw/tg,tg]:[null,0];}
function allOpp(wcs){const set=new Set();for(const A of wcs){for(const b in (m1()[A]||{}))set.add(b);}return [...set];}

function scopeNote(){
 if(player){const n=(BYP[player]||{}).n||0;return '<div class="pnote">Showing <b>'+esc(player)+'</b> only — '+n+' games. Per-player samples are thin, so many cells are empty and confidence is lower; drop the min-games slider to see more. The All/CRL toggle is ignored while a player is selected.</div>';}
 return '';
}

function renderExplorer(){
 const wcs=F.my.sel; const host=document.getElementById('outExp');
 const note=scopeNote();
 if(!wcs.length){host.innerHTML=note+'<div class="hint">Pick one or more of '+(player?'':'YOUR ')+'win conditions (combine e.g. Mortar + Elite Barbarians for a two-win-con deck). Combined matchups are the games-weighted average of each.</div>';return;}
 const opps=allOpp(wcs).map(b=>{const[r,g]=comboRate(wcs,b);return [b,r,g];}).filter(x=>x[1]!=null&&x[2]>=minG).sort((a,b)=>b[1]-a[1]);
 let h=note+'<div class="mh">'+wcs.map(w=>ci(w,'csS')+esc(w)).join(' + ')+' — win rate vs each opponent win condition'+(player?(' ('+esc(player)+')'):'')+'. Click a row for the spell breakdown.</div>';
 if(!opps.length) h+='<div class="hint">No matchups with ≥'+minG+' games. Lower the min-games slider'+(player?'':' or switch data source')+'.</div>';
 for(const [b,r,g] of opps){
   const[cd,cc]=conf(g);const open=expanded[b];
   h+='<div class="mrow'+(open?' open':'')+'" data-b="'+esc(b)+'"><div class="mtop"><div class="ml">'+ci(b,'csS')+'<b>'+esc(b)+'</b></div>'
     +'<div class="mtrack"><div class="mfill" style="width:'+r+'%;background:'+colr(r)+'"></div><span class="mpct">'+Math.round(r)+'%</span></div>'
     +'<div class="mg">'+g+'g <span style="color:'+cc+'">'+cd+'</span></div><div class="exp">'+(open?'▾':'▸')+'</div></div>';
   if(open){
     const rows=[];for(const s of SPL){const[wr,gg]=comboSpell(wcs,b,s);if(wr!=null&&gg>=Math.max(3,minG-2))rows.push([s,wr,gg]);}
     rows.sort((a,b)=>b[1]-a[1]);
     h+='<div class="sub">'+(rows.length?('<div class="subh">by the spell in '+(player?'their':'your')+' deck:</div>'+rows.map(([s,wr,gg])=>{const[c2,cc2]=conf(gg);return '<div class="srow"><div class="sl">'+ci(s,'csS')+esc(s)+'</div><div class="strack"><div class="sfill" style="width:'+wr+'%;background:'+colr(wr)+'"></div><span class="spct">'+Math.round(wr)+'%</span></div><div class="sg">'+gg+'g <span style="color:'+cc2+'">'+c2+'</span></div></div>';}).join('')):'<div class="hint" style="padding:6px 2px">Not enough spell-level games here.</div>')+'</div>';
   }
   h+='</div>';
 }
 host.innerHTML=h;
 document.querySelectorAll('#outExp .mtop').forEach(el=>el.onclick=()=>{const b=el.parentElement.dataset.b;expanded[b]=!expanded[b];renderExplorer();});
}

function weights(n){const decay=Math.max(0.5,0.95-0.05*(n-1));let w=[],s=0;for(let i=0;i<n;i++){w.push(Math.pow(decay,i));s+=w[i];}return w.map(x=>x/s);}
function coverage(A,targets,w){
 let sw=0,sm=0,parts=[];
 for(let i=0;i<targets.length;i++){const c=m1()[A]&&m1()[A][targets[i]];if(c&&c[0]>=minG){sm+=w[i]*c[1];sw+=w[i];parts.push([targets[i],c[1],c[0],w[i]]);}}
 const arch=sw?sm/sw:null;
 let bestS=null,bestC=null,bestParts=null;const mm=m2()[A]||{};
 for(const s in mm){let ssw=0,ssm=0,cnt=0,pp=[];for(let i=0;i<targets.length;i++){const c=mm[s][targets[i]];if(c&&c[0]>=Math.max(3,minG-2)){ssm+=w[i]*c[1];ssw+=w[i];cnt++;pp.push([targets[i],c[1],c[0],w[i]]);}}
   if(cnt>=Math.ceil(targets.length*0.5)&&ssw>0){const cov=ssm/ssw;if(bestC==null||cov>bestC){bestC=cov;bestS=s;bestParts=pp;}}}
 return {arch,parts,bestS,bestC,bestParts,covered:parts.length};
}
function renderCoverage(){
 const targets=F.cov.sel;const host=document.getElementById('outCov');
 const note=scopeNote();
 if(targets.length<1){host.innerHTML=note+'<div class="hint">Enter the opponent win conditions you want to cover — in priority order (first = you most expect it / most want to beat it). These are typically what the Duel Predictor lists for their next game.</div>';return;}
 const w=weights(targets.length);
 let wtxt='<div class="whead">Priority weighting ('+targets.length+' inputs → '+(targets.length>=6?'front-loaded':'fairly even')+'):</div><div class="wrow">'+targets.map((t,i)=>ci(t,'csT')+esc(t)+' <span class="wv">'+Math.round(100*w[i])+'%</span>').join('  ·  ')+'</div>';
 const cands=[];
 for(const A of WCL){const c=coverage(A,targets,w);const best=(c.bestC!=null?c.bestC:c.arch);if(best==null)continue;cands.push({A,...c,best});}
 cands.sort((a,b)=>b.best-a.best);
 let h=note+'<div class="covbox">'+wtxt+'</div>';
 h+='<div class="mh">Best win conditions to cover your inputs (weighted). Each shows its best spell.</div>';
 cands.slice(0,8).forEach((c,i)=>{
   const useS=c.bestC!=null; const val=useS?c.bestC:c.arch; const parts=useS?c.bestParts:c.parts;
   const perT=parts.slice().sort((a,b)=>b[3]-a[3]).map(p=>'<span class="pt"><span style="color:'+colr(p[1])+'">'+ci(p[0],'csT')+esc(p[0])+' '+Math.round(p[1])+'%</span></span>').join('');
   const miss=targets.filter(t=>!parts.some(p=>p[0]===t));
   h+='<div class="cov'+(i===0?' top':'')+'"><div class="covh">'+ci(c.A,'csS')+'<b>'+esc(c.A)+'</b>'
     +(useS?('<span class="withsp">with '+ci(c.bestS,'csT')+esc(c.bestS)+'</span>'):'<span class="withsp arch">archetype avg</span>')
     +'<span class="covscore" style="color:'+colr(val)+'">'+Math.round(val)+'%<span class="cl">weighted coverage</span></span></div>'
     +'<div class="perT">'+perT+(miss.length?'<span class="miss">no data vs: '+miss.map(esc).join(', ')+'</span>':'')+'</div></div>';
 });
 host.innerHTML=h;
}

function showTab(t){document.querySelectorAll('.tabpage').forEach(p=>p.style.display='none');document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('on'));document.getElementById('tab_'+t).style.display='block';document.getElementById('tb_'+t).classList.add('on');}
function syncSrcUI(){document.querySelectorAll('.seg').forEach(s=>s.classList.toggle('disabled',!!player));}
function build(){
 F.my=new Field('f_my',WCL,{placeholder:'win condition(s)…',onChange:()=>{expanded={};renderExplorer();}});
 F.cov=new Field('f_cov',WCL,{placeholder:'win conditions to cover, priority order…',onChange:renderCoverage}); F.cov.rank=true;
 document.querySelectorAll('.seg button').forEach(b=>b.onclick=()=>{if(player)return;src=b.dataset.s;document.querySelectorAll('.seg button').forEach(x=>x.classList.remove('on'));b.classList.add('on');renderExplorer();renderCoverage();});
 const psel=document.getElementById('psel');
 psel.innerHTML='<option value="">All finalists</option>'+PLAYERS.map(p=>'<option value="'+esc(p)+'">'+esc(p)+'</option>').join('');
 psel.onchange=()=>{player=psel.value;expanded={};if(player&&minG>4){minG=4;sl.value=4;document.getElementById('mgv').textContent=4;}syncSrcUI();renderExplorer();renderCoverage();};
 const sl=document.getElementById('mg');sl.oninput=e=>{minG=+e.target.value;document.getElementById('mgv').textContent=minG;renderExplorer();renderCoverage();};
 document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>showTab(b.dataset.t));
 showTab('exp');renderExplorer();renderCoverage();
}
document.addEventListener('DOMContentLoaded',build);
"""


HTML_TMPL = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Finalist Matchup Database</title><style>
:root{--bg:#0e1320;--card:#171e2e;--card2:#1e2740;--tx:#e6ecf7;--mut:#8a97b3;--line:#26304a;--acc:#3987e5}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:20px 15px 70px}h1{font-size:22px;margin:0 0 3px}.sub{color:var(--mut);font-size:13px;margin:0 0 12px}
.tabs{display:flex;gap:6px}.tabs button{background:var(--card2);color:var(--mut);border:1px solid var(--line);border-bottom:none;border-radius:9px 9px 0 0;padding:9px 16px;font-size:14px;font-weight:700;cursor:pointer}.tabs button.on{background:var(--acc);color:#fff;border-color:var(--acc)}
.tabpage{background:var(--card);border:1px solid var(--line);border-radius:0 12px 12px 12px;padding:14px}
.ctl{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:6px}
.lab{font-size:10.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em;display:block;margin-bottom:3px}
.seg{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}.seg button{background:var(--card2);color:var(--mut);border:none;padding:6px 11px;font-size:12px;cursor:pointer}.seg button.on{background:var(--acc);color:#fff}
.seg.disabled{opacity:.4;pointer-events:none}
.psel{background:var(--card2);color:var(--tx);border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:12.5px;cursor:pointer}
.sl2{display:flex;align-items:center;gap:8px;font-size:12px}.sl2 input{width:120px;accent-color:var(--acc)}.sl2 b{color:#a3e635}
.tf{position:relative;min-width:260px;flex:1}.tfbox{display:flex;flex-wrap:wrap;gap:4px;align-items:center;background:var(--card2);border:1px solid var(--line);border-radius:8px;padding:5px 7px;min-height:36px;cursor:text}
.chips{display:flex;flex-wrap:wrap;gap:4px}.chip{display:inline-flex;align-items:center;gap:3px;background:#0e1320;border:1px solid var(--line);border-radius:6px;padding:2px 5px 2px 5px;font-size:12px}
.chip .rk{background:var(--acc);color:#fff;border-radius:50%;width:15px;height:15px;font-size:10px;display:inline-flex;align-items:center;justify-content:center;font-weight:800;margin-right:1px}
.chip b{cursor:pointer;color:var(--mut);margin-left:3px}.chip b:hover{color:#ef4444}.tfin{flex:1;min-width:90px;background:transparent;border:none;outline:none;color:var(--tx);font-size:13px;padding:2px}
.tfdrop{display:none;position:absolute;left:0;right:0;top:100%;margin-top:3px;background:#1b2440;border:1px solid var(--line);border-radius:8px;max-height:240px;overflow:auto;z-index:30;box-shadow:0 8px 22px rgba(0,0,0,.4)}
.opt{display:flex;align-items:center;gap:6px;padding:6px 9px;font-size:13px;cursor:pointer}.opt:hover{background:var(--card2)}
.cs,.csS{display:inline-block;background-size:contain;background-repeat:no-repeat;background-position:center;vertical-align:middle}.csS{width:20px;height:24px;margin-right:5px}
.csT{display:inline-block;width:15px;height:18px;background-size:contain;background-repeat:no-repeat;background-position:center;vertical-align:middle;margin-right:2px}
.noi{border:1px solid var(--line);border-radius:3px;font-size:7px;color:var(--mut);text-align:center;overflow:hidden;line-height:1}.csS.noi{width:20px;height:24px;line-height:24px}.csT.noi{width:15px;height:18px;line-height:18px}
.mh{font-size:13px;color:#c8d2e6;margin:14px 2px 8px}
.pnote{background:rgba(57,135,229,.10);border:1px solid rgba(57,135,229,.35);border-radius:8px;padding:8px 11px;font-size:12px;color:#bcd4f2;margin:10px 0 4px}
.mrow{background:#141a28;border:1px solid var(--line);border-radius:10px;margin:0 0 7px;overflow:hidden}.mrow.open{border-color:var(--acc)}
.mtop{display:grid;grid-template-columns:150px 1fr 74px 20px;gap:10px;align-items:center;padding:9px 12px;cursor:pointer}
.ml{display:flex;align-items:center;font-size:14px}.mtrack{position:relative;background:var(--card2);border-radius:6px;height:22px;overflow:hidden}.mfill{position:absolute;left:0;top:0;bottom:0;border-radius:6px;opacity:.85}
.mpct{position:absolute;right:8px;top:50%;transform:translateY(-50%);font-size:12px;font-weight:800;color:#fff;text-shadow:0 1px 2px #000}.mg{font-size:11px;color:var(--mut);text-align:right}.exp{color:var(--mut);text-align:center}
.sub{background:#0e1320;border-top:1px solid var(--line);padding:10px 12px}.subh{font-size:11.5px;color:var(--mut);margin-bottom:8px}
.srow{display:grid;grid-template-columns:150px 1fr 74px;gap:10px;align-items:center;padding:3px 0}.sl{display:flex;align-items:center;font-size:12.5px}
.strack{position:relative;background:var(--card2);border-radius:5px;height:18px;overflow:hidden}.sfill{position:absolute;left:0;top:0;bottom:0;border-radius:5px;opacity:.8}.spct{position:absolute;right:6px;top:50%;transform:translateY(-50%);font-size:11px;font-weight:700;color:#fff}.sg{font-size:10.5px;color:var(--mut);text-align:right}
.covbox{background:#141a28;border:1px solid var(--line);border-radius:10px;padding:11px 13px;margin:6px 0 4px}.whead{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.03em;margin-bottom:6px}.wrow{font-size:12.5px;display:flex;flex-wrap:wrap;gap:2px;align-items:center}.wv{color:#a3e635;font-weight:700;font-size:11px}
.cov{background:#141a28;border:1px solid var(--line);border-radius:10px;padding:10px 12px;margin:0 0 8px}.cov.top{border-color:#3d6;box-shadow:0 0 0 1px rgba(51,221,102,.25)}
.covh{display:flex;align-items:center;gap:6px;font-size:15px;flex-wrap:wrap}.withsp{font-size:11.5px;color:#a9d5ff;background:rgba(57,135,229,.14);border-radius:5px;padding:1px 8px;display:inline-flex;align-items:center}.withsp.arch{color:var(--mut);background:var(--card2)}
.covscore{margin-left:auto;font-weight:800;font-size:18px}.covscore .cl{display:block;font-size:9px;color:var(--mut);font-weight:400;text-align:right}
.perT{display:flex;flex-wrap:wrap;gap:9px;margin-top:8px;font-size:12px}.perT .pt{font-weight:700}.miss{color:var(--mut);font-size:11px;font-style:italic}
.hint{color:var(--mut);font-size:13px;padding:10px 2px}.foot{color:var(--mut);font-size:11.5px;margin-top:16px;border-top:1px solid var(--line);padding-top:12px}
__CSS__
</style></head><body><div class="wrap">
<h1>Finalist Matchup Database</h1>
<p class="sub">Matchups mined from the top-16 finalists' games — with the spell layer. Combine win conditions for multi-win-con decks (e.g. Mortar + Elite Barbarians), filter to a single player's tendencies, and use the Coverage Optimizer to find the best answer to a set of predicted opponent decks.</p>
<div class="ctl" style="margin-bottom:8px">
  <div><span class="lab">Data</span><div class="seg"><button data-s="all" class="on">All (prac+CRL)</button><button data-s="crl">CRL only</button></div></div>
  <div><span class="lab">Player filter</span><select id="psel" class="psel"></select></div>
  <div class="sl2"><span class="lab" style="margin:0">min games</span><input type="range" id="mg" min="3" max="30" value="8"><b id="mgv">8</b></div>
</div>
<div class="tabs"><button data-t="exp" id="tb_exp">Matchup explorer</button><button data-t="cov" id="tb_cov">Coverage optimizer</button></div>
<div id="tab_exp" class="tabpage">
  <span class="lab">Win condition(s) — combine for multi-win-con decks</span><div id="f_my"></div>
  <div id="outExp"></div>
</div>
<div id="tab_cov" class="tabpage" style="display:none">
  <span class="lab">Opponent win conditions to cover — add in priority order (first = most important)</span><div id="f_cov"></div>
  <div id="outCov"></div>
</div>
<div class="foot">Built from __NALL__ finalist games (__NCRL__ CRL). Combined matchups average each selected win condition's cell (games-weighted) — an approximation of a true multi-win-con deck. Player filter narrows to one finalist's own games (all categories) — samples are thinner, so confidence drops. Coverage Optimizer: weights fall off by input position (more inputs → steeper, so the first ones dominate; few inputs → fairly even, since a narrow read means all of them matter); each candidate is scored as the weighted average of its win rate vs your inputs, and its best spell is the one maximizing that. Confidence dots track game count; ●○○ = small sample. CRL-only is a much smaller pool.</div>
<script>__JS__</script>
</div></body></html>"""


def main(out_path=None):
    dt = build_data()
    css, nicons = build_icons(dt)
    js = "const D0=" + json.dumps(dt) + ";\n" + JS
    html = (HTML_TMPL.replace("__NALL__", str(dt["n_all"])).replace("__NCRL__", str(dt["n_crl"]))
            .replace("__CSS__", css).replace("__JS__", js))
    if out_path is None:
        out_path = os.path.join(D, "matchup_database.html")
    open(out_path, "w", encoding="utf-8").write(html)
    print("wrote", out_path, round(len(html)/1024), "KB ·", nicons, "icons ·",
          len(dt["players"]), "players with per-player data")
    return out_path


if __name__ == "__main__":
    main()
