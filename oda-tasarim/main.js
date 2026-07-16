const revealTargets = document.querySelectorAll(
  ".inv, .plan-card, .zone, .gallery figure, .swatch, .steps li, .keep, .render-block"
);

revealTargets.forEach((el) => el.classList.add("reveal"));

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      observer.unobserve(entry.target);
    });
  },
  { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
);

revealTargets.forEach((el, i) => {
  el.style.transitionDelay = `${(i % 6) * 45}ms`;
  observer.observe(el);
});

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", (event) => {
    const id = link.getAttribute("href");
    if (!id || id === "#") return;
    const target = document.querySelector(id);
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
