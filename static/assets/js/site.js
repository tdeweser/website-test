/* IPE website — progressive enhancements. Everything works without JavaScript;
   this adds the header behaviour, menus, reveal animations and sliders. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------- Header: white background once scrolled ----------
  var topbar = document.querySelector("[data-topbar]");
  if (topbar) {
    var onScroll = function () { topbar.classList.toggle("is-scrolled", window.scrollY > 24); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ---------- Dropdown groups (folders and language picker) ----------
  var groups = document.querySelectorAll("[data-menu-group]");
  function closeGroups(except) {
    groups.forEach(function (g) {
      if (g === except) return;
      g.classList.remove("is-open");
      var b = g.querySelector("button");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  }
  var hoverable = window.matchMedia("(hover: hover) and (min-width: 1100px)");
  groups.forEach(function (g) {
    var btn = g.querySelector("button");
    var set = function (open) {
      g.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    };
    btn.addEventListener("click", function () {
      var open = !g.classList.contains("is-open");
      closeGroups(g);
      set(open);
    });
    var timer;
    g.addEventListener("mouseenter", function () { if (hoverable.matches) { clearTimeout(timer); closeGroups(g); set(true); } });
    g.addEventListener("mouseleave", function () { if (hoverable.matches) { timer = setTimeout(function () { set(false); }, 150); } });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest("[data-menu-group]")) closeGroups(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeGroups(); setMenu(false); }
  });

  // ---------- Mobile menu drawer ----------
  var toggle = document.querySelector(".menu-toggle");
  function setMenu(open) {
    if (!topbar || !toggle) return;
    topbar.classList.toggle("is-menu-open", open);
    doc.classList.toggle("menu-open", open);
    toggle.setAttribute("aria-expanded", String(open));
  }
  if (toggle) toggle.addEventListener("click", function () { setMenu(!topbar.classList.contains("is-menu-open")); });

  // ---------- Reveal on scroll ----------
  var revealables = document.querySelectorAll("[data-reveal]");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-visible"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.12 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  // ---------- Sliders: homepage media slider and summary carousels ----------
  function wireSlider(track, prev, next) {
    if (!track || !prev || !next) return;
    var step = function () {
      var item = track.firstElementChild;
      return item ? item.getBoundingClientRect().width + 20 : track.clientWidth;
    };
    var update = function () {
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
    };
    prev.addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: reduceMotion ? "auto" : "smooth" }); });
    next.addEventListener("click", function () { track.scrollBy({ left: step(), behavior: reduceMotion ? "auto" : "smooth" }); });
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }
  document.querySelectorAll("[data-slider]").forEach(function (s) {
    wireSlider(s.querySelector("[data-slider-track]"), s.querySelector("[data-slider-prev]"), s.querySelector("[data-slider-next]"));
  });
  document.querySelectorAll(".summary--carousel").forEach(function (box) {
    wireSlider(box.querySelector(".summary__items"), box.querySelector(".summary__prev"), box.querySelector(".summary__next"));
  });

  // ---------- "Deel deze pagina": native share sheet, or copy the link ----------
  document.querySelectorAll("[data-share]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var data = { title: document.title, url: location.href };
      if (navigator.share) { navigator.share(data).catch(function () {}); return; }
      if (navigator.clipboard) {
        navigator.clipboard.writeText(location.href).then(function () {
          var label = btn.textContent;
          btn.textContent = "Link gekopieerd";
          setTimeout(function () { btn.textContent = label; }, 2000);
        });
      }
    });
  });

  // ---------- Archive: filter items by title ----------
  document.querySelectorAll("[data-archive]").forEach(function (archive) {
    var input = archive.querySelector("[data-archive-search]");
    var empty = archive.querySelector("[data-archive-empty]");
    if (!input) return;
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      archive.querySelectorAll(".archive__month").forEach(function (month) {
        var visible = 0;
        month.querySelectorAll("[data-archive-item]").forEach(function (li) {
          var match = !q || li.textContent.toLowerCase().indexOf(q) !== -1;
          li.hidden = !match;
          if (match) visible++;
        });
        month.hidden = visible === 0;
        shown += visible;
      });
      if (empty) empty.hidden = shown !== 0;
    });
  });
})();
