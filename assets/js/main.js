/* Biyopet — etkileşimler */
(function () {
  "use strict";

  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Yıl ---------- */
  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Sabit menü gölgesi ---------- */
  const header = $("#site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-stuck", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Mobil menü ---------- */
  const navToggle = $("#nav-toggle");
  const navLinks = $("#nav-links");
  if (navToggle && navLinks) {
    const setOpen = (open) => {
      navToggle.setAttribute("aria-expanded", String(open));
      navLinks.classList.toggle("is-open", open);
    };
    navToggle.addEventListener("click", () => {
      setOpen(navToggle.getAttribute("aria-expanded") !== "true");
    });
    $$("a", navLinks).forEach((a) => a.addEventListener("click", () => setOpen(false)));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") setOpen(false);
    });
    document.addEventListener("click", (e) => {
      if (!navLinks.contains(e.target) && !navToggle.contains(e.target)) setOpen(false);
    });
    window.addEventListener("resize", () => {
      if (window.innerWidth > 820) setOpen(false);
    });
  }

  /* ---------- Görünme animasyonu ---------- */
  const revealItems = $$(".reveal");
  if (revealItems.length) {
    if (prefersReduced || !("IntersectionObserver" in window)) {
      revealItems.forEach((el) => el.classList.add("is-visible"));
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              io.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
      );
      revealItems.forEach((el) => io.observe(el));
    }
  }

  /* ---------- Ürün filtreleri ---------- */
  const filterBar = $("[data-product-filter]");
  if (filterBar) {
    const chips = $$(".filter-chip", filterBar);
    const cards = $$("[data-product]");
    const countEl = $("[data-filter-count]");
    const applyFilter = (filter) => {
      let visible = 0;
      cards.forEach((card) => {
        const match =
          filter === "all" ||
          card.dataset.animal === filter ||
          card.dataset.age === filter;
        card.classList.toggle("is-hidden", !match);
        if (match) visible += 1;
      });
      chips.forEach((chip) => {
        chip.setAttribute("aria-pressed", String(chip.dataset.filter === filter));
      });
      if (countEl) countEl.textContent = String(visible);
    };
    chips.forEach((chip) => {
      chip.addEventListener("click", () => applyFilter(chip.dataset.filter));
    });
    applyFilter("all");
  }

  /* ---------- Besleme rehberi sekmeleri ---------- */
  const guide = $("[data-guide]");
  if (guide) {
    const tabs = $$(".guide-tab", guide);
    const panels = $$(".guide-panel", guide);
    const select = (key) => {
      tabs.forEach((tab) => {
        const active = tab.dataset.guideTab === key;
        tab.setAttribute("aria-selected", String(active));
        tab.setAttribute("tabindex", active ? "0" : "-1");
      });
      panels.forEach((panel) => {
        panel.hidden = panel.dataset.guidePanel !== key;
      });
    };
    tabs.forEach((tab, i) => {
      tab.addEventListener("click", () => select(tab.dataset.guideTab));
      tab.addEventListener("keydown", (e) => {
        let next = null;
        if (e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
        else if (e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
        else if (e.key === "Home") next = tabs[0];
        else if (e.key === "End") next = tabs[tabs.length - 1];
        if (next) {
          e.preventDefault();
          next.focus();
          select(next.dataset.guideTab);
        }
      });
    });
    if (tabs.length) select(tabs[0].dataset.guideTab);
  }

  /* ---------- Bayilik CTA'sı: konu ön seçimi ---------- */
  const topicSelect = $("#topic");
  if (topicSelect && new URLSearchParams(window.location.search).get("konu") === "bayilik") {
    topicSelect.value = "bayilik";
  }

  /* ---------- SSS: tek seferde bir açık ---------- */
  const faqItems = $$(".faq__item");
  faqItems.forEach((item) => {
    item.addEventListener("toggle", () => {
      if (!item.open) return;
      faqItems.forEach((other) => {
        if (other !== item) other.open = false;
      });
    });
  });

  /* ---------- Form doğrulama ---------- */
  const isEmail = (value) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value.trim());

  const newsletter = $("#newsletter-form");
  if (newsletter) {
    const input = $("#newsletter-email", newsletter);
    const status = $("#newsletter-status", newsletter);
    newsletter.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!input || !isEmail(input.value)) {
        if (input) input.setAttribute("aria-invalid", "true");
        if (status) {
          status.textContent = "Lütfen geçerli bir e-posta adresi girin.";
          status.classList.add("is-error");
        }
        if (input) input.focus();
        return;
      }
      input.removeAttribute("aria-invalid");
      if (status) {
        status.textContent = "Teşekkürler! Kaydınız alındı.";
        status.classList.remove("is-error");
      }
      newsletter.reset();
    });
    if (input) {
      input.addEventListener("input", () => input.removeAttribute("aria-invalid"));
    }
  }

  const contactForm = $("#contact-form");
  if (contactForm) {
    const status = $("#form-status");
    const showError = (name, message) => {
      const field = contactForm.querySelector(`[name="${name}"]`);
      const slot = contactForm.querySelector(`[data-error-for="${name}"]`);
      if (slot) slot.textContent = message || "";
      if (field) field.setAttribute("aria-invalid", message ? "true" : "false");
    };
    contactForm.addEventListener("submit", (e) => {
      e.preventDefault();
      contactForm.classList.add("was-validated");
      let firstInvalid = null;
      const name = contactForm.elements.namedItem("name");
      const email = contactForm.elements.namedItem("email");
      const message = contactForm.elements.namedItem("message");
      const consent = contactForm.elements.namedItem("consent");

      const nameError = name && name.value.trim().length >= 2 ? "" : "Lütfen adınızı ve soyadınızı yazın.";
      const emailError = email && isEmail(email.value) ? "" : "Geçerli bir e-posta adresi girin.";
      const messageError = message && message.value.trim().length >= 10 ? "" : "Lütfen en az 10 karakterlik bir mesaj yazın.";
      const consentError = consent && consent.checked ? "" : "Devam etmek için aydınlatma metnini onaylayın.";

      showError("name", nameError);
      showError("email", emailError);
      showError("message", messageError);
      showError("consent", consentError);
      if (status) status.textContent = "";

      if (nameError) firstInvalid = name;
      else if (emailError) firstInvalid = email;
      else if (messageError) firstInvalid = message;
      else if (consentError) firstInvalid = consent;

      if (firstInvalid) {
        firstInvalid.focus();
        if (status) {
          status.textContent = "Lütfen işaretli alanları kontrol edin.";
          status.classList.add("is-error");
        }
        return;
      }

      if (status) {
        status.textContent =
          "Mesajınız alındı. En kısa sürede size dönüş yapacağız.";
        status.classList.remove("is-error");
      }
      contactForm.reset();
      contactForm.classList.remove("was-validated");
      $$("[data-error-for]", contactForm).forEach((el) => (el.textContent = ""));
      $$("[aria-invalid]", contactForm).forEach((el) => el.setAttribute("aria-invalid", "false"));
    });

    $$("input, textarea, select", contactForm).forEach((field) => {
      field.addEventListener("input", () => {
        const slot = contactForm.querySelector(`[data-error-for="${field.name}"]`);
        if (slot && slot.textContent) {
          slot.textContent = "";
          field.setAttribute("aria-invalid", "false");
        }
      });
    });
  }
})();
