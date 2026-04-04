"""Email HTML renderer for Cold Scout OSS."""
import os
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from app.config import get_settings
import bleach

settings = get_settings()


def get_template_env() -> Environment:
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    os.makedirs(template_dir, exist_ok=True)
    return Environment(loader=FileSystemLoader(template_dir))


def render_email_html(lead_data: dict, ai_body_html: str, tracking_token: str, app_url: str = "") -> str:
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'ul', 'ol', 'li', 'span', 'div', 'a', 'b', 'i']
    allowed_attrs = {'a': ['href', 'title', 'target'], '*': ['style']}
    sanitized_body = bleach.clean(ai_body_html, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    env = get_template_env()
    template_file = os.path.join(env.loader.searchpath[0], "email_html.j2")

    if not os.path.exists(template_file):
        # Create a default template
        with open(template_file, "w") as f:
            f.write(DEFAULT_EMAIL_TEMPLATE)

    template = env.get_template("email_html.j2")
    return template.render(
        business_name=lead_data.get("business_name", "Valued Business"),
        ai_body_html=sanitized_body,
        tracking_token=tracking_token,
        app_url=app_url,
        reply_email=settings.REPLY_TO_EMAIL or settings.FROM_EMAIL,
    )


DEFAULT_EMAIL_TEMPLATE = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Inter',-apple-system,sans-serif;">
  <div style="max-width:560px;margin:32px auto;background:#fff;border:1px solid #eaeaea;border-radius:12px;overflow:hidden;">
    <div style="background:#000;padding:24px 32px;">
      <h1 style="margin:0;font-size:20px;color:#fff;">Cold Scout</h1>
    </div>
    <div style="padding:28px 32px;">
      <p style="margin:0 0 16px;font-size:14px;color:#333;">Hi {{ business_name }},</p>
      {{ ai_body_html | safe }}
    </div>
    <div style="background:#fafafa;padding:16px 32px;text-align:center;">
      <p style="margin:0;font-size:11px;color:#999;">Reply to {{ reply_email }}</p>
    </div>
  </div>
</body>
</html>"""
