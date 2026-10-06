(()=>{
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const money=v=>'$'+Number(v).toFixed(2);
const FREE=(window.CHESED&&window.CHESED.freeShip)||200;
const LANDC=["jawline","chin","shoulders","collarbone","armpits","bust","below the bust","mid ribs","waist","below the waist","hips","top of the thighs"];
const LAND=["chin","shoulders","collarbone","armpits","bust","below the bust","mid ribs","waist","below the waist","hips","top of the thighs","upper thighs"];
const LENS=[10,12,14,16,18,20,22,24,26,28,30,32];

const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const root=document.documentElement;

/* smooth scrolling */
let lenis=null, mqStep=null;
if(!reduce && window.Lenis){ lenis=new Lenis({lerp:0.085,wheelMultiplier:0.9,smoothWheel:true});
  const raf=t=>{ lenis.raf(t); mqStep&&mqStep(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf);
  document.addEventListener('click',e=>{ const a=e.target.closest('a[href^="#"]'); if(!a)return; const id=a.getAttribute('href'); if(id.length<2)return;
    const el=document.querySelector(id); if(el){ e.preventDefault(); lenis.scrollTo(el,{offset:-60,duration:1.4}); } }); }

/* intro reveal once the page has painted */
const markLoaded=()=>requestAnimationFrame(()=>setTimeout(()=>root.classList.add('loaded'),60));
if(document.readyState==='complete') markLoaded(); else addEventListener('load',markLoaded);
setTimeout(()=>root.classList.add('loaded'),2200);

/* header: solid once you scroll past the banner; expose its height for sticky bars */
const hdr=$('#hdr');
const setH=()=>{ if(hdr) root.style.setProperty('--hdr-h',hdr.offsetHeight+'px'); };
setH(); addEventListener('resize',setH);
const onScroll=()=>{ if(hdr) hdr.classList.toggle('solid',scrollY>60); };
addEventListener('scroll',onScroll,{passive:true}); onScroll();

/* split headings into words for the staggered reveal */
$$('[data-split]').forEach(el=>{ let i=0; const walk=n=>{ [...n.childNodes].forEach(c=>{
    if(c.nodeType===3){ const frag=document.createDocumentFragment();
      c.textContent.split(/(\s+)/).forEach(t=>{ if(!t) return; if(/^\s+$/.test(t)){ frag.appendChild(document.createTextNode(t)); return; }
        const w=document.createElement('span'); w.className='w'; const inner=document.createElement('span'); inner.textContent=t; inner.style.setProperty('--i',i++); w.appendChild(inner); frag.appendChild(w); });
      c.replaceWith(frag); }
    else if(c.nodeType===1 && c.tagName!=='BR') walk(c); }); }; walk(el); el.setAttribute('aria-label',el.textContent.replace(/\s+/g,' ').trim()); });

/* split wordmarks into letters */
$$('[data-chars]').forEach(el=>{ const t=el.textContent; el.textContent=''; [...t].forEach((c,i)=>{ const s=document.createElement('span'); s.className='ch'; s.textContent=c; s.style.setProperty('--i',i); el.appendChild(s); }); });

/* stagger cards that enter together */
$$('.grid,.rail,.tex-grid').forEach(g=>[...g.children].forEach((c,i)=>{ const t=c.matches('[data-reveal]')?c:c.querySelector('[data-reveal]'); if(t) t.style.setProperty('--d',(i%4)*90+'ms'); }));

/* reveal on scroll: fades, word splits, image wipes, letters */
const revealSel='[data-reveal],[data-split],[data-wipe],[data-chars]';
if('IntersectionObserver' in window){ const io=new IntersectionObserver(es=>es.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }),{rootMargin:'0px 0px -10% 0px'});
  $$(revealSel).forEach(el=>io.observe(el)); } else $$(revealSel).forEach(el=>el.classList.add('in'));
const desktop=()=>innerWidth>900 && !reduce;
const clamp01=v=>Math.max(0,Math.min(1,v));
const hdrH=()=>hdr?hdr.offsetHeight:0;
const progress=el=>{ const vis=innerHeight-hdrH(), r=el.getBoundingClientRect(), span=el.offsetHeight-vis; return span>0?clamp01((hdrH()-r.top)/span):0; };
const scrollers=[];
const tick=()=>{ scrollers.forEach(f=>f()); };
if(lenis) lenis.on('scroll',tick); else addEventListener('scroll',()=>requestAnimationFrame(tick),{passive:true});
addEventListener('resize',()=>requestAnimationFrame(tick));

/* strand chart: highlight a length, pick one by click or keyboard */
function strandChart(svg,onPick){ if(!svg) return null; const gs=[...svg.querySelectorAll('.st')], gds=[...svg.querySelectorAll('.gd')];
  if(onPick) gs.forEach(g=>{ if(g.dataset.i==null) return; const go=()=>onPick(+g.dataset.i);
    g.addEventListener('click',go); g.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); go(); } }); });
  return { set(i,curly){ svg.classList.toggle('curly',!!curly); gs.forEach((g,k)=>{ g.classList.toggle('sel',k===i); if(g.dataset.i!=null) g.setAttribute('aria-pressed',k===i?'true':'false'); });
    const k=curly?i-1:i; gds.forEach((g,j)=>g.classList.toggle('on',j===k)); } }; }

