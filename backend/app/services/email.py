import smtplib
import time
from email.mime.text import MIMEText
from typing import Optional

from sqlalchemy.orm import Session

from app.config import settings
from app.models.email_log import EmailLog


def send_email(db: Session, to_email: str, subject: str, content: str, purpose: str) -> bool:
    # 如果没有配置SMTP密码，则在开发模式下跳过实际发送
    if not settings.sender_password:
        print(f"\n=== 开发模式：邮件内容 ===")
        print(f"收件人: {to_email}")
        print(f"主题: {subject}")
        print(f"内容: {content}")
        print(f"========================\n")
        db.add(EmailLog(email=to_email, purpose=purpose, status="success", retry_count=0))
        db.commit()
        return True
    
    message = MIMEText(content, "html", "utf-8")
    message["Subject"] = subject
    message["From"] = settings.sender_email
    message["To"] = to_email

    retry = 0
    last_error: Optional[str] = None
    while retry < 5:
        try:
            with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port, timeout=10) as server:
                server.login(settings.sender_email, settings.sender_password)
                server.sendmail(settings.sender_email, [to_email], message.as_string())
                db.add(EmailLog(email=to_email, purpose=purpose, status="success", retry_count=retry))
                db.commit()
                return True
        except Exception as e:  # noqa
            last_error = str(e)
            retry += 1
            time.sleep(0.5 * (2 ** (retry - 1)))
    db.add(EmailLog(email=to_email, purpose=purpose, status="fail", error_message=last_error or "", retry_count=retry))
    db.commit()
    return False