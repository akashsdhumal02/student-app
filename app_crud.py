import streamlit as st
import sqlite3
# 1. Database Connection
conn = sqlite3.connect('school_crud.db', check_same_thread=False)
cursor = conn.cursor()
# Table banavne
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        city TEXT
    )
''')
conn.commit()
st.title("🎓 Advanced Student Management App")
# Sidebar Menu (Pages switch karnyasathi)
menu = st.sidebar.selectbox("Navigation", ["Add New Students", "See Students & Delete Student"])
if menu == "Add New Students":
    st.subheader("➕ Add New Students")  
    with st.form("add_form"):
        name = st.text_input("Student Name:")
        age = st.number_input("Age:", min_value=1, max_value=100, value=20)
        city = st.text_input("City:") 
        submit = st.form_submit_button("Save Into The Database")
        if submit:
            if name and city:
                cursor.execute("INSERT INTO students (name, age, city) VALUES (?, ?, ?)", (name, age, city))
                conn.commit()
                st.success(f"✅ {name} Student Added Successfully! 🎉")
            else:
                st.warning("⚠️ Please Filled All The Details!")
elif menu == "See Students & Delete Student":
    st.subheader("📋 All Student Lists & Delete Options")
    # Database madhun data fetch karne
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            # Eka row madhe info ani delete button dakhavne
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"🆔 **ID:** {row[0]} | 👤 **Name:** {row[1]} | 🎂 **Age:** {row[2]} | 🏙️ **City:** {row[3]}")   
            with col2:
                # Pratyek student sathi vegla delete button
                if st.button("Delete", key=f"del_{row[0]}"):
                    cursor.execute("DELETE FROM students WHERE id = ?", (row[0],))
                    conn.commit()
                    st.success(f"Student ID {row[0]} delete zala!")
                    st.rerun() # App refresh karnyasathi
    else:
        st.info("There is No Student In Database.")