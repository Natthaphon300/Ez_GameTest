import streamlit as st

# ตั้งค่าหน้าเว็บ (หากใช้ร่วมกับ main.py และมีคำสั่งนี้แล้ว ให้ลบหรือคอมเมนต์บรรทัดนี้ออกครับ)
st.set_page_config(page_title="เกมตอบคำถาม 10 ข้อ", page_icon="🎮")

st.title("🎮 เกมตอบคำถามทดสอบความรู้ (10 ข้อ)")

# 1. คลังคำถามทั้งหมด 10 ข้อ (แก้ไขคำถามและตัวเลือกได้ตามต้องการ)
questions = [
    {
        "question": "1. ภาษาโปรแกรมใดนิยมใช้สร้างเว็บแอปด้วย Streamlit?",
        "options": ["Java", "Python", "C++", "PHP"],
        "answer": "Python"
    },
    {
        "question": "2. แพลตฟอร์มใดใช้สำหรับเก็บโค้ดและทำงานร่วมกัน?",
        "options": ["GitHub", "Photoshop", "Excel", "Canva"],
        "answer": "GitHub"
    },
    {
        "question": "3. คำสั่งใดใน Streamlit ใช้สำหรับแสดงหัวข้อใหญ่สุด?",
        "options": ["st.write()", "st.button()", "st.title()", "st.radio()"],
        "answer": "st.title()"
    },
    {
        "question": "4. ไฟล์ใดที่ใช้ระบุรายชื่อไลบรารีเสริมเพื่อติดตั้งบน Cloud?",
        "options": ["readme.md", "requirements.txt", "config.json", "index.html"],
        "answer": "requirements.txt"
    },
    {
        "question": "5. คำสั่งใดใน Terminal ใช้สำหรับรันแอป Streamlit?",
        "options": ["python app.py", "streamlit run app.py", "npm start", "git push"],
        "answer": "streamlit run app.py"
    },
    {
        "question": "6. ตัวแปรชนิดใดใน Python ใช้เก็บข้อมูลแบบลำดับที่แก้ไขค่าได้?",
        "options": ["Tuple", "List", "String", "Int"],
        "answer": "List"
    },
    {
        "question": "7. คำสั่งใดใช้สำหรับสร้างปุ่มตัวเลือกวงกลมใน Streamlit?",
        "options": ["st.checkbox()", "st.selectbox()", "st.radio()", "st.slider()"],
        "answer": "st.radio()"
    },
    {
        "question": "8. สัญลักษณ์ใดใช้สำหรับเขียนคอมเมนต์ในภาษา Python?",
        "options": ["//", "/* */", "#", "<!-- -->"],
        "answer": "#"
    },
    {
        "question": "9. หากต้องการแสดงเอฟเฟกต์ลูกโป่งฉลองใน Streamlit ต้องใช้คำสั่งใด?",
        "options": ["st.snow()", "st.balloons()", "st.party()", "st.celebrate()"],
        "answer": "st.balloons()"
    },
    {
        "question": "10. Branch หลักมาตรฐานเมื่อสร้าง Repository ใหม่บน GitHub มักชื่อว่าอะไร?",
        "options": ["master", "main", "root", "index"],
        "answer": "main"
    }
]

# 2. ตั้งค่าหน่วยความจำ (Session State) เพื่อจำหน้าปัจจุบันและคำตอบที่เลือกไว้
if "page" not in st.session_state:
    st.session_state.page = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "finished" not in st.session_state:
    st.session_state.finished = False

PER_PAGE = 2  # กำหนดให้แสดงหน้าละ 2 ข้อ
total_pages = len(questions) // PER_PAGE

# 3. ส่วนแสดงผลหน้าคำถาม (ยังไม่จบเกม)
if not st.session_state.finished:
    # แสดงแถบความคืบหน้า
    current_page = st.session_state.page
    st.progress((current_page + 1) / total_pages, text=f"หน้าที่ {current_page + 1} จาก {total_pages}")

    start_idx = current_page * PER_PAGE
    end_idx = start_idx + PER_PAGE

    # แสดงคำถาม 2 ข้อของหน้านั้น
    for i in range(start_idx, end_idx):
        q = questions[i]
        st.subheader(q["question"])
        
        # ดึงคำตอบเดิมที่เคยเลือกไว้ (เผื่อกดย้อนกลับ)
        saved_ans = st.session_state.answers.get(i, None)
        default_idx = q["options"].index(saved_ans) if saved_ans in q["options"] else None

        choice = st.radio(
            label="เลือกคำตอบ:",
            options=q["options"],
            key=f"q_{i}",
            index=default_idx,
            label_visibility="collapsed"
        )
        st.session_state.answers[i] = choice
        st.divider()

    # สร้างปุ่มควบคุมด้านล่าง (ย้อนกลับ / ถัดไป หรือ ส่งคำตอบ)
    col1, col2 = st.columns(2)
    
    with col1:
        if current_page > 0:
            if st.button("⬅️ ย้อนกลับ", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

    with col2:
        # เช็กว่าตอบครบทั้ง 2 ข้อในหน้านี้หรือยัง
        answered_all_on_page = all(
            st.session_state.answers.get(i) is not None for i in range(start_idx, end_idx)
        )
        
        if current_page < total_pages - 1:
            if st.button("ถัดไป ➡️", type="primary", use_container_width=True):
                if answered_all_on_page:
                    st.session_state.page += 1
                    st.rerun()
                else:
                    st.warning("⚠️ กรุณาตอบให้ครบทั้ง 2 ข้อก่อนกดถัดไปครับ")
        else:
            if st.button("✅ ส่งคำตอบทั้งหมด", type="primary", use_container_width=True):
                if answered_all_on_page:
                    st.session_state.finished = True
                    st.rerun()
                else:
                    st.warning("⚠️ กรุณาตอบให้ครบทั้ง 2 ข้อก่อนส่งคำตอบครับ")

# 4. ส่วนแสดงผลคะแนนเมื่อตอบครบทั้ง 10 ข้อแล้ว
else:
    score = 0
    st.subheader("📊 สรุปผลการทดสอบของคุณ")
    
    for i, q in enumerate(questions):
        user_ans = st.session_state.answers.get(i)
        if user_ans == q["answer"]:
            score += 1
            st.success(f"**ข้อ {i+1}: ถูกต้อง!** ({user_ans})")
        else:
            st.error(f"**ข้อ {i+1}: ผิด** — คุณตอบ *{user_ans}* (เฉลย: **{q['answer']}**)")
            
    st.metric(label="คะแนนรวมที่ได้", value=f"{score} / {len(questions)} คะแนน")
    
    if score == len(questions):
        st.balloons()
        
    # ปุ่มสำหรับเริ่มเล่นใหม่อีกครั้ง
    if st.button("🔄 เล่นใหม่อีกครั้ง", use_container_width=True):
        st.session_state.page = 0
        st.session_state.answers = {}
        st.session_state.finished = False
        st.rerun()
