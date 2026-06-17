# 📸 SIMPEL – Documentation & Screenshots

This folder contains the **visual documentation** of the SIMPEL application for the USAII 2026 hackathon submission.

---

## 🖼️ Screenshots

### 1. Question Screen
![Question Screen](screenshots/1_questions.png)
*The 7‑question intake form (Bahasa Indonesia). Users select answers via dropdowns and radio buttons — no typing required.*

### 2. Results Screen (Expanded)
![Results](screenshots/2_results.png)
*After clicking "Cek Bantuan", the app displays predicted programs with confidence scores, plain‑language reasons, required documents, and office locations. Cards can be expanded individually.*

### 3. Disclaimer Banner
![Disclaimer](screenshots/3_disclaimer.png)
*Persistent yellow warning at the bottom of every result: "Ini bukan keputusan resmi. Harap verifikasi ke kelurahan atau dinas sosial terdekat." This reinforces that the AI only suggests — it never decides.*

### 4. Print Preview
![Print](screenshots/4_print.png)
*The page is print‑friendly. Users can press Ctrl+P to get a physical checklist to bring to the village office. The disclaimer remains visible in print.*

---

## 📁 Folder Contents
docs/
├── README.md ← You are here
└── screenshots/
├── 1_questions.png
├── 2_results.png
├── 3_disclaimer.png
└── 4_print.png

---

## 🛡️ Responsible AI in the UI

- **Confidence scores** are displayed as percentages but capped at **95%** — never 100%.  
- The app uses **“mungkin” (may qualify)** language exclusively; it never states “Anda berhak” or “pasti”.  
- A **yellow disclaimer** is always visible, not dismissible.  
- The final decision is explicitly deferred to **government officers at the kelurahan** — human‑in‑the‑loop is mandatory.

---

*For technical details, model evaluation, and the full project README, please see the [main README](../README.md).*