# Troubleshooting Guide

Common issues and solutions for Modal LLM Evaluator.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Modal Setup](#modal-setup)
- [API Key Issues](#api-key-issues)
- [Execution Errors](#execution-errors)
- [Cost & Budget](#cost--budget)
- [Performance Issues](#performance-issues)
- [Streamlit UI Issues](#streamlit-ui-issues)
- [Email Issues](#email-issues)
- [Database Export](#database-export)

---

## Installation Issues

### Python Version Error

**Error:**
```
Python 3.11+ is required
```

**Fix:**
```bash
# Check Python version
python --version

# Install Python 3.11 or later
# macOS (using Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11

# Windows
# Download from https://www.python.org/downloads/
```

---

### Module Not Found Error

**Error:**
```
ModuleNotFoundError: No module named 'modal'
```

**Fix:**
```bash
# Install dependencies
pip install -r requirements.txt

# If still failing, create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

### Modal Installation Failed

**Error:**
```
ERROR: Could not install modal
```

**Fix:**
```bash
# Update pip first
pip install --upgrade pip

# Install modal
pip install modal

# Verify installation
python -m modal --version
```

---

## Modal Setup

### Modal Not Configured

**Error:**
```
modal.exception.NotLoggedInError: Not logged in
```

**Fix:**
```bash
# Run Modal setup
python -m modal setup

# Follow the prompts:
# 1. Enter email
# 2. Enter verification code
# 3. Choose organization

# Verify setup
python -m modal token set --verify
```

---

### Token Expired

**Error:**
```
modal.exception.AuthError: Token expired
```

**Fix:**
```bash
# Re-authenticate
python -m modal token set

# Or full setup again
python -m modal setup
```

---

### Modal Secrets Missing

**Error:**
```
modal.exception.SecretNotFound: Secret 'anthropic-key' not found
```

**Fix:**
```bash
# Create Modal secrets for API keys
# Anthropic
python -m modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...

# OpenAI
python -m modal secret create openai-key OPENAI_API_KEY=sk-...

# Google
python -m modal secret create google-api-key GOOGLE_API_KEY=...

# List secrets to verify
python -m modal secret list
```

---

## API Key Issues

### Invalid API Key

**Error:**
```
anthropic.AuthenticationError: Invalid API key
```

**Fix:**
1. **Verify API key is correct:**
   - Claude: https://console.anthropic.com/
   - OpenAI: https://platform.openai.com/api-keys
   - Google: https://aistudio.google.com/app/apikey

2. **Re-create Modal secret:**
   ```bash
   # Delete old secret
   python -m modal secret delete anthropic-key

   # Create new one
   python -m modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-your-new-key
   ```

3. **Check for spaces/typos:**
   - Copy API key carefully
   - Ensure no extra spaces
   - Check for truncation

---

### API Rate Limit

**Error:**
```
RateLimitError: Rate limit exceeded
```

**Fix:**
1. **Wait and retry:**
   - Free tier limits are hourly/daily
   - Wait for rate limit to reset

2. **Upgrade API plan:**
   - Anthropic: Add credits
   - OpenAI: Upgrade tier
   - Google: Request quota increase

3. **Reduce concurrency:**
   ```python
   evaluator = LLMEvaluator(
       models=["claude-3-5-sonnet-20241022"],
       parallel=False  # Disable parallel execution
   )
   ```

4. **Add retry logic:**
   ```python
   import time
   from tenacity import retry, stop_after_attempt, wait_exponential

   @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
   def run_with_retry():
       return evaluator.run(prompts, test_cases)

   results = run_with_retry()
   ```

---

### API Timeout

**Error:**
```
TimeoutError: Request timed out
```

**Fix:**
1. **Increase timeout:**
   ```python
   evaluator = LLMEvaluator(
       models=["claude-3-5-sonnet-20241022"],
       timeout=600  # 10 minutes
   )
   ```

2. **Check network connection:**
   ```bash
   # Test connectivity
   curl https://api.anthropic.com/v1/messages
   ```

3. **Use faster models:**
   - Claude Haiku instead of Sonnet
   - GPT-4o-mini instead of GPT-4o
   - Gemini Flash instead of Pro

---

## Execution Errors

### Budget Exceeded

**Error:**
```
BudgetExceededError: Budget limit of $10.00 exceeded
```

**This is expected behavior! Budget protection is working.**

**To continue:**

1. **Increase budget:**
   ```bash
   python -m modal run main.py --budget-limit=25.00
   ```

2. **Review partial results:**
   - Results up to budget limit are saved
   - Check `results/` folder

3. **Optimize costs:**
   - Use cheaper models (Haiku, Mini, Flash)
   - Reduce number of test cases
   - Reduce max_tokens

---

### Prompt Template Error

**Error:**
```
KeyError: 'question' not found in template
```

**Fix:**
1. **Ensure variables match:**
   ```python
   # Prompt template uses {question}
   prompt = "Answer this: {question}"

   # Test case must have 'question' key
   test_case = {
       "id": "test_1",
       "question": "What is 2+2?"  # ✅ Matches template
   }
   ```

2. **Check variable names:**
   - Must use `{variable_name}` in templates
   - Variables are case-sensitive
   - No spaces in variable names

---

### JSON Parse Error

**Error:**
```
json.JSONDecodeError: Expecting value: line 1 column 1
```

**Fix:**
1. **Validate JSON files:**
   ```bash
   # Check if valid JSON
   python -c "import json; json.load(open('prompts.json'))"
   ```

2. **Common JSON errors:**
   - Missing quotes around strings
   - Trailing commas
   - Single quotes instead of double quotes
   - Invalid escape sequences

3. **Use JSON validator:**
   - https://jsonlint.com/
   - VS Code JSON validation

---

### No Results Generated

**Issue:** Evaluation runs but no results appear

**Fix:**
1. **Check results folder:**
   ```bash
   ls -la results/
   ```

2. **Verify write permissions:**
   ```bash
   # Create results folder if missing
   mkdir -p results
   chmod 755 results
   ```

3. **Check for errors in logs:**
   ```bash
   # Run with verbose logging
   python -m modal run main.py --verbose
   ```

4. **Verify test cases:**
   - At least 1 test case required
   - Test cases must be valid format

---

## Cost & Budget

### Cost Higher Than Expected

**Issue:** Costs are higher than estimated

**Common Causes:**

1. **Output tokens underestimated:**
   - Models generate longer responses than expected
   - Max tokens setting too high

2. **Using expensive models:**
   - Opus/GPT-4 are 5-10x more expensive
   - Switch to Sonnet/GPT-4o

3. **Too many evaluations:**
   - Prompts × Test Cases × Models = Total
   - 5 prompts × 100 tests × 3 models = 1,500 evaluations

**Solutions:**

1. **Set strict budget limits:**
   ```python
   evaluator = LLMEvaluator(
       models=["claude-3-5-sonnet-20241022"],
       budget_limit=5.00  # Strict limit
   )
   ```

2. **Start small:**
   - Test with 5-10 test cases first
   - Scale up after validating cost

3. **Use cost estimation:**
   ```python
   # Preview cost before running
   estimated_cost = evaluator.estimate_cost(prompts, test_cases)
   print(f"Estimated: ${estimated_cost:.2f}")
   ```

---

### Budget Warning Not Received

**Issue:** No email when budget threshold reached

**Fix:**
1. **Check email configuration:**
   - Verify `.streamlit/secrets.toml`
   - Test email sending
   - See [EMAIL_SETUP.md](EMAIL_SETUP.md)

2. **Verify budget settings:**
   ```python
   evaluator = LLMEvaluator(
       models=["claude-3-5-sonnet-20241022"],
       budget_limit=10.00,
       budget_warning_threshold=0.8  # Alert at 80%
   )
   ```

3. **Check spam folder:**
   - Budget alerts may be filtered
   - Whitelist sender email

---

## Performance Issues

### Slow Execution

**Issue:** Evaluations take too long

**Expected Times:**
- 100 evaluations: 30-60 seconds
- 1,000 evaluations: 5-10 minutes
- 10,000 evaluations: 30-60 minutes

**If slower:**

1. **Check Modal status:**
   ```bash
   python -m modal status
   ```

2. **Verify parallel execution enabled:**
   ```python
   evaluator = LLMEvaluator(
       models=["claude-3-5-sonnet-20241022"],
       parallel=True  # ✅ Enabled
   )
   ```

3. **Check internet connection:**
   ```bash
   # Test speed
   curl -o /dev/null -w "Time: %{time_total}s\n" https://api.anthropic.com/v1/messages
   ```

4. **Use faster models:**
   - Haiku (fastest)
   - Mini (fast)
   - Flash (fast)

---

### Memory Errors

**Error:**
```
MemoryError: Unable to allocate array
```

**Fix:**
1. **Process in batches:**
   ```python
   # Instead of all at once
   batch_size = 100
   for i in range(0, len(test_cases), batch_size):
       batch = test_cases[i:i+batch_size]
       results = evaluator.run(prompts, batch)
   ```

2. **Reduce max_tokens:**
   ```python
   provider = ClaudeProvider(
       model="claude-3-5-sonnet-20241022",
       max_tokens=500  # Reduced from 1000
   )
   ```

3. **Clear results frequently:**
   ```python
   # Export and clear after each batch
   results.save_csv(f"batch_{i}.csv")
   del results
   ```

---

## Streamlit UI Issues

### UI Won't Load

**Error:**
```
streamlit: command not found
```

**Fix:**
```bash
# Install Streamlit
pip install streamlit

# Run UI
streamlit run streamlit_app/app.py
```

---

### Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Fix:**
```bash
# Option 1: Kill existing process
# macOS/Linux
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Option 2: Use different port
streamlit run streamlit_app/app.py --server.port 8502
```

---

### UI Not Updating

**Issue:** Changes not reflected in UI

**Fix:**
1. **Hard refresh:**
   - Press `Ctrl+Shift+R` (Windows/Linux)
   - Press `Cmd+Shift+R` (Mac)

2. **Clear Streamlit cache:**
   ```bash
   # Delete cache folder
   rm -rf .streamlit/cache
   ```

3. **Restart Streamlit:**
   ```bash
   # Kill and restart
   pkill -f streamlit
   streamlit run streamlit_app/app.py
   ```

---

### "Modal Not Configured" Warning

**Issue:** UI shows "Modal not configured"

**Fix:**
1. **Run Modal setup:**
   ```bash
   python -m modal setup
   ```

2. **Restart Streamlit:**
   - Stop Streamlit (Ctrl+C)
   - Start again

3. **Verify Modal token:**
   ```bash
   python -m modal token set --verify
   ```

---

## Email Issues

### SMTP Connection Failed

**Error:**
```
smtplib.SMTPConnectError: (421, 'Service not available')
```

**Fix:**
1. **Check SMTP settings:**
   - Verify server address
   - Verify port (587 for TLS, 465 for SSL)
   - Check username/password

2. **Test SMTP connection:**
   ```bash
   # Test with telnet
   telnet smtp.gmail.com 587
   ```

3. **Use app password:**
   - Don't use main email password
   - Create app-specific password
   - See [EMAIL_SETUP.md](EMAIL_SETUP.md)

4. **Check firewall:**
   - Ensure SMTP ports not blocked
   - Try different network

---

### Emails Going to Spam

**Issue:** Results emails in spam folder

**Fix:**
1. **Whitelist sender:**
   - Add sender email to contacts
   - Create filter to never spam

2. **Use verified sender domain:**
   - Set up SPF/DKIM records
   - Use professional email service (Brevo, SendGrid)

3. **Improve email content:**
   - Avoid spam trigger words
   - Include unsubscribe link
   - Use plain text or simple HTML

---

### Email Attachment Too Large

**Error:**
```
MessageSizeExceeded: Message too large
```

**Fix:**
1. **Export to CSV instead of Excel:**
   ```python
   results.save_csv("results.csv")  # Smaller file
   ```

2. **Compress Excel file:**
   ```bash
   zip results.zip results.xlsx
   ```

3. **Upload to cloud and send link:**
   ```python
   # Upload to S3/Google Drive/Dropbox
   url = upload_to_cloud("results.xlsx")

   # Email just the link
   results.email_results(
       recipients=["user@example.com"],
       body=f"Results available at: {url}",
       attach_excel=False
   )
   ```

4. **Filter results:**
   ```python
   # Send only failed tests
   failed = results.filter(passed=False)
   failed.email_results(recipients=["team@example.com"])
   ```

---

## Database Export

### Connection Failed

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Fix:**
1. **Verify database is running:**
   ```bash
   # PostgreSQL
   sudo systemctl status postgresql

   # MySQL
   sudo systemctl status mysql
   ```

2. **Check connection string:**
   ```python
   # Correct format
   "postgresql://username:password@hostname:port/database"

   # Common mistakes:
   # ❌ "postgres://" (should be "postgresql://")
   # ❌ Missing port (:5432)
   # ❌ Wrong password
   ```

3. **Test connection:**
   ```bash
   # PostgreSQL
   psql -h localhost -U username -d database

   # MySQL
   mysql -h localhost -u username -p database
   ```

4. **Check firewall:**
   - Database port open
   - Whitelisted IP addresses

---

### Table Creation Failed

**Error:**
```
sqlalchemy.exc.ProgrammingError: permission denied
```

**Fix:**
1. **Grant proper permissions:**
   ```sql
   -- PostgreSQL
   GRANT ALL PRIVILEGES ON DATABASE llm_evaluator TO llm_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO llm_user;

   -- MySQL
   GRANT ALL PRIVILEGES ON llm_evaluator.* TO 'llm_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Use admin account temporarily:**
   - Create tables with admin
   - Grant permissions to regular user

---

### Data Type Mismatch

**Error:**
```
DataError: invalid input syntax for type numeric
```

**Fix:**
1. **Validate data before export:**
   ```python
   # Ensure numeric fields are valid
   results.validate_schema()
   ```

2. **Handle NULL values:**
   ```python
   # Export with NULL handling
   results.export_to_database(
       connection_string="...",
       handle_nulls=True
   )
   ```

3. **Check database schema:**
   - Ensure column types match
   - Update schema if needed

---

## General Debugging

### Enable Verbose Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Run evaluation
results = evaluator.run(prompts, test_cases)
```

---

### Check Modal Logs

```bash
# View Modal logs
python -m modal app logs

# Or in Python
from modal import App
app = App.lookup("llm-evaluator")
app.logs()
```

---

### Validate Configuration

```python
# Validate before running
from evaluator.utils import validate_config

validate_config(
    prompts=prompts,
    test_cases=test_cases,
    models=models
)
```

---

## Getting Help

If you're still stuck:

1. **Check Documentation:**
   - [QUICKSTART.md](QUICKSTART.md)
   - [ARCHITECTURE.md](ARCHITECTURE.md)
   - [API_REFERENCE.md](API_REFERENCE.md)

2. **Search Issues:**
   - https://github.com/GTMVP/modal-llm-evaluator/issues

3. **Open New Issue:**
   - Include error message
   - Include configuration
   - Include steps to reproduce
   - https://github.com/GTMVP/modal-llm-evaluator/issues/new

4. **Contact Support:**
   - Email: hello@gtmvp.com
   - Include logs and error details

---

## Common Gotchas

### API Keys in Code

❌ **NEVER hardcode API keys:**
```python
# DON'T DO THIS
api_key = "sk-ant-actual-key-here"
```

✅ **Use Modal secrets:**
```bash
modal secret create anthropic-key ANTHROPIC_API_KEY=sk-ant-...
```

---

### Budget Limits

❌ **Don't set budget too low:**
```python
budget_limit=0.10  # Too low, will stop immediately
```

✅ **Realistic budget:**
```python
budget_limit=5.00  # Allows reasonable testing
```

---

### Test Case Format

❌ **Invalid test case:**
```python
test_case = {
    "question": "What is 2+2?"  # Missing 'id'
}
```

✅ **Valid test case:**
```python
test_case = {
    "id": "test_1",  # Required
    "question": "What is 2+2?"
}
```

---

### Prompt Variables

❌ **Variable mismatch:**
```python
prompt = "Answer: {question}"
test_case = {"input": "What is 2+2?"}  # Wrong key
```

✅ **Matching variables:**
```python
prompt = "Answer: {question}"
test_case = {"question": "What is 2+2?"}  # ✅ Matches
```

---

**Still need help? We're here to support you! 🚀**

Email: hello@gtmvp.com
