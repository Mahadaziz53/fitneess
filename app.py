import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from fpdf import FPDF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Ultimate Fitness App", layout="wide")

# ---------------------- SESSION STATE ----------------------
if 'email' not in st.session_state:
    st.session_state['email'] = None
if 'progress' not in st.session_state:
    st.session_state['progress'] = pd.DataFrame(columns=['Day','Weight'])
if 'diet_generated' not in st.session_state:
    st.session_state['diet_generated'] = False

# ---------------------- LOGIN / SIGNUP SIDEBAR ----------------------
st.sidebar.markdown("## 💪 Welcome to Ultimate Fitness App!")
st.sidebar.markdown("Please login or sign up to access your personalized fitness plan 🥗🏋️‍♂️")

choice = st.sidebar.radio("Select Option:", ["Login", "Signup"])

if choice == "Signup":
    st.sidebar.markdown("### 📝 Create a New Account")
    new_email = st.sidebar.text_input("📧 Enter your email", key="signup_email")
    new_pass = st.sidebar.text_input("🔒 Choose a password", type='password', key="signup_pass")
    st.sidebar.markdown("⚠️ Password should be at least 6 characters")
    if st.sidebar.button("✅ Create Account"):
        if new_email and new_pass:
            st.session_state['email'] = new_email
            st.sidebar.success(f"🎉 Account created! Logged in as {new_email}")
        else:
            st.sidebar.warning("⚠️ Please enter both email and password")

elif choice == "Login":
    st.sidebar.markdown("### 🔐 Login to Your Account")
    email = st.sidebar.text_input("📧 Email", key="login_email")
    password = st.sidebar.text_input("🔒 Password", type='password', key="login_pass")
    st.sidebar.markdown("Forgot password? Contact support 💬")
    if st.sidebar.button("🚀 Login"):
        if email and password:
            st.session_state['email'] = email
            st.sidebar.success(f"🎉 Logged in as {email}")
        else:
            st.sidebar.error("❌ Please enter both email and password")

