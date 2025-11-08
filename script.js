const yearEl = document.getElementById("year");
if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

const revealElements = document.querySelectorAll(".reveal");
if (revealElements.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  revealElements.forEach((el) => observer.observe(el));
}

const form = document.getElementById("contact-form");
if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const name = formData.get("name");
    const email = formData.get("email");
    const message = formData.get("message");

    const subject = `Ny forespørsel via OH AUDIO fra ${name}`;
    const body = `Navn: ${name}%0D%0AE-post: ${email}%0D%0A%0D%0AProsjekt:%0D%0A${message}`;
    const mailto = `mailto:olve.husby@gmail.com?subject=${encodeURIComponent(
      subject
    )}&body=${body}`;

    window.location.href = mailto;
  });
}

(function enableLiveReload() {
  const localHosts = ["localhost", "127.0.0.1"];
  if (!localHosts.includes(window.location.hostname)) {
    return;
  }

  let lastToken = null;

  const poll = async () => {
    try {
      const response = await fetch("/__livereload", { cache: "no-store" });
      if (!response.ok) {
        return;
      }
      const data = await response.json();
      if (lastToken && data.token !== lastToken) {
        window.location.reload();
      }
      lastToken = data.token;
    } catch (error) {
      // Suppress errors when the server is restarting
    }
  };

  poll();
  setInterval(poll, 1200);
})();
