"""
PDF Document generation module.
Utilizes ReportLab to dynamically synthesize customized proposal documents 
incorporating LLM-generated insights for individual leads.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from typing import List
from loguru import logger

def generate_proposal_pdf(business_name: str, category: str, benefits: List[str], output_filename: str = "proposal.pdf") -> str:
    """
    Synthesizes a tailored PDF proposal outlining digital strategy improvements based on the extracted business context.
    
    Args:
        business_name (str): The legal or trading name of the target business.
        category (str): The operational archetype of the target business.
        benefits (List[str]): Structurally generated value propositions supplied by the LLM.
        output_filename (str, optional): The designated filename for the resulting PDF. Defaults to "proposal.pdf".
        
    Returns:
        str: The absolute or relative file path to the generated document upon success, or None upon failure.
    """
    try:
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
    except Exception as e:
        logger.exception(f"Failed to generate PDF proposal for {business_name}")
        return None
