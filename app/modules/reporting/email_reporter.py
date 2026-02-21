"""
Administrator reporting summary dispatch module.
Constructs and dispatches HTML-formatted email reports with encapsulated
statistical metrics and attached analytical documents.
"""
from datetime import date
from app.config import get_settings
settings = get_settings()
from app.modules.outreach.email_sender import send_email

async def send_daily_report_email(report_data: dict, excel_filepath: str, output_date: date) -> bool:
    """
    Dispatches the aggregated daily statistical report to the configured administrative recipient.
    
    Args:
        report_data (dict): Dictionary comprising the daily quantitative metrics.
        excel_filepath (str): Absolute or relative path to the generated Excel artifact.
        output_date (date): The contextual date associated with the report.
        
    Returns:
        bool: True if the dispatch was successfully processed, False otherwise.
    """
    if not settings.ADMIN_EMAIL:
        return False
        
    subject = f"[LeadGen] Daily Report - {output_date} | {report_data.get('emails_sent', 0)} sent | {report_data.get('links_clicked', 0)} clicks"
    
    html_body = f"""
    <html>
    <body>
        <h2>Daily Lead Generation Report: {output_date}</h2>
        <table border="1" cellpadding="5" style="border-collapse: collapse;">
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Leads Discovered</td><td>{report_data.get('leads_discovered', 0)}</td></tr>
            <tr><td>Leads Qualified</td><td>{report_data.get('leads_qualified', 0)}</td></tr>
            <tr><td>Emails Sent</td><td>{report_data.get('emails_sent', 0)}</td></tr>
            <tr><td>Emails Opened</td><td>{report_data.get('emails_opened', 0)}</td></tr>
            <tr><td>Links Clicked</td><td>{report_data.get('links_clicked', 0)}</td></tr>
            <tr><td>Replies Received</td><td>{report_data.get('replies_received', 0)}</td></tr>
        </table>
        <p>Please find the detailed Excel report attached.</p>
    </body>
    </html>
    """
    
    return await send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=subject,
        html_content=html_body,
        attachment_paths=[excel_filepath] if excel_filepath else []
    )
