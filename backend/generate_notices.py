from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_hackathon_pdf():
    path = r"c:\Acadamic-regulation\backend\data\hackathon_notice.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "LBRCE OFFICIAL NOTICE: TECH-FEST HACKATHON 2026")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Subject: Invitation to Annual College Hackathon")
    c.drawString(100, 700, "Date: July 28, 2026")
    c.drawString(100, 680, "Venue: Central Computing Centre (CCC)")
    
    text = [
        "We are pleased to announce the LBRCE Hackathon 2026.",
        "This 24-hour event will challenge students to build innovative solutions",
        "in AI, Sustainability, and FinTech.",
        "",
        "Key Event Details:",
        "- Event Date: July 28, 2026",
        "- Team Size: 2-4 Members",
        "- Registration Deadline: July 20, 2026",
        "- Prize Pool: ₹50,000",
        "",
        "Contact the HOD of CSE for further details.",
        "Issued by: Dean of Academic Affairs, LBRCE."
    ]
    
    y = 650
    for line in text:
        c.drawString(100, y, line)
        y -= 20
        
    c.save()
    print(f"Created: {path}")

def create_fee_pdf():
    path = r"c:\Acadamic-regulation\backend\data\fee_payment_notice.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "LBRCE ACADEMIC YEAR 2025-26: FEE PAYMENT SCHEDULE")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Subject: Final Deadline for Semester Fee Payment")
    c.drawString(100, 700, "Circular No: LBRCE/AC/FEE/2026/04")
    
    text = [
        "All students are hereby informed that the final date for the payment",
        "of college tuition and hostel fees for the current semester is:",
        "",
        "DEADLINE: February 28, 2026",
        "",
        "Fine Policy:",
        "- Payment after Feb 28: ₹500 penalty per week.",
        "- Payment after March 10: Strict action including suspension of login IDs.",
        "",
        "Modes of Payment:",
        "1. Online Portal (ERP Login)",
        "2. Bank Challan at Union Bank of India, LBRCE Branch",
        "",
        "Please ignore this notice if you have already completed the payment.",
        "Issued by: Administrative Office, LBRCE."
    ]
    
    y = 650
    for line in text:
        c.drawString(100, y, line)
        y -= 20
        
    c.save()
    print(f"Created: {path}")

if __name__ == "__main__":
    if not os.path.exists(r"c:\Acadamic-regulation\backend\data"):
        os.makedirs(r"c:\Acadamic-regulation\backend\data")
    create_hackathon_pdf()
    create_fee_pdf()
