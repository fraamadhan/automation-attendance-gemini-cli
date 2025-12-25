# 🚀 Automation Attendance with Gemini AI

This project was inspired by my friend **Dewa**. Automate your daily internship or work presence logs using Google’s Gemini AI. This tool takes your short keypoints and expands them into professional, 100+ character descriptions required by the portal.

---

## 🛠 Setup Instructions

### 1. Install the Gemini CLI

This automation relies on the Gemini CLI to process your notes and the Python backend to serve them to your browser.

1.  **Install Gemini CLI via NPM:**
    Open your terminal and run: [gemini cli installation](https://geminicli.com/docs/get-started/installation/)

    ```bash
    npm install -g @google/gemini-cli
    ```

    _Follow the on-screen instructions after installation to authenticate and configure your API key._

2.  **Setup the Vanilla Python Server:**
    Since the Python code is vanilla, you just need to ensure you have `python-dotenv` if you are using a `.env` file:

    ```bash
    pip install python-dotenv
    ```

3.  **Configure Environment:**
    Create a `.env` file in your project root:

    ```env
    PORT=8000
    ```

4.  **Launch the Server:**
    Run your local server. This acts as the bridge for Tampermonkey:
    ```bash
    python main.py
    ```

### 2. Add Tampermonkey Extension

1.  Install the **Tampermonkey** extension for your browser ([Chrome Web Store](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)).
2.  **Crucial Step:** Open your browser's extension management (`chrome://extensions`), find Tampermonkey, and toggle **"Allow access to file URLs"** to ON.

### 3. Prepare Your Daily Keypoints

Before using the automation, ensure your server has the data ready. Type your notes in the following format:

**Example Format:**

> `activity: -adjust response BE, -fix bug, lesson: -know to fix bug with reading approach, challenge: nothing`

### 4. Install the UserScript

1.  Open the Tampermonkey Dashboard.
2.  Click the **Utilities** tab or the **"+" (Create new script)** icon.
3.  Replace the template with the following code:

```javascript
// ==UserScript==
// @name         Automation Presence 😂
// @namespace    [http://tampermonkey.net/](http://tampermonkey.net/)
// @version      2025-12-25
// @description  Integrated presence with Gemini API
// @match        [https://monev.maganghub.kemnaker.go.id/dashboard](https://monev.maganghub.kemnaker.go.id/dashboard)*
// @grant        none
// ==/UserScript==

(function () {
  "use strict";

  const url = "http://localhost:8000/get-data-presence";

  const openForm = () => {
    const todayCell = document.querySelector("td.today-highlight.clickable-day");
    if (todayCell) {
      todayCell.click();
      return true;
    } else {
      alert("Could not find today's highlight cell. Are you on the right page?");
      return false;
    }
  };

  const getData = async () => {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Status: ${response.status}`);

      const result = await response.json();

      let activity = document.querySelector('textarea[placeholder="Tulis uraian aktivitas minimal 100 karakter"]');
      let lesson = document.querySelector('textarea[placeholder="Tulis ilmu/pembelajaran yang diperoleh minimal 100 karakter"]');
      let challenge = document.querySelector('textarea[placeholder="Tulis kendala/hambatan yang dialami minimal 100 karakter"]');

      setTextareaValue(activity, result.activity);
      setTextareaValue(lesson, result.lesson);
      setTextareaValue(challenge, result.challenge);
      console.log("Data filled successfully!");
    } catch (error) {
      console.error("Fetch Error:", error.message);
    }
  };

  const setTextareaValue = (el, value) => {
    if (!el) return;
    el.focus();
    el.value = value;
    // Trigger Vue.js data binding update
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  };

  const action = () => {
    if (openForm()) {
      setTimeout(getData, 500); // Small delay to wait for modal to pop up
    }
  };

  const btn = document.createElement("button");
  btn.innerHTML = "🚀 Fill Presence";
  btn.style = `
        position: fixed;
        top: 250px;
        right: 20px;
        z-index: 9999;
        padding: 12px 24px;
        background: linear-gradient(135deg, #007bff 0%, #00d2ff 100%);
        color: white;
        border: none;
        border-radius: 16px;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s;
    `;

  btn.addEventListener("click", action);
  document.body.appendChild(btn);
})();
```

## 5. Start Automating

1. Navigate to the Kemnaker Dashboard.

2. The 🚀 Fill Presence button will appear on the right side.

3. Click it once. The script will automatically:
   - Find today's date in the calendar.
   - Click it to open the modal.
   - Fetch the expanded text from your local Gemini server.
   - Inject the text and sync it with the portal's database.

<br>

> If you have any questions, feel free to reach out: Discord: @peculiarz or just trial and error with provided code
