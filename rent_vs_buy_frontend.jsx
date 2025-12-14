# 🏠 Housekeepers Frontend README (Web-Friendly Version)

## Overview
**Housekeepers** is a cute, user-friendly React frontend for deciding whether to rent or buy in New York. It connects to a backend ML model via Docker and can display Tableau dashboards.

---

## Steps to Download, Open, and Run Locally (No Command Line Outside VS Code Needed)

### 1. Download the Project
1. Go to your GitHub repository in your browser.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Extract the ZIP file into a folder on your computer.

### 2. Open the Project in VS Code
1. Install **VS Code** if you don’t have it: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Open VS Code.
3. Click **File → Open Folder** and select the folder where you extracted the project.

### 3. Ensure Node.js is Installed
- Download Node.js: [https://nodejs.org/](https://nodejs.org/)
- Install it using default options.
- Confirm installation by opening a VS Code terminal and typing:
  ```
  node -v
  npm -v
  ```
  You should see version numbers for both Node.js and npm.

### 4. Install Project Dependencies
1. In VS Code, open the **Terminal → New Terminal**.
2. Make sure you are in the folder containing `package.json` (the root of the extracted project).
3. Run:
   ```
npm install
   ```
   ⚠️ **Common Issue:** `ENOENT` errors occur if you are not in the folder with `package.json`. Ensure `package.json` is visible in the Explorer.

### 5. Run the Project
- If your `package.json` does **not** have a `dev` script, use Vite directly:
  ```
npx vite
  ```
- The terminal will show a local URL (e.g., `http://localhost:5173`).
- Open this URL in your browser to view the frontend.

### 6. Using the Frontend
- Select your **county**, **down payment**, and **lifestyle**.
- Click **Ask the Housekeepers ✨**.
- Currently, it uses a temporary demo calculation (`calculateBreakevenFallback()`). Once the Docker ML backend is connected, predictions will come from your model.

### 7. Connecting Docker Backend
- In the component where you fetch predictions, replace the fallback function with a fetch call to your Docker API:
```javascript
// Example placeholder:
// const response = await fetch('http://localhost:5000/predict', {
//   method: 'POST',
//   body: JSON.stringify({ county, downPayment, lifestyle }),
//   headers: { 'Content-Type': 'application/json' }
// });
// const data = await response.json();
// setPrediction(data.prediction);
```
- Ensure your teammates run the Docker container locally before using the frontend.

### 8. Connecting Tableau Dashboard
- Publish your dashboard on Tableau Public.
- Embed it with an `<iframe>` inside the component (see comments in `RentVsBuyChat.jsx`).

### Notes
- Keep `calculateBreakevenFallback()` for demo purposes; it will be replaced by the backend.
- Only the listed New York counties are included.
- Make the UI cozy and cute to match the “Housekeepers” theme.

---

## Troubleshooting
- **ENOENT npm error**: Usually means `npm` cannot find `package.json`. Ensure you are running `npm install` inside the folder that contains `package.json`.
- If `package.json` is missing, make sure you downloaded the correct repository ZIP or cloned the repo properly.
- Use `npx vite` if there is no `dev` script.
- Check Node.js installation if npm commands are not recognized.
- Browser 404 at localhost:5173: Wait for Vite server to be ready, then open `http://localhost:5173/` exactly in your browser.

---

## GitHub Tips for Teammates
1. Clone the repo or download the ZIP.
2. Ensure Node.js is installed.
3. Open in VS Code and run `npm install`.
4. Start Vite server with `npm run dev` or `npx vite`.
5. Open `http://localhost:5173/` to access the frontend.
