document.addEventListener("DOMContentLoaded", function () {

    const signupForm = document.getElementById("signupForm");

    if (!signupForm) {
        console.error("signupForm not found!");
        return;
    }

    signupForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const full_name = document.getElementById("fullname").value;
        const email = document.getElementById("email").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {

            const response = await fetch("/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    full_name: full_name,
                    email: email,
                    username: username,
                    password: password
                })
            });

            const result = await response.json();

            alert(result.message);

            if (response.ok) {
                window.location.href = "/login";
            }

        } catch (error) {
            console.error("Signup error:", error);
            alert("Something went wrong. Please try again.");
        }
    });

});
