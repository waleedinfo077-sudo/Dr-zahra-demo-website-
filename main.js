const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)],D=window.SITE;
// headline: split into words that rise in
const h1=$('.hero h1');if(h1)h1.innerHTML=h1.textContent.split(' ').map((w,i)=>`<span><i style="animation-delay:${.7+i*.09}s">${w}</i></span>`).join(' ');
// renderers
const R={
treatments:(e)=>D.treatments.slice(0,+e.dataset.limit||99).map(t=>`<article class="card rv-up" ${e.hasAttribute('data-expand')?'data-x':''}><h3>${t[0]}</h3><p>${t[1]}</p><div class="more">${t[2]}</div></article>`).join(''),
products:(e)=>D.products.slice(0,+e.dataset.limit||99).map(p=>`<article class="card rv-up" data-t="${p[2]}"><span class="badge">${p[2]}</span><small>${p[1]}</small><h3>${p[0]}</h3><p>${p[3]}</p></article>`).join(''),
edu:(e)=>D.edu.map(v=>`<a class="card rv-up" data-t="${v[0]}" href="https://youtube.com/@SolaceMedicalandAesthetics"><span class="badge">${v[0]}</span><h3>${v[1]}</h3><p>${v[2]}</p></a>`).join(''),
testimonials:(e)=>`<div class="slides">${D.tst.map(t=>`<div class="slide"><q>${t[0]}</q><cite>${t[1]}</cite></div>`).join('')}</div><div class="dots">${D.tst.map((_,i)=>`<button aria-label="Slide ${i+1}"></button>`).join('')}</div>`,
faq:()=>D.faq.map(f=>`<details class="rv-up"><summary>${f[0]}</summary><p>${f[1]}</p></details>`).join('')};
$$('[data-render]').forEach(e=>e.innerHTML=R[e.dataset.render](e));
$$('[data-wa]').forEach(a=>a.href='https://wa.me/'+D.wa);
// image fallback: shows a labelled placeholder until the real file is added
$$('.fig img').forEach(i=>{const f=()=>{i.parentNode.classList.add('ph');i.parentNode.dataset.ph='Add '+i.getAttribute('src')};i.complete&&!i.naturalWidth?f():i.addEventListener('error',f)});
// reveal on scroll with stagger
const io=new IntersectionObserver(es=>es.forEach(x=>{if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}}),{threshold:.15});
const reveal=()=>$$('[class*=rv-]:not(.in)').forEach((e,i)=>{e.style.setProperty('--d',(i%4)*.09+'s');io.observe(e)});reveal();
// counters
const co=new IntersectionObserver(es=>es.forEach(x=>{if(!x.isIntersecting)return;const b=x.target,n=+b.dataset.count,t=performance.now();(function s(now){const p=Math.min((now-t)/1400,1);b.textContent=Math.round(n*(1-Math.pow(1-p,3)))+(b.dataset.suf||'');p<1&&requestAnimationFrame(s)})(t);co.unobserve(b)}));$$('[data-count]').forEach(b=>co.observe(b));
// nav, progress, parallax, back-to-top
const nav=$('.nav'),pr=$('.prog'),top=$('.top'),hi=$('.hero-img img');let tk=0;
addEventListener('scroll',()=>{if(tk)return;tk=requestAnimationFrame(()=>{const y=scrollY,m=document.body.scrollHeight-innerHeight;nav.classList.toggle('sc',y>40);pr.style.transform=`scaleX(${m?y/m:0})`;top.classList.toggle('v',y>600);if(hi&&y<innerHeight)hi.parentNode.style.transform=`translateY(${y*.12}px)`;tk=0})},{passive:true});
top.onclick=()=>scrollTo({top:0});
const bg=$('.burger'),mn=$('#menu');bg.onclick=()=>{const o=mn.classList.toggle('open');bg.setAttribute('aria-expanded',o)};
// page transition
$$('a[href$=".html"]').forEach(a=>a.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey)return;e.preventDefault();document.body.classList.add('leave');setTimeout(()=>location.href=a.href,450)}));
addEventListener('pageshow',e=>e.persisted&&document.body.classList.remove('leave'));
// expandable cards, tilt
$$('.card[data-x]').forEach(c=>c.onclick=()=>c.classList.toggle('open'));
if(matchMedia('(hover:hover)').matches)$$('.card').forEach(c=>{c.addEventListener('mousemove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transition='box-shadow .35s';c.style.transform=`perspective(700px) rotateY(${x*5}deg) rotateX(${-y*5}deg) translateY(-4px)`});c.addEventListener('mouseleave',()=>{c.style.transition='';c.style.transform=''})});
// filters + search
const cards=()=>$$('[data-render=products] .card,[data-render=edu] .card');let ft='all',q='';
const apply=()=>cards().forEach(c=>c.style.display=(ft=='all'||c.dataset.t==ft)&&c.textContent.toLowerCase().includes(q)?'':'none');
$$('.filters button').forEach(b=>b.onclick=()=>{$$('.filters button').forEach(x=>x.classList.remove('on'));b.classList.add('on');ft=b.dataset.f;apply()});
const se=$('.search');se&&se.addEventListener('input',()=>{q=se.value.toLowerCase();apply()});
// testimonial slider: autoplay + swipe
const sl=$('.slider');if(sl){const tr=$('.slides',sl),ds=$$('.dots button',sl);let i=0,t0,sx;const go=n=>{i=(n+ds.length)%ds.length;tr.style.transform=`translateX(-${i*100}%)`;ds.forEach((d,k)=>d.classList.toggle('on',k==i))};ds.forEach((d,k)=>d.onclick=()=>{go(k);rs()});const rs=()=>{clearInterval(t0);t0=setInterval(()=>go(i+1),5500)};
sl.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});sl.addEventListener('touchend',e=>{const d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>40){go(i+(d<0?1:-1));rs()}});go(0);rs()}
// booking form
const f=$('#bk');if(f){const chk=()=>{let ok=true;['n','p'].forEach(k=>{const el=f.elements[k],v=el.value.trim(),bad=!v||(k=='p'&&v.replace(/\D/g,'').length<10);el.classList.toggle('bad',bad);if(bad)ok=false});return ok};
const msg=()=>encodeURIComponent(`Hello, I'm ${f.n.value}. Concern: ${f.c.value}. Date: ${f.d.value||'flexible'}. ${f.m.value}`);
f.onsubmit=e=>{e.preventDefault();$('.ok').textContent=chk()?'Thank you. We will contact you to confirm your slot.':'Please enter your name and a valid phone number.'};
$('#wa').onclick=()=>chk()?open(`https://wa.me/${D.wa}?text=${msg()}`):$('.ok').textContent='Please enter your name and a valid phone number.'}
