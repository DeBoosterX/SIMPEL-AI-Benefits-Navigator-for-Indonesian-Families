<p align="center">
  <img src="docs/logo.png" alt="SIMPEL Logo" width="200"/>
</p>

# SIMPEL – AI Benefits Navigator for Indonesian Families

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)]([ISI_LINK_STREAMLIT])
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**SIMPEL** (Sistem Informasi Mudah Pahami Eligibility Layanan) is an AI-powered tool that asks **7 simple questions** about a household and instantly predicts which of Indonesia's four largest social programs (PKH, BPNT, PIP, PBI-JKN) they may qualify for — complete with explanations, confidence scores, required documents, and the nearest government office to visit.

> **"Satu Langkah, Semua Bantuan."**  
> *One step, all assistance.*

---

## 🎥 Demo & Resources

| Resource | Link |
|----------|------|
| **🟢 Live Web App** | [Streamlit Cloud](https://simpel.streamlit.app/) |
| **📓 Jupyter Notebook** | [eligibility_classifier.ipynb](jupyter/eligibility_classifier.ipynb) |
| **🎨 Figma Prototype** | [View on Figma]([ISI_LINK_FIGMA]) |
| **📹 Video Walkthrough** | [YouTube (unlisted)]([ISI_LINK_YOUTUBE]) |
| **📸 Documentation & Screenshots** | [docs/README.md](docs/README.md) |

---

## ❓ Problem
Millions of low-income Indonesian families miss out on cash transfers, food assistance, school aid, and free healthcare because eligibility rules are fragmented across different government websites, written in bureaucratic language, and difficult to interpret under stress. Families who are eligible do not apply simply because they do not know where to start.

---

## 💡 Solution
SIMPEL asks **7 plain-language questions** (in Bahasa Indonesia), then uses a **Random Forest classifier** trained on synthetic data to predict which national social programs a family may qualify for. The output includes:
- ✅ Program names with confidence scores
- 📝 Plain‑language explanations of why the model suggests each program
- 📄 A ready‑to‑print document checklist
- 📍 The exact government office to visit
- ⚠️ A persistent yellow disclaimer reminding users that this is a simulation, not an official decision

---

## 🛠️ Key Features
- 🧭 **Guided questionnaire** – no chatbot; designed for low‑literacy users and slow 2G/3G networks
- 🤖 **AI reasoning** – interpretable multi‑label Random Forest with feature importance
- 🛡️ **Responsible AI** – always uses *“mungkin”* (may qualify) language; confidence capped at 95%; human‑in‑the‑loop mandatory
- 🖨️ **Print‑ready** – results can be printed and taken directly to the village office
- 👥 **Kader‑friendly** – can be operated by community helpers on behalf of families without smartphones

---

## 🏗️ Architecture & Technical Decisions

- **No paid APIs, no external LLM calls.** The app runs entirely on a free Streamlit Cloud instance. The Random Forest model (`model.pkl`, ~2 MB) is loaded once into memory and all predictions happen locally in under 10 ms. No internet connection is needed for inference after the initial page load.
- **Static model – deliberate, not a bug.** The model was trained on simplified eligibility rules from official sources (Kemensos, BPJS, Kemdikbud) and does **not** auto‑update when government policies change. We deliberately chose this approach because the Indonesian government does not provide public APIs for real‑time eligibility data, and official websites are frequently unavailable — exactly the infrastructure challenge our users face. Instead, the app always provides direct links to official sources so users can manually verify the latest rules. The app is transparent that results are a simulation and must be verified at the village office.
- **Deterministic & interpretable.** Every prediction can be explained with feature importance. The output is never “you definitely qualify” – always *“Anda mungkin memenuhi syarat”* (you may qualify). Confidence is capped at 95% to prevent over‑reliance.

---

## 🧠 AI Architecture (Quick Spec)
**Input:** 7 multiple‑choice answers mapped to numeric features  
**Model:** Multi‑label Random Forest (scikit‑learn `MultiOutputClassifier`, 100 trees, max‑depth=5)  
**Output:** Up to 4 program labels (PKH, BPNT, PIP, PBI‑JKN) with probability scores  
**Explainability:** Feature importance analysis shows which factors most influence each prediction  
**Inference:** Loaded once in memory, <10ms per prediction, zero external API calls  
**Evaluation:** Validated on a held‑out test set (F1 0.95–0.99) and manually stress‑tested with edge cases (wealthy households, elderly alone)

---

## 📊 Data
All data is **100% synthetic** (4,273 households), generated programmatically based on simplified official eligibility rules from:
- [Kemensos – PKH](https://kemensos.go.id/program-keluarga-harapan-pkh)
- [Kemensos – BPNT](https://kemensos.go.id/bantuan-pangan-non-tunai-bpnt)
- [Kemendikbud – PIP](https://pip.kemdikbud.go.id/)
- [BPJS Kesehatan – PBI](https://bpjs-kesehatan.go.id/bpjs/index.php/pages/detail/2014/11)

To improve fairness and avoid over‑prediction, we added 5% label noise and included 1,500 negative samples (clearly ineligible households).

---

## ⚠️ Limitations & Scalability

- **Free‑tier deployment:** The live demo runs on Streamlit Cloud’s free tier, which supports a limited number of concurrent users. For production use, the app can be trivially moved to a paid Streamlit Cloud plan, Hugging Face Spaces, or a self‑hosted container (Docker) without code changes.
- **Single‑file architecture:** Because the entire app is one Python file, scaling horizontally is straightforward – simply spin up more identical instances behind a load balancer. The model file is tiny and CPU‑only; no GPU or cloud‑specific service is required.
- **No persistent data:** The app does not store any user information, so no database or privacy‑heavy infrastructure is needed. This also means no user‑specific history; each session is independent.

---

## 📴 Offline Roadmap (Technical)

We plan to make SIMPEL fully offline by compiling the scikit‑learn model to pure JavaScript using [m2cgen](https://github.com/BayesWitnesses/m2cgen). The pipeline:

1. Convert the trained `RandomForestClassifier` into a standalone JavaScript function (no Python required).
2. Embed that function in a static HTML page together with the questionnaire UI.
3. Bundle as a Progressive Web App (PWA) so the entire tool can be installed on a phone and run without any internet connection – even on 2G‑only devices.

This approach eliminates the need for a backend entirely and makes SIMPEL viable in the most remote areas.

---

## 🌐 Language Support

The app is available in **Bahasa Indonesia** and **English**. A language selector at the top switches all UI text, ensuring international judges can easily read the interface. The underlying AI logic is identical regardless of language.

---

## 🧰 Tech Stack
- **Full Stack:** [Streamlit](https://streamlit.io/) (Python) – single‑file web application
- **ML:** [scikit‑learn](https://scikit-learn.org/) (Random Forest, MultiOutputClassifier)
- **Data:** [pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization:** [Matplotlib](https://matplotlib.org/)
- **Model Persistence:** [joblib](https://joblib.readthedocs.io/)
- **Development:** [Jupyter Notebook](https://jupyter.org/), [Google Colab](https://colab.research.google.com/)
- **Design:** [Figma](https://figma.com/)
- **Deployment:** [Streamlit Cloud](https://streamlit.io/cloud) (free tier)
- **Version Control:** [GitHub](https://github.com/)

---

## 🗺️ What’s Next

- **Voice input** – integrate Web Speech API (online) or Vosk (offline) for illiterate users.
- **Multi‑language** – extend the language dictionary to Javanese, Sundanese, etc.
- **WhatsApp integration** – lightweight Flask webhook + WhatsApp Business Cloud API.
- **DTKS sync** – periodically fetch official welfare data into a local SQLite cache for offline‑first verification.
- **Fully offline PWA** – compile model → JavaScript, bundle with static UI (see Offline Roadmap above).
- **Guardrailed chatbot** – a fine‑tuned small model (e.g., Gemma 2B) sandboxed to answer only program‑related questions.

---

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/[ALIF_USERNAME]/simpel.git
cd simpel

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py