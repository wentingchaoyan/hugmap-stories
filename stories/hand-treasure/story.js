const storyPanels = [...document.querySelectorAll(".panel")];

const sceneObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting && entry.intersectionRatio > 0.42) {
      entry.target.classList.add("is-visible");
      const step = Number(entry.target.dataset.step || 0);
      const total = Number(document.body.dataset.storyPages || 1);
      document.documentElement.style.setProperty("--story-progress", `${Math.min(step, total) / total * 100}%`);
    }
  });
}, { threshold: [0.42, 0.7] });

storyPanels.forEach((panel) => sceneObserver.observe(panel));

requestAnimationFrame(() => document.querySelector("#cover")?.classList.add("is-visible"));
