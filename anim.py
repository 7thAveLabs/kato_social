"""Kato video renderer. python3 anim.py <name|all> <outdir>
Writes kato_<name>.mp4 (1080x1920, 30fps, with original synthesized audio), <name>_cover.jpg and <name>_fallback.jpg (4:5 still).
Built-in: steps, golf, timeback, reconcile, intro (the launch video; its sound is unique to it, do not reuse). Add word-by-word text videos in anims.json (see stagger_anim)."""
import asyncio, sys, pathlib, subprocess, wave, json, numpy as np
from playwright.async_api import async_playwright
W,H,FPS=1080,1920,30
BASE="""<!doctype html><meta charset=utf-8><style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;font-family:'Newsreader','Lora',Georgia,serif;color:#111;letter-spacing:-.03em}
.p{position:absolute;inset:0;padding:120px 96px;overflow:hidden}
.mark{position:absolute;left:96px;top:150px;font-size:60px;letter-spacing:-.04em;z-index:3}
.wash{background:linear-gradient(180deg,#fbfaf7 0%,#f6f2ea 45%,#e9e3d6 100%)}
.bone{background:#f3efe6}.page{background:#f8f6f1}
.blur{background:#3b352d;color:#fff}
.blur:before{content:"";position:absolute;inset:-260px;filter:blur(110px);background:radial-gradient(560px 480px at 22% 16%,#cdbfa4 0,transparent 70%),radial-gradient(640px 600px at 84% 36%,#8a7c66 0,transparent 70%),radial-gradient(760px 600px at 28% 74%,#a39478 0,transparent 70%),radial-gradient(560px 520px at 88% 94%,#d9cfbb 0,transparent 70%);transform:translate(var(--dx,0),var(--dy,0))}
.blur:after{content:"";position:absolute;inset:0;background:rgba(17,17,17,.22)}
.c{position:absolute;left:96px;right:96px;z-index:2}
em{font-style:italic}
</style>
<script>
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>{x=cl(x);return 1-Math.pow(1-x,3)};
const io=x=>{x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const seg=(t,a,d)=>cl((t-a)/d);
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
</script>"""
ANIMS={}
# 1. steps: each line goes bold in turn
ANIMS["steps"]=dict(music="marimba",crop=285,dur=9.0,events=[(1.0+i*1.15,n) for i,n in enumerate([0,1,2,3,4])]+[(7.4,5)],html=BASE+"""
<div class="p blur"><div class="mark">kato.</div>
<div class="c" id="list" style="top:620px;font-size:64px;white-space:nowrap;display:flex;flex-direction:column;gap:70px"></div>
<div class="c" id="end" style="top:820px;font-size:112px;line-height:1.02;opacity:0">We take care<br>of the <em>billing.</em></div></div>
<script>
const L=["Remittance received","Bank deposit verified","3 claim payments posted","Batch K-1042 reconciled","Summary ready"];
$('#list').innerHTML=L.map(t=>`<div class="r" style="display:flex;align-items:center;gap:34px"><svg width="54" height="54" viewBox="0 0 54 54"><circle cx="27" cy="27" r="24" fill="none" stroke="#fff" stroke-width="3"/><circle class="f" cx="27" cy="27" r="24" fill="#fff"/><path class="k" d="M16 28 l8 8 l15 -17" fill="none" stroke="#2c2721" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1"/></svg><span>${t}</span></div>`).join('');
window.render=t=>{
  document.querySelector('.blur').style.setProperty('--dx',(Math.sin(t*.5)*40)+'px');document.querySelector('.blur').style.setProperty('--dy',(Math.cos(t*.4)*50)+'px');
  const out=seg(t,6.9,.5);
  $$('.r').forEach((r,i)=>{const a=1.0+i*1.15; const on=ease(seg(t,a,.35)); const next=ease(seg(t,a+1.15,.4))*(i<4?1:0);
    const sp=r.querySelector('span'); const w=400+300*on-250*next; sp.style.fontVariationSettings=`'wght' ${w}`; sp.style.fontWeight=w;
    r.style.opacity=(0.34+0.66*on-0.3*next)*(1-out); r.style.transform=`translateX(${10*on-10*next}px)`;
    r.querySelector('.f').style.opacity=on; r.querySelector('.k').style.strokeDashoffset=1-ease(seg(t,a+.1,.35));});
  const e=ease(seg(t,7.3,.7)); $('#end').style.opacity=e; $('#end').style.transform=`translateY(${(1-e)*30}px)`;
};</script>""")
# 2. golf
ANIMS["golf"]=dict(music="bell",crop=285,dur=7.5,events=[(3.15,2),(3.9,3),(5.0,4)],html=BASE+"""
<div class="p bone"><div class="mark">kato.</div>
<svg class="c" style="top:560px" viewBox="0 0 888 420"><ellipse cx="660" cy="352" rx="170" ry="18" fill="#e4dfd3"/>
<path d="M0 352 H888" stroke="#111" stroke-opacity=".3" stroke-width="2"/><ellipse cx="660" cy="352" rx="32" ry="7" fill="#111"/>
<g id="pin"><path d="M660 352 V92" stroke="#111" stroke-width="5" stroke-linecap="round"/><path id="fl" d="M662 94 L790 136 L662 178 Z" fill="#111"/></g>
<circle id="ball" cx="60" cy="331" r="20" fill="#fff" stroke="#111" stroke-width="3"/></svg>
<div class="c" id="h" style="top:1040px;font-size:150px;line-height:.98;letter-spacing:-.04em;opacity:0">Work on<br>your swing.</div>
<div class="c" id="s" style="top:1390px;font-size:64px;color:#626262;font-style:italic;opacity:0">We'll handle the billing.</div></div>
<script>window.render=t=>{
 const r=ease(seg(t,.5,2.6)); const x=60+600*r; const drop=seg(t,3.05,.25);
 const b=$('#ball'); b.setAttribute('cx',x); b.setAttribute('cy',331+22*drop); b.setAttribute('r',20*(1-.55*drop)); b.style.opacity=1-drop;
 const wob=Math.sin((t-3.1)*14)*Math.exp(-(t-3.1)*3)*(t>3.1?1:0);
 $('#fl').setAttribute('d',`M662 94 L${790+wob*10} ${136+wob*8} L662 178 Z`);
 const e=ease(seg(t,3.8,.8)); $('#h').style.opacity=e; $('#h').style.transform=`translateY(${(1-e)*30}px)`;
 const e2=ease(seg(t,4.9,.8)); $('#s').style.opacity=e2;
};</script>""")
# 3. time back
ANIMS["timeback"]=dict(music="calm",crop=285,dur=7.0,events=[(0.6,0),(1.3,1),(2.0,2),(2.9,4),(4.6,5)],html=BASE+"""
<div class="p wash"><div class="mark">kato.</div>
<div class="c" id="w" style="top:560px;font-size:190px;line-height:1;letter-spacing:-.045em;display:flex;flex-direction:column;gap:34px"></div>
<div class="c" id="s" style="top:1500px;font-size:62px;color:#626262;opacity:0">We take care of the billing.</div></div>
<script>const Wd=["Get","your","time","<em>back.</em>"],T=[.6,1.3,2.0,2.9];
$('#w').innerHTML=Wd.map((w,i)=>`<span style="margin-left:${i*130}px;display:block">${w}</span>`).join('');
window.render=t=>{$$('#w span').forEach((s,i)=>{const e=ease(seg(t,T[i],.7)); s.style.opacity=e; s.style.transform=`translateY(${(1-e)*46}px)`;});
 const e=ease(seg(t,4.5,.8)); $('#s').style.opacity=e;};</script>""")
