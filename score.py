"""Put a licensed music track (and optional message sounds) on a rendered Reel, keeping the picture untouched.
  python3 score.py <video.mp4> <track.mp3> [--sfx "0.7:k,2.15:u"] [--sent sent.mp3] [--recv recv.mp3]
The track is cut from its first full section to the video's length, faded in and out, and levelled to about -17 LUFS.
--sfx lists moments (seconds) where a message appears: "u" plays the sent sound, "k" the received sound.
The video is rewritten in place. Never commit the track or sound-effect files; only the finished video belongs in the repo."""
import subprocess, sys, argparse, pathlib, numpy as np
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]).decode())
def start_of(track):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(track),'-ac','1','-ar','8000','-f','f32le','-'])
    x=np.frombuffer(raw,dtype=np.float32); n=len(x)//8000; r=np.sqrt((x[:n*8000].reshape(n,8000)**2).mean(1)); ref=np.percentile(r,75)
    for s in range(0,max(1,min(n-20,70))):
        if r[s:s+6].min()>0.45*ref: return float(s)
    return 5.0
a=argparse.ArgumentParser(); a.add_argument('video'); a.add_argument('track'); a.add_argument('--sfx',default=''); a.add_argument('--sent'); a.add_argument('--recv'); o=a.parse_args()
v=pathlib.Path(o.video); d=dur(v); st=start_of(o.track)
ins=['-i',str(v),'-ss',f'{st}','-t',f'{d}','-i',o.track]
fc=f"[1:a]afade=t=in:st=0:d=0.3,afade=t=out:st={d-1.4:.2f}:d=1.4,loudnorm=I=-17:TP=-1.5:LRA=11[m]"; mix="[m]"; k=2
sfx=[x.split(':') for x in o.sfx.split(',') if x]
for t,side in sfx:
    f=o.sent if side=='u' else o.recv
    if not f: sys.exit('--sfx needs --sent and --recv files')
    ins+=['-i',f]; fc+=f";[{k}:a]volume={0.55 if side=='u' else 0.5},adelay={int(float(t)*1000)}:all=1[s{k}]"; mix+=f"[s{k}]"; k+=1
fc = fc+f";{mix}amix=inputs={k-1}:normalize=0:duration=first,alimiter=limit=0.9[a]" if sfx else fc.replace("[m]","[a]")
tmp=v.with_suffix('.tmp.mp4')
subprocess.check_call(['ffmpeg','-y','-v','error',*ins,'-filter_complex',fc,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','44100','-t',f'{d}','-movflags','+faststart',str(tmp)])
tmp.replace(v); print(v.name,'track starts at',st,'s; length',round(dur(v),2))
