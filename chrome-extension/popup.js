document.addEventListener("DOMContentLoaded", function () {
    const slangInput = document.getElementById("slangInput");
    const translateBtn = document.getElementById("translateBtn");
    const translatedText = document.getElementById("translatedText");
    const dictionaryBtn = document.getElementById("dictionaryBtn");
    const adminBtn = document.getElementById("adminBtn");

    // 번역 버튼 클릭 시 애니메이션 효과 추가
    translateBtn.addEventListener("mousedown", function () {
        translateBtn.style.transform = "scale(0.95)";
    });

    translateBtn.addEventListener("mouseup", function () {
        translateBtn.style.transform = "scale(1)";
    });

    // 번역 버튼 클릭 시 API 호출
    translateBtn.addEventListener("click", async function () {
        const slang = slangInput.value.trim();
        if (slang === "") {
            alert("번역할 내용을 입력하세요!");
            return;
        }

        // 버튼 로딩 스타일 추가
        translateBtn.textContent = "번역 중...";
        translateBtn.disabled = true;

        try {
            // OpenAI API 또는 로컬 DB에서 번역 요청
            const response = await fetch("http://localhost:8000/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ word: slang })
            });

            const result = await response.json();
            translatedText.textContent = result.translation;

            // 결과 애니메이션 추가
            translatedText.style.opacity = "0";
            setTimeout(() => {
                translatedText.style.opacity = "1";
                translatedText.style.transition = "opacity 0.5s ease-in-out";
            }, 100);

        } catch (error) {
            console.error("번역 요청 오류:", error);
            translatedText.textContent = "번역 실패 😢";
        } finally {
            translateBtn.textContent = "번역";
            translateBtn.disabled = false;
        }
    });

    // 신조어 사전 버튼 클릭 시 페이지 이동
    dictionaryBtn.addEventListener("click", function () {
        window.location.href = "dictionary.html";
    });

    adminBtn.addEventListener("click", function () {
        window.location.href = "admin.html";
    });
});