/* overlays: mobile menu + cart */
function openLayer(el,btn){ el.hidden=false; document.body.style.overflow='hidden'; lenis&&lenis.stop(); if(btn) btn.setAttribute('aria-expanded','true');
  const f=el.querySelector('button,a'); f&&f.focus(); }
function closeLayer(el){ el.hidden=true; document.body.style.overflow=''; lenis&&lenis.start(); const b=$('#menuBtn'); b&&b.setAttribute('aria-expanded','false'); }
const drawer=$('#drawer'), cartEl=$('#cart');
$('#menuBtn')&&$('#menuBtn').addEventListener('click',e=>openLayer(drawer,e.currentTarget));
[drawer,cartEl].forEach(el=>el&&el.addEventListener('click',e=>{ if(e.target.closest('[data-close]')) closeLayer(el); }));
addEventListener('keydown',e=>{ if(e.key==='Escape'){ [drawer,cartEl].forEach(el=>el&&!el.hidden&&closeLayer(el)); } });

/* cart (preview: kept in this browser tab only) */
let cart=[]; try{ cart=JSON.parse(sessionStorage.getItem('chesedCart')||'[]'); }catch(e){}
const save=()=>{ try{ sessionStorage.setItem('chesedCart',JSON.stringify(cart)); }catch(e){} };
function renderCart(){
  const n=cart.reduce((a,i)=>a+i.qty,0), tot=cart.reduce((a,i)=>a+i.qty*i.price,0);
  const c=$('#count'); if(c){ c.hidden=!n; c.textContent=n; }
  const list=$('#cartItems'); if(!list) return;
  list.innerHTML=cart.map((i,k)=>`<li>${i.img?`<img src="${i.img}" alt="">`:'<span></span>'}<div><b>${i.title}</b><small>${i.variant?i.variant+' · ':''}${money(i.price)}${i.qty>1?' × '+i.qty:''}</small></div><button class="rm" type="button" data-rm="${k}">Remove</button></li>`).join('');
  $('#cartEmpty').hidden=!!cart.length;
  $('#cartTotal').textContent=money(tot);
  $('#cartBnpl').textContent=tot?`or 4 interest-free payments of ${money(tot/4)} with Shop Pay`:'';
  const left=FREE-tot; $('#shipMsg').textContent=tot===0?`Free US shipping over $${FREE}`:left>0?`You're ${money(left)} away from free shipping`:`You've unlocked free US shipping`;
  $('#shipFill').style.width=Math.min(100,tot/FREE*100)+'%';
}
function addToCart(item){
  const ex=cart.find(i=>i.title===item.title&&i.variant===item.variant); if(ex) ex.qty++; else cart.push({...item,qty:1});
  save(); renderCart(); const c=$('#count'); if(c){ c.classList.remove('bump'); void c.offsetWidth; c.classList.add('bump'); }
  openLayer(cartEl);
}
$('#bagBtn')&&$('#bagBtn').addEventListener('click',()=>{ renderCart(); openLayer(cartEl); });
$('#cartItems')&&$('#cartItems').addEventListener('click',e=>{ const b=e.target.closest('[data-rm]'); if(b){ cart.splice(+b.dataset.rm,1); save(); renderCart(); } });
$$('[data-addon]').forEach(b=>b.addEventListener('click',()=>{ addToCart({title:b.dataset.addon,variant:'',price:+b.dataset.price,img:''}); }));
const toast=$('#toast'); let tt;
function say(t){ if(!toast)return; toast.textContent=t; toast.classList.add('show'); clearTimeout(tt); tt=setTimeout(()=>toast.classList.remove('show'),2600); }
$('#checkoutBtn')&&$('#checkoutBtn').addEventListener('click',()=>say('Preview only: checkout connects on Shopify.'));
renderCart();

