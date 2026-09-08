document.addEventListener("DOMContentLoaded", () => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach(el => observer.observe(el));

  const menuBtn = document.querySelector(".menu-toggle");
  if (menuBtn) {
    menuBtn.addEventListener("click", () => {
      document.body.classList.toggle("menu-open");
      menuBtn.setAttribute("aria-expanded", document.body.classList.contains("menu-open") ? "true" : "false");
    });
    document.querySelectorAll("#mainNav a").forEach(link => link.addEventListener("click", () => {
      document.body.classList.remove("menu-open");
      menuBtn.setAttribute("aria-expanded", "false");
    }));
  }

  const quoteForm = document.getElementById("quoteForm");
  if (quoteForm) {
    quoteForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = document.getElementById("qName").value.trim();
      const company = document.getElementById("qCompany").value.trim();
      const phone = document.getElementById("qPhone").value.trim();
      const sector = document.getElementById("qSector").value.trim();
      const need = document.getElementById("qNeed").value.trim();
      const text = [
        "Hola AUTOMATIK CR, quiero solicitar información sobre una solución.",
        "",
        `Nombre: ${name}`,
        `Empresa: ${company || "No indicada"}`,
        `Teléfono: ${phone}`,
        `Sector: ${sector || "No indicado"}`,
        `Necesidad: ${need}`
      ].join("\n");
      window.open(`https://wa.me/50671642558?text=${encodeURIComponent(text)}`, "_blank", "noopener");
    });
  }

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
    itemsBox.innerHTML = cart.length === 0
      ? '<p class="muted">Agrega productos para iniciar.</p>'
      : cart.map(x => `<div class="cart-item"><span>${x.name}</span><b>${money(x.price)}</b></div>`).join("");
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
      if(cart.length === 0){ alert("Agrega al menos un producto."); return; }
      emptyKitchen.classList.add("hidden");
      kitchenOrder.classList.remove("hidden");
      kitchenItems.innerHTML = cart.map(x=>`<p>1x ${x.name}</p>`).join("");
      status.textContent = "Recibido";
      prepBtn.textContent = "Preparar pedido";
      prepBtn.disabled = false;
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
