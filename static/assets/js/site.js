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

  // Desktop dropdowns: click/keyboard toggle (hover + focus-within work via CSS).
  document.querySelectorAll(".site-nav__trigger").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var expanded = btn.getAttribute("aria-expanded") === "true";
      document.querySelectorAll(".site-nav__trigger").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
      btn.setAttribute("aria-expanded", String(!expanded));
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".site-nav__group")) {
      document.querySelectorAll(".site-nav__trigger").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
    }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      document.querySelectorAll(".site-nav__trigger").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
    }
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
