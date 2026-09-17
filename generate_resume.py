import os

def create_resume_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # PDF Content Stream with text layout
    stream_lines = [
        "BT",
        "/F1 22 Tf",
        "50 740 Td",
        "(PRADEEP KUMAR) Tj",
        "/F2 11 Tf",
        "0 -20 Td",
        "(Computer Science Engineering Student | Python Developer | AI/ML Enthusiast) Tj",
        "0 -15 Td",
        "(Email: pradeepkumar.cse@example.com | GitHub: github.com/your-username | LinkedIn: linkedin.com/in/your-username) Tj",
        
        # Line divider
        "ET",
        "q 0.2 0.3 0.5 rg 50 695 500 1.5 re f Q",
        "BT",
        
        # Professional Summary
        "/F1 13 Tf",
        "50 675 Td",
        "(PROFESSIONAL SUMMARY) Tj",
        "/F2 10 Tf",
        "0 -16 Td",
        "(Computer Science Engineering student focused on building practical technology solutions with Python,) Tj",
        "0 -13 Td",
        "(Artificial Intelligence, and modern web frameworks. Active builder with strong foundations in data) Tj",
        "0 -13 Td",
        "(structures, relational database modeling, and competitive hackathon prototyping.) Tj",
        
        # Education
        "/F1 13 Tf",
        "0 -24 Td",
        "(EDUCATION) Tj",
        "/F1 10 Tf",
        "0 -16 Td",
        "(Bachelor of Engineering (B.E.) - Computer Science and Engineering) Tj",
        "/F2 9.5 Tf",
        "0 -13 Td",
        "(Coursework: Object-Oriented Programming, Database Management Systems, Operating Systems, Computer Networks) Tj",
        
        # Technical Skills
        "/F1 13 Tf",
        "0 -22 Td",
        "(TECHNICAL SKILLS) Tj",
        "/F2 9.5 Tf",
        "0 -15 Td",
        "(Programming: Python, Java, C, C++) Tj",
        "0 -13 Td",
        "(Web Development: HTML5, CSS3, JavaScript, Flask, FastAPI) Tj",
        "0 -13 Td",
        "(Databases: MySQL, SQLite, MongoDB) Tj",
        "0 -13 Td",
        "(AI & Machine Learning: Natural Language Processing, Machine Learning, Data Analysis) Tj",
        "0 -13 Td",
        "(Developer Tools: Git, GitHub, VS Code, REST APIs) Tj",
        
        # Key Projects
        "/F1 13 Tf",
        "0 -22 Td",
        "(KEY PROJECTS) Tj",
        
        # Project 1
        "/F1 10 Tf",
        "0 -15 Td",
        "(1. AI-Powered College Chatbot | Python, Streamlit, NLP, Sentence Transformers) Tj",
        "/F2 9 Tf",
        "0 -12 Td",
        "(- Engineered an NLP conversational assistant indexing college admissions, curricula, and schedules.) Tj",
        "0 -11 Td",
        "(- Utilized sentence embeddings and cosine similarity to deliver instant, referenced answers.) Tj",
        
        # Project 2
        "/F1 10 Tf",
        "0 -15 Td",
        "(2. Citizen Safety and Travel Assistance Network | Python, Flask, SQLite, JS) Tj",
        "/F2 9 Tf",
        "0 -12 Td",
        "(- Developed a centralized web portal providing verified digital identity and emergency SOS broadcasts.) Tj",
        "0 -11 Td",
        "(- Built geofence-based alert zones and an administrative situational monitoring dashboard.) Tj",
        
        # Project 3
        "/F1 10 Tf",
        "0 -15 Td",
        "(3. Alcohol Quota Regulation System | Python, Flask, SQLite/MongoDB) Tj",
        "/F2 9 Tf",
        "0 -12 Td",
        "(- Implemented user age eligibility verification and dynamic monthly quota tracking across outlets.) Tj",
        
        # Project 4
        "/F1 10 Tf",
        "0 -15 Td",
        "(4. Plastic Waste Management System | Python, Flask, SQLite, HTML/CSS) Tj",
        "/F2 9 Tf",
        "0 -12 Td",
        "(- Created a municipal waste tracking and recycling rewards platform to encourage segregation.) Tj",
        
        # Hackathons & Achievements
        "/F1 13 Tf",
        "0 -22 Td",
        "(HACKATHONS & INNOVATION) Tj",
        "/F2 9.5 Tf",
        "0 -15 Td",
        "(- Participated in university hackathons engineering civic technology and environmental logistics.) Tj",
        "0 -13 Td",
        "(- Presented technical prototypes demonstrating full-stack architecture and machine learning pipelines.) Tj",
        
        "ET"
    ]
    
    content_stream = "\n".join(stream_lines).encode("latin-1")
    stream_len = len(content_stream)
    
    # Simple PDF structure
    objects = []
    
    # 1: Catalog
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    # 2: Pages
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    # 3: Page
    objects.append(
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>"
    )
    # 4: Contents
    objects.append(
        f"<< /Length {stream_len} >>\nstream\n".encode("latin-1") +
        content_stream +
        b"\nendstream"
    )
    # 5: Font Helvetica-Bold
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    # 6: Font Helvetica
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    
    # Write PDF file
    with open(output_path, "wb") as f:
        f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = []
        for i, obj in enumerate(objects, start=1):
            offsets.append(f.tell())
            f.write(f"{i} 0 obj\n".encode("latin-1"))
            f.write(obj)
            f.write(b"\nendobj\n")
            
        xref_offset = f.tell()
        f.write(b"xref\n")
        f.write(f"0 {len(objects) + 1}\n".encode("latin-1"))
        f.write(b"0000000000 65535 f \n")
        for off in offsets:
            f.write(f"{off:010d} 00000 n \n".encode("latin-1"))
            
        f.write(b"trailer\n")
        f.write(f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode("latin-1"))
        f.write(b"startxref\n")
        f.write(f"{xref_offset}\n".encode("latin-1"))
        f.write(b"%%EOF\n")

if __name__ == "__main__":
    create_resume_pdf("resume/resume.pdf")
    print("Created resume/resume.pdf successfully.")
