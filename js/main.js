/* ==========================================================================
   Dr. Sameen Zahra — interactions
   No dependencies. Every feature degrades gracefully without JS.
   ========================================================================== */
(function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const SITE = window.SITE || {};
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isTouch = window.matchMedia("(hover: none)").matches;

  /* Progressive enhancement flag: reveal styles only apply once this script runs */
  document.documentElement.classList.add("js");

  /* -------------------------------------------------------------- reveal in */
  const revealEls = $$(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach((el) => el.classList.add("is-in"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target;
          const batch = Array.from(el.parentElement ? el.parentElement.children : [el]);
          const i = Math.max(batch.indexOf(el), 0);
          el.style.setProperty("--d", `${Math.min(i, 6) * 65}ms`);
          el.classList.add("is-in");
          io.unobserve(el);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
    // safety net: anything already on screen gets revealed after load
    window.addEventListener("load", () => {
      revealEls.forEach((el) => {
        if (el.classList.contains("is-in")) return;
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.95) el.classList.add("is-in");
      });
    });
  }

  /* ---------------------------------------------------------- whatsapp links */
  $$("[data-wa]").forEach((a) => {
    if (!a.getAttribute("href") || a.getAttribute("href") === "#") {
      a.href = `https://wa.me/${SITE.wa || ""}`;
    }
    a.target = "_blank";
    a.rel = "noopener";
  });

  /* ------------------------------------------------------------ header state */
  const head = $("#site-head");
  const progress = $(".progress span");
  const toTop = $(".to-top");
  let ticking = false;

  function onScroll() {
    const y = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (head) {
      const scrolled = head.classList.contains("is-scrolled");
      if (!scrolled && y > 70) head.classList.add("is-scrolled");
      else if (scrolled && y < 18) head.classList.remove("is-scrolled");
    }
    if (progress) progress.style.transform = `scaleX(${max > 0 ? Math.min(y / max, 1) : 0})`;
    if (toTop) toTop.classList.toggle("is-visible", y > 700);
    ticking = false;
  }
  window.addEventListener(
    "scroll",
    () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(onScroll);
      }
    },
    { passive: true }
  );
  onScroll();

  if (toTop) {
    toTop.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* ------------------------------------------------------------------ drawer */
  const drawer = $("#drawer");
  const scrim = $("#scrim");
  const burger = $(".burger");
  const drawerClose = $(".drawer-close");
  let lastFocused = null;

  function openDrawer() {
    if (!drawer) return;
    lastFocused = document.activeElement;
    drawer.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false");
    if (scrim) {
      scrim.hidden = false;
      requestAnimationFrame(() => scrim.classList.add("is-visible"));
    }
    if (burger) burger.setAttribute("aria-expanded", "true");
    document.body.classList.add("is-locked");
    const first = drawer.querySelector("a, button");
    if (first) setTimeout(() => first.focus(), 80);
  }

  function closeDrawer() {
    if (!drawer || !drawer.classList.contains("is-open")) return;
    drawer.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true");
    if (burger) {
      burger.setAttribute("aria-expanded", "false");
      burger.focus({ preventScroll: true });
    }
    if (scrim) {
      scrim.classList.remove("is-visible");
      setTimeout(() => (scrim.hidden = true), 350);
    }
    document.body.classList.remove("is-locked");
    if (lastFocused) lastFocused.focus({ preventScroll: true });
  }

  if (burger) burger.addEventListener("click", openDrawer);
  if (drawerClose) drawerClose.addEventListener("click", closeDrawer);
  if (scrim) scrim.addEventListener("click", closeDrawer);
  if (drawer) {
    $$("a", drawer).forEach((a) => a.addEventListener("click", closeDrawer));
  }
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeDrawer();
  });
  if (drawer) {
    drawer.addEventListener("keydown", (e) => {
      if (e.key !== "Tab") return;
      const focusables = $$('a[href], button:not([disabled])', drawer).filter(
        (el) => el.getClientRects().length > 0
      );
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });
  }

  /* ---------------------------------------------------------------- counters */
  const counters = $$("[data-count]");
  // the markup holds the real number (for no-JS); reset only when animating
  if (!reduceMotion) {
    counters.forEach((el) => {
      el.textContent = "0" + (el.dataset.suffix || "");
    });
  }
  const animateCount = (el) => {
    const target = Number(el.dataset.count) || 0;
    const suffix = el.dataset.suffix || "";
    if (reduceMotion) {
      el.textContent = target + suffix;
      return;
    }
    const start = performance.now();
    const duration = 1500;
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  if ("IntersectionObserver" in window) {
    const co = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          animateCount(entry.target);
          co.unobserve(entry.target);
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((el) => co.observe(el));
  } else {
    counters.forEach(animateCount);
  }

  /* --------------------------------------------------------- testimonial slider */
  $$("[data-slider]").forEach((slider) => {
    const track = $(".slider-track", slider);
    const slides = $$(".slide", slider);
    if (!track || slides.length < 2) return;
    const section = slider.closest("section") || document;
    const dots = $$(".slider-dots button", slider);
    const prev = $('[data-slide="prev"]', section);
    const next = $('[data-slide="next"]', section);
    let index = 0;
    let timer = null;

    const go = (i) => {
      index = (i + slides.length) % slides.length;
      track.style.transform = `translateX(-${index * 100}%)`;
      dots.forEach((dot, k) => {
        dot.classList.toggle("is-active", k === index);
        dot.setAttribute("aria-current", k === index ? "true" : "false");
      });
      slides.forEach((s, k) => s.setAttribute("aria-hidden", k === index ? "false" : "true"));
    };

    const play = () => {
      if (reduceMotion) return;
      stop();
      timer = setInterval(() => go(index + 1), 6500);
    };
    const stop = () => {
      if (timer) clearInterval(timer);
      timer = null;
    };

    if (prev) prev.addEventListener("click", () => { go(index - 1); play(); });
    if (next) next.addEventListener("click", () => { go(index + 1); play(); });
    dots.forEach((dot, k) => dot.addEventListener("click", () => { go(k); play(); }));

    slider.addEventListener("mouseenter", stop);
    slider.addEventListener("mouseleave", play);
    slider.addEventListener("focusin", stop);
    slider.addEventListener("focusout", play);
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : play()));

    /* swipe */
    let startX = 0;
    let startY = 0;
    let dragging = false;
    slider.addEventListener("touchstart", (e) => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      dragging = true;
      stop();
    }, { passive: true });
    slider.addEventListener("touchend", (e) => {
      if (!dragging) return;
      dragging = false;
      const dx = e.changedTouches[0].clientX - startX;
      const dy = e.changedTouches[0].clientY - startY;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) go(index + (dx < 0 ? 1 : -1));
      play();
    }, { passive: true });

    go(0);
    play();
  });

  /* -------------------------------------------------------- treatment accordions */
  $$(".tx-toggle").forEach((btn) => {
    const panel = document.getElementById(btn.getAttribute("aria-controls"));
    const card = btn.closest(".tx-card");
    if (!panel) return;
    btn.addEventListener("click", () => {
      const open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      panel.hidden = open;
      if (card) card.classList.toggle("is-open", !open);
    });
  });

  /* ---------------------------------------------------------------- FAQ (details) */
  $$(".faq-item").forEach((item) => {
    item.addEventListener("toggle", () => {
      if (!item.open) return;
      const list = item.parentElement;
      $$(".faq-item", list).forEach((other) => {
        if (other !== item) other.open = false;
      });
    });
  });

  /* ------------------------------------------------------------ filters + search */
  $$(".chips").forEach((chips) => {
    const scope = chips.closest("section");
    if (!scope) return;
    const list = scope.querySelector("[data-filter-list]");
    if (!list) return;
    const items = Array.from(list.children);
    const empty = scope.querySelector("[data-filter-empty]");
    const countEl = scope.querySelector("[data-count-shown]");
    const search = scope.querySelector("[data-search-input]");
    let filter = "all";
    let query = "";

    const apply = () => {
      let shown = 0;
      items.forEach((el) => {
        const cat = (el.dataset.cat || el.dataset.time || el.dataset.topic || "").toLowerCase();
        const haystack = (el.dataset.search || el.textContent || "").toLowerCase();
        const matchCat = filter === "all" || cat === filter;
        const matchQuery = !query || haystack.includes(query);
        const visible = matchCat && matchQuery;
        el.classList.toggle("is-filtered", !visible);
        if (visible) shown += 1;
      });
      if (countEl) countEl.textContent = String(shown);
      if (empty) empty.hidden = shown > 0;
    };

    $$("button[data-filter]", chips).forEach((btn) => {
      btn.addEventListener("click", () => {
        filter = (btn.dataset.filter || "all").toLowerCase();
        $$("button[data-filter]", chips).forEach((b) => {
          const active = b === btn;
          b.classList.toggle("is-active", active);
          b.setAttribute("aria-pressed", String(active));
        });
        apply();
      });
    });

    if (search) {
      search.addEventListener("input", () => {
        query = search.value.trim().toLowerCase();
        apply();
      });
    }
    apply();
  });

  /* --------------------------------------------------------------- lightbox */
  const lightbox = $("#lightbox");
  const galleryLinks = $$("[data-lightbox]");
  if (lightbox && galleryLinks.length && typeof lightbox.showModal === "function") {
    const img = $("img", lightbox);
    const caption = $("figcaption", lightbox);
    let current = 0;

    const show = (i) => {
      current = (i + galleryLinks.length) % galleryLinks.length;
      const link = galleryLinks[current];
      img.src = link.getAttribute("href");
      img.alt = link.dataset.caption || "";
      caption.textContent = link.dataset.caption || "";
    };

    const open = (i) => {
      show(i);
      lightbox.showModal();
      document.body.classList.add("is-locked");
    };
    const close = () => lightbox.close();

    galleryLinks.forEach((link, i) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        open(i);
      });
    });
    $(".lightbox-close", lightbox).addEventListener("click", close);
    $(".lightbox-prev", lightbox).addEventListener("click", () => show(current - 1));
    $(".lightbox-next", lightbox).addEventListener("click", () => show(current + 1));
    lightbox.addEventListener("click", (e) => {
      if (e.target === lightbox) close();
    });
    lightbox.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(current - 1);
      if (e.key === "ArrowRight") show(current + 1);
    });
    lightbox.addEventListener("close", () => document.body.classList.remove("is-locked"));
  }

  /* ----------------------------------------------------------- booking form */
  const form = $("#bookingForm");
  if (form) {
    const success = $("[data-success]", form);
    const successWa = $("[data-success-wa]", form);
    const successText = $("[data-success-text]", form);
    const status = $('[data-err="form"]', form);

    const fields = {
      name: form.elements.name,
      phone: form.elements.phone,
      email: form.elements.email,
      consent: form.elements.consent,
    };

    const setError = (name, message) => {
      const err = $(`[data-err="${name}"]`, form);
      if (err) err.textContent = message;
      const wrap = form.elements[name] ? form.elements[name].closest(".field") : null;
      if (wrap) wrap.classList.toggle("has-error", Boolean(message));
    };

    const validate = () => {
      let ok = true;
      const name = fields.name.value.trim();
      const phone = fields.phone.value.replace(/[^\d]/g, "");
      const email = fields.email.value.trim();

      if (name.length < 2) { setError("name", "Please tell us your name."); ok = false; }
      else setError("name", "");

      if (phone.length < 10) { setError("phone", "Enter a valid phone number (at least 10 digits)."); ok = false; }
      else setError("phone", "");

      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        setError("email", "That email doesn't look right.");
        ok = false;
      } else setError("email", "");

      if (!fields.consent.checked) { setError("consent", "Please confirm we may contact you."); ok = false; }
      else setError("consent", "");

      if (status) status.textContent = ok ? "" : "Please check the highlighted fields.";
      return ok;
    };

    const message = () => {
      const d = form.elements;
      const lines = [
        "Hello, I'd like to book a consultation.",
        `Name: ${d.name.value.trim()}`,
        `Phone: ${d.phone.value.trim()}`,
      ];
      if (d.email.value.trim()) lines.push(`Email: ${d.email.value.trim()}`);
      if (d.concern.value) lines.push(`Concern: ${d.concern.value}`);
      if (d.clinic.value) lines.push(`Clinic: ${d.clinic.value}`);
      if (d.visit.value) lines.push(`Patient: ${d.visit.value}`);
      const when = [d.date.value, d.time.value].filter(Boolean).join(" · ");
      if (when) lines.push(`Preferred: ${when}`);
      if (d.message.value.trim()) lines.push(`Notes: ${d.message.value.trim()}`);
      return lines.join("\n");
    };

    if (form.elements.date) {
      const now = new Date();
      const iso = new Date(now.getTime() - now.getTimezoneOffset() * 60000)
        .toISOString()
        .slice(0, 10);
      form.elements.date.min = iso;
    }

    const showSuccess = () => {
      const url = `https://wa.me/${SITE.wa || ""}?text=${encodeURIComponent(message())}`;
      if (successWa) successWa.href = url;
      if (successText) {
        successText.textContent = `Thanks ${fields.name.value.trim().split(" ")[0]} — your request is ready. Send it on WhatsApp and the clinic will confirm within one working day.`;
      }
      if (success) {
        success.hidden = false;
        if (status) status.textContent = "";
        success.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
      }
    };

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validate()) {
        const firstBad = $(".field.has-error input, .field.has-error select", form) || $('input[name="consent"]', form);
        if (firstBad) firstBad.focus();
        return;
      }
      showSuccess();
    });

    const waSend = $("#waSend");
    if (waSend) {
      waSend.addEventListener("click", () => {
        if (!validate()) return;
        window.open(`https://wa.me/${SITE.wa || ""}?text=${encodeURIComponent(message())}`, "_blank", "noopener");
      });
    }

    const reset = $("[data-reset]", form);
    if (reset) {
      reset.addEventListener("click", () => {
        if (success) success.hidden = true;
        fields.name.focus();
      });
    }

    $$("input, select, textarea", form).forEach((el) => {
      el.addEventListener("input", () => {
        if (el.closest(".field") && el.closest(".field").classList.contains("has-error")) {
          el.closest(".field").classList.remove("has-error");
          const err = $(`[data-err="${el.name}"]`, form);
          if (err) err.textContent = "";
        }
        if (success && !success.hidden) success.hidden = true;
      });
    });
  }
})();
