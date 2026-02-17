"""
邮件发送节点 - 将分析结果发送到邮箱
"""
import os
import smtplib
import ssl
import time
import json
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr, formatdate, make_msgid
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_workload_identity import Client
from cozeloop.decorator import observe
from graphs.state import EmailSendInput, EmailSendOutput


def get_email_config():
    """获取邮件配置信息"""
    client = Client()
    email_credential = client.get_integration_credential("integration-email-imap-smtp")
    return json.loads(email_credential)


@observe
def email_send_node(state: EmailSendInput, config: RunnableConfig, runtime: Runtime[Context]) -> EmailSendOutput:
    """
    title: 发送邮件
    desc: 将股票分析结果通过邮件发送给指定收件人
    integrations: 邮件集成
    """
    ctx = runtime.context
    
    try:
        email_config = get_email_config()
        
        # 检查是否有收件人
        recipients = state.email_recipients if state.email_recipients else []
        if not recipients:
            return EmailSendOutput(
                status="failed",
                message="收件人列表为空",
                recipient_count=0,
                result="邮件发送失败：无收件人"
            )
        
        # 创建HTML邮件
        html_content = f"""
        <html>
        <body>
            <h2 style="color: #333;">{state.email_subject}</h2>
            <div style="line-height: 1.6; color: #555;">
                {state.email_content.replace('\n', '<br>')}
            </div>
            <hr style="margin-top: 20px; border: none; border-top: 1px solid #eee;">
            <p style="color: #999; font-size: 12px;">
                本邮件由智能股票分析系统自动发送
            </p>
        </body>
        </html>
        """
        
        msg = MIMEText(html_content, "html", "utf-8")
        msg["From"] = formataddr(("智能股票分析助手", email_config["account"]))
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = Header(state.email_subject, "utf-8")
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()
        
        all_recipients = recipients.copy()
        
        # 创建SSL上下文
        ctx_ssl = ssl.create_default_context()
        ctx_ssl.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # 尝试发送（最多3次重试）
        attempts = 3
        last_err = None
        
        for i in range(attempts):
            try:
                with smtplib.SMTP_SSL(
                    email_config["smtp_server"],
                    email_config["smtp_port"],
                    context=ctx_ssl,
                    timeout=30
                ) as server:
                    server.ehlo()
                    server.login(email_config["account"], email_config["auth_code"])
                    server.sendmail(email_config["account"], all_recipients, msg.as_string())
                    server.quit()
                
                return EmailSendOutput(
                    status="success",
                    message=f"邮件成功发送给 {len(recipients)} 位收件人",
                    recipient_count=len(recipients),
                    email_send_result=f"邮件发送成功，收件人数：{len(recipients)}"
                )
            except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError,
                    smtplib.SMTPDataError, smtplib.SMTPHeloError,
                    ssl.SSLError, OSError) as e:
                last_err = e
                time.sleep(1 * (i + 1))
        
        # 重试失败
        if last_err:
            return EmailSendOutput(
                status="failed",
                message=f"发送失败: {type(last_err).__name__}",
                recipient_count=0,
                email_send_result=f"邮件发送失败：{type(last_err).__name__}"
            )
        
        return EmailSendOutput(
            status="failed",
            message="发送失败: 未知错误",
            recipient_count=0,
            email_send_result="邮件发送失败：未知错误"
        )
        
    except smtplib.SMTPAuthenticationError as e:
        return EmailSendOutput(
            status="failed",
            message=f"认证失败: {str(e)}",
            recipient_count=0,
            email_send_result="邮件发送失败：认证失败"
        )
    except smtplib.SMTPRecipientsRefused as e:
        return EmailSendOutput(
            status="failed",
            message="收件人被拒绝",
            recipient_count=0,
            email_send_result="邮件发送失败：收件人被拒绝"
        )
    except Exception as e:
        return EmailSendOutput(
            status="failed",
            message=f"发送失败: {str(e)}",
            recipient_count=0,
            email_send_result=f"邮件发送失败：{str(e)}"
        )
