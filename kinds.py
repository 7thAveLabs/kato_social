"""Reel formats for anim.py. Each builder returns dict(dur=..., html=..., events=[]).
Declare one in anims.json with "kind": chat | todo | clock | match | define | bars | typed.
Keep everything that matters between y=250 and y=1560 (Reels cover the top and bottom of the frame).
All text is serif except inside product UI chips (match)."""
import json, html as _h

X = """<style>
.ink{background:#141312;color:#fff}
.dusk{background:linear-gradient(180deg,#2b2621 0%,#3a332b 55%,#51473b 100%);color:#fff}
.mut{color:#626262}.ink .mut,.dusk .mut{color:#b9b3a6}
.end{position:absolute;left:96px;right:96px;z-index:2;font-size:112px;line-height:1.02;letter-spacing:-.04em;opacity:0}
.sub{position:absolute;left:96px;right:96px;z-index:2;font-size:54px;line-height:1.2;letter-spacing:-.015em;opacity:0}
</style>"""
def _e(s):
    """Escape text, turning *word* into italics."""
    out = ""
    for i, p in enumerate(_h.escape(s).split("*")): out += f"<em>{p}</em>" if i % 2 else p
    return out.replace("\n", "<br>")
def _dark(theme): return theme in ("ink", "dusk")

def chat(BASE, title, msgs, end, theme="bone", sub=""):
    """Message thread. msgs: [["l"|"r"|"k", text], ...]; "k" is Kato's reply (max 5 messages, each under about 60 characters)."""
    T = [round(0.7 + 1.45 * i, 2) for i in range(len(msgs))]; te = T[-1] + 2.3
    rows = ""
    for i, (side, text) in enumerate(msgs):
        if side == "k":
            rows += f'<div class="m k"><span class="km">kato.</span>{_e(text)}</div>'
        else:
            rows += f'<div class="m {side}">{_e(text)}</div>'
        rows += f'<div class="ty {side}"><i></i><i></i><i></i></div>'
    h = BASE + X + f"""<style>
#th{{position:absolute;left:96px;right:96px;top:420px;display:flex;flex-direction:column;gap:22px;z-index:2}}
.m{{max-width:790px;font-size:58px;line-height:1.16;letter-spacing:-.02em;padding:34px 42px;border-radius:44px;opacity:0}}
.m.l{{align-self:flex-start;background:#fff;color:#111;border:1px solid #dedede;border-bottom-left-radius:10px}}
.m.r{{align-self:flex-end;background:#111;color:#fff;border-bottom-right-radius:10px}}
.m.k{{align-self:stretch;max-width:none;background:#e8e2d3;color:#111;border-radius:36px;margin-top:14px}}
.km{{display:block;font-size:44px;letter-spacing:-.04em;margin-bottom:10px}}
.ty{{position:absolute;display:flex;gap:10px;padding:26px 30px;border-radius:40px;background:#fff;border:1px solid #dedede;opacity:0}}
.ty.r{{background:#111}}.ty.k{{background:#e8e2d3}}
.ty i{{width:16px;height:16px;border-radius:50%;background:#9a958a;display:block}}
#tt{{position:absolute;left:96px;top:300px;font-size:44px;font-style:italic;z-index:2}}
</style>
<div class="p {theme}"><div class="mark">kato.</div><div id="tt" class="mut">{_e(title)}</div>
<div id="th">{rows}</div>
<div class="end" id="end" style="top:700px">{_e(end)}</div><div class="sub mut" id="sub" style="top:1420px">{_e(sub)}</div></div>
<script>{{const T={json.dumps(T)},te={te};
const ms=$$('.m'),ty=$$('.ty');
window.render=t=>{{
 const out=ease(seg(t,te-.5,.5));
 ms.forEach((m,i)=>{{const e=ease(seg(t,T[i],.35)); m.style.opacity=e*(1-out); m.style.transform=`translateY(${{(1-e)*26 - out*40}}px) scale(${{.96+.04*e}})`;
   const y=ty[i]; const on=seg(t,T[i]-.55,.15)*(1-seg(t,T[i]-.05,.1)); y.style.opacity=on*(1-out);
   y.style.top=(m.offsetTop+6)+'px'; if(m.classList.contains('r')) y.style.right='0px'; else y.style.left='0px';
   [...y.children].forEach((d,j)=>d.style.transform=`translateY(${{-7*Math.max(0,Math.sin(t*9-j*.9))}}px)`);}});
 $('#tt').style.opacity=(1-out)*ease(seg(t,.15,.4));
 const e=ease(seg(t,te,.7)); $('#end').style.opacity=e; $('#end').style.transform=`translateY(${{(1-e)*30}}px)`;
 $('#sub').style.opacity=ease(seg(t,te+.9,.7));
}};}}</script>"""
    return dict(dur=te + 3.0, html=h, events=[])

