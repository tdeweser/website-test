/* IPE website — small progressive enhancements. The site works without JavaScript. */
(function () {
  "use strict";

  // Mobile menu toggle.
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }

  // Dropdown folders: click/keyboard toggle (hover and focus-within work via CSS).
  var triggers = document.querySelectorAll(".site-nav__trigger");
  function closeAll(except) {
    triggers.forEach(function (b) { if (b !== except) b.setAttribute("aria-expanded", "false"); });
  }
  triggers.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var expanded = btn.getAttribute("aria-expanded") === "true";
      closeAll(btn);
      btn.setAttribute("aria-expanded", String(!expanded));
    });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".site-nav__folder")) closeAll(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeAll(); });

  // Carousel arrows (summary blocks).
  document.querySelectorAll(".summary--carousel").forEach(function (box) {
    var list = box.querySelector(".summary__items");
    var prev = box.querySelector(".summary__prev");
    var next = box.querySelector(".summary__next");
    if (!list || !prev || !next) return;
    function update() {
      prev.disabled = list.scrollLeft <= 2;
      next.disabled = list.scrollLeft + list.clientWidth >= list.scrollWidth - 2;
    }
    prev.addEventListener("click", function () { list.scrollBy({ left: -list.clientWidth, behavior: "smooth" }); });
    next.addEventListener("click", function () { list.scrollBy({ left: list.clientWidth, behavior: "smooth" }); });
    list.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  // "Deel deze pagina": native share sheet, or copy the link.
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

  // Archive: filter items by title.
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
