(()=>{
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const SH=[
 {k:"01",n:"Natural Black",c:"1B",h:"#2A201C"},{k:"02",n:"Jet Black",c:"1",h:"#0E0E10"},
 {k:"03",n:"Ginger",c:"350",h:"#B4552C"},{k:"04",n:"Burgundy",c:"530",h:"#6E1B2E"},
 {k:"05",n:"Brown",c:"99J",h:"#441A28"},{k:"06",n:"Honey Auburn",c:"",h:"#8D6038"},
 {k:"07",n:"Honey Blonde",c:"",h:"#C99A55"},{k:"08",n:"Natural Auburn",c:"",h:"#9E6B3C"},
 {k:"09",n:"Red",c:"",h:"#B0141F"}];
const TH=k=>({src:"assets/img/theater-"+k+"-1920.jpg",srcset:"assets/img/theater-"+k+"-1000.jpg 1000w, assets/img/theater-"+k+"-1920.jpg 1920w"});
const PR=k=>"assets/img/product-"+k+".jpg";
const full=s=>s.c?s.n+" "+s.c:s.n;
const $=id=>document.getElementById(id);

/* opening titles */
const intro=$('intro');
function startSite(){ if(!document.body.classList.contains('intro-on'))return;
  intro.classList.add('open'); document.body.classList.remove('intro-on');
  setTimeout(()=>document.body.classList.add('ready'),150);
  setTimeout(()=>intro.remove(),1300); }
if(reduce){ intro.remove(); document.body.classList.remove('intro-on'); document.body.classList.add('ready'); }
else { setTimeout(startSite,2300); $('skip').onclick=startSite; intro.addEventListener('click',startSite); }

/* shade theater */
const thImgs=$('thImgs'), rail=$('thRail'), name=$('thName');
const thEls=SH.map((s,i)=>{const im=new Image(); const t=TH(s.k); im.srcset=t.srcset; im.sizes="100vw"; im.src=t.src; if(i) im.loading="lazy"; im.alt="Model beside a lamp wearing the Body Wave wig in "+full(s); if(!i)im.className='on'; thImgs.appendChild(im); return im;});
const railBtns=SH.map((s,i)=>{const li=document.createElement('li'); const b=document.createElement('button'); b.type='button';
  b.setAttribute('aria-label','Show '+full(s)); if(!i)b.setAttribute('aria-current','true');
  b.innerHTML='<span class="sw" style="background:'+s.h+'"></span><span class="nm">'+full(s)+'</span>';
  b.onclick=()=>{const t=theater.offsetTop+(i+.5)/SH.length*(theater.offsetHeight-innerHeight); scrollTo({top:t,behavior:reduce?'auto':'smooth'});};
  li.appendChild(b); rail.appendChild(li); return b;});
let cur=0;
function setShade(i){ if(i===cur)return; thEls[cur].classList.remove('on'); thEls[i].classList.add('on');
  railBtns[cur].removeAttribute('aria-current'); railBtns[i].setAttribute('aria-current','true');
  const s=SH[i]; cur=i; $('thIdx').textContent=i+1;
  name.classList.add('out');
  setTimeout(()=>{ name.textContent=s.n; $('thCode').textContent=s.c?"Color "+s.c:"Signature shade";
    name.classList.remove('out'); name.classList.add('in'); void name.offsetWidth; name.classList.remove('in'); },reduce?0:280);
}

/* featured unit */
const media=$('uMedia'), chips=$('chips');
const uImgs=SH.map((s,i)=>{const im=new Image(); im.src=PR(s.k); if(i) im.loading="lazy"; im.alt="Body Wave lace wig in "+full(s); if(!i)im.className='on'; media.insertBefore(im,$('uCap')); return im;});
let ucur=0;
SH.forEach((s,i)=>{const li=document.createElement('li'); const b=document.createElement('button'); b.type='button'; b.className='chip';
  b.style.background=s.h; b.setAttribute('aria-label',full(s)); b.title=full(s); b.setAttribute('aria-pressed',i?'false':'true');
  b.onclick=()=>{ uImgs[ucur].classList.remove('on'); uImgs[i].classList.add('on'); chips.querySelectorAll('.chip').forEach(c=>c.setAttribute('aria-pressed','false'));
    b.setAttribute('aria-pressed','true'); ucur=i; $('uShade').textContent=full(s); $('uCap').textContent="Shown in "+full(s); };
  li.appendChild(b); chips.appendChild(li);});
let bag=0; const toast=$('toast'); let tt;
$('addBtn').onclick=()=>{ bag++; const c=$('count'); c.textContent=bag; c.classList.add('bump'); setTimeout(()=>c.classList.remove('bump'),300);
  toast.textContent="Added to bag: Body Wave Lace Wig, "+full(SH[ucur]); toast.classList.add('show'); clearTimeout(tt); tt=setTimeout(()=>toast.classList.remove('show'),2600); };

/* newsletter */
$('joinForm').addEventListener('submit',e=>{e.preventDefault(); const v=$('email').value.trim();
  $('msg').textContent=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)?"You're on the list. We'll email you on launch day.":"Enter an email address like name@example.com.";});

/* scroll-driven scenes */
const hdr=$('hdr'), theater=$('shades'), reel=$('lookbook'), track=$('track'), heb=$('heb'), story=$('story'), storyImg=$('storyImg');
const wide=()=>innerWidth>720 && !reduce;
function sizeReel(){ if(wide()){ reel.style.height=(track.scrollWidth-innerWidth+innerHeight)+'px'; } else { reel.style.height=''; track.style.transform=''; } }
function frame(){
  const y=scrollY, vh=innerHeight;
  hdr.classList.toggle('solid', y>vh*.6);
  const tr=theater.getBoundingClientRect(), tt=theater.offsetHeight-vh;
  const p=Math.min(1,Math.max(0,-tr.top/tt));
  $('thBar').style.width=(p*100)+'%';
  setShade(Math.min(SH.length-1,Math.floor(p*SH.length)));
  if(wide()){ const rr=reel.getBoundingClientRect(), rt=reel.offsetHeight-vh; const q=Math.min(1,Math.max(0,-rr.top/rt));
    track.style.transform='translate3d('+(-q*(track.scrollWidth-innerWidth))+'px,0,0)'; }
  if(!reduce){ const sr=story.getBoundingClientRect(); const s=(vh-sr.top)/(vh+sr.height);
    heb.style.transform='translate3d('+(10-s*40)+'vw,-50%,0)'; }
  if(storyImg.getBoundingClientRect().top<vh*.8) storyImg.classList.add('seen');
}
let ticking=false;
addEventListener('scroll',()=>{ if(!ticking){ ticking=true; requestAnimationFrame(()=>{frame(); ticking=false;}); } },{passive:true});
addEventListener('resize',()=>{sizeReel(); frame();});
addEventListener('load',()=>{sizeReel(); frame();});
sizeReel(); frame();

/* cursor ring */
if(matchMedia('(pointer:fine)').matches && !reduce){
  const cr=$('cursor'); let x=innerWidth/2,y=innerHeight/2,cx=x,cy=y;
  addEventListener('mousemove',e=>{x=e.clientX;y=e.clientY;cr.classList.add('on');},{passive:true});
  document.addEventListener('mouseleave',()=>cr.classList.remove('on'));
  document.addEventListener('mouseover',e=>cr.classList.toggle('big',!!e.target.closest('a,button,.shot,summary,input')));
  (function loop(){cx+=(x-cx)*.18; cy+=(y-cy)*.18; cr.style.transform='translate3d('+cx+'px,'+cy+'px,0)'; requestAnimationFrame(loop);})();
}
})();
