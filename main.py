import streamlit as st
from docxtpl import DocxTemplate
import os
import mammoth
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Resume Builder", layout="wide")
st.title("🚀 Resume Builder")

# Instructions at the top
st.markdown("### 📖 Instructions")
st.markdown("""
1. **Fill in your personal information** - Name, email, phone, LinkedIn, and GitHub profiles
2. **Write a professional summary** - Brief overview of your skills and experience
3. **Add your education** - Degree, school, year, and GPA/score
4. **Include work experience** (optional) - Previous roles and responsibilities
5. **List your projects** - Showcase your work with tech stack and descriptions
6. **Specify your skills** - Programming languages, frameworks, databases, and tools
7. **Generate and download** your resume as a DOCX file
""")
st.markdown("---")

# Helper function to validate URLs
def validate_url(url):
    if url and not url.startswith(('http://', 'https://')):
        return f"https://{url}"
    return url

# Personal Information
st.header("📋 Personal Information")
c1, c2 = st.columns(2)
with c1:
    first_name = st.text_input("First Name", placeholder="e.g., John")
with c2:
    last_name = st.text_input("Last Name", placeholder="e.g., Doe")

c3, c4 = st.columns(2)
with c3:
    email = st.text_input("Email", placeholder="e.g., john.doe@email.com")
with c4:
    phone = st.text_input("Phone Number", placeholder="e.g., +1 (555) 123-4567")

c5, c6 = st.columns(2)
with c5:
    linkedin = st.text_input("LinkedIn URL", placeholder="e.g., linkedin.com/in/johndoe")
with c6:
    github = st.text_input("GitHub URL", placeholder="e.g., github.com/johndoe")

# Professional Summary
st.header("📝 Professional Summary")
summary = st.text_area("Summary", height=100, placeholder="Write a brief professional summary about yourself...")

# Education Section
st.header("🎓 Education")
edu_count = st.number_input("Number of education entries", min_value=1, max_value=5, value=1, step=1)
educations = []
for i in range(int(edu_count)):
    with st.expander(f"Education Entry {i+1}"):
        e1, e2 = st.columns(2)
        with e1:
            degree = st.text_input("Degree", key=f"degree_{i}", placeholder="e.g., Bachelor of Computer Science")
        with e2:
            school = st.text_input("School/University", key=f"school_{i}", placeholder="e.g., University Name")
        e3, e4 = st.columns(2)
        with e3:
            edu_year = st.text_input("Year", key=f"edu_year_{i}", placeholder="e.g., 2020-2024")
        with e4:
            score = st.text_input("Score/GPA", key=f"score_{i}", placeholder="e.g., 3.8/4.0 or 85%")
        educations.append({
            "degree": degree, 
            "school": school, 
            "year": edu_year,  # Fixed: changed from "edu_year" to "year" to match template
            "score": score
        })

# Experience Section
st.header("💼 Experience")
exp_count = st.number_input("Number of experiences", min_value=0, max_value=5, value=0, step=1)
experiences = []
for i in range(int(exp_count)):
    with st.expander(f"Experience {i+1}"):
        ex1, ex2, ex3 = st.columns(3)
        with ex1:
            role = st.text_input("Role", key=f"role_{i}", placeholder="e.g., Software Developer")
        with ex2:
            company = st.text_input("Company", key=f"company_{i}", placeholder="e.g., Tech Corp")
        with ex3:
            duration = st.text_input("Duration", key=f"duration_{i}", placeholder="e.g., Jan 2023 - Present")
        desc = st.text_area("Description", key=f"desc_{i}", placeholder="Describe your responsibilities and achievements...")
        experiences.append({"role": role, "company": company, "duration": duration, "desc": desc})

# Projects Section
st.header("🚀 Projects")
proj_count = st.number_input("Number of projects", min_value=1, max_value=5, value=1, step=1)
projects = []
for i in range(int(proj_count)):
    with st.expander(f"Project {i+1}"):
        p1, p2 = st.columns(2)
        with p1:
            title = st.text_input("Title", key=f"proj_title_{i}", placeholder="e.g., E-commerce Website")
        with p2:
            stack = st.text_input("Tech Stack", key=f"stack_{i}", placeholder="e.g., React, Node.js, MongoDB")
        proj_summary = st.text_area("Summary", key=f"proj_summary_{i}", placeholder="Describe the project and your contributions...")
        projects.append({"title": title, "stack": stack, "summary": proj_summary})

