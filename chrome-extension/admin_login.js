document.addEventListener("DOMContentLoaded", function () {
    const loginBtn = document.getElementById("loginBtn");
  
    loginBtn.addEventListener("click", async function () {
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();
  
      try {
        const response = await fetch("http://localhost:8000/admin/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password })
        });
  
        if (response.ok) {
          const result = await response.json();
          localStorage.setItem("adminToken", result.token);  // ✅ 토큰 저장
          window.location.href = "admin.html";               // ✅ 이동
        } else {
          document.getElementById("errorMsg").style.display = "block";
        }
      } catch (error) {
        console.error("로그인 오류:", error);
        document.getElementById("errorMsg").textContent = "⚠️ 서버 연결 오류";
        document.getElementById("errorMsg").style.display = "block";
      }
    });
  });
  