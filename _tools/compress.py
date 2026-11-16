"""Compress BulandTech portfolio media into <site>/media/ (originals untouched)."""
import os, sys, re, subprocess, glob
from PIL import Image
import imageio_ffmpeg

SITE = sys.argv[1]
WHAT = sys.argv[2] if len(sys.argv) > 2 else 'all'
OUT = os.path.join(SITE, 'media')
os.makedirs(OUT, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()

def slug(path):
    return re.sub(r'[^a-z0-9]+', '-', os.path.splitext(os.path.basename(path))[0].lower()).strip('-')

def kb(p): return os.path.getsize(p) // 1024

if WHAT in ('all', 'images'):
    pngs = glob.glob(os.path.join(SITE, '*.png')) + glob.glob(os.path.join(SITE, 'assetts', '**', '*.png'), recursive=True)
    before = after = 0
    for src in pngs:
        s = slug(src)
        im = Image.open(src).convert('RGB')
        for suffix, width, q in (('', 1600, 82), ('-sm', 800, 76)):
            dst = os.path.join(OUT, f'{s}{suffix}.webp')
            r = im.copy()
            r.thumbnail((width, width))
            r.save(dst, 'WEBP', quality=q, method=6)
            after += os.path.getsize(dst)
        before += os.path.getsize(src)
        print(f'img {s}: {kb(src)}KB -> {kb(os.path.join(OUT, s + ".webp"))}KB / {kb(os.path.join(OUT, s + "-sm.webp"))}KB', flush=True)
    print(f'IMAGES total {before // 1048576}MB -> {after // 1048576}MB', flush=True)

if WHAT in ('all', 'videos'):
    vids = {
        'Wedding Teaser 2025 _ Art Of Devil(1080P_HD).mp4': 'wedding-teaser-2025',
        'lv_0_20260815164559.mp4': 'cinematic-wedding',
        'VN20260916_214846.mp4': 'fast-cut-teaser',
    }
    for name, out in vids.items():
        src = os.path.join(SITE, 'assetts', name)
        dst = os.path.join(OUT, out + '.mp4')
        subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-i', src,
                        '-map', '0:v:0', '-map', '0:a:0?',
                        '-vf', "scale='min(1920,iw)':-2", '-c:v', 'libx264', '-preset', 'medium', '-crf', '25',
                        '-maxrate', '4M', '-bufsize', '8M', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', dst], check=True)
        jpg = os.path.join(OUT, out + '-poster.jpg')
        subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-ss', '2', '-i', dst,
                        '-frames:v', '1', '-vf', 'scale=1280:-2', jpg], check=True)
        Image.open(jpg).save(os.path.join(OUT, out + '-poster.webp'), 'WEBP', quality=78, method=6)
        os.remove(jpg)
        print(f'vid {out}: {kb(src) // 1024}MB -> {kb(dst) // 1024}MB', flush=True)
    print('VIDEOS done', flush=True)
