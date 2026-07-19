const scriptedScenes = [...document.querySelectorAll(".panel[data-motion]")];

if (scriptedScenes.length) {
  const sceneObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && entry.intersectionRatio >= 0.42) {
        entry.target.classList.add("is-story-visible");
      }
    });
  }, { threshold: [0.42, 0.7] });

  scriptedScenes.forEach((scene) => sceneObserver.observe(scene));
  scriptedScenes.filter((scene) => scene.getBoundingClientRect().top < innerHeight).forEach((scene) => scene.classList.add("is-story-visible"));
  requestAnimationFrame(() => document.body.classList.add("story-scenes-ready"));
}
