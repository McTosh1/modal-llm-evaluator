# Images for Modal LLM Evaluator

This folder contains screenshots and visual assets for the project README.

## Quick Start - Automated Screenshots

### Option 1: Automated (Recommended)

1. **Install Playwright:**
   ```bash
   pip install playwright pillow
   playwright install chromium
   ```

2. **Launch Streamlit:**
   ```bash
   # In one terminal
   cd C:\claude_code\modal-llm-evaluator
   streamlit run streamlit_app/app.py
   ```

3. **Run Screenshot Script:**
   ```bash
   # In another terminal
   cd C:\claude_code\modal-llm-evaluator\docs\images
   python take_screenshots.py
   ```

4. **Review and optimize:**
   - Check screenshots in this folder
   - Compress images (use TinyPNG.com or ImageOptim)
   - Replace placeholder URLs in README.md

### Option 2: Manual Screenshots

See [SCREENSHOT_GUIDE.md](SCREENSHOT_GUIDE.md) for detailed manual instructions.

## Required Images

| File | Size | Description | Status |
|------|------|-------------|--------|
| `banner.png` | 1200x400px | Project hero banner | ⏳ Placeholder |
| `screenshot-home.png` | 1920x1080px | Home page | ⏳ Placeholder |
| `screenshot-results.png` | 1920x1080px | Results dashboard | ⏳ Placeholder |
| `screenshot-comparison.png` | 1920x1080px | Model comparison | ⏳ Placeholder |
| `screenshot-cost.png` | 1920x1080px | Cost tracking | ⏳ Placeholder |
| `demo.gif` | 800x600px | Animated demo | ⏳ Todo |
| `results-example.png` | 1200x600px | Results example | ⏳ Todo |

## After Taking Screenshots

1. **Optimize images:**
   ```bash
   # Use online tools:
   # - TinyPNG.com (PNG compression)
   # - Squoosh.app (advanced compression)
   # - ImageOptim (Mac)
   # - FileOptimizer (Windows)
   ```

2. **Update README.md:**
   - Replace placeholder URLs with local image paths
   - Remove TODO comments

   Change from:
   ```markdown
   <!-- TODO: Replace with real banner image -->
   ![Banner](https://via.placeholder.com/...)
   ```

   To:
   ```markdown
   ![Banner](docs/images/banner.png)
   ```

3. **Commit changes:**
   ```bash
   git add docs/images/
   git commit -m "Add screenshots for documentation"
   git push
   ```

## Creating the Banner

### Option A: Use Canva (Easy)
1. Go to https://canva.com
2. Create design: 1200x400px
3. Use gradient background (#5B21B6 to #1E40AF)
4. Add text: "⚡ Modal LLM Evaluator"
5. Add subtitle: "Evaluate LLM Prompts at Scale"
6. Download as PNG
7. Save as `banner.png`

### Option B: Use Figma (Professional)
1. Create 1200x400px frame
2. Add gradient background
3. Add logo/text
4. Export as PNG
5. Save as `banner.png`

### Option C: Quick CSS Banner (Code)
See `create_banner.html` for a simple HTML/CSS banner you can screenshot.

## Creating the Demo GIF

### Windows - ScreenToGif
1. Download from https://www.screentogif.com/
2. Record the workflow:
   - Launch app
   - Navigate through pages
   - Start evaluation
   - View results
3. Edit and optimize in ScreenToGif
4. Save as `demo.gif` (<5MB)

### Mac - Gifski
1. Record with QuickTime
2. Convert to GIF with Gifski
3. Optimize file size
4. Save as `demo.gif`

### Online - RecordScreen.io
1. Go to https://recordscreen.io
2. Record browser tab
3. Download as GIF
4. Save as `demo.gif`

## Image Guidelines

- **Format:** PNG for screenshots, GIF for animations
- **Quality:** High resolution (2x/retina when possible)
- **Size:** <500KB per PNG, <5MB for GIF
- **Consistency:** Same theme/style across all screenshots
- **Professional:** Clean UI, no errors/debug info visible

## Placeholder URLs (Current)

The README currently uses these placeholders:
- Banner: `https://via.placeholder.com/1200x400/5B21B6/FFFFFF/?text=...`
- Screenshots: `https://via.placeholder.com/800x600/E5E7EB/1F2937/?text=...`
- Demo: `https://via.placeholder.com/800x400/5B21B6/FFFFFF/?text=...`

Replace with real images for professional appearance!

## Need Help?

- **Detailed Guide:** See [SCREENSHOT_GUIDE.md](SCREENSHOT_GUIDE.md)
- **Automation Script:** Run `python take_screenshots.py`
- **Questions:** Open an issue or email hello@gtmvp.com

---

**Status: Using placeholders - real screenshots needed before publishing!**
