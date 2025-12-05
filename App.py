import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

st.set_page_config(page_title="Pembukuan Harian UMKM", layout="wide")
st.title("📘 Pembukuan & Keuangan Harian UMKM")

# Menginisialisasi session state
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Form Input Transaksi
st.subheader("✏️ Input Transaksi")
with st.form("transaction_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        jenis = st.selectbox("Jenis Transaksi", ["Pemasukan", "Pengeluaran", "Hutang", "Piutang"])
        deskripsi = st.text_input("Deskripsi / Keterangan")
    with col2:
        jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
        tanggal = st.date_input("Tanggal Transaksi", datetime.date.today())

    submit = st.form_submit_button("Simpan Transaksi")

    if submit:
        st.session_state.transactions.append({
            "Tanggal": tanggal,
            "Jenis": jenis,
            "Deskripsi": deskripsi,
            "Jumlah": jumlah
        })
        st.success("Transaksi berhasil disimpan!")

# Menampilkan tabel transaksi
df = pd.DataFrame(st.session_state.transactions)
st.subheader("📄 Daftar Transaksi")
if df.empty:
    st.info("Belum ada transaksi.")
else:
    st.dataframe(df, use_container_width=True)

# Ringkasan Keuangan
if not df.empty:
    st.subheader("📊 Ringkasan Keuangan")

    pemasukan = df[df["Jenis"] == "Pemasukan"]["Jumlah"].sum()
    pengeluaran = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
    hutang = df[df["Jenis"] == "Hutang"]["Jumlah"].sum()
    piutang = df[df["Jenis"] == "Piutang"]["Jumlah"].sum()

    saldo = pemasukan - pengeluaran
    saldo_bersih = pemasukan - pengeluaran + piutang - hutang

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Pemasukan", f"Rp {pemasukan:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {pengeluaran:,.0f}")
    col3.metric("Total Piutang", f"Rp {piutang:,.0f}")
    col4.metric("Total Hutang", f"Rp {hutang:,.0f}")

    st.metric("💰 Saldo Bersih", f"Rp {saldo_bersih:,.0f}")

# Export Excel
st.subheader("⬇️ Download Laporan Excel")

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="openpyxl")
    df.to_excel(writer, index=False, sheet_name="Laporan")
    writer.close()
    return output.getvalue()

if not df.empty:
    st.download_button(
        "Download Laporan",
        data=to_excel(df),
        file_name="laporan_keuangan_umkm.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
