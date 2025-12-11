"""
Quick email test script
Tests your email setup with Brevo or any SMTP service
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# CONFIGURATION - UPDATE THESE!
# ============================================

# For Brevo (formerly Sendinblue)
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@example.com"  # Your Brevo login email
SMTP_PASSWORD = "your-smtp-key-here"      # Get from Brevo → SMTP & API

# Email details
FROM_EMAIL = "ai@synapmarketing.com"
FROM_NAME = "SynapMarketing AI"
TO_EMAIL = "your-test-email@gmail.com"  # Your email to receive test

# ============================================
# TEST SCRIPT
# ============================================

def send_test_email():
    """Send a test email"""

    print("🚀 Starting email test...")
    print(f"📧 From: {FROM_EMAIL}")
    print(f"📬 To: {TO_EMAIL}")
    print(f"🌐 SMTP: {SMTP_SERVER}:{SMTP_PORT}")
    print()

    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "✅ Test Email from SynapMarketing"
    message["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    message["To"] = TO_EMAIL

    # HTML content
    html = """
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #667eea;">✅ Email Test Successful!</h1>

            <p>If you're reading this, your email setup is working perfectly!</p>

            <h2>What was tested:</h2>
            <ul>
                <li>✅ SMTP connection</li>
                <li>✅ Authentication</li>
                <li>✅ Sending from custom domain</li>
                <li>✅ HTML rendering</li>
            </ul>

            <h2>Next steps:</h2>
            <ol>
                <li>Check if this landed in inbox (not spam)</li>
                <li>Test with mail-tester.com for spam score</li>
                <li>Integrate with LLM Evaluator</li>
            </ol>

            <hr>
            <p style="color: #666; font-size: 12px;">
                Sent from: <strong>{from_email}</strong><br>
                Server: {smtp_server}<br>
                Time: {timestamp}
            </p>
        </body>
    </html>
    """.format(
        from_email=FROM_EMAIL,
        smtp_server=SMTP_SERVER,
        timestamp=__import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # Plain text fallback
    text = """
    EMAIL TEST SUCCESSFUL!

    If you're reading this, your email setup is working!

    What was tested:
    - SMTP connection
    - Authentication
    - Sending from custom domain

    Next: Check if this landed in inbox (not spam)
    """

    # Attach both versions
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Send email
    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

        print("Authenticating...")
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        print("Sending email...")
        server.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())

        print()
        print("=" * 50)
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print("=" * 50)
        print()
        print(f"📬 Check your inbox: {TO_EMAIL}")
        print("💡 If not in inbox, check spam folder")
        print()
        print("🎯 Next: Test spam score at mail-tester.com")

        server.quit()

        return True

    except smtplib.SMTPAuthenticationError:
        print()
        print("=" * 50)
        print("❌ AUTHENTICATION FAILED")
        print("=" * 50)
        print()
        print("Check your credentials:")
        print(f"  Username: {SMTP_USERNAME}")
        print("  Password: {SMTP_PASSWORD[:5]}...")
        print()
        print("For Brevo:")
        print("  1. Go to SMTP & API settings")
        print("  2. Generate new SMTP key")
        print("  3. Update SMTP_PASSWORD in this script")

        return False

    except smtplib.SMTPException as e:
        print()
        print("=" * 50)
        print("❌ SMTP ERROR")
        print("=" * 50)
        print(f"Error: {str(e)}")
        print()
        print("Check:")
        print(f"  Server: {SMTP_SERVER}")
        print(f"  Port: {SMTP_PORT}")
        print(f"  From: {FROM_EMAIL}")

        return False

    except Exception as e:
        print()
        print("=" * 50)
        print("❌ UNEXPECTED ERROR")
        print("=" * 50)
        print(f"Error: {str(e)}")

        return False


if __name__ == "__main__":
    print()
    print("=" * 50)
    print("  EMAIL TEST SCRIPT")
    print("=" * 50)
    print()

    # Check if configured
    if SMTP_PASSWORD == "your-smtp-key-here":
        print("⚠️  CONFIGURATION NEEDED!")
        print()
        print("Please update these variables in the script:")
        print("  - SMTP_USERNAME (your Brevo login email)")
        print("  - SMTP_PASSWORD (your SMTP key from Brevo)")
        print("  - FROM_EMAIL (ai@synapmarketing.com)")
        print("  - TO_EMAIL (your email to receive test)")
        print()
        print("For Brevo SMTP key:")
        print("  1. Login to app.brevo.com")
        print("  2. Go to SMTP & API")
        print("  3. Click 'Generate a new SMTP key'")
        print("  4. Copy and paste here")
        print()
    else:
        send_test_email()
