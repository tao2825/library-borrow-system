import streamlit as st
import model
from datetime import date
import io
import pandas as pd
import plotly.express as px

# เพิ่ม Imports สำหรับ ReportLab
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def render_report():
    st.subheader("📊 รายงานสรุประบบยืม-คืนหนังสือ")

    # ... (ส่วนที่ 1 และ 2: กราฟวงกลมและกราฟแท่ง คงไว้ตามเดิม) ...
    # [ตัดโค้ดส่วนกราฟออกเพื่อความกระชับ แต่ในไฟล์จริงของคุณให้คงไว้]

    # ===============================
    # 3) รายการผู้ยืม–คืนทั้งหมด
    # ===============================
    st.markdown("### 3) รายการผู้ยืม–คืนทั้งหมด")

    col1, col2, col3 = st.columns(3)
    with col1:
        report_start = st.date_input("วันที่เริ่มต้น (รายงาน)", value=date(2025, 6, 1), key="report_start")
    with col2:
        report_end = st.date_input("วันที่สิ้นสุด (รายงาน)", value=date.today(), key="report_end")
    with col3:
        status_label = st.selectbox("สถานะการยืม–คืน", ["ทั้งหมด", "ยังไม่คืน", "คืนแล้ว"], key="report_status")

    if report_start > report_end:
        st.warning("วันที่เริ่มต้นต้องไม่มากกว่าวันที่สิ้นสุด")
        return

    status_map = {"ทั้งหมด": "all", "ยังไม่คืน": "borrowed", "คืนแล้ว": "returned"}
    selected_status = status_map[status_label]

    report_df = model.get_borrow_report(
        report_start.isoformat(),
        report_end.isoformat(),
        selected_status
    )

    if report_df.empty:
        st.info("ไม่พบข้อมูลตามเงื่อนไขที่เลือก")
        return

    st.dataframe(report_df, use_container_width=True)

    # ===============================
    # 4) ส่งออกรายงาน
    # ===============================
    st.markdown("### 4) ส่งออกรายงาน")

    # --- CSV & Excel (โค้ดเดิมของคุณ) ---
    col_csv, col_excel, col_pdf = st.columns(3)
    
    with col_csv:
        csv_buffer = io.StringIO()
        report_df.to_csv(csv_buffer, index=False)
        st.download_button("⬇️ ดาวน์โหลด CSV", data=csv_buffer.getvalue(), file_name="report.csv", mime="text/csv")

    with col_excel:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer) as writer:
            report_df.to_excel(writer, index=False, sheet_name="Sheet1")
        st.download_button("⬇️ ดาวน์โหลด Excel", data=excel_buffer.getvalue(), file_name="report.xlsx")

    with col_pdf:
        # ---------- PDF (ภาษาไทยด้วย NotoSansThai) ----------
        try:
            # 1. ลงทะเบียน Font (ตรวจสอบว่าไฟล์ .ttf อยู่ในโฟลเดอร์เดียวกับ app.py)
            pdfmetrics.registerFont(TTFont("NotoSansThai", "NotoSansThai-Regular.ttf"))

            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            
            # สร้างสไตล์ภาษาไทย
            thai_title = ParagraphStyle(name="ThaiTitle", fontName="NotoSansThai", fontSize=16, alignment=1, leading=20)
            thai_body = ParagraphStyle(name="ThaiBody", fontName="NotoSansThai", fontSize=10, leading=14)

            elements = []
            elements.append(Paragraph("รายงานผู้ยืม–คืนหนังสือ", thai_title))
            elements.append(Paragraph(f"ช่วงวันที่ {report_start} ถึง {report_end}", thai_body))
            elements.append(Paragraph("<br/><br/>", thai_body))

            # เตรียมข้อมูลตาราง (ใช้ Paragraph เพื่อให้ตัดคำไทยได้)
            table_data = []
            # หัวตาราง
            header = [Paragraph(f"<b>{col}</b>", thai_body) for col in report_df.columns]
            table_data.append(header)
            
            # ข้อมูลในตาราง
            for _, row in report_df.iterrows():
                table_data.append([Paragraph(str(val), thai_body) for val in row.values])

            # สร้างตาราง
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))

            elements.append(table)
            doc.build(elements)

            st.download_button(
                label="⬇️ ดาวน์โหลด PDF",
                data=pdf_buffer.getvalue(),
                file_name="borrow_report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"ไม่สามารถสร้าง PDF ได้: {e}")
            st.info("โปรดตรวจสอบว่ามีไฟล์ NotoSansThai-Regular.ttf อยู่ในเครื่อง")