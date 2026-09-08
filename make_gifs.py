from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random, os

OUT='/mnt/data/profile_fix/assets'
os.makedirs(OUT, exist_ok=True)
BG=(13,17,23,255)
GREEN=(180,255,80,255)
WHITE=(235,241,247,255)
MUTED=(139,148,158,255)
FONT='/usr/share/fonts/truetype/lato/Lato-Semibold.ttf'
FONT_B='/usr/share/fonts/truetype/lato/Lato-Bold.ttf'

def font(path,size): return ImageFont.truetype(path,size)

# Welcome typing / cursor GIF
W,H=1000,150
frames=[]
text='WELCOME TO MY GITHUB PROFILE'
f_big=font(FONT_B,34)
f_small=font(FONT,16)
for k in range(len(text)+10):
    im=Image.new('RGBA',(W,H),BG)
    d=ImageDraw.Draw(im)
    shown=text[:min(k,len(text))]
    box=d.textbbox((0,0),shown,font=f_big)
    tw=box[2]-box[0]
    x=(W-tw)//2
    y=45
    d.text((x,y),shown,font=f_big,fill=GREEN)
    if k < len(text):
        # cursor at current position
        d.line((x+tw+3,y+3,x+tw+3,y+38),fill=WHITE,width=2)
    elif k < len(text)+7:
        if (k-len(text))%2==0:
            d.line((x+tw+3,y+3,x+tw+3,y+38),fill=WHITE,width=2)
    else:
        # subtle fade cue
        d.text((W//2,H-28),'software · design · photography',font=f_small,anchor='mm',fill=MUTED)
    frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE))
frames[0].save(os.path.join(OUT,'welcome-profile.gif'),save_all=True,append_images=frames[1:],duration=[55]*len(frames),loop=0,optimize=False,disposal=2)

# Wind/snow strip under name
W,H=1000,95
random.seed(7)
flakes=[(random.randint(0,W),random.randint(0,H),random.choice([1,1,2])) for _ in range(32)]
frames=[]
for t in range(18):
    im=Image.new('RGBA',(W,H),BG)
    d=ImageDraw.Draw(im)
    # wind streaks moving left->right with slight wave
    for i in range(9):
        y=12+i*9
        phase=(t*16+i*43)%120
        x=-180+phase*9
        length=90+(i%3)*35
        pts=[]
        for s in range(25):
            xx=x+s*length/24
            yy=y+math.sin((s/24)*math.pi*2+t*.35+i)*2.2
            pts.append((xx,yy))
        d.line(pts,fill=(120,220,95,150 if i%2 else 110),width=2)
        d.line([(p[0],p[1]+3) for p in pts],fill=(200,255,150,45),width=1)
    # drifting snow
    for idx,(sx,sy,r) in enumerate(flakes):
        xx=(sx+t*8+idx*3)%W
        yy=(sy+t*(1+(idx%3))//2)%H
        d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(240,246,250,170))
    # center signature
    d.text((W//2,H-18),'~  wind / snow  ~',font=font(FONT,15),anchor='mm',fill=MUTED)
    frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE))
frames[0].save(os.path.join(OUT,'wind-under-name.gif'),save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=False,disposal=2)
print('created')
