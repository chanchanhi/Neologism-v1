document.addEventListener("DOMContentLoaded", async function () {
    const searchInput = document.getElementById("searchInput");
    const searchBtn = document.getElementById("searchBtn");
    const dictionaryTable = document.getElementById("dictionaryTable");
    const backBtn = document.getElementById("backBtn");
    const addWordBtn = document.getElementById("addWordBtn");
    const prevPageBtn = document.getElementById("prevPage");
    const nextPageBtn = document.getElementById("nextPage");
    const pageInfo = document.getElementById("pageInfo");

    let currentPage = 1;
    const itemsPerPage = 10;
    let allData = [];

    // ✅ 전체 신조어 목록 불러오기
    async function fetchDictionary() {
        try {
            const response = await fetch("http://localhost:8000/dictionary/search?word=");
            allData = await response.json();
            currentPage = 1;
            renderTable();
        } catch (error) {
            console.error("데이터 불러오기 실패:", error);
        }
    }

    // ✅ 테이블을 현재 페이지 기준으로 렌더링
    function renderTable() {
        dictionaryTable.innerHTML = "";
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedData = allData.slice(start, end);

        paginatedData.forEach(entry => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.initial}</td>
                <td>${entry.word}</td>
                <td>${entry.translation}</td>
                <td><button class="editBtn" data-word="${entry.word}">수정</button></td>
            `;
            dictionaryTable.appendChild(row);
        });

        updatePagination();
    }

    // ✅ 페이지네이션 업데이트 (현재 페이지 정보 갱신)
    function updatePagination() {
        const totalPages = Math.ceil(allData.length / itemsPerPage);
        pageInfo.textContent = `${currentPage} / ${totalPages}`;
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages;
    }

    // ✅ 검색 기능 (입력 시 필터링, 검색어 없으면 전체 데이터)
    searchBtn.addEventListener("click", function () {
        const query = searchInput.value.trim();
        if (query === "") {
            fetchDictionary(); // 검색어가 없으면 전체 리스트 다시 로드
        } else {
            const filteredData = allData.filter(entry => entry.word.includes(query));
            allData = filteredData;
            currentPage = 1;
            renderTable();
        }
    });

    // ✅ 이전 페이지 이동
    prevPageBtn.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
        }
    });

    // ✅ 다음 페이지 이동
    nextPageBtn.addEventListener("click", function () {
        if (currentPage < Math.ceil(allData.length / itemsPerPage)) {
            currentPage++;
            renderTable();
        }
    });

    // ✅ 번역 수정 기능 (버튼 클릭 시 수정 가능)
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
                fetchDictionary();
            }
        }
    });

    // ✅ "돌아가기" 버튼 클릭 시 팝업 페이지로 이동
    backBtn.addEventListener("click", function () {
        window.location.href = "popup.html";
    });

    // ✅ "신조어 추가" 버튼 클릭 시 추가 페이지로 이동
    addWordBtn.addEventListener("click", function () {
        window.location.href = "add_word.html";
    });

    // ✅ 페이지 로드 시 전체 신조어 목록 가져오기
    fetchDictionary();
});

