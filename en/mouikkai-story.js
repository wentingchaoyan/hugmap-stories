const builderDialog = document.querySelector("#builderDialog");
const miniResult = document.querySelector("#miniResult");
document.querySelector("#openBuilder")?.addEventListener("click", () => builderDialog?.showModal());
document.querySelector("#makeMiniBook")?.addEventListener("click", () => {
  const selected = [...builderDialog.querySelectorAll("input:checked")].map((input) => input.value);
  miniResult.hidden = false;
  miniResult.innerHTML = selected.length
    ? `<strong>Ways of communicating you noticed:</strong> ${selected.join(", ")}<br>1. Watch the gaze and what happens before and after. 2. Wait briefly for the next signal. 3. Check with the child: “Up?” “No?” “Again?” The same movement can have more than one meaning, so keep exploring together by watching the response.`
    : "It is okay not to know yet. When a favorite activity stops, watch the child's eyes, hands, and body, then wait briefly for the next signal.";
});
