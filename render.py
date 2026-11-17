"""Kato Instagram renderer v2. python3 render.py posts.json out/
Slides are 1080x1350 JPEG. No buttons, links or URLs on images: nothing on a post is tappable."""
import asyncio, json, sys, html, pathlib, io, base64
from playwright.async_api import async_playwright
W, H = 1080, 1350
CSS = """
:root{--ink:#111;--paper:#fff;--bone:#f3efe6;--page:#f8f6f1;--mist:#e8e5de;--muted:#626262;--line:#dedede;
--serif:'Newsreader','Lora',Georgia,serif;--sans:'Inter',sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;font-family:var(--sans);color:var(--ink)}
.post{width:1080px;height:1350px;padding:84px 92px;display:flex;flex-direction:column;position:relative;overflow:hidden;background:var(--page)}
.bone{background:var(--bone)} .dark{background:var(--ink);color:#fff}
.wash{background:linear-gradient(180deg,#fbfaf7 0%,#f6f2ea 45%,#e9e3d6 100%)}
.blur{background:#3b352d;color:#fff}
.blur:before{content:"";position:absolute;inset:-200px;filter:blur(90px);
background:radial-gradient(520px 420px at 22% 18%,#cdbfa4 0,transparent 70%),radial-gradient(600px 520px at 82% 34%,#8a7c66 0,transparent 70%),
radial-gradient(700px 520px at 30% 78%,#a39478 0,transparent 70%),radial-gradient(520px 480px at 88% 92%,#d9cfbb 0,transparent 70%)}
.blur:after{content:"";position:absolute;inset:0;background:rgba(17,17,17,.18)}
.post>*{position:relative;z-index:2}
.photo{color:#fff;background-size:cover;background-position:center}
.photo .sub{color:#f3efe6}.photo .tag{color:#e8e5de}
.stat{font-family:var(--serif);font-size:300px;line-height:.86;letter-spacing:-.05em}
.src{font-size:24px;color:#e8e5de;opacity:.85;margin-top:8px}
.top{display:flex;justify-content:space-between;align-items:baseline}
.mark{font-family:var(--serif);font-size:54px;letter-spacing:-.04em;line-height:1}
.tag{font-family:var(--serif);font-size:26px;letter-spacing:.04em;color:var(--muted);font-weight:500}
.dark .tag,.dark .sub,.blur .tag{color:#b9b6ae} .blur .sub{color:#efeae0}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px}
.body.c{align-items:center;text-align:center}
h1{font-family:var(--serif);font-weight:400;letter-spacing:-.04em;line-height:1;font-size:132px}
h1.m{font-size:108px} h1.s{font-size:88px;line-height:1.04} h1.xs{font-size:64px;line-height:1.08;letter-spacing:-.03em}
em{font-style:italic}
.sub{font-family:var(--serif);font-size:50px;line-height:1.25;letter-spacing:-.015em;color:var(--muted);max-width:840px}
.stag{display:flex;flex-direction:column;gap:26px;font-family:var(--serif);font-size:124px;letter-spacing:-.04em;line-height:1}
.note{font-size:24px;color:var(--muted);margin-top:18px} .blur .note,.dark .note{color:#cfc9bc}
.card{background:var(--paper);color:var(--ink);border-radius:28px;padding:40px 44px;border:1px solid var(--line);box-shadow:0 24px 60px -30px rgba(17,17,17,.25)}
.hd{display:flex;justify-content:space-between;align-items:baseline;font-size:26px;font-weight:600;padding-bottom:24px;border-bottom:1px solid var(--line)}
.hd .mark{font-size:34px;font-weight:400}
.batch{background:var(--bone);border-radius:16px;padding:28px 30px;margin:28px 0 8px;display:flex;justify-content:space-between;align-items:center}
.batch b{font-size:30px;font-weight:600;display:block}.batch span{font-size:24px;color:var(--muted)}.batch .amt{font-size:44px;font-weight:500;letter-spacing:-.02em}
.row{display:flex;justify-content:space-between;align-items:center;padding:24px 4px;border-bottom:1px solid var(--line);font-size:28px}.row:last-child{border:0}
.row .k{color:var(--muted)} .st{display:flex;align-items:center;gap:12px;font-weight:500}
.dot{width:26px;height:26px;border-radius:50%;background:var(--ink);color:#fff;font-size:16px;display:flex;align-items:center;justify-content:center}
.dot.open{background:transparent;border:2px solid var(--ink);color:var(--ink);font-weight:700}
.feed{display:flex;flex-direction:column;gap:44px;font-size:56px;font-family:var(--serif);letter-spacing:-.02em}
.feed div{display:flex;gap:26px;align-items:center}
.feed i{width:30px;height:30px;border-radius:50%;border:2px solid currentColor;display:inline-block;flex:none;position:relative}
.feed i:after{content:"";position:absolute;left:8px;top:4px;width:8px;height:14px;border:solid currentColor;border-width:0 2.5px 2.5px 0;transform:rotate(45deg)}
.bars{display:flex;flex-direction:column;gap:22px;width:100%}
.bars div{height:92px;border-radius:14px;background:var(--mist);display:flex;align-items:center;padding:0 32px;font-family:var(--serif);font-size:32px;color:var(--muted);justify-content:space-between}
.bars div b{font-weight:500;color:var(--ink)}
.num{font-family:var(--serif);font-size:190px;line-height:.8;letter-spacing:-.05em;opacity:.16}
.golf{width:100%;height:340px}
.golf svg{width:100%;height:100%;display:block}
"""

