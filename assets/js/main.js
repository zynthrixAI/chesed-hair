(()=>{
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const money=v=>'$'+Number(v).toFixed(2);
const FREE=(window.CHESED&&window.CHESED.freeShip)||200;
const FIG_Y=[62,84,92,110,126,140,154,170,186,202,220,238], FIG_YC=[54,62,84,92,110,126,140,154,170,186,202,220];
const LANDC=["jawline","chin","shoulders","collarbone","armpits","bust","below the bust","mid ribs","waist","below the waist","hips","top of the thighs"];
const LAND=["chin","shoulders","collarbone","armpits","bust","below the bust","mid ribs","waist","below the waist","hips","top of the thighs","upper thighs"];
const LENS=[10,12,14,16,18,20,22,24,26,28,30,32];

/* figure: move the clip + marker to a landmark index */
function setFig(svg,i,curly){ if(!svg)return; const y=(curly?FIG_YC:FIG_Y)[Math.max(0,Math.min(11,i))];
  const r=svg.querySelector('.fig-clip'); if(r) r.setAttribute('height',y);
  const m=svg.querySelector('.fig-mark'); if(m){ m.setAttribute('y1',y); m.setAttribute('y2',y); } }

/* overlays: mobile menu + cart */
function openLayer(el,btn){ el.hidden=false; document.body.style.overflow='hidden'; if(btn) btn.setAttribute('aria-expanded','true');
  const f=el.querySelector('button,a'); f&&f.focus(); }
function closeLayer(el){ el.hidden=true; document.body.style.overflow=''; const b=$('#menuBtn'); b&&b.setAttribute('aria-expanded','false'); }
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

/* home: shade theater */
const stage=$('#thStage');
if(stage){ const imgs=[...stage.querySelectorAll('img')], btns=$$('.th-sw button');
  btns.forEach(b=>b.addEventListener('click',()=>{ const i=+b.dataset.i;
    imgs.forEach((im,k)=>im.classList.toggle('on',k===i)); btns.forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));
    $('#thName').textContent=b.dataset.name; $('#thBlurb').textContent=b.dataset.blurb;
    const col=$('#thCol'); col.href=b.dataset.col; col.textContent='Shop '+b.dataset.colname; $('#thProd').href=b.dataset.prod; })); }

/* home: length visualizer */
const range=$('#lenRange');
if(range){ const svg=$('.lv-fig svg'); let curly=0;
  const upd=()=>{ const i=+range.value, L=curly?LANDC:LAND; setFig(svg,i,curly);
    $('#lvVal').textContent=LENS[i]+'"'; $('#lvLand').textContent='ends at your '+L[i];
    range.setAttribute('aria-valuetext',LENS[i]+' inches, ends at your '+L[i]); };
  range.addEventListener('input',upd);
  $$('.lenviz .seg button').forEach(b=>b.addEventListener('click',()=>{ curly=+b.dataset.curly; $$('.lenviz .seg button').forEach(x=>x.setAttribute('aria-checked',x===b?'true':'false')); upd(); }));
  upd(); }

/* length guide: straight / curly toggle */
$$('.lg-seg button').forEach(b=>b.addEventListener('click',()=>{ $$('.lg-seg button').forEach(x=>x.setAttribute('aria-checked',x===b?'true':'false'));
  $$('.lg-row').forEach(r=>r.hidden=r.dataset.kind!==b.dataset.show); }));

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
  const main=$('#gMain'), mimgs=[...main.querySelectorAll('img')], thumbs=$$('.g-thumbs button');
  thumbs.forEach(t=>t.addEventListener('click',()=>{ const i=+t.dataset.i; mimgs.forEach((im,k)=>im.classList.toggle('on',k===i)); thumbs.forEach(x=>x.setAttribute('aria-pressed',x===t?'true':'false')); }));
  const curly=pdp.dataset.curly==='1', LM=JSON.parse($('#landmarks').textContent);
  const lenBtns=$$('.len-row button'), elBtns=$$('.el-row button'), mini=$('.len-hint svg');
  let len=16;
  function setLen(l,push){ len=l; const i=LENS.indexOf(l);
    lenBtns.forEach(b=>b.setAttribute('aria-checked',+b.dataset.len===l?'true':'false'));
    elBtns.forEach(b=>b.classList.toggle('on',+b.dataset.len===l));
    $('#lenVal').textContent=l+'"'; $('#stickyLen').textContent=l+'"';
    $('#lenLand').innerHTML=l+'" ends at your <b>'+LM[i]+'</b>.'+(curly?' Waves and curls sit about 2 inches higher than straight hair.':'');
    setFig(mini,i,curly);
    if(push){ const u=new URL(location); u.searchParams.set('length',l); history.replaceState(null,'',u); } }
  lenBtns.forEach(b=>b.addEventListener('click',()=>setLen(+b.dataset.len,true)));
  elBtns.forEach(b=>b.addEventListener('click',()=>{ setLen(+b.dataset.len,true); $('#buy').scrollIntoView({behavior:'smooth',block:'start'}); }));
  const q=+new URL(location).searchParams.get('length'); setLen(LENS.includes(q)?q:16,false);
  const add=()=>addToCart({title:pdp.dataset.title,variant:len+'"',price:+pdp.dataset.price,img:pdp.dataset.img});
  $('#addBtn').addEventListener('click',add); $('#stickyAdd').addEventListener('click',add);
  $$('.buy .shop-pay').forEach(b=>b.addEventListener('click',()=>say('Preview only: Shop Pay connects on Shopify.')));
  /* sticky add-to-bag once the main button scrolls away (mobile) */
  const sb=$('#stickyBuy');
  if('IntersectionObserver' in window){ new IntersectionObserver(([e])=>{ const show=!e.isIntersecting&&e.boundingClientRect.top<0;
    sb.classList.toggle('show',show); sb.setAttribute('aria-hidden',show?'false':'true'); $('#stickyAdd').tabIndex=show?0:-1; }).observe($('#addBtn')); }
}
})();
