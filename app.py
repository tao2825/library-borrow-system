import streamlit as st

from pages import book_page
from pages import member_page
from pages import borrow_page
from pages import report_page

# ✅ เพิ่มเติม: import หน้า admin
from pages import admin_page

# ✅ เพิ่มเติม: import หน้า login (View)
from pages import login_page

# =========================
# UI Config (ต้องอยู่บรรทัดแรกสุดของส่วน UI)
# =========================
st.set_page_config(page_title="ระบบยืม-คืนหนังสือ", page_icon="📚")

# ✅ เพิ่มเติม: init session สําหรับ login/logout
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

# ✅ ซ่อน Multi-page auto nav ด้วย CSS
st.markdown("""
<style>
/* 1) ตัวหลัก: Sidebar navigation ของ multipage */
section[data-testid="stSidebarNav"] {display: none !important;}

/* 2) fallback: เผื่อ DOM เปลี่ยนชื่อ/โครง */
div[data-testid="stSidebarNav"] {display: none !important;}
nav[data-testid="stSidebarNav"] {display: none !important;}
/* 3) fallback เพิ่มเติม: ซ่อนหัวข้อ Pages / รายการหน้า (บางเวอร์ชัน) */
div[data-testid="stSidebarNavItems"] {display: none !important;}
div[data-testid="stSidebarNavSeparator"] {display: none !important;}
/* 4) fallback สุดท้าย: ถ้า Streamlit render เป็น <ul>/<li> ใน sidebar */
aside ul:has(a[href*="?page="]) {display: none !important;}
aside ul:has(a[href*="/book_page"]) {display: none !important;}
aside ul:has(a[href*="/member_page"]) {display: none !important;}
aside ul:has(a[href*="/borrow_page"]) {display: none !important;}
</style>
""", unsafe_allow_html=True)

# =========================
# UI Logic
# =========================

# ✅ เพิ่มเติม: Login Gate (ถ้ายังไม่ล็อกอินให้ไปหน้า login)
if not st.session_state["is_logged_in"]:
    login_page.render_login()
    st.stop()

# ✅ แก้ไขใหม่: ให้ส่วนหัวเว็บทํางานหลัง Login เท่านั้น
st.title("📚 ระบบยืม-คืนหนังสือ (Streamlit + SQLite)")
st.write("ตัวอย่าง Web App เชื่อมฐานข้อมูล (ปรับโครงสร้างแบบ MVC เชิงแนวคิด)")

# ✅ เพิ่มเติม: แสดงผู้ใช้ + ปุ่ม Logout
user = st.session_state.get("user") or {}
role = user.get('role', '-') # ดึงค่า role ออกมาเก็บในตัวแปรเพื่อใช้งานต่อ
st.sidebar.markdown(f"👤 ผู้ใช้: **{user.get('username','-')}**")
st.sidebar.markdown(f"🔑 บทบาท: **{role}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state["is_logged_in"] = False
    st.session_state["user"] = None
    st.session_state["page"] = "books"
    st.rerun()

# ---------- เมนูแบบคลิกแถบ ----------
if "page" not in st.session_state:
    st.session_state.page = "books"

# ===== Sidebar Menu Title =====
st.sidebar.markdown("""
<style>
.menu-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>
<div class="menu-title">
เมนู
</div>
""", unsafe_allow_html=True)

# ฟังก์ชันสําหรับสร้างปุ่มเมนูใน Sidebar
def nav_button(label, key, icon=""):
    active = (st.session_state.page == key)
    btn = st.sidebar.button(
        f"{icon} {label}",
        use_container_width=True,
        key=f"btn_{key}"
    )
    if btn:
        st.session_state.page = key
        st.rerun()

# ✅ แก้ไข: staff ทำได้ทุกอย่าง “ยกเว้นจัดการ user และดูรายงาน”
nav_button("หนังสือ", "books", "📚")
nav_button("สมาชิก", "members", "👤")
nav_button("ยืม-คืน", "borrows", "🔄")

# ✅ แสดงเฉพาะ admin เท่านั้น
if role == "admin":
    nav_button("รายงาน", "reports", "📊")
    nav_button("จัดการผู้ใช้", "admin", "🛠️")

# ---------- Routing ----------
if st.session_state.page == "books":
    book_page.render_book()

elif st.session_state.page == "members":
    member_page.render_member()

elif st.session_state.page == "borrows":
    borrow_page.render_borrow()

elif st.session_state.page == "reports":
    # ✅ ป้องกัน staff เข้าหน้ารายงาน
    if role != "admin":
        st.warning("⚠ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น")
    else:
        report_page.render_report()

elif st.session_state.page == "admin":
    if role != "admin":
        st.warning("⚠ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น")
    else:
        admin_page.render_admin()

else:
    # fallback
    book_page.render_book()

    nav_button("รายงาน", "reports", "📊")
    