# Skills Section
st.header("🛠️ Skills")
skills = {
    "programming_languages": st.text_input("Programming Languages", placeholder="e.g., Python, JavaScript, Java"),
    "frameworks": st.text_input("Frameworks & Libraries", placeholder="e.g., React, Django, Flask"),
    "databases": st.text_input("Databases", placeholder="e.g., MySQL, MongoDB, PostgreSQL"),
    "other_tools": st.text_input("Other Tools & Technologies", placeholder="e.g., Git, Docker, AWS")
}

# Function to generate DOCX from template
def generate_resume_docx(data):
    try:
        if not os.path.exists("temp.docx"):
            st.error("❌ Template file 'temp.docx' not found. Please ensure the template file is in the same directory as this script.")
            return None

        doc = DocxTemplate("temp.docx")
        doc.render(data)

        docx_io = BytesIO()
        doc.save(docx_io)
        docx_io.seek(0)
        return docx_io
    except Exception as e:
        st.error(e)
        return None

# Validation function
def validate_required_fields():
    errors = []
    if not first_name.strip():
        errors.append("First Name is required")
    if not last_name.strip():
        errors.append("Last Name is required")
    if not email.strip():
        errors.append("Email is required")
    
    # Validate email format
    if email.strip() and "@" not in email:
        errors.append("Please enter a valid email address")
    
    # Check if at least one education entry has required fields
    edu_valid = False
    for edu in educations:
        if edu["degree"].strip() and edu["school"].strip():
            edu_valid = True
            break
    if not edu_valid:
        errors.append("At least one education entry with Degree and School is required")
    
    # Check if at least one project has required fields
    proj_valid = False
    for proj in projects:
        if proj["title"].strip() and proj["summary"].strip():
            proj_valid = True
            break
    if not proj_valid:
        errors.append("At least one project with Title and Summary is required")
    
    return errors

# Generate Resume
st.markdown("---")
st.header("📄 Generate Your Resume")

