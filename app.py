import streamlit as st
from openai import OpenAI

# ==============================
# Setup
# ==============================
st.set_page_config(page_title="Role-based Creative Chatbot + Image Studio", page_icon="🎨", layout="wide")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# Sidebar
# ==============================
st.sidebar.title("🎭 Choose Your Creative Role")
role = st.sidebar.selectbox(
    "Select a role for your chatbot:",
    [
        "🎬 Film Director",
        "🎨 Visual Artist",
        "👗 Fashion Stylist",
        "🕺 Dance Coach",
        "🎤 Performing Arts Critic",
        "📸 Photographer",
        "🎮 Game Designer",
        "🧠 Creative Strategist",
    ],
)

st.sidebar.markdown("---")
st.sidebar.title("🖼️ Image Studio")
generate_image = st.sidebar.checkbox("Enable image generation")

# ==============================
# Main Page
# ==============================
st.title("🤖 Role-based Creative Chatbot + Image Studio")
st.write(
    f"Your chatbot is now acting as a **{role}**. Ask questions or request creative ideas below!"
)

# User input
user_input = st.text_area("💬 Enter your message:", height=120, placeholder="Type something creative...")

if st.button("Generate Response 🚀"):
    if user_input.strip() == "":
        st.warning("Please enter a message first!")
    else:
        with st.spinner("Thinking..."):
            prompt = f"You are a {role}. Respond professionally and creatively to the following: {user_input}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a creative expert chatbot."},
                    {"role": "user", "content": prompt},
                ],
            )

            ai_reply = response.choices[0].message.content
            st.success("✅ Chatbot Response:")
            st.write(ai_reply)

        # ==============================
        # Image Generation
        # ==============================
        if generate_image:
            with st.spinner("Generating image..."):
                image_prompt = f"Create an artistic image based on the idea: {user_input}"
                image_result = client.images.generate(
                    model="gpt-image-1",
                    prompt=image_prompt,
                    size="1024x1024"
                )

                image_url = image_result.data[0].url
                st.image(image_url, caption="🎨 AI-generated image", use_container_width=True)

# Footer
st.markdown("---")
st.caption("Created by [Your Name] · Powered by OpenAI · Streamlit App © 2025")

