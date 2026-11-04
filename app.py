from google import genai
import os
import streamlit as st

# Initialize Streamlit Page Config
st.set_page_config(
    page_title="UBC Science Co-op LinkedIn Post Generator",
    page_icon="🎓",
    layout="wide",
)

# Check if API key exists in secrets
if "GEMINI_API_KEY" not in st.secrets:
  st.error("Error: GEMINI_API_KEY is missing from Streamlit Secrets!")
  st.stop()

# Initialize Gemini Client with API key from secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# App Header
st.title("🎓 UBC Science Co-op LinkedIn Content Engine")
st.markdown(
    "Transform raw stats, industry articles, or program updates into polished,"
    " employer-focused LinkedIn posts that drive engagement and co-op hiring."
)

# Sidebar Configuration for Content Strategy
st.sidebar.header("Content Settings")
pillar = st.sidebar.selectbox(
    "Select Content Pillar",
    [
        (
            "Pillar A: Program Proof & Metrics (The Numbers)"
            if "A" in "Pillar A"
            else "Pillar A: Program Proof & Metrics"
        ),
        "Pillar B: The Hiring Timeline & Operational Ease",
        "Pillar C: Industry Trends & General Co-op Value (Hook-and-Bridge)",
        "Pillar D: Student Spotlight & Impact Stories",
    ],
)

tone = st.sidebar.selectbox(
    "Select Tone & Style",
    [
        "Authoritative & Strategic (Best for hiring managers/executives)",
        "Conversational & Approachable (Best for general networking)",
        "Data-Driven & Analytical (Focus on ROI and skills depth)",
    ],
)

include_cta = st.sidebar.checkbox(
    "Include UBC Science Co-op Employer CTA", value=True
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Tip: Paste raw notes, statistics, or article takeaways below. The AI will"
    " structure the hook, body, and bridge."
)

# Main Content Area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
  st.subheader("1. Input Raw Material")
  raw_input = st.text_area(
      "Paste stats, notes, article snippets, or rough thoughts here:",
      height=300,
      placeholder=(
          "e.g., We have over 400 computer science and data science students"
          " looking for summer co-op terms. Employers love their practical"
          " experience with Python and machine learning pipelines. Applications"
          " open next month."
      ),
  )

  generate_btn = st.button(
      "Generate LinkedIn Post", type="primary", use_container_width=True
  )

with col2:
  st.subheader("2. Staging Area & Draft")

  if generate_btn:
    if not raw_input.strip():
      st.warning("Please enter some raw notes or source material first.")
    else:
      with st.spinner("Drafting your post with Gemini..."):
        try:
          # Construct system prompt enforcing voice and safety/quality guidelines
          system_instruction = (
              "You are an expert career educator and program coordinator for"
              " the UBC Science Co-op program. Your goal is to write"
              " high-engagement LinkedIn posts targeting engineering and"
              " science hiring managers, tech leads, and recruiters to"
              " encourage them to hire UBC Science Co-op students.\n\nGuidelines:\n-"
              " Craft a compelling, attention-grabbing hook (short, punchy first"
              " line).\n- Use clean formatting with short paragraphs and"
              " bullet points for readability.\n- Maintain an authentic,"
              " professional, yet approachable voice.\n- Seamlessly bridge the"
              " core topic back to the value of hiring UBC Science Co-op"
              " students.\n- Include a clear, professional Call-to-Action"
              " (CTA) prompting employers to connect, review hiring timelines,"
              " or visit the employer portal."
          )

          prompt = (
              f"Please generate a LinkedIn post based on the following"
              f" details:\n\nContent Pillar: {pillar}\nDesired Tone:"
              f" {tone}\nInclude Employer CTA:"
              f" {'Yes' if include_cta else 'No'}\n\nRaw Source Material /"
              f" Notes:\n{raw_input}"
          )

          response = client.models.generate_content(
              model="gemini-3.8-flash",
              contents=prompt,
              config={
                  "system_instruction": system_instruction,
                  "temperature": 0.7,
              },
          )

          # Store in session state so edits persist
          st.session_state["generated_draft"] = response.text

        except Exception as e:
          st.error(f"Error generating post: {e}")

  # Display draft in an editable text area (Human-in-the-Loop staging)
  if "generated_draft" in st.session_state:
    edited_draft = st.text_area(
        "Review and refine your draft below before copying:",
        value=st.session_state["generated_draft"],
        height=350,
    )

    st.success("Draft ready! Review above and copy for publishing.")
  else:
    st.info("Your generated post will appear here for review and editing.") 
