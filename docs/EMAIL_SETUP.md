# Email Setup Guide

Configure automated email notifications for evaluation results.

## Table of Contents

- [Quick Start](#quick-start)
- [SMTP Configuration](#smtp-configuration)
- [Popular Email Providers](#popular-email-providers)
- [Testing Email Setup](#testing-email-setup)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Create Secrets File

Create `.streamlit/secrets.toml` in the project root:

```bash
mkdir -p .streamlit
touch .streamlit/secrets.toml
```

### 2. Add SMTP Configuration

```toml
[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your-email@gmail.com"
smtp_password = "your-app-password"
sender_email = "your-email@gmail.com"
sender_name = "LLM Evaluator"
use_tls = true
```

### 3. Verify Configuration

1. Launch Streamlit: `streamlit run streamlit_app/app.py`
2. Go to Settings page
3. Click "Test Email Configuration"
4. Check your inbox

---

## SMTP Configuration

### Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `smtp_server` | SMTP server hostname | `smtp.gmail.com` |
| `smtp_port` | SMTP server port | `587` (TLS) or `465` (SSL) |
| `smtp_username` | Email account username | `user@example.com` |
| `smtp_password` | Email account password or app password | `your-app-password` |
| `sender_email` | From email address | `noreply@example.com` |
| `sender_name` | From name | `LLM Evaluator Bot` |
| `use_tls` | Use TLS encryption | `true` or `false` |

### Security Best Practices

✅ **DO:**
- Use app-specific passwords (not your main password)
- Enable 2FA on your email account
- Use `.streamlit/secrets.toml` (automatically gitignored)
- Rotate passwords regularly

❌ **DON'T:**
- Commit passwords to version control
- Share your secrets.toml file
- Use your main email password
- Disable 2FA to enable SMTP

---

## Popular Email Providers

### Gmail

**Best for:** Personal projects, development

**Configuration:**
```toml
[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your-email@gmail.com"
smtp_password = "your-app-password"
sender_email = "your-email@gmail.com"
sender_name = "LLM Evaluator"
use_tls = true
```

**Setup Steps:**

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Create App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Enter "LLM Evaluator"
   - Copy the 16-character password
   - Use this as `smtp_password`

3. **Test Configuration**
   - Send test email from Settings page

**Limits:**
- 500 emails/day (free Gmail)
- 2,000 emails/day (Google Workspace)

**Troubleshooting:**
- Ensure "Less secure app access" is OFF (use app passwords instead)
- Check spam folder for test emails
- Verify 2FA is enabled

---

### Outlook / Microsoft 365

**Best for:** Enterprise users

**Configuration:**
```toml
[email]
smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_username = "your-email@outlook.com"
smtp_password = "your-password"
sender_email = "your-email@outlook.com"
sender_name = "LLM Evaluator"
use_tls = true
```

**Setup Steps:**

1. **Enable SMTP AUTH** (if using Office 365)
   - Admin center → Settings → Org settings
   - Mail → Modern authentication
   - Enable SMTP AUTH

2. **Use App Password** (if 2FA enabled)
   - Go to https://account.microsoft.com/security
   - Security info → Add method → App password
   - Create password for "LLM Evaluator"

3. **Test Configuration**

**Limits:**
- 300 emails/day (Outlook.com)
- 10,000 emails/day (Office 365)

---

### Brevo (formerly SendinBlue)

**Best for:** High-volume sending, production

**Configuration:**
```toml
[email]
smtp_server = "smtp-relay.brevo.com"
smtp_port = 587
smtp_username = "your-brevo-email@example.com"
smtp_password = "your-smtp-key"
sender_email = "noreply@yourdomain.com"
sender_name = "LLM Evaluator"
use_tls = true
```

**Setup Steps:**

1. **Create Free Account**
   - Go to https://www.brevo.com
   - Sign up (free tier: 300 emails/day)

2. **Get SMTP Credentials**
   - Dashboard → SMTP & API
   - Copy SMTP server and port
   - Generate SMTP key (use as password)

3. **Verify Sender Domain** (optional but recommended)
   - Add your domain
   - Add DNS records
   - Verify ownership

**Limits:**
- 300 emails/day (free)
- 40,000 emails/month (Lite plan - $25/mo)
- Unlimited (Business plans)

**Advantages:**
- ✅ Higher delivery rates
- ✅ Email tracking and analytics
- ✅ No need for app passwords
- ✅ Dedicated IP available

---

### SendGrid

**Best for:** Developers, API integration

**Configuration:**
```toml
[email]
smtp_server = "smtp.sendgrid.net"
smtp_port = 587
smtp_username = "apikey"
smtp_password = "your-sendgrid-api-key"
sender_email = "verified@yourdomain.com"
sender_name = "LLM Evaluator"
use_tls = true
```

**Setup Steps:**

1. **Create Account**
   - Go to https://sendgrid.com
   - Free tier: 100 emails/day

2. **Create API Key**
   - Settings → API Keys
   - Create API Key
   - Full Access or Restricted (Mail Send)
   - Copy key (use as password)
   - Username is always `apikey`

3. **Verify Sender**
   - Settings → Sender Authentication
   - Verify single sender email

**Limits:**
- 100 emails/day (free)
- 40,000 emails/month (Essentials - $20/mo)

---

### Amazon SES

**Best for:** AWS users, large scale

**Configuration:**
```toml
[email]
smtp_server = "email-smtp.us-east-1.amazonaws.com"
smtp_port = 587
smtp_username = "your-smtp-username"
smtp_password = "your-smtp-password"
sender_email = "verified@yourdomain.com"
sender_name = "LLM Evaluator"
use_tls = true
```

**Setup Steps:**

1. **Enable SES**
   - AWS Console → SES
   - Verify email address or domain

2. **Create SMTP Credentials**
   - SES → SMTP Settings
   - Create SMTP Credentials
   - Download credentials file

3. **Request Production Access**
   - By default, SES is in sandbox mode
   - Can only send to verified addresses
   - Request production access for unrestricted sending

**Limits:**
- 200 emails/day (sandbox)
- 50,000 emails/day (production, free tier)
- $0.10 per 1,000 emails after free tier

**Region Selection:**
- Use region closest to your users
- Update `smtp_server` with correct region

---

## Testing Email Setup

### Method 1: Streamlit UI

1. Launch Streamlit app
2. Navigate to Settings page
3. Scroll to Email Configuration
4. Enter test recipient email
5. Click "Send Test Email"
6. Check inbox (and spam folder)

**Success:** You'll see "✅ Test email sent successfully"

**Failure:** Error message will indicate the problem

---

### Method 2: Python Script

Create `test_email.py`:

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration (from secrets.toml)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"
SENDER_EMAIL = "your-email@gmail.com"
RECIPIENT_EMAIL = "test@example.com"

# Create message
message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = RECIPIENT_EMAIL
message["Subject"] = "Test Email - LLM Evaluator"

body = "This is a test email from Modal LLM Evaluator."
message.attach(MIMEText(body, "plain"))

# Send email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)
        print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
```

Run:
```bash
python test_email.py
```

---

## Email Templates

### Evaluation Complete Email

**Subject:** `LLM Evaluation Complete: {experiment_name}`

**Body:**
```
Hi,

Your LLM evaluation has completed successfully!

Experiment: prompt-optimization-001
Date: 2024-12-12 10:30 AM
Duration: 12 minutes

Results Summary:
- Total Evaluations: 750
- Success Rate: 94.3%
- Total Cost: $12.34
- Best Performer: Claude 3.5 Sonnet + "Marketing" prompt

Detailed results are attached.

View full results: http://localhost:8501

---
Sent by Modal LLM Evaluator
```

---

### Budget Warning Email

**Subject:** `⚠️ Budget Warning: {experiment_name}`

**Body:**
```
Hi,

Your LLM evaluation is approaching the budget limit.

Experiment: large-scale-test
Current Cost: $8.00
Budget Limit: $10.00
Utilization: 80%

The evaluation will automatically stop at $10.00.

To increase the budget, stop the evaluation and restart with a higher limit.

---
Sent by Modal LLM Evaluator
```

---

### Budget Exceeded Email

**Subject:** `🛑 Budget Exceeded: {experiment_name}`

**Body:**
```
Hi,

Your LLM evaluation has stopped due to budget limit.

Experiment: large-scale-test
Final Cost: $10.00
Budget Limit: $10.00
Completed: 650 / 1000 evaluations (65%)

Partial results are attached.

To complete the remaining evaluations, run again with a higher budget limit.

---
Sent by Modal LLM Evaluator
```

---

## Troubleshooting

### Error: "SMTP AUTH extension not supported"

**Cause:** Wrong SMTP server or port

**Fix:**
- Verify SMTP server address
- Check port (587 for TLS, 465 for SSL)
- Ensure `use_tls = true`

---

### Error: "Username and Password not accepted"

**Cause:** Wrong credentials or app password not used

**Fix:**
- Use app-specific password (not main password)
- Enable 2FA on email account
- Generate new app password
- Check for typos in password

---

### Error: "Connection timed out"

**Cause:** Firewall or network blocking SMTP

**Fix:**
- Check firewall settings
- Try different network
- Test with `telnet smtp.gmail.com 587`
- Contact IT if on corporate network

---

### Emails Going to Spam

**Cause:** Email not properly authenticated

**Fix:**
- Use verified sender email
- Set up SPF/DKIM records (for custom domains)
- Use reputable SMTP service (Brevo, SendGrid)
- Avoid spam trigger words in subject/body
- Send test to yourself first

---

### Error: "Recipient address rejected"

**Cause:** Invalid recipient email or SES sandbox mode

**Fix:**
- Verify recipient email is valid
- If using SES, request production access
- Check recipient isn't blocked/bounced

---

### Email Delivery Delayed

**Cause:** Provider rate limiting or queue delays

**Normal:**
- Gmail: usually instant
- Outlook: 1-5 minutes
- SES: 1-2 minutes
- Brevo/SendGrid: usually instant

**If longer:**
- Check provider status page
- Review sending limits
- Check spam folder

---

## Advanced Configuration

### Multiple Recipients

```toml
[email]
# ... other settings ...
default_recipients = [
    "team@example.com",
    "manager@example.com",
    "client@example.com"
]
```

### Email Templates

Custom HTML email templates:

```toml
[email]
# ... other settings ...
template_file = "templates/email_template.html"
```

### Attachments

Configure auto-attach results:

```toml
[email]
# ... other settings ...
attach_results = true
attach_format = "excel"  # or "csv"
max_attachment_size_mb = 10
```

---

## Security Checklist

- [ ] Using app-specific passwords
- [ ] 2FA enabled on email account
- [ ] `.streamlit/secrets.toml` in `.gitignore`
- [ ] Secrets not in version control
- [ ] Using TLS/SSL encryption
- [ ] Regular password rotation
- [ ] Monitoring for unauthorized access
- [ ] Using verified sender domains (production)

---

## Production Recommendations

**For Production Use:**

1. **Use Dedicated Email Service**
   - Brevo, SendGrid, or Amazon SES
   - NOT Gmail/Outlook for high volume

2. **Verify Sender Domain**
   - Add SPF, DKIM, DMARC records
   - Improves deliverability

3. **Monitor Delivery**
   - Track bounces and complaints
   - Remove bad addresses
   - Monitor spam reports

4. **Rate Limiting**
   - Don't send too many emails at once
   - Space out bulk sends
   - Respect provider limits

5. **Compliance**
   - Include unsubscribe link (if marketing)
   - Follow CAN-SPAM / GDPR rules
   - Privacy policy for data handling

---

## Need Help?

- **Email Issues:** Check provider documentation
- **SMTP Errors:** See troubleshooting section above
- **Feature Requests:** Open GitHub issue
- **Support:** Email hello@gtmvp.com

---

**Happy Sending! 📧**
