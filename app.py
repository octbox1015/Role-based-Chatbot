import streamlit as st
from openai import OpenAI
import base64

# ===============================
# Initialize OpenAI client
# ===============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ===============================
# Page Setup
# ===============================
st.set_page_config(page_title="🎭 Role-based Creative Chatbot + Image Studio", layout="wide")

st.title("🎭 Role-based Creative Chatbot + Image Studio")
st.markdown("Welcome! This app lets you chat with an AI that can **think and speak** like different creative professionals — and even **generate images** 🎨.")

# ===============================
# Role Options
# ===============================
roles = {
    "Film Critic": "You are a sharp and insightful film critic with expertise in feminist and postcolonial theory. You analyze films with depth, discussing symbolism, gender politics, and visual aesthetics.",
    "Fashion Consultant": "You are an energetic and confident fashion consultant. You give style advice that is trendy, personal, and inspiring.",
    "Dance Coach": "You are a professional dance coach specializing in K-pop and stage performance. You provide detailed, encouraging feedback on rhythm, body control, and stage presence.",
    "Digital Artist": "You are a digital artist and visual designer. You describe vivid, imaginative prompts for visual art and image generation.",
    "Creative Writing Mentor": "You are a creative writing mentor who helps writers craft emotional, rhythmic, and imagery-rich sentences.",
}

# ===============================
# Sidebar
# ===============================
st.sidebar.header("🧠 Choose a Role")
role = st.sidebar.selectbox("Select a role:", list(roles.keys()))
system_prompt = roles[role]

st.sidebar.markdown("---")
st.sidebar.info(f"💬 The chatbot will respond as a **{role}**.")

# ===============================
# Chat Section
# ===============================
st.subheader(f"💬 Chat with {role}")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Type your message here:")

if st.button("Send Message"):
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Call OpenAI Chat API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.chat_history
            ]
        )

        output = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": output})

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**🧍 You:** {chat['content']}")
    else:
        st.markdown(f"**🎭 {role}:** {chat['content']}")

# ===============================
# Image Studio Section
# ===============================
st.markdown("---")
st.subheader("🎨 Image Studio")

image_prompt = st.text_input("Describe your image idea (e.g., 'A dreamy sunset over a neon city skyline'):")

if st.button("Generate Image"):
    if image_prompt:
        with st.spinner("🎨 Generating your image... please wait."):
            result = client.images.generate(
                model="gpt-image-1",
                prompt=image_prompt,
                size="1024x1024"
            )
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)
            st.image(image_bytes, caption="Generated Image", use_container_width=True)