# 4. card reconcile
ANIMS["reconcile"]=dict(music="keys",crop=320,dur=8.5,events=[(1.4,0),(2.9,1),(4.4,2),(5.9,5)],html=BASE+"""
<style>.card{background:#fff;border-radius:36px;padding:56px 56px 30px;border:1px solid #dedede;box-shadow:0 40px 90px -50px rgba(17,17,17,.35);font-family:Inter,sans-serif;letter-spacing:0}
.hd{display:flex;justify-content:space-between;align-items:baseline;font-size:34px;font-weight:600;padding-bottom:32px;border-bottom:1px solid #dedede}
.bt{background:#f3efe6;border-radius:20px;padding:36px 38px;margin:36px 0 10px;display:flex;justify-content:space-between;align-items:center}
.bt b{font-size:40px;font-weight:600;display:block}.bt span{font-size:31px;color:#626262}.amt{font-size:58px;font-weight:500;letter-spacing:-.02em}
.row{display:flex;justify-content:space-between;align-items:center;padding:34px 4px;border-bottom:1px solid #dedede;font-size:37px;position:relative;height:112px}.row:last-child{border:0}
.row .k{color:#626262}.v{position:absolute;right:4px;display:flex;align-items:center;gap:16px;font-weight:500}
.d{width:34px;height:34px;border-radius:50%;background:#111;color:#fff;font-size:20px;display:flex;align-items:center;justify-content:center}
.o{width:34px;height:34px;border-radius:50%;border:3px solid #c9c5bb;border-top-color:#111}</style>
<div class="p page"><div class="mark">kato.</div>
<div class="c" id="h" style="top:380px;font-size:104px;line-height:1.03;letter-spacing:-.04em">Know what arrived.<br><em>Know what hasn't.</em></div>
<div class="c" style="top:740px"><div class="card"><div class="hd"><span>Payments</span><span style="font-family:Lora,serif;font-weight:400;font-size:44px;letter-spacing:-.04em">kato.</span></div>
<div class="bt"><div><b>K-1042</b><span id="bs" style="position:relative;display:block;height:40px;width:300px"><span class="a" style="position:absolute">In progress</span><span class="b" style="position:absolute;color:#111;font-weight:600">Reconciled</span></span></div><div class="amt">$2,480.00</div></div>
<div class="row"><span class="k">Remittance</span><span class="v a"><span class="o"></span>Waiting</span><span class="v b"><span class="d">&#10003;</span>Received</span></div>
<div class="row"><span class="k">Bank deposit</span><span class="v a"><span class="o"></span>Checking</span><span class="v b"><span class="d">&#10003;</span>Verified</span></div>
<div class="row"><span class="k">PMS payments</span><span class="v a"><span class="o"></span>Pending</span><span class="v b"><span class="d">&#10003;</span>Posted</span></div></div></div>
<div class="c" id="s" style="top:1560px;font-size:62px;color:#626262;opacity:0">Three records that agree.</div></div>
<script>const T=[1.4,2.9,4.4];
window.render=t=>{$$('.row').forEach((r,i)=>{const e=ease(seg(t,T[i],.4)); r.querySelector('.a').style.opacity=1-e; const b=r.querySelector('.b'); b.style.opacity=e; b.style.transform=`translateY(${(1-e)*10}px)`; r.querySelector('.o').style.transform=`rotate(${t*300}deg)`;});
 const e=ease(seg(t,5.9,.5)); $('#bs .a').style.opacity=1-e; $('#bs .b').style.opacity=e; $('.bt').style.background=`rgb(${243-6*e},${239-4*e},${230-2*e})`;
 const e2=ease(seg(t,6.6,.8)); $('#s').style.opacity=e2;};</script>""")


