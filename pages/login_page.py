# pages/login_page.py
import streamlit as st
import controller

def render_login():
    # 1. หัวข้อใหญ่
    st.title("🔐 เข้าสู่ระบบ")

    # 2. เริ่มสร้าง Form
    with st.form("login_form"):
        # ย้ายข้อมูลผู้จัดทำเข้ามาไว้ในนี้ เพื่อให้แสดงผลพร้อมกับช่องกรอกข้อมูล
        st.markdown("### 👤 ข้อมูลผู้จัดทำ")
        st.write("**ชื่อ:** นายธนกฤต แสนธรรมพล")
        st.write("**รหัสนักศึกษา:** 6760259108")
        st.write("**หมู่เรียน:** ว.6707T")
        
        # เพิ่มเส้นคั่นให้เหมือนในรูปตัวอย่าง
        st.divider()
        
        # ส่วนกรอกข้อมูล
        username = st.text_input("ชื่อผู้ใช้", placeholder="เช่น admin")
        password = st.text_input("รหัสผ่าน", type="password", placeholder="เช่น 1234")
        
        # ปุ่มส่งข้อมูล
        submitted = st.form_submit_button("Login")
        
        if submitted:
            ok, msgs, user_info = controller.login(username, password)
            if not ok:
                for m in msgs:
                    st.error(m)
            else:
                for m in msgs:
                    st.success(m)
                
                # เก็บค่าลง session_state เมื่อ login สำเร็จ
                st.session_state["is_logged_in"] = True
                st.session_state["user"] = user_info
                st.session_state["page"] = "books" 
                st.rerun()
