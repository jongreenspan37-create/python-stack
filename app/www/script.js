const result = document.getElementById("result");

document.querySelectorAll("button[data-script]").forEach((button) => {
  button.addEventListener("click", async () => {
    const name = button.dataset.script;
    result.textContent = `Running ${name}...`;
    try {
      const res = await fetch(`/api/run/${name}`);
      console.log(`/api/run/${name}`)
      const data = await res.json();
      
      result.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      result.textContent = `Request failed: ${err}`;
    }
  });
});

document.getElementById("add-user-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.target;
  const body = {
    firstName: form.firstName.value,
    lastName: form.lastName.value,
    email: form.email.value,
  };

  result.textContent = "Adding user...";
  try {
    const res = await fetch("/api/run/add_user/add_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    result.textContent = JSON.stringify(data, null, 2);
    if (data.status === "ok") {
      form.reset();
    }
  } catch (err) {
    result.textContent = `Request failed: ${err}`;
  }
});