/* email signup (preview: nothing is stored) */
$$('[data-join]').forEach(f=>f.addEventListener('submit',e=>{ e.preventDefault(); const v=f.querySelector('input').value.trim(), m=f.querySelector('.msg');
  m.textContent=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)?"You're on the list. (Preview: no email is saved.)":"Enter an email address like name@example.com."; }));

/* phones: crop the label column off the strand charts so the strands get the full width */
const cropCharts=()=>$$('.lenviz .strands,.every-len .strands').forEach(svg=>svg.setAttribute('viewBox',innerWidth<=720?'140 0 500 340':'0 0 640 340'));
cropCharts(); addEventListener('resize',cropCharts);

/* home: shade theater (scroll-driven on desktop, tap on phones) */
const theater=$('[data-theater]'), stage=$('#thStage');
if(theater&&stage){ const imgs=[...stage.querySelectorAll('img')], btns=$$('.th-sw button'), nm=$('#thName'), bl=$('#thBlurb'); let cur=0;
  const n=btns.length, pad=v=>String(v).padStart(2,'0');
  function setShade(i){ if(i===cur) return; const b=btns[i]; stage.dataset.dir=i>cur?'f':'b'; const old=cur; cur=i;
    imgs.forEach((im,k)=>{ im.classList.toggle('prev',k===old); im.classList.toggle('on',k===i); if(k===i) im.loading='eager'; });
    btns.forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
    $('#thIdx').textContent=pad(i+1)+' / '+pad(n);
    nm.classList.add('out'); bl.classList.add('fade');
    setTimeout(()=>{ nm.textContent=b.dataset.name; bl.textContent=b.dataset.blurb; nm.classList.remove('out'); nm.classList.add('in'); void nm.offsetWidth; nm.classList.remove('in'); bl.classList.remove('fade'); }, reduce?0:320);
    const col=$('#thCol'); col.href=b.dataset.col; col.textContent='Shop '+b.dataset.colname; $('#thProd').href=b.dataset.prod; }
  btns.forEach((b,i)=>b.addEventListener('click',()=>{ if(desktop()&&lenis){ const span=theater.offsetHeight-(innerHeight-hdrH()); lenis.scrollTo(theater.offsetTop-hdrH()+span*(i+.5)/n,{duration:1.2}); } else setShade(i); }));
  scrollers.push(()=>{ if(!desktop()) return; const p=progress(theater); $('#thBar').style.width=(p*100)+'%'; setShade(Math.min(n-1,Math.floor(p*n))); });
  imgs.slice(1,3).forEach(im=>im.loading='eager'); }

/* home: lookbook moves sideways while you scroll down (desktop) */
const hs=$('[data-hscroll]'), track=$('#lookTrack');
if(hs&&track){ const size=()=>{ if(desktop()){ hs.style.height=(track.scrollWidth-innerWidth+innerHeight-hdrH())+'px'; } else { hs.style.height=''; track.style.transform=''; } };
  size(); addEventListener('load',size); addEventListener('resize',size);
  scrollers.push(()=>{ if(!desktop()) return; track.style.transform='translate3d('+(-progress(hs)*(track.scrollWidth-innerWidth))+'px,0,0)'; }); }

/* home: layered hero parallax */
const hero=$('.hero');
if(hero&&!reduce){ const panes=[...hero.querySelectorAll('[data-par]')], copy=$('#heroCopy');
  scrollers.push(()=>{ const y=scrollY, h=hero.offsetHeight; if(y>h) return; const q=y/h;
    panes.forEach(p=>p.style.transform='translate3d(0,'+(y*parseFloat(p.dataset.par))+'px,0)');
    if(copy){ copy.style.transform='translate3d(0,'+(-y*0.18)+'px,0)'; copy.style.opacity=String(1-q*1.4); } }); }

/* home: length visualizer */
const range=$('#lenRange');
if(range){ let curly=0; const chart=strandChart($('.lenviz .strands'),i=>{ range.value=i; upd(); });
  const upd=()=>{ const i=+range.value, L=curly?LANDC:LAND; chart&&chart.set(i,curly);
    $('#lvVal').textContent=LENS[i]+'"'; $('#lvLand').textContent=L[i];
    range.setAttribute('aria-valuetext',LENS[i]+' inches, ends at your '+L[i]); };
  range.addEventListener('input',upd);
  $$('.lenviz .seg button').forEach(b=>b.addEventListener('click',()=>{ curly=+b.dataset.curly; $$('.lenviz .seg button').forEach(x=>x.setAttribute('aria-checked',x===b?'true':'false')); upd(); }));
  upd(); }

