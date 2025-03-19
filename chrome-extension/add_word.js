document.addEventListener("DOMContentLoaded", function () {
    const newWordInput = document.getElementById("newWord");
    const newMeaningInput = document.getElementById("newMeaning");
    const saveBtn = document.getElementById("saveBtn");
    const backBtn = document.getElementById("backBtn");

    // ✅ 신조어 저장 기능
    saveBtn.addEventListener("click", async function () {
        const word = newWordInput.value.trim();
        const meaning = newMeaningInput.value.trim();

        if (!word || !meaning) {
            alert("신조어와 뜻을 입력해주세요!");
            return;
        }

        // ✅ 서버에 신조어 추가 요청
        try {
            const response = await fetch("http://localhost:8000/dictionary/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ word: word, translation: meaning })
            });

            if (response.ok) {
                alert("신조어가 성공적으로 추가되었습니다!");
                window.location.href = "dictionary.html"; // 사전 페이지로 이동
            } else {
                alert("신조어 추가에 실패했습니다.");
            }
        } catch (error) {
            console.error("오류 발생:", error);
            alert("오류가 발생했습니다. 다시 시도해주세요.");
        }
    });

    // ✅ 돌아가기 버튼
    backBtn.addEventListener("click", function () {
        window.location.href = "dictionary.html";
    });
});
