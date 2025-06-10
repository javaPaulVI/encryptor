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
    output.textContent = "Please enter a token to decrypt.";
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
      output.textContent = `Message: ${data.message}\nTimestamp: ${data.timestamp}`;
    } else {
      output.textContent = `Error: ${data.error}`;
    }
  } catch (error) {
    output.textContent = `Network error: ${error.message}`;
  }
}