/* length guide: straight / curly toggle */
$$('.lg-seg button').forEach(b=>b.addEventListener('click',()=>{ $$('.lg-seg button').forEach(x=>x.setAttribute('aria-checked',x===b?'true':'false'));
  const svg=$('.lg-chart .strands'); if(svg) svg.classList.toggle('curly',b.dataset.curly==='1'); }));

/* collection: filter + sort */
const grid=$('#colGrid');
if(grid){ const key=grid.dataset.key, cards=[...grid.querySelectorAll('.card')], chips=$$('.fchip');
  chips.forEach(ch=>ch.addEventListener('click',()=>{ chips.forEach(x=>x.setAttribute('aria-pressed',x===ch?'true':'false'));
    const f=ch.dataset.filter; let shown=0; cards.forEach(c=>{ const ok=f==='all'||c.dataset[key]===f; c.hidden=!ok; if(ok)shown++; });
    $('#noMatch').hidden=!!shown; }));
  $('#sort')&&$('#sort').addEventListener('change',e=>{ const v=e.target.value; const s=[...cards];
    if(v==='az') s.sort((a,b)=>a.dataset.name.localeCompare(b.dataset.name));
    if(v==='price') s.sort((a,b)=>a.dataset.price-b.dataset.price);
    s.forEach(c=>grid.appendChild(c)); }); }

/* product page */
const pdp=$('[data-product]');
if(pdp){
  const gg=$('#gGrid'), dots=$$('.g-dots i');
  if(gg&&dots.length) gg.addEventListener('scroll',()=>{ const i=Math.round(gg.scrollLeft/gg.clientWidth); dots.forEach((d,k)=>d.classList.toggle('on',k===i)); },{passive:true});
  const curly=pdp.dataset.curly==='1', LM=JSON.parse($('#landmarks').textContent);
  const lenBtns=$$('.len-row button'), meter=$('#lenMeter');
  const chart=strandChart($('.every-len .strands'),i=>setLen(LENS[i],true));
  let len=16;
  function setLen(l,push){ len=l; const i=LENS.indexOf(l);
    lenBtns.forEach(b=>b.setAttribute('aria-checked',+b.dataset.len===l?'true':'false'));
    $('#lenVal').textContent=l+'"'; $('#stickyLen').textContent=l+'"';
    $('#lenLand').innerHTML=l+'" ends at your <b>'+LM[i]+'</b>.'+(curly?' Waves and curls sit about 2 inches higher than straight hair.':'');
    if(meter) meter.style.setProperty('--p',i/11);
    $$('.el-val').forEach(e=>e.textContent=l+'"'); $$('.el-land').forEach(e=>e.textContent=LM[i]);
    chart&&chart.set(i,curly);
    if(push){ const u=new URL(location); u.searchParams.set('length',l); history.replaceState(null,'',u); } }
  lenBtns.forEach(b=>b.addEventListener('click',()=>setLen(+b.dataset.len,true)));
  const q=+new URL(location).searchParams.get('length'); setLen(LENS.includes(q)?q:16,false);
  const add=()=>addToCart({title:pdp.dataset.title,variant:len+'"',price:+pdp.dataset.price,img:pdp.dataset.img});
  $('#addBtn').addEventListener('click',add); $('#stickyAdd').addEventListener('click',add); $('#elAdd')&&$('#elAdd').addEventListener('click',add);
  $$('.buy .shop-pay').forEach(b=>b.addEventListener('click',()=>say('Preview only: Shop Pay connects on Shopify.')));
  /* sticky add-to-bag once the main button scrolls away (mobile) */
  const sb=$('#stickyBuy');
  if('IntersectionObserver' in window){ new IntersectionObserver(([e])=>{ const show=!e.isIntersecting&&e.boundingClientRect.top<0;
    sb.classList.toggle('show',show); sb.setAttribute('aria-hidden',show?'false':'true'); $('#stickyAdd').tabIndex=show?0:-1; }).observe($('#addBtn')); }
}