def todo(BASE, title, items, end, theme="wash", sub=""):
    """A to-do card whose lines are struck through one by one, then replaced by the end line (3 to 5 items, each under about 28 characters)."""
    T = [round(1.0 + 0.95 * i, 2) for i in range(len(items))]; te = T[-1] + 1.5
    rows = "".join(f'<div class="it"><span class="bx"><svg viewBox="0 0 40 40"><path d="M9 21 l8 8 l15 -18" fill="none" stroke="#111" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1"/></svg></span><span class="tx">{_e(x)}<b></b></span></div>' for x in items)
    h = BASE + X + f"""<style>
#cd{{position:absolute;left:96px;right:96px;top:400px;background:#fffdf8;border-radius:28px;padding:64px 60px 70px;box-shadow:0 50px 90px -50px rgba(17,17,17,.45);z-index:2;color:#111;transform-origin:50% 0}}
#cd h2{{font-weight:400;font-size:50px;font-style:italic;color:#626262;padding-bottom:34px;border-bottom:2px solid #e8e5de;margin-bottom:26px;letter-spacing:-.02em}}
.it{{display:flex;align-items:center;gap:30px;padding:26px 0;font-size:58px;letter-spacing:-.025em;white-space:nowrap}}
.bx{{width:52px;height:52px;border:3px solid #111;border-radius:12px;flex:none;display:block}}.bx svg{{width:100%;height:100%;display:block}}
.tx{{position:relative}}.tx b{{position:absolute;left:-6px;top:54%;height:4px;background:#111;width:0;border-radius:2px}}
</style>
<div class="p {theme}"><div class="mark">kato.</div>
<div id="cd"><h2>{_e(title)}</h2>{rows}</div>
<div class="end" id="end" style="top:700px;font-size:150px;line-height:.98">{_e(end)}</div><div class="sub mut" id="sub" style="top:1420px">{_e(sub)}</div></div>
<script>{{const T={json.dumps(T)},te={te};
window.render=t=>{{
 const inn=ease(seg(t,.1,.6)), out=io(seg(t,te-.6,.7)); const c=$('#cd');
 c.style.opacity=inn*(1-out); c.style.transform=`translateY(${{(1-inn)*60+out*140}}px) rotate(${{-1.2+out*5}}deg)`;
 $$('.it').forEach((r,i)=>{{const e=ease(seg(t,T[i],.45)); r.querySelector('b').style.width=`calc(${{e*100}}% + ${{e*12}}px)`;
   r.querySelector('path').style.strokeDashoffset=1-ease(seg(t,T[i]-.15,.3)); r.querySelector('.tx').style.opacity=1-.6*e;}});
 const e=ease(seg(t,te,.7)); $('#end').style.opacity=e; $('#end').style.transform=`translateY(${{(1-e)*34}}px)`;
 $('#sub').style.opacity=ease(seg(t,te+.9,.7));
}};}}</script>"""
    return dict(dur=te + 3.0, html=h, events=[])

