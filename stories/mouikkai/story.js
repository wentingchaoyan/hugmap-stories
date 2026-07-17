const builderDialog = document.querySelector("#builderDialog");
const miniResult = document.querySelector("#miniResult");

document.querySelector("#openBuilder")?.addEventListener("click", () => builderDialog?.showModal());

document.querySelector("#makeMiniBook")?.addEventListener("click", () => {
  const selected = [...builderDialog.querySelectorAll("input:checked")].map((input) => input.value);
  miniResult.hidden = false;
  miniResult.innerHTML = selected.length
    ? `<strong>見つけた「伝える」：</strong>${selected.join("・")}<br>①その前後と視線を見る　②次のサインを少し待つ　③「抱っこ？」「いや？」「もういっかい？」と本人に確かめる。同じ動きでも意味は一つとは限りません。反応を見ながら一緒に探してみましょう。`
    : "まだ分からなくても大丈夫です。まずは、好きな遊びが止まったときの目・手・身体を見て、次のサインが出るまで少し待ってみましょう。";
});
