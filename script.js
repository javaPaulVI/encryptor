const encryptBtn = document.getElementById('encrypt-btn');
const decryptBtn = document.getElementById('decrypt-btn');
const encryptMessageInput = document.getElementById('encrypt-message');
const decryptTokenInput = document.getElementById('decrypt-token');
const encryptResult = document.getElementById('encrypt-result');
const decryptResult = document.getElementById('decrypt-result');

async function encryptMessage() {
    const message = encryptMessageInput.value.trim();
    encryptResult.textContent = '';
    if (!message) {
        encryptResult.textContent = 'Please enter a message to encrypt.';
        encryptResult.classList.add('error');
        return;
    }

    try {
        const response = await fetch('/encrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (response.ok) {
            encryptResult.textContent = data.encrypted;
            encryptResult.classList.remove('error');
        } else {
            encryptResult.textContent = data.error || 'Encryption failed.';
            encryptResult.classList.add('error');
        }
    } catch (err) {
        encryptResult.textContent = 'Network error or server not reachable.';
        encryptResult.classList.add('error');
    }
}

async function decryptToken() {
    const token = decryptTokenInput.value.trim();
    decryptResult.textContent = '';
    if (!token) {
        decryptResult.textContent = 'Please enter a token to decrypt.';
        decryptResult.classList.add('error');
        return;
    }

    try {
        const response = await fetch('/decrypt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token })
        });

        const data = await response.json();

        if (response.ok) {
            decryptResult.textContent = `Message: ${data.message}\nTimestamp: ${data.timestamp}`;
            decryptResult.classList.remove('error');
        } else {
            decryptResult.textContent = data.error || 'Decryption failed.';
            decryptResult.classList.add('error');
        }
    } catch (err) {
        decryptResult.textContent = 'Network error or server not reachable.';
        decryptResult.classList.add('error');
    }
}

encryptBtn.onclick = encryptMessage;
decryptBtn.onclick = decryptToken;