def clock(BASE, top, end, frm=1180, to=1020, theme="dusk", sub=""):
    """A clock whose hands wind backwards from `frm` to `to` (minutes after midnight). No digits are shown: it illustrates time back, never a claimed number of hours."""
    te = 5.4; d = _dark(theme); ink = "#fff" if d else "#111"
    ticks = "".join(f'<line x1="0" y1="-262" x2="0" y2="{-226 if i%3==0 else -244}" stroke="{ink}" stroke-width="{7 if i%3==0 else 3}" stroke-linecap="round" opacity="{1 if i%3==0 else .5}" transform="rotate({i*30})"/>' for i in range(12))
    h = BASE + X + f"""<div class="p {theme}"><div class="mark">kato.</div>
<div class="c" id="top" style="top:330px;font-size:66px;line-height:1.12;letter-spacing:-.025em">{_e(top)}</div>
<svg id="ck" style="position:absolute;left:230px;top:560px;z-index:2" width="620" height="620" viewBox="-310 -310 620 620">
<circle r="290" fill="none" stroke="{ink}" stroke-width="5" opacity=".9"/>{ticks}
<path id="arc" fill="none" stroke="{ink}" stroke-width="26" opacity=".16" stroke-linecap="round"/>
<line id="hh" x1="0" y1="22" x2="0" y2="-150" stroke="{ink}" stroke-width="13" stroke-linecap="round"/>
<line id="mh" x1="0" y1="30" x2="0" y2="-222" stroke="{ink}" stroke-width="8" stroke-linecap="round"/>
<circle r="13" fill="{ink}"/></svg>
<div class="end" id="end" style="top:1250px">{_e(end)}</div><div class="sub mut" id="sub" style="top:1500px">{_e(sub)}</div></div>
<script>{{const A={frm},B={to},te={te};
const pt=(deg,r)=>[r*Math.sin(deg*Math.PI/180),-r*Math.cos(deg*Math.PI/180)];
window.render=t=>{{
 const u=io(seg(t,1.3,3.4)); const m=A+(B-A)*u;
 $('#mh').setAttribute('transform',`rotate(${{m*6}})`); $('#hh').setAttribute('transform',`rotate(${{m*.5}})`);
 const a0=B*.5, a1=m*.5, a2=A*.5; // shade the hours given back, between the starting hour and where the hand is now
 const [x1,y1]=pt(a1,196),[x2,y2]=pt(a2,196); $('#arc').setAttribute('d',u>0.01?`M${{x1}} ${{y1}} A196 196 0 ${{(a2-a1)>180?1:0}} 1 ${{x2}} ${{y2}}`:'');
 $('#top').style.opacity=ease(seg(t,.2,.6)); $('#ck').style.opacity=ease(seg(t,.4,.6));
 const e=ease(seg(t,te-.4,.7)); $('#end').style.opacity=e; $('#end').style.transform=`translateY(${{(1-e)*30}}px)`;
 $('#sub').style.opacity=ease(seg(t,te+.6,.7));
}};}}</script>"""
    return dict(dur=te + 3.0, html=h, events=[])

def match(BASE, head, pairs, end, left="Remittance", right="Bank deposit", theme="page"):
    """Two columns of sample-data chips that get checked against each other. pairs: [[left, right, true|false], ...] (3 or 4 rows); false rows are flagged, never matched.
    Uses made-up amounts, so the caption must say "Example shown with sample data." """
    T = [round(1.5 + 1.25 * i, 2) for i in range(len(pairs))]; te = T[-1] + 1.5
    rows = ""
    for i, (a, b, ok) in enumerate(pairs):
        y = 760 + i * 178
        rows += (f'<div class="ch a" style="top:{y}px">{_h.escape(a)}</div><div class="ch b{"" if ok else " no"}" style="top:{y}px">{_h.escape(b)}</div>'
                 f'<div class="ln" style="top:{y+59}px"></div><div class="dt{"" if ok else " no"}" style="top:{y+33}px">{"&#10003;" if ok else "!"}</div>')
    h = BASE + X + f"""<style>
.ch{{position:absolute;width:372px;height:122px;border-radius:22px;background:#fff;border:1px solid #dedede;box-shadow:0 22px 44px -30px rgba(17,17,17,.4);z-index:2;display:flex;align-items:center;justify-content:center;font-family:Inter,sans-serif;font-size:36px;font-weight:500;letter-spacing:-.01em;color:#111;opacity:0}}
.ch.a{{left:96px}}.ch.b{{left:612px}}.ch.no{{background:transparent;border:3px dashed #a9a399;box-shadow:none;color:#626262;font-weight:400}}
.ln{{position:absolute;left:468px;width:0;height:4px;background:#111;z-index:2}}
.dt{{position:absolute;left:512px;width:56px;height:56px;border-radius:50%;background:#111;color:#fff;font-size:30px;font-family:Inter,sans-serif;display:flex;align-items:center;justify-content:center;z-index:3;opacity:0}}
.dt.no{{background:#f8f6f1;color:#111;border:4px solid #111;font-weight:700}}
.lb{{position:absolute;top:690px;width:372px;text-align:center;font-size:40px;font-style:italic;z-index:2}}
</style>
<div class="p {theme}"><div class="mark">kato.</div>
<div class="c" id="hd" style="top:330px;font-size:96px;line-height:1.03;letter-spacing:-.04em">{_e(head)}</div>
<div class="lb mut" style="left:96px">{_e(left)}</div><div class="lb mut" style="left:612px">{_e(right)}</div>
{rows}
<div class="sub" id="sub" style="top:{760+len(pairs)*178+50}px;font-size:60px">{_e(end)}</div></div>
<script>{{const T={json.dumps(T)},te={te},OK={json.dumps([bool(p[2]) for p in pairs])};
const A=$$('.ch.a'),B=$$('.ch.b'),L=$$('.ln'),D=$$('.dt');
window.render=t=>{{
 $('#hd').style.opacity=ease(seg(t,.15,.6));
 A.forEach((a,i)=>{{const e=ease(seg(t,.5+i*.12,.5)); a.style.opacity=e; a.style.transform=`translateX(${{(e-1)*40}}px)`;
   const f=ease(seg(t,.7+i*.12,.5)); B[i].style.opacity=f; B[i].style.transform=`translateX(${{(1-f)*40}}px)`;
   const g=ease(seg(t,T[i],.4)); L[i].style.width=(OK[i]?144*g:52*g)+'px'; L[i].style.opacity=OK[i]?1:.45;
   const k=ease(seg(t,T[i]+.3,.3)); D[i].style.opacity=k; D[i].style.transform=`scale(${{.5+.5*k+.18*Math.sin(Math.PI*seg(t,T[i]+.3,.4))}})`;
   if(!OK[i]) B[i].style.transform+=` translateX(${{6*Math.sin((t-T[i])*26)*Math.exp(-(t-T[i])*5)*(t>T[i]?1:0)}}px)`;}});
 $('#sub').style.opacity=ease(seg(t,te,.7));
}};}}</script>"""
    return dict(dur=te + 2.8, html=h, events=[], crop=320)

