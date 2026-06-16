import streamlit as st
import joblib
import numpy as np

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="SIMPEL", page_icon="🧭", layout="centered")

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
st.title("🧭 SIMPEL – Cek Bantuan Sosial yang Mungkin Anda Dapat")
st.caption("SIMPEL is a hackathon prototype. Not an official government tool. Built for USAII's Global AI Hackathon 2026.")
st.markdown("Jawab 7 pertanyaan singkat di bawah ini. **Data Anda tidak disimpan.**")
st.caption("ℹ️ Kriteria yang digunakan adalah penyederhanaan untuk simulasi. "
           "Klik **sumber resmi** di setiap program untuk informasi lengkap.")

# ---------- PROGRAM DETAILS ----------
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
pendapatan = st.selectbox(
    "1. Rata‑rata pendapatan keluarga per bulan?",
    ["< Rp500.000", "Rp500.000 – Rp1.000.000", "Rp1.000.000 – Rp2.000.000", "> Rp2.000.000"]
)

jumlah_anggota = st.selectbox(
    "2. Jumlah anggota keluarga (termasuk Anda)?",
    ["1", "2", "3", "4", "5 atau lebih"]
)

anak_sekolah = st.radio(
    "3. Apakah ada anak usia sekolah (7–18 tahun) di keluarga?",
    ["Ya", "Tidak"]
)

anak_balita = st.radio(
    "4. Apakah ada anak balita (0–6 tahun) atau ibu hamil?",
    ["Ya", "Tidak"]
)

lansia = st.radio(
    "5. Apakah ada anggota keluarga lanjut usia (≥60 tahun)?",
    ["Ya", "Tidak"]
)

disabilitas = st.radio(
    "6. Apakah ada anggota keluarga dengan disabilitas berat?",
    ["Ya", "Tidak"]
)

dinding_rumah = st.selectbox(
    "7. Jenis dinding terluas rumah Anda?",
    ["Tembok", "Semi permanen (setengah tembok)", "Papan/kayu", "Bambu/lainnya"]
)

# ---------- BUTTON & AI PREDICTION ----------
if st.button("🔍 Cek Bantuan yang Mungkin Saya Dapat", type="primary"):
    if not model_loaded:
        st.error("Model AI tidak tersedia. Periksa kembali folder model/.")
    else:
        # Map the text responses to numbers (they must match the training data)
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
        program_names = list(encoder.classes_)  # ['BPNT','PBI_JKN','PIP','PKH'] (alphabetical)

        for i, prog in enumerate(program_names):
            if proba[i][0][1] >= 0.5:
                program_list.append(prog)
                # Limit the confidence level to 95% so it doesn’t seem too definitive
                raw_conf = proba[i][0][1]
                confidences[prog] = min(raw_conf, 0.95)

        # Arrange the program so that it looks more natural: PKH, BPNT, PIP, PBI_JKN
        urutan = ["PKH", "BPNT", "PIP", "PBI_JKN"]
        program_list = [p for p in urutan if p in program_list]

        # ---------- SHOW RESULTS ----------
        st.markdown("---")
        st.subheader("📋 Hasil Pemeriksaan")

        if not program_list:
            st.warning(
                "Berdasarkan data yang Anda masukkan, saat ini tidak terdeteksi program yang sesuai. "
                "Namun, ini hanya simulasi. Silakan kunjungi kelurahan untuk informasi lebih lanjut."
            )
        else:
            st.success(
                f"Berdasarkan informasi Anda, Anda **mungkin** memenuhi syarat untuk "
                f"{len(program_list)} program berikut."
            )

            for prog in program_list:
                info = program_info[prog]
                conf = confidences[prog]

                with st.expander(f"✅ {info['nama']} – Tingkat kecocokan: {conf:.0%}"):
                    # Program-specific details
                    st.markdown(f"**Mengapa?** {info['alasan']}")
                    st.markdown(f"**Deskripsi:** {info['deskripsi']}")
                    st.markdown("**Dokumen yang harus disiapkan:**")
                    docs = info['dokumen'].split(', ')
                    for doc in docs:
                        st.markdown(f"- {doc}")
                    st.markdown(f"**Ke mana harus pergi:** {info['tempat']}")
                    st.markdown(f"**Sumber resmi:** {info['sumber']}")
        
        st.markdown("---")

        # ---------- DISCLAIMER ----------
        st.warning(
            "⚠️ **Peringatan Penting:** Hasil ini **bukan keputusan resmi** dan hanya bersifat simulasi. "
            "Kriteria sebenarnya bisa lebih kompleks dan dapat berubah sewaktu‑waktu. "
            "**Harap verifikasi langsung ke kelurahan atau dinas sosial terdekat.** "
            "Ini adalah alat bantu, bukan penentu akhir."
        )

        # ---------- PRINTING TIPS ----------
        st.info("💡 Tips: Anda bisa mencetak halaman ini (Ctrl+P) untuk dibawa ke kelurahan sebagai panduan awal.")
