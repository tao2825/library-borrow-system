# pages/login_page.py
import streamlit as st
import controller

def render_login():
    st.title("🔐 เข้าสู่ระบบครับ")
    st.markdown("### 👤 ข้อมูลผู้จัดทำ")
    st.write("**ชื่อ:** นายวีรพงษ์ แวววงศ์")
    st.write("**รหัสนักศึกษา:** 6740259113")
    st.write("**หมู่เรียน:** ว.6706")
    with st.form("login_form"):
        username = st.text_input("ชื่อผู้ใช้", placeholder="เช่น admin")
        password = st.text_input("รหัสผ่าน", type="password", placeholder="เช่น 1234")
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
                st.session_state["page"] = "books" # หรือให้ไป borrows ก็ได้

                st.rerun()
