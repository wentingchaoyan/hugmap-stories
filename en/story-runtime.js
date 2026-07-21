const panels = [...document.querySelectorAll("[data-step]")];
const progressFill = document.querySelector("#progressFill");
const progressCount = document.querySelector("#progressCount");
const progressLabel = document.querySelector("#progressLabel");
const textToggle = document.querySelector("#textToggle");
const motionToggle = document.querySelector("#motionToggle");
const storyPages = Number(document.body.dataset.storyPages || 1);

const observer = new IntersectionObserver((entries) => {
  const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (!visible) return;
  const step = Number(visible.target.dataset.step);
  const storyStep = Math.min(step, storyPages);
  const isAfterword = visible.target.id === "afterword";
  progressFill.style.width = `${(storyStep / storyPages) * 100}%`;
  progressCount.textContent = isAfterword ? "End" : `${storyStep} / ${storyPages}`;
  progressLabel.textContent = visible.target.dataset.label || (step === 0 ? "Start" : isAfterword ? "After the story" : `Page ${storyStep}`);
  history.replaceState(null, "", `#${visible.target.id}`);
}, { threshold: [0.45, 0.7] });

panels.forEach((panel) => observer.observe(panel));
textToggle?.addEventListener("click", () => {
  const next = document.body.classList.toggle("large-text");
  textToggle.setAttribute("aria-pressed", String(next));
  textToggle.textContent = next ? "Default text" : "Larger text";
});
motionToggle?.addEventListener("click", () => {
  const next = document.body.classList.toggle("reduce-motion");
  motionToggle.setAttribute("aria-pressed", String(next));
  motionToggle.textContent = next ? "Restore motion" : "Reduce motion";
});
document.querySelector("#restart")?.addEventListener("click", () => document.querySelector("#cover")?.scrollIntoView({ behavior: "smooth" }));
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.body.classList.add("reduce-motion");
  motionToggle?.setAttribute("aria-pressed", "true");
  if (motionToggle) motionToggle.textContent = "Restore motion";
}

const languageLink = document.createElement("a");
languageLink.href = `../../../stories/${location.pathname.split("/").filter(Boolean).at(-2)}/index.html`;
languageLink.textContent = "日本語";
languageLink.lang = "ja";
languageLink.className = "language-switch";
document.querySelector(".story-header > div")?.prepend(languageLink);
