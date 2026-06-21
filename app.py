import streamlit as st
import joblib
import numpy as np
from lang import strings

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="SIMPEL", page_icon="🧭", layout="centered")

# ---------- LANGUAGE SETUP ----------
if 'lang' not in st.session_state:
    st.session_state.lang = 'id'

# Tiny language selector – placed at the very top
lang_col1, lang_col2 = st.columns([6, 1])
with lang_col2:
    lang = st.selectbox(
        strings[st.session_state.lang]["lang_label"],
        ["id", "en"],
        format_func=lambda x: "Bahasa Indonesia" if x == "id" else "English",
        key="lang_selector",
        on_change=lambda: st.session_state.update(lang=st.session_state.lang_selector)
    )
    st.session_state.lang = lang

t = strings[lang]

# ---------- LOAD MODEL & ENCODER (cached) ----------
@st.cache_resource
def load_model():
    model = joblib.load("model/model.pkl")
    encoder = joblib.load("model/encoder.pkl")
    return model, encoder

try:
    model, encoder = load_model()
    model_loaded = True
except Exception as e:
    st.error("Gagal memuat model. Pastikan file model.pkl dan encoder.pkl ada di folder model/")
    model_loaded = False

# ---------- HEADER ----------
st.title(t["title"])
st.caption("SIMPEL is a hackathon prototype. Not an official government tool. Built for USAII's Global AI Hackathon 2026.")
st.markdown(t["subtitle"])
st.caption(t["caption"])

# ---------- PROGRAM DETAILS ----------
# Program descriptions remain in Indonesian – they are official names/details.
program_info = {
    "PKH": {
        "nama": "Program Keluarga Harapan (PKH)",
        "deskripsi": "Bantuan tunai bersyarat untuk keluarga dengan ibu hamil, anak usia sekolah, lansia, atau disabilitas.",
        "dokumen": "KTP, KK, surat keterangan tidak mampu dari RT/RW, buku nikah (jika ada), rapor anak (untuk komponen pendidikan).",
        "tempat": "Dinas Sosial Kabupaten/Kota atau pendamping PKH di kelurahan.",
        "alasan": "Karena pendapatan rendah dan terdapat anak usia sekolah, balita, lansia, atau disabilitas.",
        "sumber": "[Kemensos – PKH](https://kemensos.go.id/program-keluarga-harapan-pkh)"
    },
    "BPNT": {
        "nama": "Bantuan Pangan Non‑Tunai (BPNT / Sembako)",
        "deskripsi": "Bantuan pangan senilai Rp200.000/bulan untuk membeli beras, telur, dan kebutuhan pokok di e‑warong.",
        "dokumen": "KTP, KK, surat keterangan tidak mampu dari RT/RW.",
        "tempat": "Kelurahan/desa (terdaftar di DTKS) atau koordinator BPNT setempat.",
        "alasan": "Karena pendapatan rendah, jumlah anggota keluarga ≥3, dan kondisi rumah non‑permanen.",
        "sumber": "[Kemensos – BPNT](https://kemensos.go.id/bantuan-pangan-non-tunai-bpnt)"
    },
    "PIP": {
        "nama": "Program Indonesia Pintar (PIP / KIP)",
        "deskripsi": "Bantuan biaya pendidikan untuk siswa SD, SMP, SMA/sederajat dari keluarga kurang mampu.",
        "dokumen": "KTP orang tua, KK, surat keterangan tidak mampu, rapor, surat keterangan dari sekolah.",
        "tempat": "Sekolah (operator dapodik) atau Dinas Pendidikan setempat.",
        "alasan": "Karena pendapatan rendah dan terdapat anak usia sekolah (7–18 tahun).",
        "sumber": "[Kemendikbud – PIP](https://pip.kemdikbud.go.id/)"
    },
    "PBI_JKN": {
        "nama": "BPJS Kesehatan PBI (JKN gratis)",
        "deskripsi": "Jaminan kesehatan gratis untuk masyarakat miskin dan tidak mampu, iuran dibayar pemerintah.",
        "dokumen": "KTP, KK, surat keterangan tidak mampu dari kelurahan.",
        "tempat": "Kelurahan atau kantor BPJS Kesehatan terdekat.",
        "alasan": "Karena pendapatan sangat rendah atau kondisi rumah sederhana (dinding non‑tembok).",
        "sumber": "[BPJS Kesehatan – PBI](https://bpjs-kesehatan.go.id/bpjs/index.php/pages/detail/2014/11)"
    }
}

