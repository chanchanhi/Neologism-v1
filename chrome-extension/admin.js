document.addEventListener("DOMContentLoaded", async function () {
    const adminTable = document.getElementById("adminTable");
    const backBtn = document.getElementById("backBtn");
    // ✅ 승인 대기 신조어 가져오기
    async function fetchPending() {
        try {
            const response = await fetch("http://localhost:8000/admin/pending");
            const data = await response.json();
            renderTable(data);
        } catch (err) {
            console.error("승인 대기 목록 불러오기 실패:", err);
        }
    }

    // ✅ 테이블 렌더링
    function renderTable(data) {
        adminTable.innerHTML = "";
        data.forEach(entry => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${entry.word}</td>
                <td>${entry.translation}</td>
                <td>${entry.pending_translation || "-"}</td>
                <td>${entry.request_type || "-"}</td> <!-- ✅ 요청 종류 표시 -->
                <td>
                    <button class="approveBtn" data-id="${entry.id}">✅</button>
                    <button class="rejectBtn" data-id="${entry.id}">🚫</button>
                </td>
            `;
            adminTable.appendChild(row);
        });
    }

    // 승인 & 거부 버튼 처리
    adminTable.addEventListener("click", async function (event) {
        const id = event.target.dataset.id;

        if (event.target.classList.contains("approveBtn")) {
            await fetch(`http://localhost:8000/admin/approve/${id}`, {
                method: "POST",
            });
            alert("✅ 승인 완료!");
            fetchPending();
        }

        if (event.target.classList.contains("rejectBtn")) {
            const confirmReject = confirm("🚫 정말 거부하시겠습니까?");
            if (confirmReject) {
                await fetch(`http://localhost:8000/admin/reject/${id}`, {
                    method: "POST",
                });
                alert("요청이 거부되었습니다.");
                fetchPending();
            }
        }
    });

    backBtn.addEventListener("click", function () {
        window.location.href = "popup.html";
    });

    // ✅ 페이지 로딩 시 데이터 불러오기
    fetchPending();
});
