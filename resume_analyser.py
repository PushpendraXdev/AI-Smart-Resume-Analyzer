import streamlit as st
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go

#description based score
def ats_score(resume,job_description):
    texts=[resume.lower(),job_description.lower()]
    tf=TfidfVectorizer(stop_words='english')
    tf_matri=tf.fit_transform(texts)
    similar=cosine_similarity(tf_matri[0:1],tf_matri[1:2])[0][0]
    score=round(similar*100,2)
    return score
# auto score
def auto_score(resume):
    scored=0
    if '@' in resume or 'email' in resume.lower():
        scored+=5
    if 'linkedin' in resume.lower():
        scored+=3
    if 'achievements' in resume.lower() or 'certificates' in resume.lower() or 'certifications' in resume.lower():
        scored+=10
    if 'skills' in resume.lower():
        scored+=15
    if 'experience' in resume.lower() or 'internship' in resume.lower() or 'experiences' in resume.lower() or 'internships' in resume.lower():
        scored+=25
    if 'project' in resume.lower() or 'projects' in resume.lower():
        scored+=25
    if 'professional summary' in resume.lower() or 'summary' in resume.lower():
        scored+=5
    return scored

#sidebar
st.sidebar.title("AI Resume Analyser")
st.sidebar.write("________________________________________________________________________________________________________")
user_name=st.sidebar.text_input("Enter your good name")
st.sidebar.subheader("About")
st.sidebar.markdown("""
AI Resume Analyzer is an intelligent web application that helps job seekers optimize their resumes for better shortlisting chances. Powered by machine learning and natural language processing, the tool scans uploaded resumes and provides a detailed analysis based on key hiring metrics.

🔍 Key Features:

🍏 Resume Score based on job readiness.

🍏 Skill Match with the target job description.

🍏 Keyword Analysis for ATS compatibility.

🍏 Charts & Visual Insights.

🍏 Section Check to verify all essential parts (summary, skills, education, experience, etc.)
""")

st.sidebar.write("________________________________________________________________________________________________________")
st.sidebar.write("Whether you're a fresher or an experienced professional, this AI tool helps user to analyse its resume data its performance.")


#starting

st.title('🧠 AI Resume Analyser')
if user_name:
    st.header(f"Hey! {user_name}")
else:
  st.header("Hey!")
st.write("An intelligent ATS-friendly resume analyzer with keyword matching, scoring, feedback, and visual insights — built with NLP. Here your resume is fully analysed and based on keyword and description it gives you score,charts and strong points what should needed.")
st.write('____________________________________________________________________________________________________________')
job_description=st.text_input("Job Desceiption",width=1000)
uploaded_file=st.file_uploader("👉🏻 Please upload your 'Resume'",type=["pdf"])


if uploaded_file:
    st.sidebar.subheader(f"Thankyou!")
    st.sidebar.write(f"for choosing our Platform, Hope you it helps you.")
    st.write("________________________________________________________________________________________________________")
    st.success("Data is Accepted")
    st.write("________________________________________________________________________________________________________")
    file_type=uploaded_file.type
    resume=""
    if file_type=="application/pdf":
        try:
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page in doc:
                    resume+=page.get_text()
        except Exception as e:
            st.error(f"File error:{e}")
    else:
        st.error(f"file type is not pdf")

    st.text_area("Resume content",resume,height=200)

    ats_sc= ats_score(resume,job_description)
    st.write("________________________________________________________________________________________________________")
    st.header("Your Resume Score 🔔")
    st.write("________________________________________________________________________________________________________")
    st.subheader("✅ 𝑨𝒄𝒄𝒐𝒓𝒅𝒊𝒏𝒈 𝒕𝒐 𝒅𝒆𝒔𝒄𝒓𝒊𝒑𝒕𝒊𝒐𝒏 🔦")
    st.metric(label="ATS Score 🛠",value=f"{ats_sc}%")
    if ats_sc>=90:
        st.success("Excellent ♛")
    elif ats_sc>=75:
     st.success("Good ♞")
    elif ats_sc>=50:
     st.success("Not Bad->Need Improvement")
    else:
     st.error("Fair")
    st.write("________________________________________________________________________________________________________")
    st.subheader("✅ 𝑨𝒄𝒄𝒐𝒓𝒅𝒊𝒏𝒈 𝒕𝒐 𝑨𝒖𝒕𝒐 𝑺𝒄𝒐𝒓𝒆 💡")
    st.write("(This auto score is based on keyword and description its around every job, every field based)")
    auto_scored=auto_score(resume)
    st.metric(label="ATS Score 💪🏼",value=f"{auto_scored}")
    if auto_scored>=90:
        st.success("Excellent ♛")
    elif auto_scored>=75:
        st.success("Good ♞")
    elif auto_scored>=50:
        st.success("Not Bad -> Need Improvement")
    else:
        st.error("Fair")
    st.write("________________________________________________________________________________________________________")

    st.subheader("Charts Based Configure 🕯")
    col1,col2=st.columns(2)
    left=100-auto_scored
    with col1:
        values=[auto_scored,left]
        fig=go.Figure(data=[go.Pie(values=values)])
        #fig.update.traces('values')
       # fig.update_layout(title='Auto Score and Description')
        st.plotly_chart(fig)
    with col2:
        vscore=[20,40,60,80,100]
        hwhat=['Description','Auto']
        fig=go.Figure(data=[
            go.Bar(x=hwhat,y=values)
        ])
        #fig.update_layout(title='Auto Score')
        st.plotly_chart(fig)

