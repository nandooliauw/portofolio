// Small progressive enhancement: current year + active section in the nav.
// The page is fully readable with JavaScript disabled.

(function () {
  "use strict";

  var yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }

  var links = Array.prototype.slice.call(document.querySelectorAll('.nav nav a[href^="#"]'));
  if (!links.length || !("IntersectionObserver" in window)) {
    return;
  }

  var sections = links
    .map(function (link) {
      var id = link.getAttribute("href").slice(1);
      var el = document.getElementById(id);
      return el ? { link: link, el: el } : null;
    })
    .filter(Boolean);

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) {
          return;
        }
        sections.forEach(function (pair) {
          var isCurrent = pair.el === entry.target;
          pair.link.style.color = isCurrent ? "var(--text)" : "";
        });
      });
    },
    { rootMargin: "-45% 0px -50% 0px" }
  );

  sections.forEach(function (pair) {
    observer.observe(pair.el);
  });
})();
