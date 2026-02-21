import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from typing import List

def generate_proposal_pdf(business_name: str, category: str, benefits: List[str], output_filename: str = "proposal.pdf") -> str:
    """
    Generates a personalized PDF proposal for a lead.
    Returns the file path.
    """
    os.makedirs("tmp", exist_ok=True)
    filepath = os.path.join("tmp", output_filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    
    Story = []
    
    title = f"Digital Growth Proposal for<br/><b>{business_name}</b>"
    Story.append(Paragraph(title, styles['Title']))
    Story.append(Spacer(1, 24))
    
    intro = f"As a local {category}, your digital presence is critical to capturing nearby customers. Here are three key areas we've identified that can bring more foot traffic and sales:"
    Story.append(Paragraph(intro, styles['Normal']))
    Story.append(Spacer(1, 12))
    
    for b in benefits:
        Story.append(Paragraph(f"• {b}", styles['Normal']))
        Story.append(Spacer(1, 6))
        
    Story.append(Spacer(1, 24))
    Story.append(Paragraph("Let's talk about building a platform tailored to your needs.", styles['Normal']))
    
    doc.build(Story)
    return filepath
