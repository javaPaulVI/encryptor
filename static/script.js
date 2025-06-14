document.addEventListener('DOMContentLoaded', () => {
  const encryptBtn = document.getElementById('encryptBtn');
  const decryptBtn = document.getElementById('decryptBtn');

  encryptBtn.onclick = encryptMessage;
  decryptBtn.onclick = decryptMessage;
});

async function encryptMessage() {
  const message = document.getElementById('messageInput').value;
  const output = document.getElementById('encryptedOutput');

  if (!message.trim()) {
    output.textContent = "Please enter a message to encrypt.";
    return;
  }

  try {
    const response = await fetch('/encrypt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    if (response.ok) {
      output.textContent = data.encrypted;
    } else {
      output.textContent = `Error: ${data.error}`;
    }
  } catch (error) {
    output.textContent = `Network error: ${error.message}`;
  }
}

async function decryptMessage() {
  const token = document.getElementById('tokenInput').value;
  const output = document.getElementById('decryptedOutput');

  if (!token.trim()) {
    output.innerHTML = `<div id="Error" class="output-box">Please Enter a token to decrypt</div>`;
    return;
  }

  try {
    const response = await fetch('/decrypt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token }),
    });

    const data = await response.json();

    if (response.ok) {
      output.innerHTML = `        <div id="decryptedOutputMessage" class="output-box">${data.message}</div>
        <div id="decryptedOutputTime" class="output-box">Time of Encryption: ${new Date(data.timestamp).toLocaleString()}</div>`;
    } else {
      output.innerHTML = `<div id="Error" class="output-box">Error: ${data.error}</div>`;
    }
  } catch (error) {
    output.innerHTML = `<div id="Error" class="output-box">Network error: ${error.message}</div>`;
  }
}
