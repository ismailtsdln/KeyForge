// JavaScript for RPG Web Interface

// API Configuration
const API_BASE = '';

// State
let currentMode = 'password';
let currentPassword = '';

// DOM Elements
const themeToggle = document.getElementById('themeToggle');
const passwordModeBtn = document.getElementById('passwordModeBtn');
const passphraseModeBtn = document.getElementById('passphraseModeBtn');
const passwordPanel = document.getElementById('passwordPanel');
const passphrasePanel = document.getElementById('passphrasePanel');

// Password Mode Elements
const passwordDisplay = document.getElementById('passwordDisplay');
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const lengthSlider = document.getElementById('lengthSlider');
const lengthValue = document.getElementById('lengthValue');
const countSlider = document.getElementById('countSlider');
const countValue = document.getElementById('countValue');
const uppercaseCheck = document.getElementById('uppercaseCheck');
const lowercaseCheck = document.getElementById('lowercaseCheck');
const digitsCheck = document.getElementById('digitsCheck');
const specialCheck = document.getElementById('specialCheck');
const strengthSection = document.getElementById('strengthSection');
const strengthValue = document.getElementById('strengthValue');
const strengthFill = document.getElementById('strengthFill');
const strengthDetails = document.getElementById('strengthDetails');

// Passphrase Mode Elements
const passphraseDisplay = document.getElementById('passphraseDisplay');
const generatePhraseBtn = document.getElementById('generatePhraseBtn');
const copyPhraseBtn = document.getElementById('copyPhraseBtn');
const wordCountSlider = document.getElementById('wordCountSlider');
const wordCountValue = document.getElementById('wordCountValue');
const separatorInput = document.getElementById('separatorInput');
const capitalizeCheck = document.getElementById('capitalizeCheck');
const addNumberCheck = document.getElementById('addNumberCheck');
const phraseStrengthSection = document.getElementById('phraseStrengthSection');
const phraseStrengthValue = document.getElementById('phraseStrengthValue');
const phraseStrengthFill = document.getElementById('phraseStrengthFill');
const phraseStrengthDetails = document.getElementById('phraseStrengthDetails');

// Multiple Passwords
const multiplePasswords = document.getElementById('multiplePasswords');
const passwordList = document.getElementById('passwordList');

// Toast
const toast = document.getElementById('toast');
const toastText = document.getElementById('toastText');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    attachEventListeners();
});

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('.theme-icon');
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Event Listeners
function attachEventListeners() {
    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);

    // Mode switching
    passwordModeBtn.addEventListener('click', () => switchMode('password'));
    passphraseModeBtn.addEventListener('click', () => switchMode('passphrase'));

    // Password mode
    generateBtn.addEventListener('click', generatePassword);
    copyBtn.addEventListener('click', () => copyToClipboard(currentPassword));
    lengthSlider.addEventListener('input', (e) => lengthValue.textContent = e.target.value);
    countSlider.addEventListener('input', (e) => countValue.textContent = e.target.value);

    // Passphrase mode
    generatePhraseBtn.addEventListener('click', generatePassphrase);
    copyPhraseBtn.addEventListener('click', () => copyToClipboard(currentPassword));
    wordCountSlider.addEventListener('input', (e) => wordCountValue.textContent = e.target.value);

    // Auto-generate on Enter key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            if (currentMode === 'password') {
                generatePassword();
            } else {
                generatePassphrase();
            }
        }
    });
}

// Mode Switching
function switchMode(mode) {
    currentMode = mode;

    if (mode === 'password') {
        passwordModeBtn.classList.add('active');
        passphraseModeBtn.classList.remove('active');
        passwordPanel.classList.add('active');
        passphrasePanel.classList.remove('active');
    } else {
        passphraseModeBtn.classList.add('active');
        passwordModeBtn.classList.remove('active');
        passphrasePanel.classList.add('active');
        passwordPanel.classList.remove('active');
    }

    multiplePasswords.style.display = 'none';
}

// Password Generation
async function generatePassword() {
    const length = parseInt(lengthSlider.value);
    const count = parseInt(countSlider.value);
    const useUppercase = uppercaseCheck.checked;
    const useLowercase = lowercaseCheck.checked;
    const useDigits = digitsCheck.checked;
    const useSpecial = specialCheck.checked;

    if (!useUppercase && !useLowercase && !useDigits && !useSpecial) {
        showToast('Please select at least one character type', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                length,
                count,
                use_uppercase: useUppercase,
                use_lowercase: useLowercase,
                use_digits: useDigits,
                use_special: useSpecial
            })
        });

        const data = await response.json();

        if (data.success) {
            if (count === 1) {
                currentPassword = data.passwords[0];
                displayPassword(currentPassword);
                await analyzeStrength(currentPassword);
                multiplePasswords.style.display = 'none';
            } else {
                displayMultiplePasswords(data.passwords);
                currentPassword = data.passwords[0];
                strengthSection.style.display = 'none';
            }
        } else {
            showToast(data.error || 'Failed to generate password', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
        console.error(error);
    }
}