# ---------- QUESTIONNAIRE ----------
# Underlying options always use the original Indonesian strings (for model compatibility).
# The format_func translates the displayed labels.
income_options = ["< Rp500.000", "Rp500.000 – Rp1.000.000", "Rp1.000.000 – Rp2.000.000", "> Rp2.000.000"]
family_options = ["1", "2", "3", "4", "5 atau lebih"]
wall_options = ["Tembok", "Semi permanen (setengah tembok)", "Papan/kayu", "Bambu/lainnya"]
yes_no = ["Ya", "Tidak"]

pendapatan = st.selectbox(
    t["q1"],
    income_options,
    format_func=lambda x, opts=income_options, lang_opts=t["income_options"]: lang_opts[opts.index(x)]
)
jumlah_anggota = st.selectbox(
    t["q2"],
    family_options,
    format_func=lambda x, opts=family_options, lang_opts=t["family_options"]: lang_opts[opts.index(x)]
)
anak_sekolah = st.radio(
    t["q3"],
    yes_no,
    format_func=lambda x: t["yes"] if x == "Ya" else t["no"]
)
anak_balita = st.radio(
    t["q4"],
    yes_no,
    format_func=lambda x: t["yes"] if x == "Ya" else t["no"]
)
lansia = st.radio(
    t["q5"],
    yes_no,
    format_func=lambda x: t["yes"] if x == "Ya" else t["no"]
)
disabilitas = st.radio(
    t["q6"],
    yes_no,
    format_func=lambda x: t["yes"] if x == "Ya" else t["no"]
)
dinding_rumah = st.selectbox(
    t["q7"],
    wall_options,
    format_func=lambda x, opts=wall_options, lang_opts=t["wall_options"]: lang_opts[opts.index(x)]
)

# ---------- BUTTON & AI PREDICTION ----------
if st.button(t["btn"], type="primary"):
    if not model_loaded:
        st.error("Model AI tidak tersedia. Periksa kembali folder model/.")
    else:
        # Map the text responses to numbers (must match training data – always use Indonesian strings)
        income_map = {
            "< Rp500.000": 0,
            "Rp500.000 – Rp1.000.000": 1,
            "Rp1.000.000 – Rp2.000.000": 2,
            "> Rp2.000.000": 3
        }
        anggota_map = {"1": 1, "2": 2, "3": 3, "4": 4, "5 atau lebih": 5}
        dinding_map = {
            "Tembok": 0,
            "Semi permanen (setengah tembok)": 1,
            "Papan/kayu": 2,
            "Bambu/lainnya": 3
        }

        # Create an array of 7 features
        features = np.array([
            income_map[pendapatan],
            anggota_map[jumlah_anggota],
            1 if anak_sekolah == "Ya" else 0,
            1 if anak_balita == "Ya" else 0,
            1 if lansia == "Ya" else 0,
            1 if disabilitas == "Ya" else 0,
            dinding_map[dinding_rumah]
        ]).reshape(1, -1)

        # Multi-label probability prediction
        proba = model.predict_proba(features)

        # Collect programs with a probability of ≥ 0.5
        program_list = []
        confidences = {}
        program_names = list(encoder.classes_)

        for i, prog in enumerate(program_names):
            if proba[i][0][1] >= 0.5:
                program_list.append(prog)
                raw_conf = proba[i][0][1]
                confidences[prog] = min(raw_conf, 0.95)

        # Arrange the programs in a natural order
        urutan = ["PKH", "BPNT", "PIP", "PBI_JKN"]
        program_list = [p for p in urutan if p in program_list]

        # ---------- SHOW RESULTS ----------
        st.markdown("---")
        st.subheader(t["result_title"])

        if not program_list:
            st.warning(t["no_result"])
        else:
            st.success(t["success_msg"].format(len(program_list)))

            for prog in program_list:
                info = program_info[prog]
                conf = confidences[prog]

                with st.expander(f"✅ {info['nama']} – Tingkat kecocokan: {conf:.0%}"):
                    st.markdown(f"**{t['why']}** {info['alasan']}")
                    st.markdown(f"**{t['desc']}:** {info['deskripsi']}")
                    st.markdown(f"**{t['docs']}:**")
                    docs = info['dokumen'].split(', ')
                    for doc in docs:
                        st.markdown(f"- {doc}")
                    st.markdown(f"**{t['place']}:** {info['tempat']}")
                    st.markdown(f"**{t['source']}:** {info['sumber']}")

        st.markdown("---")

        # ---------- DISCLAIMER ----------
        st.warning(t["disclaimer"])

        # ---------- PRINTING TIPS ----------
        st.info(t["print_tip"])

        # ---------- RESET BUTTON ----------
        if st.button(t["reset"]):
            st.rerun()