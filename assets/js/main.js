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
    const el=document.querySelector(id); if(el){ e.preventDefault(); lenis.scrollTo(el,{offset:-((document.querySelector('.hdr')||{}).offsetHeight||60)-24,duration:1.4}); } }); }

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

/* simple menu: hovering or focusing a texture shows its wigs */
$$('[data-sm-tabs] a').forEach(a=>{ const show=()=>{ const panel=a.closest('.dd-panel');
  panel.querySelectorAll('[data-sm-tabs] a').forEach(x=>x.classList.toggle('on',x===a));
  panel.querySelectorAll('[data-sm-pane]').forEach(p=>p.classList.toggle('on',p.dataset.smPane===a.dataset.sm)); };
  a.addEventListener('mouseenter',show); a.addEventListener('focus',show); });

/* overlays: mobile menu + cart */
function openLayer(el,btn){ clearTimeout(el._ct); el.classList.remove('closing'); el.hidden=false; document.body.style.overflow='hidden'; lenis&&lenis.stop(); if(btn) btn.setAttribute('aria-expanded','true');
  const f=el.querySelector('button,a'); f&&f.focus(); }
function closeLayer(el){ if(el.hidden||el.classList.contains('closing')) return;
  const done=()=>{ el.hidden=true; el.classList.remove('closing'); };
  if(reduce) done(); else { el.classList.add('closing'); el._ct=setTimeout(done,380); }
  document.body.style.overflow=''; lenis&&lenis.start(); const b=$('#menuBtn'); b&&b.setAttribute('aria-expanded','false'); }
const drawer=$('#drawer'), cartEl=$('#cart');
$('#menuBtn')&&$('#menuBtn').addEventListener('click',e=>openLayer(drawer,e.currentTarget));
[drawer,cartEl].forEach(el=>el&&el.addEventListener('click',e=>{ if(e.target.closest('[data-close]')) closeLayer(el); }));
addEventListener('keydown',e=>{ if(e.key==='Escape'){ [drawer,cartEl,$('#srch')].forEach(el=>el&&!el.hidden&&closeLayer(el)); } });

/* small localStorage helpers: per-browser conveniences only, safe when storage is blocked */
const store={ get(k){ try{ return JSON.parse(localStorage.getItem(k)); }catch(e){ return null; } }, set(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} } };
const prize=()=>store.get('chesedPrize');
const discOf=(p,tot)=>!p||!tot?0:p.pct?tot*p.pct/100:Math.min(p.amt,tot);

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
  const pz=prize(), d=discOf(pz,tot), dl=$('#cartDisc');
  if(dl){ dl.hidden=!d; if(d){ $('#cartDiscLabel').textContent=`${pz.code} · ${pz.label} (applied at checkout)`; $('#cartDiscAmt').textContent='−'+money(d); } }
  $('#cartBnpl').textContent=tot?`or 4 interest-free payments of ${money((tot-d)/4)} with Shop Pay`:'';
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

/* product cards: quick add with a length picker */
document.addEventListener('click',e=>{ const q=e.target.closest('[data-quick]');
  if(q){ const lens=q.closest('.card').querySelector('[data-quick-lens]'); const open=lens.hidden; lens.hidden=!open; q.setAttribute('aria-expanded',open?'true':'false'); q.textContent=open?'Pick a length':'Quick add'; if(open) lens.querySelector('button').focus(); return; }
  const b=e.target.closest('[data-quick-lens] button'); if(!b) return; const g=b.parentElement;
  addToCart({title:g.dataset.title,variant:b.dataset.len+'"',price:+g.dataset.price,img:g.dataset.img});
  g.hidden=true; const qb=g.closest('.card').querySelector('[data-quick]'); qb.setAttribute('aria-expanded','false'); qb.textContent='Quick add'; });

