// Inicializa mapa em Porto Velho
const map = L.map('map').setView([-8.7608, -63.8999], 14);
const modal = document.getElementById("modal");
const btnAbrir = document.getElementById("btnAbrirModal");
const btnCancelar = document.querySelector(".cancelar");
const btnConfirmar = document.querySelector(".confirmar");

// Mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);

// Melhor ponto (filial ideal)
fetch("/api/melhor-ponto")
  .then(res => res.json())
  .then(p => {
    if (!p) return;

    L.circleMarker([p.lat, p.lng], {
      radius: 12,
      color: "red",
      fillColor: "red",
      fillOpacity: 0.7
    })
    .addTo(map)
    .bindPopup("🔥 Melhor local para abrir o iFood");
  });

// Pins dos pedidos
fetch("/api/pontos")
  .then(res => res.json())
  .then(pontos => {
    const bounds = [];

    pontos.forEach(p => {
      const marker = L.marker([p.lat, p.lng])
        .addTo(map)
        .bindPopup(`
          <b>${p.rua}</b><br>
          Nº ${p.numero}<br>
          ${p.bairro}
        `);

      bounds.push([p.lat, p.lng]);
    });

    if (bounds.length) {
      map.fitBounds(bounds);
    }
  });

// Upload do Excel
document.getElementById("btnUpload").addEventListener("click", () => {
  const file = document.getElementById("fileInput").files[0];

  if (!file) {
    alert("Selecione um arquivo Excel (.xlsx)");
    return;
  }

  const formData = new FormData();
  formData.append("arquivo", file);

  fetch("/api/upload", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    alert(data.mensagem || "Planilha enviada com sucesso");
    location.reload();
  })
  .catch(err => {
    console.error(err);
    alert("Erro ao enviar a planilha");
  });
});

btnAbrir.addEventListener("click", () => {
  modal.classList.remove("hidden");
});

btnCancelar.addEventListener("click", () => {
  modal.classList.add("hidden");
});

btnConfirmar.addEventListener("click", () => {
  const file = document.getElementById("fileInput").files[0];

  if (!file) {
    alert("Selecione um arquivo Excel (.xlsx)");
    return;
  }

  const formData = new FormData();
  formData.append("arquivo", file);

  fetch("/api/upload", {
    method: "POST",
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      alert(data.mensagem || "Importação concluída");
      modal.classList.add("hidden");
      location.reload();
    })
    .catch(err => {
      console.error(err);
      alert("Erro ao importar a planilha");
    });
});
