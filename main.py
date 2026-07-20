from typing import TypedDict, Annotated
from langchain_mistralai import ChatMistralAI
from langgraph.graph import START, END, StateGraph
from dotenv import load_dotenv
load_dotenv()

def merge_string(existing: str, new: str) -> str:
    """
    Reducer for string fields.
    If new value is not empty, use it.
    Otherwise keep existing.
    """
    if new:
        return new
    return existing


class ApplicationState(TypedDict):
    job_description : str
    resume_text : str
    job_analysis : Annotated[str, merge_string]
    skill_gap : Annotated[str, merge_string]
    resume_analysis : Annotated[str, merge_string]
    tailored_resume : Annotated[str, merge_string]
    cover_letter : Annotated[str, merge_string]
    interview_prep : Annotated[str, merge_string]
    final_package : Annotated[str, merge_string]

llm = ChatMistralAI(model="ministral-8b-2512",temperature=0.1)

def analyze_job_description(state:ApplicationState) -> dict:
    """
    Extract skills, requirements, keywords from job description.
    """
    print("Analyzing job description...")

    prompt = f"""
    You are an expert job description analyzer.

    Analyze the following job description and extract:
    1. Required Technical Skills
    2. Preferred/Nice-to-have Skills
    3. Key Responsibilities
    4. Important Keywords for ATS
    5. Company/Role Tone (formal, startup, creative, etc.)

    Format your response clearly with headers for each section.

    Job Description:
    {state['job_description']}
    """

    response = llm.invoke(prompt)
    return {"job_analysis": response.content}

def analyze_resume(state: ApplicationState) -> dict:
    """
    Extract candidate skills, experience, and strengths from resume.
    """
    print("Analyzing resume...")

    prompt = f"""
    You are an expert resume analyzer and career coach.

    Analyze the following resume and extract:
    1. Technical Skills the candidate has
    2. Years and type of Experience
    3. Key Projects and Achievements
    4. Strengths
    5. Areas that need improvement or are missing metrics

    Format your response clearly with headers for each section.

    Resume:
    {state['resume_text']}
    """

    response = llm.invoke(prompt)
    return {"resume_analysis": response.content}

def analyze_skill_gaps(state: ApplicationState) -> dict:
    """
    Compare JD requirements vs resume skills and find gaps.
    """
    print("Analyzing skill gaps...")

    prompt = f"""
    You are a career advisor helping a candidate improve their job application.

    Compare the Job Description Analysis and Resume Analysis below.

    Job Description Analysis:
    {state['job_analysis']}

    Resume Analysis:
    {state['resume_analysis']}

    Provide:
    1. Matching Skills (candidate has what the job needs)
    2. Missing Skills (job requires but candidate lacks)
    3. Skills to Highlight More (candidate has but didn't showcase well)
    4. Quick Recommendations to strengthen the application

    Be specific and actionable.
    """

    response = llm.invoke(prompt)
    return {"skill_gap": response.content}

def tailor_resume(state: ApplicationState) -> dict:
    """
    Rewrite and tailor the resume to match the job description.
    """
    print("✍️ Tailoring resume...")

    prompt = f"""
    You are an expert resume writer specializing in tailoring resumes for specific jobs.

    Using the candidate's original resume, the job description analysis, and skill gap analysis,
    rewrite and improve the resume to:
    1. Use keywords from the job description naturally
    2. Rewrite bullet points to be more impactful and measurable
    3. Highlight the most relevant experience for this specific role
    4. Add quantifiable achievements where possible
    5. Make it ATS-friendly

    Original Resume:
    {state['resume_text']}

    Job Description Analysis:
    {state['job_analysis']}

    Skill Gap Analysis:
    {state['skill_gap']}

    Write the full tailored resume in a clean, professional format.
    """

    response = llm.invoke(prompt)
    return {"tailored_resume": response.content}

def generate_cover_letter(state: ApplicationState) -> dict:
    """
    Generate a personalized, tailored cover letter.
    """
    print("Generating cover letter...")

    prompt = f"""
    You are an expert cover letter writer.

    Write a compelling, personalized cover letter for this candidate applying to this job.

    Guidelines:
    - 3-4 paragraphs
    - Opening: Hook that shows genuine interest in the role
    - Middle: Highlight 2-3 most relevant experiences/skills that match the job
    - Middle: Show you understand the company's needs
    - Closing: Confident call to action
    - Tone should match the company tone from the job description
    - Do NOT be generic — make it feel personal and specific

    Job Description Analysis:
    {state['job_analysis']}

    Candidate's Tailored Resume:
    {state['tailored_resume']}

    Skill Gaps and Strengths:
    {state['skill_gap']}

    Write the full cover letter.
    """

    response = llm.invoke(prompt)
    return {"cover_letter": response.content}

def generate_interview_prep(state: ApplicationState) -> dict:
    """
    Generate likely interview questions and suggested answers.
    """
    print("🎯 Generating interview prep...")

    prompt = f"""
    You are an expert interview coach.

    Based on the job description and candidate's profile, generate a helpful interview preparation guide.

    Include:

    ## Technical Questions (5 questions)
    - Questions likely to be asked based on required skills
    - For each: the question + a strong suggested answer based on candidate's experience

    ## Behavioral Questions (5 questions)
    - STAR-format questions relevant to the role
    - For each: the question + a strong suggested answer using candidate's background

    ## Questions to Ask the Interviewer (3 questions)
    - Smart questions that show genuine interest

    ## Key Talking Points
    - 3 main things the candidate should emphasize in the interview

    Job Description Analysis:
    {state['job_analysis']}

    Candidate Profile:
    {state['resume_analysis']}

    Skill Gaps to Address:
    {state['skill_gap']}
    """

    response = llm.invoke(prompt)
    return {"interview_prep": response.content}

def assemble_final_package(state: ApplicationState) -> dict:
    """
    Assemble everything into a final clean summary package.
    """
    print("📦 Assembling final package...")

    final_package = f"""
# AI Job Application Package
{'='*60}

## SKILL GAP ANALYSIS
{state['skill_gap']}

{'='*60}

## TAILORED RESUME
{state['tailored_resume']}

{'='*60}

## COVER LETTER
{state['cover_letter']}

{'='*60}

## INTERVIEW PREPARATION
{state['interview_prep']}

{'='*60}
    """

    return {"final_package": final_package}

graph = StateGraph(ApplicationState)
graph.add_node("analyze_job",analyze_job_description)
graph.add_node("analyze_resume",analyze_resume)
graph.add_node("skill_gap",analyze_skill_gaps)
graph.add_node("tailor_resume",tailor_resume)
graph.add_node("cover_letter",generate_cover_letter)
graph.add_node("interview_prep",generate_interview_prep)
graph.add_node("final_package",assemble_final_package)

graph.add_edge(START, "analyze_job")
graph.add_edge(START, "analyze_resume")
graph.add_edge("analyze_job",     "skill_gap")
graph.add_edge("analyze_resume", "skill_gap")
graph.add_edge("skill_gap", "tailor_resume")
graph.add_edge("skill_gap", "interview_prep")
graph.add_edge("tailor_resume",  "cover_letter")
graph.add_edge("interview_prep", "cover_letter")
graph.add_edge("cover_letter",  "final_package")
graph.add_edge("final_package", END)

graph.compile()