def define(BASE, term, pos, lines, end, theme="wash", size=230):
    """Dictionary entry: a term, its part of speech, 2 or 3 definition lines, and a closing line."""
    T = [round(1.5 + 1.55 * i, 2) for i in range(len(lines))]; te = T[-1] + 1.9
    ls = "".join(f'<div class="dl">{_e(x)}</div>' for x in lines)
    rule = "#fff" if _dark(theme) else "#111"
    h = BASE + X + f"""<style>
#df{{position:absolute;left:96px;right:96px;top:{470+int(size*1.12)+70}px;z-index:2;display:flex;flex-direction:column;gap:34px}}
.dl{{font-size:64px;line-height:1.16;letter-spacing:-.025em;opacity:0}}
#ru{{position:absolute;left:96px;top:{470+int(size*1.12)+24}px;height:3px;background:{rule};width:0;z-index:2}}
</style>
<div class="p {theme}"><div class="mark">kato.</div>
<div class="c mut" id="ps" style="top:372px;font-size:44px;font-style:italic">{_e(pos)}</div>
<div class="c" id="tm" style="top:440px;font-size:{size}px;line-height:1.1;letter-spacing:-.05em;white-space:nowrap">{_e(term)}</div>
<div id="ru"></div><div id="df">{ls}</div>
<div class="sub mut" id="sub" style="top:1440px">{_e(end)}</div></div>
<script>{{const T={json.dumps(T)},te={te};
window.render=t=>{{
 const e=ease(seg(t,.2,.7)); $('#tm').style.opacity=e; $('#tm').style.transform=`translateY(${{(1-e)*40}}px)`; $('#ps').style.opacity=ease(seg(t,.6,.5));
 $('#ru').style.width=(888*ease(seg(t,.9,.7)))+'px';
 $$('.dl').forEach((d,i)=>{{const k=ease(seg(t,T[i],.6)); d.style.opacity=k; d.style.transform=`translateY(${{(1-k)*24}}px)`;}});
 $('#sub').style.opacity=ease(seg(t,te,.7));
}};}}</script>"""
    return dict(dur=te + 2.8, html=h, events=[])

