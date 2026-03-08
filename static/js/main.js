// =============================
// PRELOADER
// =============================
window.addEventListener("load", function () {
  const preloader = document.getElementById("preloader");

  if (preloader) {
    preloader.style.opacity = "0";
    preloader.style.pointerEvents = "none";

    setTimeout(() => {
      preloader.style.display = "none";
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
// APPEND MESSAGE FUNCTION
// =============================
function appendMessage(sender, message) {

  const chatBox = document.getElementById("chat-box");

  if (!chatBox) return;

  const msg = document.createElement("div");

  if (sender === "You") {
    msg.classList.add("chat-message", "user");
    msg.innerHTML = "<strong>You:</strong> " + message;
  } else {
    msg.classList.add("chat-message", "bot");
    msg.innerHTML = "<strong>AI:</strong> " + message;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// =============================
// CHATBOT
// =============================
document.addEventListener("DOMContentLoaded", function () {

  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const chatBox = document.getElementById("chat-box");

  if (!chatForm || !chatInput || !chatBox) return;

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

      const typing = document.createElement("div");
      typing.classList.add("typing");
      typing.innerHTML = "AI is typing...";
      chatBox.appendChild(typing);

      chatBox.scrollTop = chatBox.scrollHeight;

      setTimeout(() => {
        typing.remove();
        appendMessage("AI", data.reply);
      }, 800);

    } catch (error) {
      appendMessage("AI", "Server error occurred.");
    }
  });

  // ENTER KEY SEND
  chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      chatForm.requestSubmit();
    }
  });

});

// =============================
// PROGRESS BAR
// =============================
document.addEventListener("DOMContentLoaded", function () {

  const progressBars = document.querySelectorAll(".progress-fill");

  progressBars.forEach((bar) => {
    const width = bar.getAttribute("data-width");

    setTimeout(() => {
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
// CHAT TOGGLE
// =============================
document.addEventListener("DOMContentLoaded", function () {

  const chatBtn = document.getElementById("chat-toggle");
  const chatContainer = document.getElementById("chat-container");

  if (!chatBtn || !chatContainer) return;

  chatBtn.addEventListener("click", function () {

    if (chatContainer.style.display === "block") {
      chatContainer.style.display = "none";
    } else {
      chatContainer.style.display = "block";
    }

  });

});

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