/* product page: show what a won code saves on this wig */
function codeNotes(){ const pz=prize(); $$('[data-code-note]').forEach(n=>{ const pr=+(n.closest('[data-product]')||{}).dataset?.price||0; const d=discOf(pz,pr);
  n.hidden=!d; if(d) n.innerHTML=`Your code <b>${pz.code}</b> takes ${pz.label}: <b>${money(pr-d)}</b> at checkout.`; }); }
codeNotes();

/* search overlay: instant results from a small index of every page */
const srch=$('#srch'), sIn=$('#srchIn'), sList=$('#srchList');
if(srch&&sIn){ let idx=null, sel=-1;
  const load=()=>idx?Promise.resolve(idx):fetch('/assets/search.json').then(r=>r.json()).then(d=>idx=d).catch(()=>idx=[]);
  const norm=v=>v.toLowerCase().replace(/["”“]/g,'').replace(/\s+/g,' ').trim();
  const esc=v=>v.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function run(){ const q=norm(sIn.value); $('#srchPop').hidden=!!q; sel=-1;
    if(!q){ sList.innerHTML=''; $('#srchNone').hidden=true; return; }
    load().then(d=>{ const words=q.split(' ');
      const hits=d.map(e=>{ const hay=norm(e.t+' '+e.k+' '+(e.s||'')); if(!words.every(w=>hay.includes(w))) return null;
        return {e,score:(norm(e.t).startsWith(q)?3:0)+(norm(e.t).includes(q)?2:0)+(e.k==='Wig'?0:1)}; }).filter(Boolean).sort((a,b)=>b.score-a.score).slice(0,24);
      sList.innerHTML=hits.map(({e})=>`<li><a href="${e.u}">${e.i?`<img src="${e.i}" alt="" loading="lazy">`:'<span class="srch-ic"></span>'}<span><b>${esc(e.t)}</b><small>${e.k}${e.p?' · '+money(e.p):''}</small></span></a></li>`).join('');
      $('#srchNone').hidden=!!hits.length; }); }
  const open=()=>{ openLayer(srch); sIn.focus(); load(); };
  $$('[data-search]').forEach(b=>b.addEventListener('click',open));
  addEventListener('keydown',e=>{ if(e.key==='/'&&srch.hidden&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){ e.preventDefault(); open(); } });
  srch.addEventListener('click',e=>{ if(e.target.closest('[data-close]')) closeLayer(srch); const c=e.target.closest('[data-q]'); if(c){ sIn.value=c.dataset.q; run(); sIn.focus(); } });
  sIn.addEventListener('input',run);
  sIn.addEventListener('keydown',e=>{ const links=[...sList.querySelectorAll('a')]; if(!links.length) return;
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){ e.preventDefault(); sel=(sel+(e.key==='ArrowDown'?1:-1)+links.length)%links.length; links.forEach((a,k)=>a.classList.toggle('on',k===sel)); links[sel].scrollIntoView({block:'nearest'}); } });
  $('#srchForm').addEventListener('submit',e=>{ e.preventDefault(); const links=[...sList.querySelectorAll('a')]; const a=links[Math.max(0,sel)]; if(a) location.href=a.href; }); }

/* welcome wheel: email popup where every spin wins (odds shown in the fine print) */
const spin=$('#spin'), tab=$('#spinTab');
if(spin){ const prizes=JSON.parse(spin.dataset.prizes), g=$('#wheelSpin'), DAY=864e5;
  const shown=()=>{ try{ return sessionStorage.getItem('chesedSpinShown'); }catch(e){ return '1'; } };
  const markShown=()=>{ try{ sessionStorage.setItem('chesedSpinShown','1'); }catch(e){} };
  const snoozed=()=>{ const t=store.get('chesedSpinSnooze'); return t&&Date.now()-t<7*DAY; };
  let spun=false;
  function openSpin(){ if(!spin.hidden) return; markShown(); tab.hidden=true; if(prize()) showWin(prize(),false); openLayer(spin); setTimeout(()=>$('#spinEmail')&&!prize()&&$('#spinEmail').focus(),50); }
  function closeSpin(){ closeLayer(spin); if(!prize()){ store.set('chesedSpinSnooze',Date.now()); tab.hidden=false; } }
  function showWin(p,anim){ $('#spinStep1').hidden=true; $('#spinStep2').hidden=false; $('#spinWon').textContent=p.label+' your first order';
    $('#spinCode').textContent=p.code; if(!anim) $('#spinWon').focus(); }
  spin.addEventListener('click',e=>{ if(e.target.closest('[data-spin-close]')){ closeSpin(); if(e.target.closest('[data-spin-shop]')&&!/\/(products|collections)\//.test(location.pathname)) location.href='/collections/wigs/'; } });
  addEventListener('keydown',e=>{ if(e.key==='Escape'&&!spin.hidden) closeSpin(); });
  tab.addEventListener('click',openSpin);
  $('#spinCopy').addEventListener('click',()=>{ const c=$('#spinCode').textContent; (navigator.clipboard?navigator.clipboard.writeText(c):Promise.reject()).then(()=>say('Code copied: '+c)).catch(()=>say('Your code: '+c)); });
  $('#spinForm').addEventListener('submit',e=>{ e.preventDefault(); if(spun) return; const v=$('#spinEmail').value.trim();
    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)){ $('#spinMsg').textContent='Enter an email address like name@example.com.'; return; }
    $('#spinMsg').textContent=''; spun=true;
    let r=Math.random()*100, i=0; for(;i<prizes.length-1;i++){ r-=prizes[i].weight; if(r<0) break; }
    const n=prizes.length, slice=360/n, jitter=(Math.random()-.5)*slice*.6, deg=360*6-(i+.5)*slice+jitter;
    const win=prizes[i]; store.set('chesedPrize',win); store.set('chesedSpinSnooze',null);
    const done=()=>{ showWin(win,true); setTimeout(()=>$('#spinWon').focus(),30); renderCart(); codeNotes(); };
    if(reduce||!g.animate){ g.style.transform=`rotate(${deg}deg)`; done(); return; }
    g.animate([{transform:'rotate(0deg)'},{transform:`rotate(${deg}deg)`}],{duration:4800,easing:'cubic-bezier(.12,.75,.1,1)',fill:'forwards'}).finished.then(done); });
  /* when to show it: after 12s, or desktop exit intent; once per visit; quiet for a week after "no thanks" */
  if(prize()||snoozed()){ if(!prize()) tab.hidden=false; }
  else if(!shown()){ const t=setTimeout(()=>{ if(cartEl.hidden&&drawer.hidden&&(!srch||srch.hidden)) openSpin(); },12000);
    if(matchMedia('(hover:hover) and (pointer:fine)').matches) document.addEventListener('mouseout',function x(e){ if(!e.relatedTarget&&e.clientY<=0){ clearTimeout(t); document.removeEventListener('mouseout',x); if(!shown()) openSpin(); } }); }
}

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

/* home: pinned sections whose track moves sideways while you scroll down (desktop): textures + lookbook */
$$('[data-hscroll]').forEach(hs=>{ const track=hs.querySelector('[data-htrack]'); if(!track) return;
  const now=hs.querySelector('[data-hnow]'), bar=hs.querySelector('[data-hbar]'), n=track.children.length;
  const dist=()=>Math.max(0,track.scrollWidth-track.parentElement.clientWidth);
  const size=()=>{ if(desktop()){ hs.style.height=(dist()+innerHeight-hdrH())+'px'; } else { hs.style.height=''; track.style.transform=''; } };
  size(); addEventListener('load',size); addEventListener('resize',size);
  scrollers.push(()=>{ if(!desktop()) return; const p=progress(hs); track.style.transform='translate3d('+(-p*dist())+'px,0,0)';
    if(now) now.textContent=String(Math.min(n,1+Math.round(p*(n-1)))).padStart(2,'0');
    if(bar) bar.style.transform='scaleX('+Math.max(1/n,p)+')'; }); });

/* home: shade panels open on hover or focus (tap scrolls on phones) */
$$('[data-sx]').forEach(row=>{ const items=[...row.children];
  items.forEach(li=>{ const open=()=>items.forEach(x=>x.classList.toggle('on',x===li)); li.addEventListener('mouseenter',open); li.querySelector('a').addEventListener('focus',open); }); });

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

/* collection: dropdown filters (multi-select, AND across groups), pills, live count, sort */
const grid=$('#colGrid'), fb=$('[data-fbar]');
if(grid&&fb){ const cards=[...grid.querySelectorAll('.card')], groups=[...fb.querySelectorAll('[data-fgroup]')];
  const sel=()=>{ const o={}; groups.forEach(g=>o[g.dataset.fgroup]=[...g.querySelectorAll('input:checked')].map(i=>i.value)); return o; };
  const matches=(c,o)=>Object.entries(o).every(([k,v])=>!v.length||v.includes(c.dataset[k]));
  function setOpen(g,open){ groups.forEach(x=>{ const on=open&&x===g; x.classList.toggle('open',on); x.querySelector('.fbtn').setAttribute('aria-expanded',on?'true':'false'); });
    fb.classList.toggle('popped',!!open); document.body.classList.toggle('sheet-open',!!open&&innerWidth<=720); }
  function preview(){ const o=sel(), n=cards.filter(c=>matches(c,o)).length; $$('[data-fpop-count],.fpop [data-fcount]').forEach(e=>e.textContent=n); }
  function apply(){ const o=sel(); let n=0;
    cards.forEach(c=>{ const ok=matches(c,o); if(ok) n++;
      if(ok&&c.hidden){ c.hidden=false; c.classList.add('fout'); requestAnimationFrame(()=>requestAnimationFrame(()=>c.classList.remove('fout'))); }
      else if(!ok) c.hidden=true; });
    $$('.fcount [data-fcount]').forEach(e=>e.textContent=n); preview();
    $('#noMatch').hidden=!!n;
    const pills=fb.querySelector('[data-fpills]'); pills.innerHTML=''; let any=false;
    groups.forEach(g=>{ const ch=[...g.querySelectorAll('input:checked')], b=g.querySelector('.fbtn'), lab=b.querySelector('[data-flabel]');
      const base=g.querySelector('.fpop-h').textContent; lab.textContent=ch.length?base+' ('+ch.length+')':base; b.classList.toggle('has',!!ch.length);
      ch.forEach(i=>{ any=true; const li=document.createElement('li'), x=document.createElement('button'); x.type='button'; x.textContent=i.dataset.fname; x.setAttribute('aria-label','Remove '+i.dataset.fname);
        x.addEventListener('click',()=>{ i.checked=false; apply(); }); li.appendChild(x); pills.appendChild(li); }); });
    fb.querySelector('[data-fclear]').hidden=!any;
    const u=new URL(location); Object.entries(o).forEach(([k,v])=>v.length?u.searchParams.set(k,v.join(',')):u.searchParams.delete(k)); history.replaceState(null,'',u); }
  groups.forEach(g=>{ g.querySelector('.fbtn').addEventListener('click',e=>{ e.stopPropagation(); setOpen(g,!g.classList.contains('open')); });
    g.querySelectorAll('input').forEach(i=>i.addEventListener('change',()=>{ apply(); }));
    g.querySelector('[data-fdone]').addEventListener('click',()=>setOpen(null,false));
    g.querySelector('[data-fclear-group]').addEventListener('click',()=>{ g.querySelectorAll('input').forEach(i=>i.checked=false); apply(); }); });
  $$('[data-fclear]').forEach(b=>b.addEventListener('click',()=>{ fb.querySelectorAll('input').forEach(i=>i.checked=false); apply(); }));
  fb.querySelector('[data-fscrim]').addEventListener('click',()=>setOpen(null,false));
  document.addEventListener('click',e=>{ if(!e.target.closest('.fgroup')) setOpen(null,false); });
  addEventListener('keydown',e=>{ if(e.key==='Escape') setOpen(null,false); });
  /* restore filters from the URL, e.g. ?color=red,ginger-350 */
  const u=new URL(location); groups.forEach(g=>{ const v=(u.searchParams.get(g.dataset.fgroup)||'').split(','); g.querySelectorAll('input').forEach(i=>i.checked=v.includes(i.value)); });
  apply();
  const sorter=$('#sort'); sorter&&sorter.addEventListener('change',e=>{ const v=e.target.value; const s=[...cards];
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

/* carousels: drag with the mouse (touch already scrolls natively), with a little momentum */
$$('[data-rv-track],[data-drag]').forEach(tr=>{ tr.setAttribute('data-drag',''); let down=false,moved=false,x0=0,s0=0,lx=0,lt=0,v=0,raf=0;
  tr.addEventListener('dragstart',e=>e.preventDefault());
  tr.addEventListener('pointerdown',e=>{ if(e.pointerType!=='mouse'||e.button!==0) return; down=true; moved=false; x0=lx=e.clientX; s0=tr.scrollLeft; lt=performance.now(); v=0; cancelAnimationFrame(raf); });
  addEventListener('pointermove',e=>{ if(!down) return; const dx=e.clientX-x0;
    if(!moved&&Math.abs(dx)>6){ moved=true; tr.classList.add('dragging'); }
    if(moved){ tr.scrollLeft=s0-dx; const t=performance.now(); v=(e.clientX-lx)/Math.max(1,t-lt); lx=e.clientX; lt=t; } });
  addEventListener('pointerup',()=>{ if(!down) return; down=false; if(!moved) return; let vel=-v*16;
    const glide=()=>{ vel*=0.93; tr.scrollLeft+=vel; if(Math.abs(vel)>0.6&&!reduce) raf=requestAnimationFrame(glide); else tr.classList.remove('dragging'); }; glide(); });
  tr.addEventListener('click',e=>{ if(moved){ e.preventDefault(); e.stopPropagation(); moved=false; } },true); });
$$('[data-rail-bar]').forEach(bar=>{ const tr=bar.closest('section').querySelector('[data-rv-track]'); if(!tr) return;
  const upd=()=>{ const max=tr.scrollWidth-tr.clientWidth, w=Math.max(.12,tr.clientWidth/tr.scrollWidth); bar.style.width=(w*100)+'%'; bar.style.transform='translateX('+(max>0?tr.scrollLeft/max*(1/w-1)*100:0)+'%)'; };
  tr.addEventListener('scroll',()=>requestAnimationFrame(upd),{passive:true}); addEventListener('resize',upd); upd(); });

/* accordions open and close smoothly (height animated, never a snap) */
$$('details').forEach(d=>{ const sm=d.querySelector(':scope>summary'); if(!sm) return; d.classList.add('anim'); let a=null, shutting=false;
  sm.addEventListener('click',e=>{ if(reduce||!d.animate) return; e.preventDefault(); const from=d.offsetHeight; if(a) a.cancel();
    const cs=getComputedStyle(d), pad=parseFloat(cs.paddingTop)+parseFloat(cs.paddingBottom)+parseFloat(cs.borderTopWidth)+parseFloat(cs.borderBottomWidth);
    if(!d.open||shutting){ shutting=false; d.classList.remove('shut'); d.open=true; const to=d.offsetHeight;
      a=d.animate({height:[from+'px',to+'px']},{duration:520,easing:'cubic-bezier(.16,1,.3,1)'}); a.onfinish=()=>{a=null;}; }
    else { shutting=true; d.classList.add('shut'); const to=sm.offsetHeight+pad;
      a=d.animate({height:[from+'px',to+'px']},{duration:420,easing:'cubic-bezier(.16,1,.3,1)'}); a.onfinish=()=>{ d.open=false; d.classList.remove('shut'); shutting=false; a=null; }; } }); });

/* home: texture spotlight shade switcher */
const spot=$('[data-spot]');
if(spot){ const imgs=[...spot.querySelectorAll('.spot-media img')], sws=[...spot.querySelectorAll('.spot-sw button')];
  const pick=b=>{ const i=+b.dataset.i; imgs.forEach((im,k)=>{ if(k===i) im.loading='eager'; im.classList.toggle('on',k===i); });
    sws.forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
    $('#spotName').textContent=$('#spotTag').textContent=b.dataset.name; $('#spotBuy').href=b.dataset.url; };
  sws.forEach(b=>{ b.addEventListener('click',()=>pick(b)); b.addEventListener('mouseenter',()=>{ imgs[+b.dataset.i].loading='eager'; }); }); }

/* product page: shade swatches show their name on hover, keep the chosen length, and prefetch */
const shadeName=$('#shadeName');
if(shadeName){ const cur=shadeName.textContent, seen=new Set();
  $$('.shade-sw a').forEach(a=>{ a.addEventListener('mouseenter',()=>{ shadeName.textContent=a.dataset.name;
      if(!seen.has(a.href)){ seen.add(a.href); const l=document.createElement('link'); l.rel='prefetch'; l.href=a.href; document.head.appendChild(l); } });
    a.addEventListener('mouseleave',()=>{ shadeName.textContent=cur; });
    a.addEventListener('click',e=>{ const len=new URL(location).searchParams.get('length'); if(len&&!a.classList.contains('on')){ e.preventDefault(); location.href=a.pathname+'?length='+len; } }); }); }

/* WhatsApp: number not set yet in the preview */
$$('[data-ph-wa]').forEach(a=>a.addEventListener('click',e=>{ e.preventDefault(); say('Preview: Chesed\'s WhatsApp number goes here.'); }));

/* long pages: highlight the section you're reading in the table of contents */
const tocLinks=$$('.toc a');
if(tocLinks.length&&'IntersectionObserver' in window){ const map=new Map(tocLinks.map(a=>[a.getAttribute('href').slice(1),a]));
  const io=new IntersectionObserver(es=>{ es.forEach(e=>{ if(e.isIntersecting){ tocLinks.forEach(a=>a.classList.toggle('on',a===map.get(e.target.id))); } }); },{rootMargin:'-30% 0px -60% 0px'});
  map.forEach((a,id)=>{ const h=document.getElementById(id); h&&io.observe(h); }); tocLinks[0].classList.add('on'); }

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

/* marquee: rows run in opposite directions, speed up and lean with scroll velocity */
const mq=$('.marquee'), rows=$$('.marquee .mq-track');
if(mq&&rows.length&&lenis){ mq.classList.add('mq-js'); let last=0, skew=0, vis=true;
  const st=rows.map(t=>({t,dir:+t.dataset.mq||-1,x:0,base:t.closest('.mq-small')?0.03:0.05}));
  st.forEach(r=>{ if(r.dir>0) r.x=-r.t.scrollWidth/2; });
  new IntersectionObserver(([e])=>{ vis=e.isIntersecting; }).observe(mq);
  mqStep=t=>{ const dt=last?Math.min(64,t-last):16; last=t; if(!vis) return; const v=lenis.velocity||0;
    skew+=((Math.max(-6,Math.min(6,v*-0.3)))-skew)*0.12;
    st.forEach(r=>{ const half=r.t.scrollWidth/2; r.x+=r.dir*(r.base+Math.min(1,Math.abs(v)*0.018))*dt;
      if(half){ if(-r.x>=half) r.x+=half; if(r.x>0) r.x-=half; }
      r.t.style.transform='translate3d('+r.x+'px,0,0) skewX('+(r.dir<0?skew:-skew).toFixed(2)+'deg)'; }); }; }

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
