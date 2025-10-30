import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import importlib
import os

st.set_page_config(page_title="🍽️ Central Menu Assistant", layout="wide")
st.markdown("<h1 style='text-align:center; color:#ff6600;'>🍽️ دستیار مرکزی منو</h1>", unsafe_allow_html=True)

# API Key برای دستیار
api_key = os.environ.get("GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp"
central_llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# لیست رستوران‌ها
restaurants = {
    "تاج محل": "restaurants.taj_mahal",
    "بلا ایتالیا": "restaurants.bella_italia"
}

# ===== دستیار مرکزی =====
st.subheader("💬 دستیار مرکزی")
central_question = st.text_input("می‌خوای یه چیزی درباره رستوران‌ها یا منو بدونی؟", key="central_input")
if central_question:
    system_prompt = (
        "تو دستیار مرکزی هستی. درباره‌ی رستوران‌ها و منوها اطلاعات میدی و می‌تونی "
        "به کاربر کمک کنی تا رستوران مناسب رو انتخاب کنه. "
        "اگر سوال ربطی به رستوران‌ها یا منوها نداشت، با لحنی دوستانه بگو: "
        "«من فقط درباره‌ی رستوران‌ها و منوها می‌تونم کمکت کنم :)»\n\n"
        f"لیست رستوران‌ها:\n{list(restaurants.keys())}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال کاربر: {central_question}")]
    answer = central_llm.invoke(msg)
    st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:10px;'>{answer}</div>", unsafe_allow_html=True)

# ===== انتخاب رستوران =====
st.subheader("🏠 انتخاب رستوران")
selected = st.selectbox("رستوران مورد نظر خود را انتخاب کنید:", list(restaurants.keys()))
if st.button("ورود به رستوران"):
    st.session_state["restaurant"] = selected
    st.experimental_rerun()

# ===== لود صفحه رستوران =====
if "restaurant" in st.session_state:
    restaurant_module = restaurants[st.session_state["restaurant"]]
    st.markdown(f"### شما وارد {st.session_state['restaurant']} شدید")
    restaurant_page = importlib.import_module(restaurant_module)