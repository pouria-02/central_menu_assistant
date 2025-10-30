import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# API Key از Streamlit Secrets
api_key = st.secrets["GOOGLE_API_KEY"]

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

# دستیار مرکزی (قبل از انتخاب رستوران)
def central_assistant(question):
    system_prompt = (
        "تو دستیار رستوران هستی و می‌تونی درباره‌ی رستوران‌ها و منوها جواب بدی. "
        "اگر سوال مرتبط نبود، با خوشرویی بگو: «من فقط درباره‌ی رستوران‌ها و منوها می‌تونم کمک کنم :)»\n\n"
        f"رستوران‌ها و منوها:\n{restaurants}"
    )
    msg = [HumanMessage(content=f"{system_prompt}\n\nسؤال: {question}")]
    response = llm.invoke(msg)
    return response.content

st.title("🍽️ منوی مرکزی رستوران‌ها و دستیار هوشمند")

# بخش دستیار مرکزی قبل از انتخاب رستوران
st.subheader("💬 دستیار مرکزی")
central_question = st.text_input("می‌تونی سوالت رو درباره رستوران‌ها و منوها بپرسی:")
if central_question:
    central_answer = central_assistant(central_question)
    st.markdown(f"**🍳 پاسخ دستیار:** {central_answer}")

# انتخاب رستوران
selected_restaurant = st.selectbox("رستوران مورد نظر را انتخاب کنید:", list(restaurants.keys()))

st.subheader(f"📋 منوی {selected_restaurant}")
for dish, desc in restaurants[selected_restaurant].items():
    st.markdown(f"- **{dish}**: {desc}")

# دستیار مخصوص رستوران انتخاب شده
st.markdown("---")
st.subheader(f"💬 پرسش و پاسخ با دستیار {selected_restaurant}")
restaurant_question = st.text_input(f"سوال درباره منوی {selected_restaurant} بنویسید:", key="restaurant_q")
if restaurant_question:
    system_prompt_restaurant = (
        f"تو یه دستیار رستوران هستی و فقط درباره‌ی منوی {selected_restaurant} پاسخ بده. "
        f"اگر سوال مرتبط نبود، بگو: «من فقط درباره‌ی منوی {selected_restaurant} می‌تونم کمک کنم :)»\n\n"
        f"منو:\n{restaurants[selected_restaurant]}"
    )
    msg_restaurant = [HumanMessage(content=f"{system_prompt_restaurant}\n\nسؤال مشتری: {restaurant_question}")]
    restaurant_answer = llm.invoke(msg_restaurant)
    st.markdown(f"**🍳 پاسخ دستیار:** {restaurant_answer}")