/* carousels: reviews + shade rails */
$$('[data-rv-track]').forEach(tr=>{ const sec=tr.closest('section'); const btns=sec?[...sec.querySelectorAll('[data-rv]')]:[];
  const step=()=>{ const it=tr.children[0]; return it?it.getBoundingClientRect().width+parseFloat(getComputedStyle(tr).columnGap||0):tr.clientWidth; };
  const state=()=>{ const max=tr.scrollWidth-tr.clientWidth-2; btns.forEach(b=>b.disabled=+b.dataset.rv<0?tr.scrollLeft<=2:tr.scrollLeft>=max); };
  btns.forEach(b=>b.addEventListener('click',()=>tr.scrollBy({left:step()*+b.dataset.rv,behavior:reduce?'auto':'smooth'})));
  tr.addEventListener('scroll',()=>requestAnimationFrame(state),{passive:true}); addEventListener('resize',state); state(); });

/* scroll-linked motion: outline type drifts sideways, inset photos float */
const through=el=>{ const r=el.getBoundingClientRect(); return clamp01((innerHeight-r.top)/(innerHeight+r.height)); };
if(!reduce){
  $$('[data-drift]').forEach(el=>{ const sec=el.parentElement; scrollers.push(()=>{ const p=through(sec); if(p<=0||p>=1) return; el.style.transform='translate3d('+(-p*28)+'%,0,0)'; }); });
  $$('[data-speed]').forEach(el=>{ const k=parseFloat(el.dataset.speed); scrollers.push(()=>{ if(!desktop()) { el.style.transform=''; return; } const r=el.getBoundingClientRect(); const c=r.top+r.height/2-innerHeight/2; el.style.transform='translate3d(0,'+(c*k)+'px,0)'; }); });
}

/* marquee: speeds up and leans with scroll velocity */
const mq=$('.marquee'), mqt=$('.mq-track');
if(mq&&mqt&&lenis){ mq.classList.add('mq-js'); let x=0, last=0, skew=0, vis=true;
  new IntersectionObserver(([e])=>{ vis=e.isIntersecting; }).observe(mq);
  mqStep=t=>{ const dt=last?Math.min(64,t-last):16; last=t; if(!vis) return; const v=lenis.velocity||0;
    x-=(0.045+Math.min(1.2,Math.abs(v)*0.02))*dt; const half=mqt.scrollWidth/2; if(half&&-x>=half) x+=half;
    skew+=((Math.max(-8,Math.min(8,v*-0.35)))-skew)*0.12; mqt.style.transform='translate3d('+x+'px,0,0) skewX('+skew.toFixed(2)+'deg)'; }; }

/* shared-image page transition: the clicked product photo flies into the product page */
if(CSS.supports&&CSS.supports('view-transition-name','a')){
  document.addEventListener('click',e=>{ const a=e.target.closest('.card-link'); if(!a) return; $$('[style*="view-transition-name"]').forEach(x=>x.style.viewTransitionName='');
    const im=a.querySelector('.card-img img'); if(im) im.style.viewTransitionName='pdp-hero'; }); }

/* custom cursor + magnetic buttons (mouse only) */
if(matchMedia('(hover:hover) and (pointer:fine)').matches && !reduce){
  const cur=document.createElement('div'); cur.className='cursor'; cur.innerHTML='<b></b>'; cur.setAttribute('aria-hidden','true'); document.body.appendChild(cur);
  let x=-100,y=-100,cx=x,cy=y; addEventListener('mousemove',e=>{ x=e.clientX; y=e.clientY; cur.classList.add('on'); },{passive:true});
  document.addEventListener('mouseleave',()=>cur.classList.remove('on'));
  document.addEventListener('mouseover',e=>{ const t=e.target.closest('[data-cursor]'); cur.classList.toggle('big',!!t); if(t) cur.querySelector('b').textContent=t.dataset.cursor; });
  (function loop(){ cx+=(x-cx)*.2; cy+=(y-cy)*.2; cur.style.transform='translate3d('+cx+'px,'+cy+'px,0)'; requestAnimationFrame(loop); })();
  $$('.btn:not(.wide):not(.shop-pay)').forEach(b=>{ if(b.closest('form')) return; b.classList.add('mag');
    b.addEventListener('mousemove',e=>{ const r=b.getBoundingClientRect(); b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.22)+'px,'+((e.clientY-r.top-r.height/2)*.35)+'px)'; });
    b.addEventListener('mouseleave',()=>{ b.style.transform=''; }); });
}
tick();
})();
