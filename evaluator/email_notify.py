"""
Email notifications for LLM Evaluator
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from datetime import datetime


class EmailNotifier:
    """Send email notifications for evaluations"""

    def __init__(
        self,
        smtp_server="smtp-relay.brevo.com",
        smtp_port=587,
        username=None,
        password=None,
        from_email="ai@synapmarketing.com",
        from_name="LLM Evaluator"
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username or os.environ.get("SMTP_USERNAME")
        self.password = password or os.environ.get("SMTP_PASSWORD")
        self.from_email = from_email
        self.from_name = from_name

    def send_test(self, to_email):
        """Send a test email"""

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1 style="color: #667eea;">✅ LLM Evaluator Email Test</h1>

                <p>Your LLM Evaluator email notifications are working!</p>

                <h2>Setup Details:</h2>
                <ul>
                    <li>From: <strong>{self.from_email}</strong></li>
                    <li>Server: {self.smtp_server}</li>
                    <li>Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</li>
                </ul>

                <p>You'll receive notifications when:</p>
                <ul>
                    <li>✅ Evaluations complete</li>
                    <li>💰 Budget limits are reached</li>
                    <li>❌ Errors occur</li>
                </ul>

                <hr style="margin: 20px 0;">
                <p style="color: #666; font-size: 12px;">
                    Sent by LLM Evaluator<br>
                    <a href="https://github.com/synapmarketing/llm-evaluator">View on GitHub</a>
                </p>
            </body>
        </html>
        """

        return self._send_email(
            to_email=to_email,
            subject="✅ LLM Evaluator Email Test",
            html_content=html
        )

    def send_evaluation_complete(
        self,
        to_email,
        experiment_name,
        total_evaluations,
        pass_rate,
        total_cost,
        avg_latency,
        best_model=None,
        results_file=None
    ):
        """Send notification when evaluation completes"""

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
                    <h1 style="color: #667eea; margin-bottom: 10px;">🎉 Evaluation Complete!</h1>

                    <p style="font-size: 18px; color: #333;">
                        Your LLM evaluation <strong>{experiment_name}</strong> has finished.
                    </p>

                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; color: white; margin: 20px 0;">
                        <h2 style="margin: 0 0 15px 0; color: white;">📊 Results Summary</h2>

                        <table style="width: 100%; color: white;">
                            <tr>
                                <td style="padding: 8px 0;"><strong>Total Evaluations:</strong></td>
                                <td style="text-align: right;">{total_evaluations:,}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0;"><strong>Pass Rate:</strong></td>
                                <td style="text-align: right;">{pass_rate:.1%}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0;"><strong>Total Cost:</strong></td>
                                <td style="text-align: right;">${total_cost:.2f}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0;"><strong>Avg Latency:</strong></td>
                                <td style="text-align: right;">{avg_latency:.2f}s</td>
                            </tr>
                            {f'<tr><td style="padding: 8px 0;"><strong>Best Model:</strong></td><td style="text-align: right;">{best_model}</td></tr>' if best_model else ''}
                        </table>
                    </div>

                    <p style="margin-top: 30px;">
                        <a href="#" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            View Full Results
                        </a>
                    </p>

                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">

                    <p style="color: #666; font-size: 12px;">
                        Completed at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
                        Sent by LLM Evaluator
                    </p>
                </div>
            </body>
        </html>
        """

        attachments = []
        if results_file and os.path.exists(results_file):
            with open(results_file, 'rb') as f:
                attachments.append({
                    'filename': os.path.basename(results_file),
                    'content': f.read(),
                    'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                })

        return self._send_email(
            to_email=to_email,
            subject=f"✅ Evaluation Complete: {experiment_name}",
            html_content=html,
            attachments=attachments
        )

    def send_budget_alert(self, to_email, experiment_name, current_cost, budget_limit):
        """Send alert when budget limit is reached"""

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1 style="color: #ffc107;">⚠️ Budget Limit Reached</h1>

                <p>Your evaluation <strong>{experiment_name}</strong> has reached the budget limit.</p>

                <div style="background: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>Current Cost:</strong> ${current_cost:.2f}</p>
                    <p style="margin: 5px 0 0 0;"><strong>Budget Limit:</strong> ${budget_limit:.2f}</p>
                </div>

                <p>The evaluation has been stopped to prevent exceeding your budget.</p>

                <p style="color: #666; font-size: 12px;">
                    Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </p>
            </body>
        </html>
        """

        return self._send_email(
            to_email=to_email,
            subject=f"⚠️ Budget Alert: {experiment_name}",
            html_content=html
        )

    def send_error_notification(self, to_email, experiment_name, error_message):
        """Send notification when an error occurs"""

        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h1 style="color: #dc3545;">❌ Evaluation Error</h1>

                <p>An error occurred during evaluation: <strong>{experiment_name}</strong></p>

                <div style="background: #f8d7da; border-left: 5px solid #dc3545; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; font-family: monospace; color: #721c24;">{error_message}</p>
                </div>

                <p>Please check the logs for more details.</p>

                <p style="color: #666; font-size: 12px;">
                    Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </p>
            </body>
        </html>
        """

        return self._send_email(
            to_email=to_email,
            subject=f"❌ Error: {experiment_name}",
            html_content=html
        )

    def _send_email(self, to_email, subject, html_content, attachments=None):
        """Internal method to send email via SMTP"""

        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email

            # Add HTML content
            message.attach(MIMEText(html_content, "html"))

            # Add attachments
            if attachments:
                for attachment in attachments:
                    part = MIMEApplication(attachment['content'])
                    part.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=attachment['filename']
                    )
                    message.attach(part)

            # Send via SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.from_email, to_email, message.as_string())
            server.quit()

            print(f"✅ Email sent to {to_email}")
            return True

        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False


# Quick test function
def test_email():
    """Quick test of email functionality"""

    print("Testing email notifications...")

    # Get credentials from environment or prompt
    username = os.environ.get("SMTP_USERNAME") or input("SMTP Username: ")
    password = os.environ.get("SMTP_PASSWORD") or input("SMTP Password: ")
    to_email = input("Send test to (your email): ")

    notifier = EmailNotifier(username=username, password=password)

    # Send test email
    success = notifier.send_test(to_email)

    if success:
        print("\n✅ Test email sent!")
        print(f"📬 Check your inbox: {to_email}")
        print("💡 If not in inbox, check spam folder")
    else:
        print("\n❌ Failed to send test email")
        print("Check your SMTP credentials")


if __name__ == "__main__":
    test_email()
