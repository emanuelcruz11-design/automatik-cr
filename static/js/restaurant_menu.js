const demo=window.RESTAURANT_DEMO;
let cart=[];
let currentOrder=null;
const STORAGE_KEY='automatik_demo_order_v11';
const fmt=n=>'₡'+Math.round(Number(n||0)).toLocaleString('es-CR');
const q=s=>document.querySelector(s),qa=s=>[...document.querySelectorAll(s)];
const timeNow=()=>new Date().toLocaleTimeString('es-CR',{hour:'2-digit',minute:'2-digit',hour12:false});
function addMinutesLabel(mins){const d=new Date(Date.now()+mins*60000);return d.toLocaleTimeString('es-CR',{hour:'2-digit',minute:'2-digit',hour12:false});}
function saveLocal(o){currentOrder=o;localStorage.setItem(STORAGE_KEY,JSON.stringify(o));}
function loadLocal(){try{return JSON.parse(localStorage.getItem(STORAGE_KEY)||'null')}catch(e){return null}}
function makeLocalId(){return 'BU-'+String(Date.now()).slice(-4)}
function filterMenu(){const term=q('#searchInput').value.toLowerCase().trim();const cat=q('.cat-btn.active')?.dataset.cat||'Todos';qa('.food-card').forEach(card=>{const okCat=cat==='Todos'||card.dataset.category===cat;const okSearch=!term||card.dataset.name.includes(term);card.style.display=okCat&&okSearch?'':'none'})}
qa('.cat-btn').forEach(b=>b.addEventListener('click',()=>{qa('.cat-btn').forEach(x=>x.classList.remove('active'));b.classList.add('active');filterMenu()}));q('#searchInput').addEventListener('input',filterMenu);
qa('.add-btn').forEach(btn=>btn.addEventListener('click',()=>{const id=Number(btn.dataset.id),found=cart.find(x=>x.id===id);if(found)found.qty++;else cart.push({id,name:btn.dataset.name,price:Number(btn.dataset.price),qty:1});renderCart();btn.textContent='Agregado ✓';setTimeout(()=>btn.textContent='Agregar +',700)}));
function total(){return cart.reduce((s,x)=>s+x.price*x.qty,0)}
function renderCart(){const count=cart.reduce((s,x)=>s+x.qty,0);q('#cartCount').textContent=count;q('#cartTotal').textContent=fmt(total());q('#drawerTotal').textContent=fmt(total());q('#cartFab').classList.toggle('hidden',!count);q('#cartItems').innerHTML=cart.length?cart.map(x=>`<div class="cart-row"><div><strong>${x.name}</strong><small>${fmt(x.price)} c/u</small></div><div class="qty"><button data-act="minus" data-id="${x.id}">−</button><b>${x.qty}</b><button data-act="plus" data-id="${x.id}">+</button></div></div>`).join(''):'<p>Tu carrito está vacío.</p>';qa('.qty button').forEach(b=>b.onclick=()=>{const x=cart.find(i=>i.id===Number(b.dataset.id));if(!x)return;b.dataset.act==='plus'?x.qty++:x.qty--;cart=cart.filter(i=>i.qty>0);renderCart()})}
function openCart(){q('#cartDrawer').classList.add('open');q('#drawerBackdrop').classList.remove('hidden')}function closeCart(){q('#cartDrawer').classList.remove('open');q('#drawerBackdrop').classList.add('hidden')}q('#cartFab').onclick=openCart;q('#closeCart').onclick=closeCart;q('#drawerBackdrop').onclick=closeCart;
q('#submitOrder').onclick=async()=>{
  if(!cart.length)return;
  const btn=q('#submitOrder');btn.disabled=true;btn.textContent='Preparando pago…';
  const created=timeNow();
  const payload={mesa:demo.mesa,customer:q('#customerName').value.trim()||'Cliente',notes:q('#orderNotes').value.trim(),items:cart.map(x=>({name:x.name,price:x.price,qty:x.qty})),total:total()};
  let order={id:makeLocalId(),...payload,status:'Pendiente de pago',payment_status:'Pendiente',started_at:created,created_at:created,estimated_delivery_at:addMinutesLabel(25),finished_at:null,paid_at:null,payment_method:null,invoice_number:null,status_history:[{status:'Pendiente de pago',time:created}]};
  try{const r=await fetch('/api/restaurant/orders',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(r.ok){order=await r.json()}}catch(e){}
  saveLocal(order);
  btn.disabled=false;btn.textContent='Continuar al pago';closeCart();q('#orderId').textContent=order.id;q('#orderFinalTotal').textContent=fmt(order.total);q('#statusModal').classList.remove('hidden');cart=[];renderCart();renderStatus(order);
};
function renderStatus(o){q('#orderStatus').textContent=o.status;const statuses=['Pendiente de pago','Recibido','En preparación','Listo','Entregado'];const idx=statuses.indexOf(o.status);q('#progressTrack').innerHTML=statuses.map((s,i)=>`<span class="progress-step ${i<=idx?'done':''}" title="${s}"></span>`).join('');const pending=o.status==='Pendiente de pago';q('#paymentBlock').classList.toggle('hidden',!pending);q('#paidConfirmation').classList.toggle('hidden',o.payment_status!=='Pagado');q('#invoiceBtn').classList.toggle('hidden',o.payment_status!=='Pagado');const next=q('#continueKitchen');if(next)next.classList.toggle('hidden',o.payment_status!=='Pagado');q('#orderStart').textContent=o.started_at||o.created_at||'--:--';q('#orderEstimate').textContent=o.estimated_delivery_at||'--:--';q('#orderFinish').textContent=o.finished_at||'Pendiente'}
q('#payOrder').onclick=async()=>{
  if(!currentOrder||currentOrder.status!=='Pendiente de pago')return;
  const btn=q('#payOrder');btn.disabled=true;btn.textContent='Procesando pago…';
  const payment_method=q('#paymentMethod').value;const stamp=timeNow();
  let updated={...currentOrder,status:'Recibido',payment_status:'Pagado',paid_at:stamp,payment_method,invoice_number:currentOrder.invoice_number||('FAC-DEMO-'+currentOrder.id.replace('BU-','')),status_history:[...(currentOrder.status_history||[]),{status:'Recibido',time:stamp}]};
  try{const r=await fetch('/api/restaurant/orders/'+currentOrder.id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'Recibido',payment_method})});if(r.ok)updated=await r.json()}catch(e){}
  saveLocal(updated);btn.disabled=false;btn.textContent='Pagar y enviar a cocina';renderStatus(updated);
};
q('#invoiceBtn').onclick=async(e)=>{
  e.preventDefault();const o=currentOrder||loadLocal();if(!o)return;
  try{const r=await fetch('/demo-restaurante/factura-demo.pdf',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o)});if(!r.ok)throw new Error();const blob=await r.blob();const url=URL.createObjectURL(blob);window.open(url,'_blank');setTimeout(()=>URL.revokeObjectURL(url),60000)}catch(err){alert('No se pudo generar el comprobante. Intentá nuevamente.')}
};
q('#closeStatus').onclick=()=>q('#statusModal').classList.add('hidden');
const existing=loadLocal();if(existing&&existing.payment_status==='Pagado'){currentOrder=existing;}
