# 🧭 SIMPEL – AI Benefits Navigator for Indonesian Families

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
| **📓 Jupyter Notebook** | [eligibility_classifier_v3.ipynb](jupyter/eligibility_classifier_v3.ipynb) |
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

## 🧠 AI Architecture
**Input:** 7 multiple‑choice answers mapped to numeric features  
**Model:** Multi‑label Random Forest (scikit‑learn `MultiOutputClassifier`)  
**Output:** Up to 4 program labels (PKH, BPNT, PIP, PBI‑JKN) with probability scores  
**Explainability:** Feature importance analysis shows which factors most influence each prediction  
**Inference:** Loaded once in memory, <10ms per prediction, zero external API calls

---

## 📊 Data
All data is **100% synthetic** (4,273 households), generated programmatically based on simplified official eligibility rules from:
- [Kemensos – PKH](https://kemensos.go.id/program-keluarga-harapan-pkh)
- [Kemensos – BPNT](https://kemensos.go.id/bantuan-pangan-non-tunai-bpnt)
- [Kemendikbud – PIP](https://pip.kemdikbud.go.id/)
- [BPJS Kesehatan – PBI](https://bpjs-kesehatan.go.id/bpjs/index.php/pages/detail/2014/11)

To improve fairness and avoid over‑prediction, we added 5% label noise and included 1,500 negative samples (clearly ineligible households).

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
