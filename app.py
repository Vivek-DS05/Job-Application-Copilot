import streamlit as st
from pypdf import PdfReader
from main import graph, ApplicationState

# ── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Application Copilot",
    page_icon="💼",
    layout="wide"
)

# ── Header ─────────────────────────────────────────────────
st.title("💼 AI Job Application Copilot")
st.caption("Upload your resume + paste a job description → Get a complete tailored application package")
st.divider()


# ── PDF Helper ─────────────────────────────────────────────
def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# ── Input Section ──────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Your Resume")
    resume_option = st.radio(
        "How do you want to provide your resume?",
        ["Upload PDF", "Paste Text"],
        horizontal=True
    )

    resume_text = ""

    if resume_option == "Upload PDF":
        uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
        if uploaded_file:
            resume_text = extract_text_from_pdf(uploaded_file)
            st.success("✅ Resume uploaded!")
            with st.expander("Preview extracted text"):
                st.write(resume_text[:1000] + "...")
    else:
        resume_text = st.text_area(
            "Paste your resume here",
            height=300,
            placeholder="Paste your full resume text here..."
        )

with col2:
    st.subheader("🏢 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=350,
        placeholder="Paste the full job description here..."
    )

st.divider()

# ── Generate Button ────────────────────────────────────────
generate_btn = st.button(
    "🚀 Generate My Application Package",
    type="primary",
    use_container_width=True
)

# ── Run Graph ──────────────────────────────────────────────
if generate_btn:
    if not resume_text:
        st.error("❌ Please provide your resume.")
    elif not job_description:
        st.error("❌ Please paste the job description.")
    else:
        with st.status("🤖 AI Agents Working...", expanded=True) as status:
            st.write("⚡ Step 1: Analyzing JD + Resume (parallel)...")
            st.write("⚡ Step 2: Finding skill gaps...")
            st.write("⚡ Step 3: Tailoring resume + Interview prep (parallel)...")
            st.write("⚡ Step 4: Writing cover letter...")
            st.write("⚡ Step 5: Assembling package...")

            try:
                # ── Compile and run the graph ──────────────────────
                app = graph.compile()

                result = app.invoke({
                    "job_description": job_description,
                    "resume_text":     resume_text,
                    "job_analysis":    "",
                    "resume_analysis": "",
                    "skill_gap":       "",
                    "tailored_resume": "",
                    "cover_letter":    "",
                    "interview_prep":  "",
                    "final_package":   ""
                })

                status.update(
                    label="✅ Done! Package Ready!",
                    state="complete"
                )

            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(f"Something went wrong: {str(e)}")
                st.stop()

        st.success("🎉 Your Application Package is Ready!")
        st.divider()

        # ── Results in Tabs ────────────────────────────────────
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Skill Gaps",
            "📄 Tailored Resume",
            "💌 Cover Letter",
            "🎯 Interview Prep",
            "📦 Full Package"
        ])

        with tab1:
            st.subheader("📊 Skill Gap Analysis")
            st.markdown(result["skill_gap"])

        with tab2:
            st.subheader("📄 Tailored Resume")
            st.markdown(result["tailored_resume"])
            st.download_button(
                "⬇️ Download Resume",
                result["tailored_resume"],
                "tailored_resume.txt"
            )

        with tab3:
            st.subheader("💌 Cover Letter")
            st.markdown(result["cover_letter"])
            st.download_button(
                "⬇️ Download Cover Letter",
                result["cover_letter"],
                "cover_letter.txt"
            )

        with tab4:
            st.subheader("🎯 Interview Prep")
            st.markdown(result["interview_prep"])
            st.download_button(
                "⬇️ Download Interview Prep",
                result["interview_prep"],
                "interview_prep.txt"
            )

        with tab5:
            st.subheader("📦 Complete Package")
            st.markdown(result["final_package"])
            st.download_button(
                "⬇️ Download Full Package",
                result["final_package"],
                "full_package.txt"
            )