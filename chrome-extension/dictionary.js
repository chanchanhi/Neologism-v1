document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const searchBtn = document.getElementById("searchBtn");
    const dictionaryTable = document.getElementById("dictionaryTable");
    const backBtn = document.getElementById("backBtn");

    // 검색 버튼 클릭 시 API 호출
    searchBtn.addEventListener("click", async function () {
        const query = searchInput.value.trim();
        if (query === "") {
            alert("검색어를 입력하세요!");
            return;
        }

        // 신조어 검색 API 호출
        const response = await fetch(`http://localhost:8000/dictionary/search?word=${query}`);
        const result = await response.json();

        // 테이블 초기화
        dictionaryTable.innerHTML = "";

        result.forEach(entry => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.initial}</td>
                <td>${entry.word}</td>
                <td>${entry.translation}</td>
                <td><button class="editBtn" data-word="${entry.word}">수정</button></td>
            `;
            dictionaryTable.appendChild(row);
        });
    });

    // 수정 버튼 클릭 이벤트 위임
    dictionaryTable.addEventListener("click", async function (event) {
        if (event.target.classList.contains("editBtn")) {
            const word = event.target.dataset.word;
            const newTranslation = prompt(`${word}의 새로운 번역을 입력하세요:`);
            if (newTranslation) {
                await fetch("http://localhost:8000/dictionary/update", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ word: word, translation: newTranslation })
                });
                alert("번역이 업데이트되었습니다!");
                searchBtn.click(); // 검색 버튼 다시 클릭하여 업데이트된 데이터 표시
            }
        }
    });

    // 돌아가기 버튼 클릭 시 팝업 페이지로 이동
    backBtn.addEventListener("click", function () {
        window.location.href = "popup.html";
    });
});