# 5. intro: the dot from "kato." drops in, rolls across and writes the wordmark, then lands as the period.
def _intro_audio(dur,path,sr=44100):
    """One-off sound for the intro only: three soft thuds as the dot lands, a low rolling rumble, then a single warm chord that blooms and fades."""
    rng=np.random.default_rng(7); n=int(dur*sr); t=np.arange(n)/sr; y=np.zeros(n)
    for at,amp in [(0.90,.9),(1.30,.5),(1.55,.25)]:                      # thuds: pitch drops, never rises
        k=int(at*sr); tt=np.arange(n-k)/sr; f=58+70*np.exp(-tt*28)
        y[k:]+=amp*np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*16)
    noise=rng.standard_normal(n); kern=np.ones(260)/260; low=np.convolve(noise,kern,mode="same"); low=np.convolve(low,kern,mode="same")
    env=np.clip((t-1.7)/0.25,0,1)*np.clip((3.05-t)/0.3,0,1)                 # roll: filtered noise with a slow wobble
    y+=9.0*low*env*(0.7+0.3*np.sin(2*np.pi*7*t))
    k=int(3.0*sr); tt=np.arange(n-k)/sr                                    # bloom: one chord, slow attack, long tail
    chord=sum(a*(np.sin(2*np.pi*f*tt)+np.sin(2*np.pi*f*1.003*tt)) for f,a in [(146.83,.5),(220.0,.42),(329.63,.3),(369.99,.26),(440.0,.16),(880.0,.05)])
    y[k:]+=0.42*chord*(1-np.exp(-tt*5))*np.exp(-tt*0.55)*(1+0.05*np.sin(2*np.pi*0.8*tt))
    for d,g in [(.11,.3),(.23,.22),(.37,.15),(.53,.1)]:                    # small room
        dd=int(d*sr); y[dd:]+=g*y[:-dd]
    y*=np.clip((dur-t)/1.2,0,1); y=y/max(1e-9,np.abs(y).max())*0.75
    with wave.open(path,'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y*32767).astype('<i2').tobytes())
ANIMS["intro"]=dict(dur=9.0,events=[],crop=285,audio_fn=_intro_audio,html=BASE+"""
<div class="p wash">
<div id="grp" style="position:absolute;left:0;right:0;top:0;bottom:0">
 <div id="wm" style="position:absolute;left:0;right:0;top:760px;text-align:center;font-size:330px;line-height:1;letter-spacing:-.045em;white-space:nowrap"><span id="txt">kato</span><span id="per" style="visibility:hidden">.</span><span id="bl" style="display:inline-block;width:0;height:0;vertical-align:baseline"></span></div>
 <div id="dot" style="position:absolute;border-radius:50%;background:#111;left:0;top:0"></div>
</div>
<div class="c" id="t1" style="top:1130px;text-align:center;font-size:96px;letter-spacing:-.035em;opacity:0">Get your <em>time back.</em></div>
<div class="c" id="t2" style="top:1290px;text-align:center;font-size:52px;letter-spacing:-.01em;color:#626262;opacity:0">We take care of the billing.</div>
</div>
<script>{
const txt=$('#txt'),per=$('#per'),dot=$('#dot'); let G=null;
function geo(){const a=txt.getBoundingClientRect(),p=per.getBoundingClientRect(),b=$('#bl').getBoundingClientRect();
  const r=Math.round(a.height*0.062); return {l:a.left,xf:p.left+p.width*0.5,base:b.top,r,x0:a.left-90};}
const fall=(t)=>{ // height above the floor
  if(t<0.4) return 1200; if(t<0.9){const u=(t-0.4)/0.5; return 1200*(1-u*u);}
  if(t<1.3){const u=(t-0.9)/0.4; return 150*4*u*(1-u);} if(t<1.55){const u=(t-1.3)/0.25; return 44*4*u*(1-u);}
  if(t>=7.1&&t<7.6){const u=(t-7.1)/0.5; return 70*4*u*(1-u);} return 0;};
window.render=t=>{ if(!G) G=geo(); const g=G;
  const roll=io(seg(t,1.7,1.3)); const x=g.x0+(g.xf-g.x0)*roll; const h=fall(t);
  const sq=(t>=0.9&&t<0.98)||(t>=1.3&&t<1.36)?0.78:1;                      // squash on landing
  const pop=1+0.35*Math.sin(Math.PI*seg(t,3.0,0.35));                        // one pulse when it becomes the period
  dot.style.width=dot.style.height=(2*g.r)+'px';
  dot.style.transform=`translate(${x-g.r}px,${g.base-2*g.r-h}px) scale(${pop/ (sq<1?0.9:1)},${pop*sq})`; dot.style.transformOrigin='50% 100%';
  dot.style.opacity=t<0.4?0:1;
  const rev=Math.max(0,x-g.r-6-g.l); txt.style.clipPath=`inset(-20% ${Math.max(0,txt.getBoundingClientRect().width-rev)}px -20% 0)`;
  const up=ease(seg(t,3.7,0.9)); $('#grp').style.transform=`translateY(${-150*up}px)`;
  const a=ease(seg(t,4.4,0.9)); $('#t1').style.opacity=a; $('#t1').style.transform=`translateY(${(1-a)*24}px)`;
  $('#t2').style.opacity=ease(seg(t,5.7,0.9));
};}</script>""")

PROFILES={
 "calm":   dict(scale=[261.63,293.66,329.63,392.0,440.0,523.25], pad=[130.81,196.0,261.63,329.63], timbre="sine",   echo=.28),
 "marimba":dict(scale=[220.0,261.63,293.66,329.63,392.0,440.0],  pad=[110.0,164.81,220.0],          timbre="marimba",echo=.19),
 "bell":   dict(scale=[392.0,440.0,493.88,587.33,659.25,783.99], pad=[98.0,146.83,196.0,246.94],    timbre="bell",   echo=.34),
 "keys":   dict(scale=[293.66,329.63,369.99,440.0,493.88,587.33],pad=[146.83,220.0,293.66],         timbre="epiano", echo=.25, pulse=(73.42,.667)),
 "swell":  dict(scale=[174.61,220.0,261.63,349.23,440.0,523.25], pad=[87.31,130.81,174.61,220.0],   timbre="swell",  echo=.40),
}
def _tone(kind,f,tt):
    s=lambda m:np.sin(2*np.pi*f*m*tt)
    if kind=="marimba": return (s(1)+.5*s(4)*np.exp(-tt*18))*np.exp(-tt*6)*np.minimum(1,tt/.004)
    if kind=="bell":    return (s(1)+.5*s(2.76)*np.exp(-tt*3)+.25*s(5.4)*np.exp(-tt*6))*np.exp(-tt*1.6)*np.minimum(1,tt/.005)
    if kind=="epiano":  return (s(1)+.4*s(2)*np.exp(-tt*3))*(1+.15*np.sin(2*np.pi*5*tt))*np.exp(-tt*2.5)*np.minimum(1,tt/.008)
    if kind=="swell":   return (s(1)+.3*s(2))*np.minimum(1,tt/.5)*np.exp(-np.maximum(0,tt-.5)*1.2)
    return (s(1)+.35*s(2)*np.exp(-tt*5)+.12*s(3)*np.exp(-tt*8))*np.exp(-tt*2.2)*np.minimum(1,tt/.008)
def audio(dur,events,path,profile="calm",sr=44100):
    """Original synthesized audio: a quiet pad plus one note per on-screen event. No third-party music."""
    P=PROFILES[profile]; n=int(dur*sr); t=np.arange(n)/sr; y=np.zeros(n)
    pad=sum(np.sin(2*np.pi*f*t+i)*(.5/(i+1)) for i,f in enumerate(P["pad"]))
    y+=0.11*pad*np.minimum(1,t/1.5)*np.minimum(1,(dur-t)/1.5)*(0.8+0.2*np.sin(2*np.pi*.12*t))
    if P.get("pulse"):
        f,step=P["pulse"]; k=0.5
        while k<dur-1.5:
            i=int(k*sr); tt=np.arange(n-i)/sr; y[i:]+=0.10*np.sin(2*np.pi*f*tt)*np.exp(-tt*5)*np.minimum(1,tt/.01); k+=step
    for at,note in events:
        k=int(at*sr); m=n-k
        if m>0: y[k:]+=0.26*_tone(P["timbre"],P["scale"][note],np.arange(m)/sr)
    d=int(P["echo"]*sr); y[d:]+=0.25*y[:-d]
    y=y/max(1e-9,np.abs(y).max())*0.7
    with wave.open(path,'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y*32767).astype('<i2').tobytes())
def stagger_anim(words,theme="wash",sub="",step=130,size=190,music="calm"):
    """Generic word-by-word text video. words: list of strings (may contain <em>). theme: wash|bone|page|blur."""
    T=[round(.6+.75*i,2) for i in range(len(words))]; ts=T[-1]+1.6
    col="#efeae0" if theme=="blur" else "#626262"
    h=BASE+f"""<div class="p {theme}"><div class="mark">kato.</div>
<div class="c" id="w" style="top:560px;font-size:{size}px;white-space:nowrap;line-height:1;letter-spacing:-.045em;display:flex;flex-direction:column;gap:34px"></div>
<div class="c" id="s" style="top:1500px;font-size:62px;color:{col};opacity:0">{sub}</div></div>
<script>{{const Wd={json.dumps(words)},T={json.dumps(T)};
$('#w').innerHTML=Wd.map((w,i)=>`<span style="margin-left:${{i*{step}}}px;display:block">${{w}}</span>`).join('');
window.render=t=>{{const bl=document.querySelector('.blur'); if(bl){{bl.style.setProperty('--dx',(Math.sin(t*.5)*40)+'px');bl.style.setProperty('--dy',(Math.cos(t*.4)*50)+'px');}}
 $$('#w span').forEach((s,i)=>{{const e=ease(seg(t,T[i],.7)); s.style.opacity=e; s.style.transform=`translateY(${{(1-e)*46}}px)`;}});
 $('#s').style.opacity=ease(seg(t,{ts},.8));}};}}</script>"""
    n=len(words); ev=[(T[i],min(i,5)) for i in range(n)]+([(ts,5)] if sub else [])
    return dict(dur=ts+2.6,events=ev,html=h,music=music)
# extra text videos can be declared in anims.json: {"name": {"words":[...],"theme":"wash","sub":"","step":130,"size":190,"music":"calm"}}
if pathlib.Path(__file__).with_name("anims.json").exists():
    for k,v in json.loads(pathlib.Path(__file__).with_name("anims.json").read_text()).items(): ANIMS[k]=stagger_anim(**v)
async def run(names,out):
    out=pathlib.Path(out); out.mkdir(exist_ok=True,parents=True)
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        for nm in names:
            pg=await br.new_page(viewport={"width":W,"height":H})
            a=ANIMS[nm]; fd=out/f"_f_{nm}"; fd.mkdir(exist_ok=True)
            await pg.set_content(a["html"]); await pg.evaluate("document.fonts.ready")
            nf=int(a["dur"]*FPS)
            for i in range(nf):
                await pg.evaluate(f"render({i/FPS})")
                await pg.screenshot(path=str(fd/f"{i:04d}.jpg"),type="jpeg",quality=90)
            (a["audio_fn"](a["dur"],str(out/f"{nm}.wav")) if a.get("audio_fn") else audio(a["dur"],a["events"],str(out/f"{nm}.wav"),a.get("music","calm")))
            subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",str(fd/"%04d.jpg"),"-i",str(out/f"{nm}.wav"),
              "-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-preset","medium","-c:a","aac","-b:a","160k","-movflags","+faststart","-shortest",str(out/f"kato_{nm}.mp4")],check=True)
            import shutil; from PIL import Image
            last=fd/f"{nf-1:04d}.jpg"; shutil.copy(last,out/f"{nm}_cover.jpg")   # 9:16 cover (final frame)
            c=a.get("crop",285); Image.open(last).crop((0,c,1080,c+1350)).save(out/f"{nm}_fallback.jpg",quality=92)  # 4:5 still
            shutil.rmtree(fd); (out/f"{nm}.wav").unlink(); print(nm,nf); await pg.close()
        await br.close()
names=list(ANIMS) if sys.argv[1]=="all" else [sys.argv[1]]
asyncio.run(run(names,sys.argv[2]))