def bars(BASE, title, segs, end, theme="bone", sub=""):
    """A day drawn as stacked blocks that re-divide. segs: [[label, before, after], ...] (3 or 4; each column of numbers sums to 1). A block whose `after` is 0 disappears.
    Shows proportions only, with no numbers: it is a picture of the idea, not a measured result."""
    te = 5.6
    blocks = "".join(f'<div class="sg{" k" if b[2]==0 else ""}"><span>{_e(b[0])}</span></div>' for b in segs)
    h = BASE + X + f"""<style>
#col{{position:absolute;left:96px;right:96px;top:640px;height:700px;z-index:2}}
.sg{{position:absolute;left:0;right:0;border-radius:26px;background:#fff;border:1px solid #dedede;display:flex;align-items:center;padding:0 44px;font-size:54px;letter-spacing:-.025em;color:#111;overflow:hidden;white-space:nowrap}}
.sg.k{{background:#111;color:#fff;border-color:#111}}
</style>
<div class="p {theme}"><div class="mark">kato.</div>
<div class="c" id="hd" style="top:330px;font-size:92px;line-height:1.03;letter-spacing:-.04em">{_e(title)}</div>
<div id="col">{blocks}</div>
<div class="sub" id="end" style="top:1400px;font-size:76px;letter-spacing:-.03em">{_e(end)}</div></div>
<script>{{const S={json.dumps([[b[1],b[2]] for b in segs])},te={te},Ht=700,G=16;
window.render=t=>{{
 $('#hd').style.opacity=ease(seg(t,.15,.6));
 const u=io(seg(t,2.2,2.4)); let y=0;
 $$('.sg').forEach((s,i)=>{{const f=S[i][0]+(S[i][1]-S[i][0])*u; const hh=Math.max(0,f*Ht-G);
   const e=ease(seg(t,.5+i*.14,.5)); s.style.top=y+'px'; s.style.height=hh+'px'; s.style.opacity=e*(hh<34?hh/34:1);
   s.style.transform=`translateX(${{(1-e)*-50}}px)`; s.querySelector('span').style.opacity=hh<70?Math.max(0,(hh-34)/36):1; y+=f*Ht;}});
 const k=ease(seg(t,te-.6,.7)); $('#end').style.opacity=k; $('#end').style.transform=`translateY(${{(1-k)*24}}px)`;
}};}}</script>"""
    return dict(dur=te + 2.8, html=h, events=[])

def typed(BASE, q, a, end, theme="ink", size=104):
    """A question typed out letter by letter, then 1 or 2 short answer lines and a closing line."""
    n = len(q); tq = 0.5 + n * 0.055; T = [round(tq + 0.9 + 1.5 * i, 2) for i in range(len(a))]; te = T[-1] + 1.8
    ls = "".join(f'<div class="al">{_e(x)}</div>' for x in a)
    car = "#fff" if _dark(theme) else "#111"
    h = BASE + X + f"""<style>
#q{{position:absolute;left:96px;right:96px;top:360px;font-size:{size}px;line-height:1.06;letter-spacing:-.04em;z-index:2}}
#q i{{display:inline-block;width:6px;height:{int(size*.82)}px;background:{car};vertical-align:-10%;margin-left:8px}}
#an{{position:absolute;left:96px;right:96px;top:1010px;z-index:2;display:flex;flex-direction:column;gap:30px}}
.al{{font-size:62px;line-height:1.16;letter-spacing:-.025em;opacity:0}}
</style>
<div class="p {theme}"><div class="mark">kato.</div>
<div id="q"><span id="qt"></span><i id="cr"></i></div><div id="an" class="mut">{ls}</div>
<div class="sub" id="sub" style="top:1420px;font-size:72px;letter-spacing:-.03em">{_e(end)}</div></div>
<script>{{const Q={json.dumps(q)},T={json.dumps(T)},te={te},tq={tq};
window.render=t=>{{
 const k=Math.floor(cl((t-.5)/(tq-.5))*Q.length); $('#qt').textContent=Q.slice(0,k);
 $('#cr').style.opacity=(t<tq+.3||Math.floor(t*2.2)%2==0)?(1-seg(t,te,.4)):0;
 $$('.al').forEach((d,i)=>{{const e=ease(seg(t,T[i],.6)); d.style.opacity=e; d.style.transform=`translateY(${{(1-e)*22}}px)`;}});
 const e=ease(seg(t,te,.7)); $('#sub').style.opacity=e; $('#sub').style.transform=`translateY(${{(1-e)*22}}px)`;
}};}}</script>"""
    return dict(dur=te + 2.8, html=h, events=[])

KINDS = dict(chat=chat, todo=todo, clock=clock, match=match, define=define, bars=bars, typed=typed)
def build(kind, BASE, params): return KINDS[kind](BASE, **params)
