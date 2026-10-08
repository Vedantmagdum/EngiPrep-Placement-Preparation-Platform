
document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("chatbotToggle");
    const windowBox = document.getElementById("chatbotWindow");
    const closeButton = document.getElementById("chatbotClose");
    const messages = document.getElementById("chatbotMessages");
    const form = document.getElementById("chatbotForm");
    const input = document.getElementById("chatbotInput");
    const sendButton = document.getElementById("chatbotSend");
    const status = document.getElementById("chatbotStatus");
    const suggestions = document.getElementById("chatbotSuggestions");

    if (
        !toggle ||
        !windowBox ||
        !closeButton ||
        !messages ||
        !form ||
        !input ||
        !sendButton ||
        !status
    ) {
        return;
    }

    let history = [];
    let isSending = false;

    function openChat() {
        windowBox.classList.add("open");
        toggle.setAttribute("aria-expanded", "true");
        input.focus();
        scrollMessages();
    }

    function closeChat() {
        windowBox.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
    }

    function scrollMessages() {
        messages.scrollTop = messages.scrollHeight;
    }

    function addMessage(text, sender) {
        const bubble = document.createElement("div");

        bubble.className = "chat-message " + sender;
        bubble.textContent = text;

        messages.appendChild(bubble);
        scrollMessages();

        return bubble;
    }

    function setBusy(busy) {
        isSending = busy;
        sendButton.disabled = busy;
        input.disabled = busy;
        sendButton.textContent = busy ? "…" : "➤";
        status.textContent = busy
            ? "EngiPrep AI is thinking..."
            : "Ask about aptitude, coding, interviews or careers.";
    }

    async function sendMessage(text) {
        text = text.trim();

        if (!text || isSending) {
            return;
        }

        if (text.length > 2000) {
            addMessage(
                "Please keep your message under 2000 characters.",
                "bot"
            );
            return;
        }

        addMessage(text, "user");

        const previousHistory = history.slice(-10);

        history.push({
            role: "user",
            text: text
        });

        input.value = "";
        setBusy(true);

        const loadingBubble = addMessage(
            "Thinking...",
            "bot"
        );

        try {
            const response = await fetch("/chatbot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: text,
                    history: previousHistory
                })
            });

            const result = await response.json();

            loadingBubble.remove();

            if (!response.ok) {
                throw new Error(
                    result.reply || "The request failed."
                );
            }

            const reply = result.reply ||
                "Sorry, I could not generate a response.";

            addMessage(reply, "bot");

            history.push({
                role: "assistant",
                text: reply
            });

            history = history.slice(-10);

        } catch (error) {
            loadingBubble.remove();

            addMessage(
                error.message ||
                "Unable to connect right now. Please try again.",
                "bot"
            );

            console.error("EngiPrep chatbot error:", error);

        } finally {
            setBusy(false);
            input.focus();
        }
    }

    toggle.addEventListener("click", function () {
        if (windowBox.classList.contains("open")) {
            closeChat();
        } else {
            openChat();
        }
    });

    closeButton.addEventListener("click", closeChat);

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        sendMessage(input.value);
    });

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            form.requestSubmit();
        }
    });

    if (suggestions) {
        suggestions.addEventListener("click", function (event) {
            const button = event.target.closest("button");

            if (button && button.dataset.prompt) {
                sendMessage(button.dataset.prompt);
            }
        });
    }

    document.addEventListener("keydown", function (event) {
        if (
            event.key === "Escape" &&
            windowBox.classList.contains("open")
        ) {
            closeChat();
        }
    });

    addMessage(
        "Hi! 👋 I'm EngiPrep AI, your placement preparation assistant. Ask me about aptitude, coding, technical interviews, resumes or study plans.",
        "bot"
    );

});
