# Screenshot Creation Guide

Follow these steps to create professional screenshots for the README.

## Prerequisites

1. Launch the Streamlit UI:
   ```bash
   cd C:\claude_code\modal-llm-evaluator
   streamlit run streamlit_app/app.py
   ```

2. The app will open in your browser at `http://localhost:8501`

## Screenshots Needed

### 1. Banner Image (banner.png)
**Size:** 1200x400px
**Content:** Project logo/title with tagline

**How to create:**
- Use Canva, Figma, or Photoshop
- Dark purple/blue gradient background (#5B21B6 to #1E40AF)
- White text: "⚡ Modal LLM Evaluator"
- Subtitle: "Evaluate LLM prompts at scale with parallel execution"
- Include icons: Modal logo, Claude, GPT, Gemini logos (if permitted)

**Quick option:** Use this placeholder URL temporarily:
```
https://via.placeholder.com/1200x400/5B21B6/FFFFFF/?text=Modal+LLM+Evaluator
```

### 2. Home Page Screenshot (screenshot-home.png)
**Page:** Home (🏠 Home in sidebar)
**Size:** 1920x1080 (full page)
**Viewport:** 1920x1080

**What to show:**
- Welcome message and overview
- Feature highlights
- Quick stats section
- Navigation sidebar visible
- Clean, professional appearance

**Steps:**
1. Navigate to Home page
2. Scroll to show key features
3. Take full-page screenshot
4. Crop to 1920x1080 if needed
5. Save as `screenshot-home.png`

### 3. Results Dashboard (screenshot-results.png)
**Page:** Results (📊 Results in sidebar)
**Size:** 1920x1080

**Prerequisites:**
- Run at least one evaluation first to have data
- Use the simple example:
  ```bash
  python -m modal run main.py \
    --prompts-file=examples/prompts_simple.json \
    --test-cases-file=examples/test_cases_simple.json
  ```

**What to show:**
- Results table with evaluation data
- Charts showing model performance
- Pass rate metrics
- Cost information
- Professional, data-rich view

**Steps:**
1. Run an evaluation (see prerequisites)
2. Navigate to Results page
3. Select the latest experiment
4. Ensure charts are visible and attractive
5. Take screenshot
6. Save as `screenshot-results.png`

### 4. Model Comparison (screenshot-comparison.png)
**Page:** Model Comparison (🤖 Model Comparison in sidebar)
**Size:** 1920x1080

**Prerequisites:**
- Same as Results - need evaluation data
- Ideally with multiple models tested

**What to show:**
- Side-by-side model performance charts
- Comparison metrics
- Cost vs performance visualization
- Clear visual distinctions between models

**Steps:**
1. Navigate to Model Comparison page
2. Ensure comparison charts are displayed
3. Take screenshot showing comparative analysis
4. Save as `screenshot-comparison.png`

### 5. Cost Tracker (screenshot-cost.png)
**Page:** Cost Tracker (💰 Cost Tracker in sidebar)
**Size:** 1920x1080

**Prerequisites:**
- Evaluation data with cost information

**What to show:**
- Cost breakdown by model
- Budget tracking
- Cost trends over time
- Cost per evaluation metrics

**Steps:**
1. Navigate to Cost Tracker page
2. Ensure cost visualizations are displayed
3. Take screenshot showing cost analysis
4. Save as `screenshot-cost.png`

### 6. Animated Demo (demo.gif)
**Type:** Animated GIF
**Duration:** 10-15 seconds
**Size:** 800x600px max

**What to show:**
1. Home page (2 seconds)
2. Navigate to Run Evaluation (2 seconds)
3. Configure a simple evaluation (3 seconds)
4. Start evaluation (2 seconds)
5. View results appearing (4 seconds)

**Tools to use:**
- **Windows:** ScreenToGif (free, easy)
- **Mac:** Gifski, Kap (both free)
- **Online:** RecordScreen.io, Giphy Capture

**Recording tips:**
- Record at 1920x1080, then resize to 800x600
- Use 10-15 FPS for smaller file size
- Keep under 5MB file size
- Show smooth, professional workflow

**Steps:**
1. Launch screen recorder
2. Select browser window
3. Follow the workflow above
4. Export as GIF
5. Optimize for web (use Gifski or ezgif.com)
6. Save as `demo.gif`

### 7. Results Example (results-example.png)
**Type:** Screenshot or mockup
**Size:** 1920x1080

**What to show:**
- Beautiful results dashboard
- Real evaluation data
- Multiple charts visible
- Professional appearance
- Shows the "Product Description Optimization" case study mentioned in README

**Option A - Real Screenshot:**
1. Run the product description example
2. Navigate to Results
3. Take screenshot of best-looking view
4. Save as `results-example.png`

**Option B - Mockup:**
- Create a polished version in Figma/Canva
- Show idealized results view
- Include annotations if helpful

## Screenshot Tips

### Quality
- Use highest resolution (retina/2x if possible)
- Ensure text is crisp and readable
- No blur or compression artifacts

### Composition
- Include sidebar for context
- Show enough content without overwhelming
- Use attractive data/charts
- Keep UI clean (no debug info, errors)

### Lighting/Theme
- Use Streamlit default theme (light mode)
- Or use dark mode consistently
- Ensure good contrast
- Professional color scheme

### Optimization
- PNG format for screenshots
- Compress without quality loss (TinyPNG, ImageOptim)
- Keep under 500KB per image
- GIF under 5MB

## Quick Screenshot Tools

### Windows
- **Snipping Tool** - Built-in, basic
- **ShareX** - Free, advanced features
- **Windows + Shift + S** - Quick snip

### Mac
- **Command + Shift + 4** - Area screenshot
- **Command + Shift + 5** - Advanced options
- **CleanShot X** - Professional (paid)

### Linux
- **Flameshot** - Feature-rich
- **GNOME Screenshot** - Built-in
- **Spectacle** - KDE tool

## Browser Extensions

- **GoFullPage** - Full page screenshots
- **Awesome Screenshot** - Annotation tools
- **Nimbus Screenshot** - Screen recording too

## After Creating Screenshots

1. Save all images to `docs/images/` folder
2. Verify they display correctly in README:
   ```bash
   # Preview locally
   # Open README.md in VS Code and use Markdown preview
   # Or push to GitHub and check the preview
   ```

3. Optimize file sizes:
   ```bash
   # Use TinyPNG.com or ImageOptim
   # Target: <500KB per PNG, <5MB for GIF
   ```

4. Commit to git:
   ```bash
   git add docs/images/
   git commit -m "Add screenshots for README"
   git push
   ```

## Placeholder Images (Temporary)

If you want to publish quickly without screenshots, use these placeholders:

```markdown
![Banner](https://via.placeholder.com/1200x400/5B21B6/FFFFFF/?text=Modal+LLM+Evaluator)
![Home](https://via.placeholder.com/1920x1080/E5E7EB/1F2937/?text=Home+Dashboard)
![Results](https://via.placeholder.com/1920x1080/E5E7EB/1F2937/?text=Results+View)
![Comparison](https://via.placeholder.com/1920x1080/E5E7EB/1F2937/?text=Model+Comparison)
![Cost](https://via.placeholder.com/1920x1080/E5E7EB/1F2937/?text=Cost+Tracker)
```

Replace with real images as soon as possible!

## Need Help?

- **Example screenshots**: Check other open source projects for inspiration
  - Streamlit gallery: https://streamlit.io/gallery
  - GitHub awesome lists with screenshots

- **Design help**:
  - Canva templates for banners
  - Figma community files

- **Questions**: Open an issue or email hello@gtmvp.com

---

**Take your time and create professional screenshots - they're the first impression!**
