from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import random

def create_notice_pdf(filename, title, subject, date, content_lines):
    path = os.path.join(r"c:\Acadamic-regulation\backend\data", filename)
    c = canvas.Canvas(path, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"LBRCE OFFICIAL NOTICE: {title}")
    
    # Meta
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(100, 730, f"Issued Date: February 20, 2026")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 705, f"Subject: {subject}")
    c.drawString(100, 685, f"Event/Deadline Date: {date}")
    
    # Content
    c.setFont("Helvetica", 11)
    y = 650
    for line in content_lines:
        if line == "":
            y -= 10
            continue
        c.drawString(100, y, line)
        y -= 18
        
    # Footer
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, y - 40, "Authorized by: Campus Administration, LBRCE")
    
    c.save()
    print(f"Generated: {filename}")

def generate_all():
    data_dir = r"c:\Acadamic-regulation\backend\data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 1. Workshop
    create_notice_pdf(
        "workshop_ai.pdf",
        "GEN-AI WORKSHOP 2026",
        "Practical Workshop on Prompt Engineering and LLMs",
        "March 15, 2026",
        [
            "The Department of IT is organizing a one-day workshop on Generative AI.",
            "Students will learn how to build RAG applications like this agent!",
            "",
            "Time: 09:00 AM to 04:00 PM",
            "Venue: Seminar Hall 2",
            "Registration Fee: ₹200",
            "Prerequisites: Basic knowledge of Python."
        ]
    )

    # 2. Condonation Fees
    create_notice_pdf(
        "condonation_notice.pdf",
        "CONDONATION FEE DEADLINE",
        "Payment for Shortage of Attendance (B.Tech/M.Tech)",
        "April 10, 2026",
        [
            "Students having attendance between 65% and 75% must pay the",
            "condonation fee to be eligible for the end-semester examinations.",
            "",
            "Last Date to Pay: April 10, 2026",
            "Fee Amount: ₹1,500",
            "Payment Mode: Online ERP portal only.",
            "",
            "Note: Medical certificates must be submitted to the HOD office",
            "before the deadline."
        ]
    )

    # 3. Coding Contest
    create_notice_pdf(
        "coderush_2026.pdf",
        "CODERUSH NATIONAL CONTEST",
        "Annual Competitive Programming Championship",
        "May 05, 2026",
        [
            "Are you the fastest coder in LBRCE? Prove it at CodeRush 2026.",
            "Languages allowed: C++, Java, Python.",
            "",
            "Event Date: May 05, 2026",
            "Duration: 3 Hours",
            "Top Prize: Internship opportunity at TechCorp + ₹10,000.",
            "Register on the college portal under 'Student Activities'."
        ]
    )

    # 4. Vibe Coding Event
    create_notice_pdf(
        "vibe_coding.pdf",
        "MIDNIGHT VIBE CODING",
        "Lo-fi Beats & High-Code Session",
        "June 21, 2026",
        [
            "Join us for a unique 'Vibe Coding' night. No stress, just code.",
            "We provide the coffee, the lo-fi beats, and the high-speed internet.",
            "You bring your project and your laptop.",
            "",
            "Date: June 21, 2026",
            "Time: 08:00 PM to 02:00 AM",
            "Venue: Open Roof Amphitheater",
            "Entry: Free for all LBRCE students."
        ]
    )

    # 5. Technical Symposium
    create_notice_pdf(
        "symposium_notice.pdf",
        "TECH-VOICE SYMPOSIUM",
        "Paper Presentation & Project Expo",
        "September 12, 2026",
        [
            "Call for Papers: Submit your original research papers.",
            "Categories: Robotics, Blockchain, Cloud Computing.",
            "",
            "Submission Deadline: August 20, 2026",
            "Symposium Date: September 12, 2026",
            "Best Project Award: ₹15,000",
            "Certificates will be provided to all participants."
        ]
    )

if __name__ == "__main__":
    generate_all()