if st.button("🔄 Generate DOCX Resume", type="primary", use_container_width=True):
    # Validate required fields
    validation_errors = validate_required_fields()
    
    if validation_errors:
        st.error("Please fill in the following required fields:")
        for error in validation_errors:
            st.error(f"• {error}")
    else:
        # Prepare data for template
        data = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": email.strip(),
            "phone_number": phone.strip(),
            "linkedin": validate_url(linkedin.strip()) if linkedin.strip() else "",
            "github": validate_url(github.strip()) if github.strip() else "",
            "summary": summary.strip(),
            "educations": [edu for edu in educations if edu["degree"].strip() or edu["school"].strip()],
            "experiences": [exp for exp in experiences if exp["role"].strip() or exp["company"].strip()],
            "projects": [proj for proj in projects if proj["title"].strip() or proj["summary"].strip()],
            "skills": {
                "programming_languages": skills["programming_languages"].strip(),
                "frameworks": skills["frameworks"].strip(),
                "databases": skills["databases"].strip(),
                "other_tools": skills["other_tools"].strip()
            }
        }

        with st.spinner("Generating your resume..."):
            docx_io = generate_resume_docx(data)

        if docx_io:
            # Preview using Mammoth
            st.info("📋 **Note:** The preview below is only for checking the details and may not show perfect formatting. Download the DOCX file to see the actual formatted resume.")
            
            try:
                # Reset BytesIO position for reading
                docx_io.seek(0)
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
                                max-width: 800px;
                                margin: 0 auto;
                                line-height: 1.6;
                            }}
                            h1, h2, h3 {{
                                color: #2c3e50;
                            }}
                            p {{
                                margin-bottom: 10px;
                            }}
                            a {{
                                color: #3498db;
                                text-decoration: none;
                            }}
                            a:hover {{
                                text-decoration: underline;
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
                st.warning(f"⚠️ Preview not available: {str(e)}")
                st.info("Don't worry! You can still download the DOCX file below.")

            # Reset BytesIO position for download
            docx_io.seek(0)
            
            # Download DOCX
            st.success("✅ DOCX Resume generated successfully!")
            
            # Create columns for download and feedback
            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    label="📥 Download DOCX Resume",
                    data=docx_io.getvalue(),
                    file_name=f"{first_name}_{last_name}_Resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            
            # Additional tips after successful generation
            st.info("💡 **Tips after downloading:**")
            st.info("• Open the DOCX file in Microsoft Word or Google Docs for final formatting")
            st.info("• You can manually add hyperlinks by selecting URLs and pressing Ctrl+K")
            st.info("• Customize fonts, colors, and spacing as needed")


# Sample data section
st.markdown("---")
st.markdown("### 📝 Need Help Getting Started?")
if st.button("Fill with Sample Data", help="Click to populate fields with example data"):
    data = {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com",
    "phone_number": "1 (123) 456-7890",
    "linkedin": "https://linkedin.com/in/janedoe",
    "github": "https://github.com/janedoe",
    "summary": "Detail-oriented software engineer with 3+ years of experience building scalable web applications. Passionate about building applications with clean code, performance optimization, and collaborative development.",

    "educations": [
        {
            "degree": "Bachelor of Technology in Computer Science",
            "school": "ABC University",
            "edu_year": "2018 - 2022",
            "score": "CGPA: 8.7/10"
        },
        {
            "degree": "High School Diploma",
            "school": "XYZ High School",
            "edu_year": "2016 - 2018",
            "score": "Percentage: 92%"
        }
    ],

    "experiences": [
        {
            "role": "Software Engineer",
            "company": "Tech Solutions Inc.",
            "duration": "July 2022 – Present",
            "desc": "• Developed RESTful APIs and integrated third-party services\n• Improved application performance by 30% through code refactoring\n• Collaborated with cross-functional teams using Agile methodology"
        },
        {
            "role": "Backend Developer Intern",
            "company": "Innovate Labs",
            "duration": "Jan 2022 – May 2022",
            "desc": "• Built microservices with Node.js and Express\n• Integrated MongoDB for dynamic data storage\n• Wrote unit and integration tests with Jest"
        }
    ],

    "projects": [
        {
            "title": "E-Commerce Web App",
            "stack": "React, Node.js, MongoDB",
            "summary": "• Designed and implemented a full-stack e-commerce platform with secure user authentication, cart system, and order history."
        },
        {
            "title": "AI Chatbot",
            "stack": "Python, TensorFlow, Flask",
            "summary": "• Developed a context-aware chatbot using NLP techniques, capable of handling customer service queries in real-time."
        }
    ],

    "skills": {
        "programming_languages": "Python, JavaScript, C++",
        "frameworks": "React, Node.js, Flask",
        "databases": "MongoDB, PostgreSQL",
        "other_tools": "Git, Docker, AWS, Linux"
    }
}
    with st.spinner("Generating your resume..."):
            docx_io = generate_resume_docx(data)
    if docx_io:
            # Preview using Mammoth
            st.info("📋 **Note:** The preview below is only for checking the details and may not show perfect formatting. Download the DOCX file to see the actual formatted resume.")
            
            try:
                # Reset BytesIO position for reading
                docx_io.seek(0)
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
                                max-width: 800px;
                                margin: 0 auto;
                                line-height: 1.6;
                            }}
                            h1, h2, h3 {{
                                color: #2c3e50;
                            }}
                            p {{
                                margin-bottom: 10px;
                            }}
                            a {{
                                color: #3498db;
                                text-decoration: none;
                            }}
                            a:hover {{
                                text-decoration: underline;
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
                st.warning(f"⚠️ Preview not available: {str(e)}")
                st.info("Don't worry! You can still download the DOCX file below.")

            # Reset BytesIO position for download
            docx_io.seek(0)
            
            # Download DOCX
            st.success("✅ DOCX Resume generated successfully!")
            
            # Create columns for download and feedback
            col1, col2 = st.columns([3, 1])
            with col1:
                st.download_button(
                    label="📥 Download DOCX Resume",
                    data=docx_io.getvalue(),
                    file_name=f"{first_name}_{last_name}_Resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            

# Footer
st.markdown("---")
st.markdown("*Built with ❤️ by Chaanakyaa M*")