javascript
document.addEventListener("DOMContentLoaded", function () {

    const signupForm = document.getElementById("signupForm");

    console.log("Signup JS loaded");
    console.log("Signup form:", signupForm);

    if (!signupForm) {
        console.error("signupForm not found!");
        return;
    }

    signupForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        console.log("Signup form submitted");

        const full_name = document.getElementById("fullname").value.trim();
        const email = document.getElementById("email").value.trim();
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {

            console.log("Sending signup request...");

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

            console.log("Response status:", response.status);

            const result = await response.json();

            console.log("Server response:", result);

            alert(result.message);

            if (response.ok) {
                window.location.href = "/login";
            }

        } catch (error) {

            console.error("Signup error:", error);

            alert("Unable to connect to the server.");
        }
    });
});
;
