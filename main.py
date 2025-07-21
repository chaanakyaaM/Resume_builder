import streamlit as st
from docxtpl import DocxTemplate
import os
import mammoth
from io import BytesIO

# Set page configuration
st.set_page_config(page_title=" Resume Builder", layout="wide")
st.title("Resume Builder")

st.sidebar.title("Resume Sections")
st.sidebar.markdown("Fill out the fields below 👇")

# Personal Information
st.header("Personal Information")
c1, c2 = st.columns(2)
with c1:
    first_name = st.text_input("First Name")
with c2:
    last_name = st.text_input("Last Name")

email = st.text_input("Email")
phone = st.text_input("Phone Number")
linkedin = st.text_input("LinkedIn")
github = st.text_input("GitHub")

# Professional Summary
st.header("Professional Summary")
summary = st.text_area("Summary", height=100)

# Education Section
st.header("🎓 Education")
edu_count = st.number_input("Number of education entries", min_value=1, max_value=5, value=1, step=1)
educations = []
for i in range(int(edu_count)):
    with st.expander(f"Education Entry {i+1}"):
        degree = st.text_input("Degree", key=f"degree_{i}")
        school = st.text_input("School/University", key=f"school_{i}")
        edu_year = st.text_input("Year", key=f"edu_year_{i}")
        score = st.text_input("Score/GPA", key=f"score_{i}")
        educations.append({"degree": degree, "school": school, "year": edu_year, "score": score})

# Experience Section
st.header("Experience")
exp_count = st.number_input("Number of experiences", min_value=1, max_value=5, value=1, step=1)
experiences = []
for i in range(int(exp_count)):
    with st.expander(f"Experience {i+1}"):
        role = st.text_input("Role", key=f"role_{i}")
        company = st.text_input("Company", key=f"company_{i}")
        duration = st.text_input("Duration", key=f"duration_{i}")
        desc = st.text_area("Description", key=f"desc_{i}")
        experiences.append({"role": role, "company": company, "duration": duration, "desc": desc})

# Projects Section
st.header("Projects")
proj_count = st.number_input("Number of projects", min_value=1, max_value=5, value=1, step=1)
projects = []
for i in range(int(proj_count)):
    with st.expander(f"Project {i+1}"):
        title = st.text_input("Title", key=f"proj_title_{i}")
        stack = st.text_input("Tech Stack", key=f"stack_{i}")
        proj_summary = st.text_area("Summary", key=f"proj_summary_{i}")
        projects.append({"title": title, "stack": stack, "summary": proj_summary})

# Skills Section
st.header("Skills")
skills = {
    "programming_languages": st.text_input("Programming Languages"),
    "frameworks": st.text_input("Frameworks & Libraries"),
    "other_tools": st.text_input("Other Tools & Technologies")
}

# Function to generate DOCX from template
def generate_resume_docx(data):
    try:
        if not os.path.exists("temp.docx"):
            st.error("Template file 'temp.docx' not found.")
            return None

        doc = DocxTemplate("temp.docx")
        doc.render(data)

        docx_io = BytesIO()
        doc.save(docx_io)
        docx_io.seek(0)
        return docx_io
    except Exception as e:
        st.error(f"Error generating DOCX: {str(e)}")
        return None

# Generate Resume
st.markdown("---")
if st.button("Generate DOCX Resume"):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone,
        "linkedin": linkedin,
        "github": github,
        "summary": summary,
        "educations": educations,
        "experiences": experiences,
        "projects": projects,
        "skills": skills
    }

    docx_io = generate_resume_docx(data)

    if docx_io:
        # Preview using Mammoth
        st.markdown("- Note: The preview may not be perfect due to formatting limitations.You can see the generated resume after downloading it")
        try:
            result = mammoth.convert_to_html(docx_io)
            html_content = result.value

            styled_html = f"""
            <html>
                <head>
                    <style>
                        body {{
                            background-color: white;
                            color: black;
                            font-family: Calibri, sans-serif;
                            padding: 20px;
                        }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
            </html>
            """

            st.markdown("### 📄 Resume Preview")
            st.components.v1.html(styled_html, height=600, scrolling=True)
        except Exception as e:
            st.error(f"Error previewing DOCX: {str(e)}")

        # Download DOCX
        st.success("DOCX Resume generated successfully!")
        st.download_button(
            label="📥 Download DOCX",
            data=docx_io.getvalue(),
            file_name=f"{first_name}_{last_name}_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# Footer
st.markdown("*Built with ❤️ by Chaanakyaa M*")