def photo_bg(name):
    """Load photos/<name>.jpg, crop to 4:5, apply the Kato filter (muted, warm, darkened, soft, light grain), return a data URI."""
    from PIL import Image, ImageEnhance, ImageFilter
    import numpy as np
    im=Image.open(pathlib.Path(__file__).with_name("photos")/f"{name}.jpg").convert("RGB")
    w,h=im.size; tw=int(h*W/H)
    if tw<=w: im=im.crop(((w-tw)//2,0,(w-tw)//2+tw,h))
    else:
        th=int(w*H/W); im=im.crop((0,(h-th)//2,w,(h-th)//2+th))
    im=im.resize((W,H),Image.LANCZOS)
    im=ImageEnhance.Color(im).enhance(0.62); im=ImageEnhance.Contrast(im).enhance(0.92); im=im.filter(ImageFilter.GaussianBlur(1.4))
    a=np.asarray(im).astype("float32"); k=min(0.62,78.0/max(1.0,a.mean())); a=a*np.array([1.04,1.0,0.90])*k+np.array([20,16,11])   # warm tint, darken, lift blacks
    y=np.linspace(0,1,H)[:,None,None]; a*=1-0.22*np.abs(y-0.45)                                   # soft vertical vignette
    a+=np.random.default_rng(11).normal(0,5.5,a.shape)                                           # film grain
    im=Image.fromarray(np.clip(a,0,255).astype("uint8")); b=io.BytesIO(); im.save(b,"JPEG",quality=88)
    return "data:image/jpeg;base64,"+base64.b64encode(b.getvalue()).decode()
def em(s):
    out=""
    for i,p in enumerate(html.escape(s).split("*")): out+=f"<em>{p}</em>" if i%2 else p
    return out.replace("\n","<br>")
def card(c):
    rows="".join(f'<div class="row"><span class="k">{html.escape(k)}</span><span class="st"><span class="dot {"" if ok else "open"}">{"&#10003;" if ok else "!"}</span>{html.escape(v)}</span></div>' for k,v,ok in c["rows"])
    return (f'<div><div class="card"><div class="hd"><span>{html.escape(c["title"])}</span><span class="mark">kato.</span></div>'
            f'<div class="batch"><div><b>{html.escape(c["batch"])}</b><span>{html.escape(c["status"])}</span></div><div class="amt">{html.escape(c["amount"])}</div></div>{rows}</div>'
            '</div>')
def slide(s,i,n):
    b=""
    if s.get("golf"): b+=('<div class="golf"><svg viewBox="0 0 896 340"><ellipse cx="640" cy="282" rx="150" ry="16" fill="#e4dfd3"/>'
        '<path d="M0 282 H896" stroke="#111" stroke-opacity=".3" stroke-width="2"/>'
        '<ellipse cx="640" cy="282" rx="30" ry="6" fill="#111"/>'
        '<path d="M640 282 V52" stroke="#111" stroke-width="5" stroke-linecap="round"/>'
        '<path d="M642 54 L758 92 L642 130 Z" fill="#111"/>'
        '<circle cx="330" cy="262" r="19" fill="#fff" stroke="#111" stroke-width="3"/>'
        '<path d="M150 262 H170 M190 262 H222 M246 262 H290" stroke="#111" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/></svg></div>')
    if s.get("stat"): b+=f'<div class="stat">{html.escape(s["stat"])}</div>'
    if s.get("num"): b+=f'<div class="num">{html.escape(s["num"])}</div>'
    if s.get("stagger"):
        k=len(s["stagger"]); step=s.get("step",110)
        b+=f'<div class="stag" style="font-size:{s.get("fs",124)}px">'+"".join(f'<span style="margin-left:{j*step}px">{em(w)}</span>' for j,w in enumerate(s["stagger"]))+'</div>'
    if s.get("headline"): b+=f'<h1 class="{s.get("size","")}">{em(s["headline"])}</h1>'
    if s.get("sub"): b+=f'<div class="sub">{em(s["sub"])}</div>'
    if s.get("source"): b+=f'<div class="src">{html.escape(s["source"])}</div>'
    if s.get("bars"): b+='<div class="bars">'+"".join(f'<div><b>{html.escape(a)}</b><span>{html.escape(c)}</span></div>' for a,c in s["bars"])+'</div>'
    if s.get("feed"):
        b+='<div class="feed">'+"".join(f'<div style="opacity:{o}"><i></i>{html.escape(t)}</div>' for t,o in s["feed"])+'</div>'
    if s.get("card"): b+=card(s["card"])
    tag=f"{i+1:02d} / {n:02d}" if n>1 else ""
    ph=s.get("photo"); bg=f' style="background-image:url({photo_bg(ph)})"' if ph else ""
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="post {s.get("theme","")}{" photo" if ph else ""}"{bg}>'
            f'<div class="top"><span class="mark">kato.</span><span class="tag">{tag}</span></div>'
            f'<div class="body {"c" if s.get("center") else ""}">{b}</div></div>')
async def main(pp,od):
    posts=json.loads(pathlib.Path(pp).read_text()); out=pathlib.Path(od); out.mkdir(parents=True,exist_ok=True)
    async with async_playwright() as p:
        br=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        pg=await br.new_page(viewport={"width":W,"height":H})
        for post in posts:
            n=len(post["slides"])
            for i,s in enumerate(post["slides"]):
                await pg.set_content(slide(s,i,n)); await pg.evaluate("document.fonts.ready")
                f=out/(f'{post["id"]}.jpg' if n==1 else f'{post["id"]}_{i+1}.jpg')
                await pg.screenshot(path=str(f),type="jpeg",quality=92)
        await br.close()
asyncio.run(main(sys.argv[1],sys.argv[2]))
