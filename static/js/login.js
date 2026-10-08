document
  .getElementById("loginForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.querySelector("input[name=username]").value;

    const password = document.querySelector("input[name=password]").value;

    const response = await fetch("/login", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    const result = await response.json();

    if (result.message === "Login Successful") {
      window.location.href = "/profile";
    } else {
      alert(result.message);
    }
  });
