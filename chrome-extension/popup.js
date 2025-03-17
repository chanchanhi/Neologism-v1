document.addEventListener("DOMContentLoaded", function () {
    const slangInput = document.getElementById("slangInput");
    const translateBtn = document.getElementById("translateBtn");
    const translatedText = document.getElementById("translatedText");
    const dictionaryBtn = document.getElementById("dictionaryBtn");

    // 번역 버튼 클릭 시 API 호출
    translateBtn.addEventListener("click", async function () {
        const slang = slangInput.value.trim();
        if (slang === "") {
            alert("신조어를 입력하세요!");
            return;
        }

        // OpenAI API 또는 로컬 DB에서 번역 요청
        const response = await fetch("http://localhost:8000/translate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ word: slang })
        });

        const result = await response.json();
        translatedText.textContent = result.translation;
    });

    // 신조어 사전 버튼 클릭 시 사전 페이지로 이동
    dictionaryBtn.addEventListener("click", function () {
        window.location.href = "dictionary.html";
    });
});
