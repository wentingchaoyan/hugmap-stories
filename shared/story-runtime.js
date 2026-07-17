const panels = [...document.querySelectorAll("[data-step]")];
const progressFill = document.querySelector("#progressFill");
const progressCount = document.querySelector("#progressCount");
const progressLabel = document.querySelector("#progressLabel");
const textToggle = document.querySelector("#textToggle");
const motionToggle = document.querySelector("#motionToggle");
const storyPages = Number(document.body.dataset.storyPages || 1);

const observer = new IntersectionObserver(
  (entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!visible) return;

    const step = Number(visible.target.dataset.step);
    const storyStep = Math.min(step, storyPages);
    const isAfterword = visible.target.id === "afterword";
    progressFill.style.width = `${(storyStep / storyPages) * 100}%`;
    progressCount.textContent = isAfterword ? "おわり" : `${storyStep} / ${storyPages}`;
    progressLabel.textContent = visible.target.dataset.label || (step === 0 ? "はじまり" : isAfterword ? "おはなしのあとに" : `${storyStep}ページ`);
    history.replaceState(null, "", `#${visible.target.id}`);
  },
  { threshold: [0.45, 0.7] },
);

panels.forEach((panel) => observer.observe(panel));

textToggle?.addEventListener("click", () => {
  const next = document.body.classList.toggle("large-text");
  textToggle.setAttribute("aria-pressed", String(next));
  textToggle.textContent = next ? "文字をもどす" : "文字を大きく";
});

motionToggle?.addEventListener("click", () => {
  const next = document.body.classList.toggle("reduce-motion");
  motionToggle.setAttribute("aria-pressed", String(next));
  motionToggle.textContent = next ? "動きをもどす" : "動きを減らす";
});

document.querySelector("#restart")?.addEventListener("click", () => {
  document.querySelector("#cover")?.scrollIntoView({ behavior: "smooth" });
});

if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.body.classList.add("reduce-motion");
  motionToggle?.setAttribute("aria-pressed", "true");
  if (motionToggle) motionToggle.textContent = "動きをもどす";
}
