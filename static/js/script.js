document.getElementById("startBtn").addEventListener("click", () => {
  const mode = document.getElementById("mode").value;
  const status = document.getElementById("status");

  fetch("/start_detection", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ mode: mode }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        status.innerText = `Error: ${data.error}`;
      } else {
        status.innerText = data.message;
        document.getElementById("startBtn").disabled = true;
        document.getElementById("stopBtn").disabled = false;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

document.getElementById("stopBtn").addEventListener("click", () => {
  const status = document.getElementById("status");

  fetch("/stop_detection", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        status.innerText = `Error: ${data.error}`;
      } else {
        status.innerText = data.message;
        document.getElementById("startBtn").disabled = false;
        document.getElementById("stopBtn").disabled = true;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
