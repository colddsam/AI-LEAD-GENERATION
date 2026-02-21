from datetime import date
from app.config import settings
from app.modules.outreach.email_sender import send_email

async def send_daily_report_email(report_data: dict, excel_filepath: str, output_date: date) -> bool:
    """
    Sends the generated daily report to the administrator.
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
    
    # We use the same email sender module built for outreach, but direct it to ADMIN
    return await send_email(
        to_email=settings.ADMIN_EMAIL,
        subject=subject,
        html_content=html_body,
        attachment_paths=[excel_filepath] if excel_filepath else []
    )
