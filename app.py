import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# API Key
api_key = os.environ.get("GOOGLE_API_KEY")

# مدل Google Gemini
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, api_key=api_key)

# تعریف منوهای دو رستوران
restaurants = {
    "رستوران آلفا": {
        "پیتزا مارگاریتا": "خمیر نازک، سس گوجه، پنیر موتزارلا، ریحان",
        "برگر کلاسیک": "گوشت گوساله، نان، پنیر چدار، کاهو، گوجه، سس مخصوص"
    },
    "رستوران بتا": {
        "املت سبزیجات": "تخم مرغ، فلفل دلمه‌ای، گوجه، سبزیجات تازه",
        "پنکیک با عسل": "آرد، شیر، تخم مرغ، عسل، کره"
    }
}

# دستیار مرکزی
def central_assistant(question):
    system_prompt = (
        "تو دستیار رستوران هستی و میتونی درباره‌ی رستوران‌ها و منوها جواب بدی. "
        "اگر سوال مرتبط نبود، با خوشرویی بگو: «من فقط درباره‌ی رستوران‌ها و منوها می‌تونم کمک کنم :)»\n\n"
        f"رستوران‌ها و منوها:\n{restaurants}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال: {question}")]
    response = llm.invoke(msg)
    return response.content

st.title("🍽️ انتخاب رستوران و دستیار هوشمند")

# انتخاب رستوران
selected_restaurant = st.selectbox("رستوران مورد نظر را انتخاب کنید:", list(restaurants.keys()))

st.subheader(f"📋 منوی {selected_restaurant}")
for dish, desc in restaurants[selected_restaurant].items():
    st.markdown(f"- **{dish}**: {desc}")

# سوال و جواب
st.markdown("---")
st.subheader("💬 پرسش و پاسخ با دستیار")
question = st.text_input("سوال خود را بنویسید یا بپرسید:")
if question:
    answer = central_assistant(question)
    st.markdown(f"**🍳 پاسخ دستیار:** {answer}")
