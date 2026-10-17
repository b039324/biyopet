/* =========================================================
   Biyopet — main.js
   Bölümler:
   1) Ürünleri JSON'dan yükleme
   2) Kategori filtreleme (Tümü / Köpek / Kedi)
   3) Ürün modalı (aç/kapa)
   4) Mobil menü
   5) İletişim formu (arayüz)
   6) Küçük yardımcılar (yıl, scroll vs.)
   ========================================================= */

(() => {
  "use strict";

  /* ---------- Global durum ---------- */
  let urunler = [];                 // JSON'dan gelen tüm ürünler
  let aktifKategori = "tumu";       // varsayılan: tüm ürünler

  /* ---------- DOM referansları ---------- */
  const productGrid = document.getElementById("productGrid");
  const tabs = document.querySelectorAll(".tab");

  const modal = document.getElementById("productModal");
  const modalImage = document.getElementById("modalImage");
  const modalTitle = document.getElementById("modalTitle");
  const modalLongDesc = document.getElementById("modalLongDesc");
  const modalFeatures = document.getElementById("modalFeatures");
  const modalCloseBtn = document.getElementById("modalClose");

  const navToggle = document.getElementById("navToggle");
  const primaryNav = document.getElementById("primaryNav");
  const header = document.getElementById("siteHeader");

  const contactForm = document.getElementById("contactForm");
  const formFeedback = document.getElementById("formFeedback");

  const yearEl = document.getElementById("year");

  /* =========================================================
     1) ÜRÜNLERİ YÜKLE
     ========================================================= */
  async function urunleriYukle() {
    try {
      const response = await fetch("data/urunler.json");
      if (!response.ok) {
        throw new Error(`JSON yüklenemedi (HTTP ${response.status})`);
      }
      const data = await response.json();
      urunler = Array.isArray(data.urunler) ? data.urunler : [];
      urunleriRenderEt(aktifKategori);
    } catch (err) {
      console.error("Ürün yükleme hatası:", err);
      productGrid.innerHTML = `
        <p class="loading">
          Ürünler yüklenemedi. Lütfen sayfayı yerel bir sunucu üzerinden açın
          (bkz. README.md).
        </p>`;
    }
  }

  /* =========================================================
     2) ÜRÜNLERİ RENDER ET (kategoriye göre filtrele)
        - "tumu"    → filtre yok, tümü gösterilir
        - "kopek"   → sadece köpek ürünleri
        - "kedi"    → sadece kedi ürünleri
     ========================================================= */
  function urunleriRenderEt(kategori) {
    const filtreli = (kategori === "tumu")
      ? urunler
      : urunler.filter(u => u.kategori === kategori);

    if (filtreli.length === 0) {
      productGrid.innerHTML = `<p class="loading">Bu kategoride henüz ürün yok.</p>`;
      return;
    }

    productGrid.innerHTML = "";

    filtreli.forEach((urun, i) => {
      const card = document.createElement("article");
      card.className = "product-card";
      card.style.animationDelay = `${i * 60}ms`;

      // Güvenli metin basımı için textContent kullanıyoruz.
      const img = document.createElement("img");
      img.src = urun.gorsel;
      img.alt = urun.ad;
      img.loading = "lazy";

      const body = document.createElement("div");
      body.className = "product-card-body";

      const title = document.createElement("h3");
      title.textContent = urun.ad;

      const desc = document.createElement("p");
      desc.textContent = urun.kisaAciklama;

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "btn btn-primary";
      btn.textContent = "Detaylar";
      btn.addEventListener("click", () => modalAc(urun));

      body.appendChild(title);
      body.appendChild(desc);
      body.appendChild(btn);

      card.appendChild(img);
      card.appendChild(body);
      productGrid.appendChild(card);
    });
  }

  /* =========================================================
     3) KATEGORİ SEKMELERİ
     ========================================================= */
  function sekmeAyarla(kategori) {
    aktifKategori = kategori;

    tabs.forEach(tab => {
      const isActive = tab.dataset.category === kategori;
      tab.classList.toggle("is-active", isActive);
      tab.setAttribute("aria-selected", isActive ? "true" : "false");
    });

    // tabpanel'in aria-labelledby değerini de güncelleyelim (erişilebilirlik)
    const activeTab = document.querySelector(`.tab[data-category="${kategori}"]`);
    if (activeTab) {
      productGrid.setAttribute("aria-labelledby", activeTab.id);
    }

    urunleriRenderEt(kategori);
  }

  tabs.forEach(tab => {
    tab.addEventListener("click", () => sekmeAyarla(tab.dataset.category));
  });

  /* =========================================================
     4) ÜRÜN MODALI
     ========================================================= */
  function modalAc(urun) {
    modalImage.src = urun.gorsel;
    modalImage.alt = urun.ad;
    modalTitle.textContent = urun.ad;
    modalLongDesc.textContent = urun.uzunAciklama || "";

    modalFeatures.innerHTML = "";
    (urun.ozellikler || []).forEach(oz => {
      const li = document.createElement("li");
      li.textContent = oz;
      modalFeatures.appendChild(li);
    });

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";

    // Erişilebilirlik: kapatma butonuna odaklan
    modalCloseBtn.focus();
  }

  function modalKapat() {
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  // Modal kapatma: çarpı butonu + arka plan tıklaması
  modal.addEventListener("click", (e) => {
    if (e.target.matches("[data-close]") || e.target === modal) {
      modalKapat();
    }
  });

  // ESC tuşu ile kapatma
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("is-open")) {
      modalKapat();
    }
  });

  /* =========================================================
     5) MOBİL MENÜ
     ========================================================= */
  function menuyuKapat() {
    primaryNav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
    navToggle.setAttribute("aria-label", "Menüyü aç");
  }

  navToggle.addEventListener("click", () => {
    const isOpen = primaryNav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    navToggle.setAttribute("aria-label", isOpen ? "Menüyü kapat" : "Menüyü aç");
  });

  // Menü linkine tıklanınca mobil menüyü kapat
  primaryNav.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", menuyuKapat);
  });

  /* =========================================================
     6) İLETİŞİM FORMU (backend yok, sadece arayüz)
     ========================================================= */
  contactForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = contactForm.name.value.trim();
    const email = contactForm.email.value.trim();
    const message = contactForm.message.value.trim();

    // Basit doğrulama
    if (!name || !email || !message) {
      formFeedback.textContent = "Lütfen tüm alanları doldurun.";
      formFeedback.style.color = "#b23b3b";
      return;
    }

    // Başarılı geri bildirim
    formFeedback.textContent = "Mesajınız alındı. En kısa sürede size dönüş yapacağız.";
    formFeedback.style.color = "";
    contactForm.reset();
  });

  /* =========================================================
     7) KÜÇÜK YARDIMCILAR
     ========================================================= */
  // Footer yılı
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // Sayfa kaydırılınca header'a hafif gölge (isteğe bağlı)
  window.addEventListener("scroll", () => {
    if (window.scrollY > 10) {
      header.style.boxShadow = "0 2px 12px rgba(47,95,59,0.08)";
    } else {
      header.style.boxShadow = "none";
    }
  }, { passive: true });

  /* ---------- Başlat ---------- */
  urunleriYukle();
})();