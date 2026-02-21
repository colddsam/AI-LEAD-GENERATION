import os
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any

def get_template_env() -> Environment:
    """Returns a Jinja2 Environment for rendering email templates."""
    # Ensure templates directory exists
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    os.makedirs(template_dir, exist_ok=True)
    return Environment(loader=FileSystemLoader(template_dir))

def render_email_html(lead_data: Dict[str, Any], ai_body_html: str, tracking_token: str, app_url: str) -> str:
    """
    Renders the final HTML email body using Jinja2, injecting the tracking pixel and AI content.
    """
    env = get_template_env()
    
    # Create a simple default template if it doesn't exist
    template_file = os.path.join(env.loader.searchpath[0], "email_html.j2")
    if not os.path.exists(template_file):
        with open(template_file, "w") as f:
            f.write("""
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .footer { font-size: 12px; color: #777; margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        {{ ai_body_html | safe }}
        
        <div class="footer">
            <p>Sent with care to {{ business_name }}.</p>
            <p>If you prefer not to receive these emails, please reply with 'unsubscribe'.</p>
        </div>
        <!-- Tracking Pixel -->
        <img src="{{ app_url }}/api/v1/track/open/{{ tracking_token }}" width="1" height="1" style="display:none;" />
    </div>
</body>
</html>
""")
            
    template = env.get_template("email_html.j2")
    
    html_content = template.render(
        business_name=lead_data.get("business_name", "Valued Business"),
        ai_body_html=ai_body_html,
        tracking_token=tracking_token,
        app_url=app_url
    )
    return html_content
