/* ============================================================
   ANAND CHAVAN — Professional Portfolio Core JS
   Includes: Preloader, Custom Cursor, AI Chatbot, 
   Reveal Animations, and Navigation Logic.
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
    // 1. INITIALIZE REVEAL ANIMATIONS
    initReveal();

    // 2. NAVIGATION: SCROLL EFFECT (For Logo & Background Blur)
    const nav = document.querySelector(".nav");
    window.addEventListener("scroll", function() {
        if (window.scrollY > 50) {
            nav.classList.add("scrolled");
        } else {
            nav.classList.remove("scrolled");
        }
    });

    // 3. NAVIGATION: MOBILE MENU TOGGLE
    const navToggle = document.getElementById("navToggle");
    const navLinksContainer = document.getElementById("navLinks");
    const navLinks = document.querySelectorAll(".nav-link");

    if (navToggle && navLinksContainer) {
        navToggle.addEventListener("click", function () {
            navLinksContainer.classList.toggle("open");
            navToggle.classList.toggle("open");
        });

        // Close mobile menu when a link is clicked
        navLinks.forEach(link => {
            link.addEventListener("click", () => {
                navLinksContainer.classList.remove("open");
                navToggle.classList.remove("open");
            });
        });
    }

    // 4. SKILLS: PROGRESS BAR ANIMATION
    const progressBars = document.querySelectorAll(".progress-fill");
    progressBars.forEach((bar) => {
        const width = bar.getAttribute("data-width");
        setTimeout(() => {
            bar.style.width = width + "%";
        }, 500);
    });

    // 5. BACK TO TOP BUTTON
    const backToTop = document.getElementById("backToTop");
    if (backToTop) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 400) {
                backToTop.classList.add("show");
            } else {
                backToTop.classList.remove("show");
            }
        });

        backToTop.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // 6. ARCHITECTURE BOXES: STAGGERED ENTRANCE
    const archBoxes = document.querySelectorAll('.arch-box');
    archBoxes.forEach((box, index) => {
        box.style.opacity = "0";
        box.style.transform = "translateY(30px)";
        setTimeout(() => {
            box.style.transition = "all 0.5s ease";
            box.style.opacity = "1";
            box.style.transform = "translateY(0)";
        }, index * 200);
    });

    // 7. CHATBOT: TOGGLE & FORM LOGIC
    const chatBtn = document.getElementById("chat-toggle");
    const chatContainer = document.getElementById("chat-container");
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatBox = document.getElementById("chat-box");

    if (chatBtn && chatContainer) {
        chatBtn.addEventListener("click", function () {
            if (chatContainer.style.display === "flex") {
                chatContainer.style.display = "none";
            } else {
                chatContainer.style.display = "flex";
            }
        });
    }

    if (chatForm && chatInput && chatBox) {
        chatForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // Show User message
            appendMessage("You", message);
            chatInput.value = "";

            // Show Typing indicator
            const typing = document.createElement("div");
            typing.classList.add("chat-message", "bot", "typing");
            typing.innerHTML = `
                <div class="bot-msg">
                    <img src="/static/images/anand_chatbot_64.png" class="bot-avatar" alt="AI">
                    <div class="msg-content">
                        <strong>AI:</strong> <span class='dot-flashing'>...</span>
                    </div>
                </div>`;
            chatBox.appendChild(typing);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();

                setTimeout(() => {
                    typing.remove();
                    appendMessage("AI", data.response);
                }, 600);
            } catch (error) {
                typing.remove();
                appendMessage("AI", "I'm having a bit of trouble connecting to my brain. Try again?");
            }
        });
    }
});

/* ============================================================
   HELPER FUNCTIONS (Global Scope)
   ============================================================ */

// PRELOADER LOGIC
window.addEventListener("load", function () {
    const preloader = document.getElementById("preloader");
    if (preloader) {
        preloader.style.opacity = "0";
        preloader.style.pointerEvents = "none";
        setTimeout(() => { preloader.style.display = "none"; }, 500);
    }
});

// CUSTOM CURSOR LOGIC
const cursor = document.getElementById("cursor");
const follower = document.getElementById("cursorFollower");
if (cursor && follower) {
    document.addEventListener("mousemove", (e) => {
        cursor.style.left = e.clientX + "px";
        cursor.style.top = e.clientY + "px";
        follower.style.left = e.clientX + "px";
        follower.style.top = e.clientY + "px";
    });
}

// REVEAL ON SCROLL LOGIC
function initReveal() {
    const reveals = document.querySelectorAll(".reveal");
    function revealOnScroll() {
        const windowHeight = window.innerHeight;
        reveals.forEach((el) => {
            const elementTop = el.getBoundingClientRect().top;
            if (elementTop < windowHeight - 100) {
                el.classList