# ---------------------- MAIN APP ----------------------
if st.session_state['email']:
    # ---------------------- WELCOME HEADER ----------------------
    st.markdown(f"""
    <div style='background-color:#e0f7fa;padding:25px;border-radius:15px;margin-bottom:20px'>
        <h1 style='text-align:center;color:#ff6f61;'>🎉 Welcome, {st.session_state['email'].split('@')[0].title()}!</h1>
        <h3 style='text-align:center;color:#333333;'>Your personalized fitness journey starts here 💪🏋️‍♂️🥗</h3>
        <p style='text-align:center;font-size:18px;color:#555555;'>
        Set your goals, track your progress, and achieve your dream body with our easy-to-follow plans and motivational guidance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------- PERSONAL DETAILS ----------------------
    goal = st.selectbox("🎯 Your Goal", ["Lose Weight","Gain Weight","Maintain Weight"])
    daily_time = st.number_input("⏱ Daily Exercise Time (minutes)", min_value=10, max_value=180, value=60)
    weight = st.number_input("⚖ Current Weight (kg)", min_value=20, max_value=200, value=70)

    # Height input in Feet & Inches
    st.markdown("### 📏 Enter Your Height")
    feet = st.number_input("Feet", min_value=3, max_value=8, value=5, key="height_feet")
    inches = st.number_input("Inches", min_value=0, max_value=11, value=6, key="height_inches")
    height = feet*30.48 + inches*2.54
    st.write(f"Your height in cm: {height:.1f} cm")

    age = st.number_input("🎂 Age", min_value=10, max_value=100, value=25)
    gender = st.selectbox("🚻 Gender", ["Male","Female"])

    # Calories (simple calculation)
    if goal=="Lose Weight":
        calories = 2000 - 300
    elif goal=="Gain Weight":
        calories = 2000 + 500
    else:
        calories = 2000

    # ---------------------- METRICS ----------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("⚖ Weight (kg)", weight, f"{weight-65} kg change")
    col2.metric("🔥 Daily Calories", f"{calories} kcal", "+200 kcal")
    col3.metric("⏱ Exercise Time", f"{daily_time} min", "Goal 60 min")

    # ---------------------- MOTIVATIONAL QUOTE ----------------------
    quotes = [
        "🏃‍♂️ Push yourself because no one else is going to do it for you!",
        "💥 Success starts with self-discipline!",
        "💪 Don't stop until you're proud!",
        "⚡ Consistency is the key to transformation!"
    ]
    st.info(f"💡 Daily Motivation: {random.choice(quotes)}")

    # ---------------------- TABS ----------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🍽 Diet","🏋 Exercise","📅 Schedule","📊 Progress","📄 PDF","📧 Email Reminder"])

    # ---------------------- DIET TAB ----------------------
    with tab1:
        st.markdown("### 🥗 Personalized Diet Plan")
        if st.button("Generate Diet"):
            st.session_state['diet_generated'] = True
        
        if st.session_state['diet_generated']:
            diet = {
                "Lose Weight":[("Breakfast","Oatmeal & Fruits"),("Lunch","Grilled Chicken Salad"),("Dinner","Steamed Veggies & Fish")],
                "Gain Weight":[("Breakfast","Eggs & Toast"),("Lunch","Chicken & Rice"),("Dinner","Salmon & Quinoa")],
                "Maintain Weight":[("Breakfast","Yogurt & Fruits"),("Lunch","Balanced Plate"),("Dinner","Chicken Stir-Fry")]
            }
            for meal, desc in diet[goal]:
                st.write(f"- **{meal}**: {desc}")

    # ---------------------- EXERCISE TAB ----------------------
    exercises = {
        "Lose Weight":[("Running","30 min"),("Squats","15 min"),("Pushups","15 min")],
        "Gain Weight":[("Bench Press","40 min"),("Deadlift","40 min"),("Pullups","15 min")],
        "Maintain Weight":[("Circuit Training","30 min"),("Jump Rope","15 min"),("Yoga","20 min")]
    }
    with tab2:
        st.markdown("### 🏋 Personalized Exercise Plan")
        for ex,t in exercises[goal]:
            st.write(f"- **{ex}**: {t}")

    # ---------------------- SCHEDULE TAB ----------------------
    with tab3:
        st.markdown("### 📅 Weekly Schedule")
        schedule = pd.DataFrame({
            "Day":["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
            "Diet":[diet[goal][0][1],diet[goal][1][1],diet[goal][2][1],
                    diet[goal][0][1],diet[goal][1][1],diet[goal][2][1],"Rest"],
            "Exercise":[exercises[goal][0][0],exercises[goal][1][0],exercises[goal][2][0],
                        exercises[goal][0][0],exercises[goal][1][0],exercises[goal][2][0],"Yoga"]
        })
        st.table(schedule)

    # ---------------------- PROGRESS TAB ----------------------
    with tab4:
        st.markdown("### 📊 Track Your Progress")
        day = st.number_input("Day", min_value=1, value=1, key="day")
        new_weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=weight, key="weight_input")
        if st.button("Add Progress", key="add_progress"):
            new_row = pd.DataFrame([{'Day':day,'Weight':new_weight}])
            st.session_state.progress = pd.concat([st.session_state.progress, new_row], ignore_index=True)
            st.success("✅ Progress added!")

        if not st.session_state.progress.empty:
            st.progress(min(100, int((new_weight-50)*2)))  # simple progress bar
            fig, ax = plt.subplots()
            ax.plot(st.session_state.progress['Day'], st.session_state.progress['Weight'], marker='o', color='green')
            ax.set_xlabel("Day")
            ax.set_ylabel("Weight (kg)")
            ax.set_title("Weight Progress Over Time")
            st.pyplot(fig)

    # ---------------------- PDF TAB ----------------------
    with tab5:
        if st.button("Generate PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, txt=f"Fitness Plan for {st.session_state['email']}", ln=True, align="C")
            pdf.output("Fitness_Plan.pdf")
            st.success("✅ PDF Generated!")

    # ---------------------- EMAIL REMINDER TAB ----------------------
    with tab6:
        if st.button("Send Daily Email Reminder"):
            def send_email(to_email, subject, message):
                sender_email = "youremail@gmail.com"  # replace with your email
                password = "your_app_password"        # app password
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                try:
                    server = smtplib.SMTP('smtp.gmail.com',587)
                    server.starttls()
                    server.login(sender_email,password)
                    server.send_message(msg)
                    server.quit()
                except Exception as e:
                    st.error(f"❌ Email failed: {e}")
            send_email(st.session_state['email'], "Daily Fitness Reminder", f"Hello {st.session_state['email']}, don't forget your {goal} plan today!")
            st.success("📧 Email Reminder Sent!")
