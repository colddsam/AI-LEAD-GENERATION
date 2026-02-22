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
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
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
        
        # --- Add Visual Chart ---
        drawing = Drawing(400, 200)
        
        data = [
            (30, 80),   # Current metrics (e.g., Visibility, Engagement)
            (75, 120)   # Projected metrics
        ]
        
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = data
        bc.strokeColor = colors.white
        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 150
        bc.valueAxis.valueStep = 30
        
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.categoryNames = ['Visibility', 'Engagement']
        
        # Custom colors for Current vs Projected
        bc.bars[0].fillColor = colors.HexColor('#94a3b8') # Slate for Current
        bc.bars[1].fillColor = colors.HexColor('#3498db') # Brand Blue for Projected

        drawing.add(bc)
        
        # Add Chart Title via String Shape
        title_str = String(200, 185, 'Projected Growth vs Current State', fontSize=12, textAnchor='middle')
        drawing.add(title_str)
        
        Story.append(drawing)
        Story.append(Spacer(1, 24))
        # --- End Visual Chart ---

        Story.append(Paragraph("Let's talk about building a platform tailored to your needs.", styles['Normal']))
        
        doc.build(Story)
        return filepath
    except Exception as e:
        logger.exception(f"Failed to generate PDF proposal for {business_name}")
        return None
