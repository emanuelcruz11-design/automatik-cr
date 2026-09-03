
document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add("visible");
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(el => observer.observe(el));

  const cart = [];
  const itemsBox = document.getElementById("cartItems");
  const countBox = document.getElementById("cartCount");
  const totalBox = document.getElementById("cartTotal");
  const sendBtn = document.getElementById("sendOrder");
  const kitchenOrder = document.getElementById("kitchenOrder");
  const emptyKitchen = document.getElementById("emptyKitchen");
  const kitchenItems = document.getElementById("kitchenItems");
  const prepBtn = document.getElementById("prepBtn");
  const status = document.getElementById("orderStatus");

  const money = n => "₡" + n.toLocaleString("es-CR");

  function renderCart(){
    if(!itemsBox) return;
    if(cart.length === 0){
      itemsBox.innerHTML = '<p class="muted">Agrega productos para iniciar.</p>';
    } else {
      itemsBox.innerHTML = cart.map(x => `<div class="cart-item"><span>${x.name}</span><b>${money(x.price)}</b></div>`).join("");
    }
    countBox.textContent = `${cart.length} producto${cart.length === 1 ? "" : "s"}`;
    totalBox.textContent = money(cart.reduce((s,x)=>s+x.price,0));
  }

  document.querySelectorAll(".add-item").forEach(btn => {
    btn.addEventListener("click", e => {
      const row = e.target.closest(".product");
      cart.push({name: row.dataset.name, price: Number(row.dataset.price)});
      renderCart();
      e.target.textContent = "Agregado ✓";
      setTimeout(()=> e.target.textContent = "Agregar", 800);
    });
  });

  if(sendBtn){
    sendBtn.addEventListener("click", () => {
      if(cart.length === 0){
        alert("Agrega al menos un producto.");
        return;
      }
      emptyKitchen.classList.add("hidden");
      kitchenOrder.classList.remove("hidden");
      kitchenItems.innerHTML = cart.map(x=>`<p>1x ${x.name}</p>`).join("");
      status.textContent = "Recibido";
      prepBtn.textContent = "Preparar pedido";
    });
  }

  if(prepBtn){
    prepBtn.addEventListener("click", () => {
      if(status.textContent === "Recibido"){
        status.textContent = "Preparando";
        prepBtn.textContent = "Marcar listo";
      } else {
        status.textContent = "Listo para entregar";
        prepBtn.textContent = "Pedido listo ✓";
        prepBtn.disabled = true;
      }
    });
  }
});