// Passphrase Generation
async function generatePassphrase() {
    const wordCount = parseInt(wordCountSlider.value);
    const separator = separatorInput.value || '-';
    const capitalize = capitalizeCheck.checked;
    const includeNumber = addNumberCheck.checked;

    try {
        const response = await fetch(`${API_BASE}/api/passphrase`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                word_count: wordCount,
                separator,
                capitalize,
                include_number: includeNumber
            })
        });

        const data = await response.json();

        if (data.success) {
            currentPassword = data.passphrase;
            displayPassphrase(currentPassword);
            await analyzeStrength(currentPassword, true);
        } else {
            showToast(data.error || 'Failed to generate passphrase', 'error');
        }
    } catch (error) {
        showToast('Network error. Please try again.', 'error');
        console.error(error);
    }
}

// Display Functions
function displayPassword(password) {
    passwordDisplay.innerHTML = `<span style="color: var(--text-primary)">${escapeHtml(password)}</span>`;
    animateElement(passwordDisplay);
}

function displayPassphrase(passphrase) {
    passphraseDisplay.innerHTML = `<span style="color: var(--text-primary)">${escapeHtml(passphrase)}</span>`;
    animateElement(passphraseDisplay);
}

function displayMultiplePasswords(passwords) {
    multiplePasswords.style.display = 'block';
    passwordList.innerHTML = '';

    passwords.forEach((pwd, index) => {
        const item = document.createElement('div');
        item.className = 'password-item';
        item.innerHTML = `
            <span>${escapeHtml(pwd)}</span>
            <button onclick="copyToClipboard('${escapeHtml(pwd)}')" style="background: none; border: none; cursor: pointer; font-size: 1.2rem;">📋</button>
        `;
        passwordList.appendChild(item);
    });

    animateElement(multiplePasswords);
}

// Strength Analysis
async function analyzeStrength(password, isPassphrase = false) {
    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });

        const data = await response.json();

        if (data.success) {
            const section = isPassphrase ? phraseStrengthSection : strengthSection;
            const valueElem = isPassphrase ? phraseStrengthValue : strengthValue;
            const fillElem = isPassphrase ? phraseStrengthFill : strengthFill;
            const detailsElem = isPassphrase ? phraseStrengthDetails : strengthDetails;

            const analysis = data.analysis;

            // Update strength display
            valueElem.textContent = `${analysis.strength} (${analysis.score}/100)`;
            fillElem.style.width = `${analysis.score}%`;

            // Set color based on score
            const color = getStrengthColor(analysis.score);
            fillElem.style.background = color;
            valueElem.style.color = color;

            // Update details
            let details = `
                <div><strong>Length:</strong> ${analysis.length} characters</div>
                <div><strong>Entropy:</strong> ${analysis.entropy} bits</div>
            `;

            if (analysis.feedback && analysis.feedback.length > 0) {
                details += `<div style="margin-top: 10px;"><strong>Feedback:</strong></div>`;
                analysis.feedback.forEach(fb => {
                    details += `<div style="margin-left: 10px;">• ${fb}</div>`;
                });
            }

            detailsElem.innerHTML = details;
            section.style.display = 'block';
            animateElement(section);
        }
    } catch (error) {
        console.error('Failed to analyze strength:', error);
    }
}

// Utility Functions
function copyToClipboard(text) {
    if (!text) {
        showToast('Nothing to copy!', 'error');
        return;
    }

    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard! ✓');
    }).catch(() => {
        // Fallback method
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('Copied to clipboard! ✓');
    });
}

function showToast(message, type = 'success') {
    toastText.textContent = message;

    if (type === 'error') {
        toast.style.background = 'var(--danger)';
    } else {
        toast.style.background = 'var(--success)';
    }

    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function getStrengthColor(score) {
    if (score < 20) return '#ef4444';  // Red
    if (score < 40) return '#f97316';  // Orange
    if (score < 60) return '#eab308';  // Yellow
    if (score < 80) return '#84cc16';  // Light green
    return '#22c55e';  // Green
}

function animateElement(element) {
    element.style.animation = 'none';
    setTimeout(() => {
        element.style.animation = 'fadeIn 0.4s ease';
    }, 10);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make copyToClipboard available globally for inline onclick
window.copyToClipboard = copyToClipboard;
