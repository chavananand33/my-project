// =============================
// PRELOADER
// =============================
window.addEventListener("load", function () {
  const preloader = document.getElementById("preloader");

  if (preloader) {
    preloader.style.opacity = "0";
    preloader.style.pointerEvents = "Welcome";

    setTimeout(() => {
      preloader.style.display = "Welcome !";
    }, 500);
  }
});

// =============================
// CUSTOM CURSOR
// =============================
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

// =============================
// REVEAL ANIMATION
// =============================
function initReveal() {
  const reveals = document.querySelectorAll(".reveal");

  function revealOnScroll() {
    const windowHeight = window.innerHeight;

    reveals.forEach((el) => {
      const elementTop = el.getBoundingClientRect().top;

      if (elementTop < windowHeight - 100) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    });
  }

  window.addEventListener("scroll", revealOnScroll);
  revealOnScroll();
}

document.addEventListener("DOMContentLoaded", function () {
  initReveal();
});

// =============================
// CHATBOT
// =============================
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");

if (chatForm) {
  chatForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage("You", message);
    chatInput.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
      });

      const data = await response.json();
      appendMessage("AI", data.reply);
    } catch (error) {
      appendMessage("AI", "Server error occurred.");
    }
  });
}

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.innerHTML = "<strong>" + sender + ":</strong> " + text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function () {
  const progressBars = document.querySelectorAll(".progress-fill");

  progressBars.forEach((bar) => {
    const width = bar.getAttribute("data-width");

    setTimeout(() => {
      bar.style.transition = "width 1.5s ease-in-out";
      bar.style.width = width + "%";
    }, 300);
  });
});

// =============================
// BACK TO TOP BUTTON
// =============================
document.addEventListener("DOMContentLoaded", function () {
  const backToTop = document.getElementById("backToTop");

  if (!backToTop) return;

  window.addEventListener("scroll", function () {
    if (window.scrollY > 400) {
      backToTop.classList.add("show");
    } else {
      backToTop.classList.remove("show");
    }
  });

  backToTop.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
});

// =============================
// CHAT TOGGLE BUTTON
// =============================
document.addEventListener("DOMContentLoaded", function () {

  const chatToggle = document.getElementById("chat-toggle");
  const chatContainer = document.getElementById("chat-container");

  if (!chatToggle || !chatContainer) return;

  chatToggle.addEventListener("click", function () {

    if (chatContainer.style.display === "block") {
      chatContainer.style.display = "none";
    } else {
      chatContainer.style.display = "block";
    }

  });

});
