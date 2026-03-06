# 🚀 Quick Start Guide - Elevator Dashboard

Complete step-by-step guide to set up your GitHub repository and deploy the Streamlit app.

## ✅ Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface (Easiest)

1. **Go to GitHub**
   - Visit https://github.com/new

2. **Create New Repository**
   - Repository name: `IDAI104_[YourID]-[YourName]`
   - Example: `IDAI104_12345-JohnSmith`
   - Description: "Elevator Predictive Maintenance Dashboard"
   - Select: Public (so graders can access)
   - Check: "Add a README file"
   - Click: "Create repository"

3. **Copy Repository URL**
   - Look for the green "Code" button
   - Copy the HTTPS URL
   - Example: `https://github.com/YourUsername/IDAI104_12345-JohnSmith.git`

### Option B: Using Git Command Line

```bash
# Create local folder
mkdir IDAI104_[YourID]-[YourName]
cd IDAI104_[YourID]-[YourName]

# Initialize git repository
git init

# Add remote origin (replace with your URL)
git remote add origin https://github.com/YourUsername/IDAI104_[YourID]-[YourName].git

# Create initial commit
git add .
git commit -m "Initial commit: Elevator dashboard project"

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## ✅ Step 2: Upload Files to GitHub

### Method 1: Upload via GitHub Web Interface

1. **Go to Your Repository**
   - Visit: https://github.com/YourUsername/IDAI104_[YourID]-[YourName]

2. **Add Files**
   - Click: "Add file" → "Upload files"
   - Drag and drop these files:
     ```
     app.py
     elevator_sensor_data_cleaned.csv
     requirements.txt
     README.md
     STAGE_1_RESEARCH.md
     stage_2_data_cleaning.py
     stage_3_visualizations.py
     STAGE_4_INSIGHTS.py
     viz_1_timeseries.png
     viz_2_histograms.png
     viz_3_scatter.png
     viz_4_boxplot.png
     viz_5_heatmap.png
     ```

3. **Commit Changes**
   - Add commit message: "Add project files"
   - Click: "Commit changes"

### Method 2: Using Git Command Line

```bash
# Navigate to your project folder
cd IDAI104_[YourID]-[YourName]

# Copy all files here (from outputs directory)
cp /path/to/outputs/* .

# Add all files
git add .

# Commit
git commit -m "Add complete project files"

# Push to GitHub
git push origin main
```

---

## ✅ Step 3: Grant Access to Graders

1. **Go to Repository Settings**
   - Visit: https://github.com/YourUsername/IDAI104_[YourID]-[YourName]/settings
   - Click: "Collaborators" (left menu)

2. **Add Email Access**
   - Click: "Add people"
   - Enter: `ai.assignments@wacpinternational.org`
   - Select: "Maintain" access level (gives read access)
   - Click: "Add"

3. **Verify Access**
   - They'll receive an email invitation
   - They can now view your repository

---

## ✅ Step 4: Deploy to Streamlit Cloud

### Prerequisites
- GitHub account (already created above)
- Streamlit account (create at https://streamlit.io/cloud)
- Repository pushed to GitHub

### Deployment Steps

1. **Sign Up for Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Click: "Sign up"
   - Use GitHub to authenticate (easiest)
   - Accept permissions

2. **Deploy Your App**
   - Click: "New app" (after login)
   - Select:
     - Repository: `YourUsername/IDAI104_[YourID]-[YourName]`
     - Branch: `main`
     - Main file path: `app.py`
   - Click: "Deploy"

3. **Wait for Deployment**
   - Streamlit will install dependencies from `requirements.txt`
   - App will build (takes 1-2 minutes)
   - You'll see: "Your app is live at: https://[app-name].streamlit.app"

4. **Get Your Live URL**
   - Copy the URL from Streamlit Cloud
   - Example: `https://elevator-dashboard-123.streamlit.app`
   - Test that it works

### Troubleshooting Deployment

If deployment fails:

1. **Check requirements.txt**
   ```
   streamlit>=1.28.0
   pandas>=1.5.0
   numpy>=1.23.0
   matplotlib>=3.7.0
   seaborn>=0.12.0
   plotly>=5.10.0
   ```

2. **Verify app.py exists**
   - Make sure file is in root directory (not in subfolder)

3. **Check data file path**
   - In `app.py`, ensure: `df = pd.read_csv('elevator_sensor_data_cleaned.csv')`
   - File must be in same directory as app.py

4. **View Logs**
   - Click "Manage app" on Streamlit Cloud
   - Click "View logs" to see error messages

---

## ✅ Step 5: Verify Everything Works

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run app locally
streamlit run app.py

# Test at: http://localhost:8501
```

**Test these features:**
- ✅ App loads without errors
- ✅ All 5 pages work (Overview, Visualizations, Analysis, Insights, About)
- ✅ Visualizations display correctly
- ✅ Filters work on Analysis page
- ✅ CSV download works
- ✅ Metrics show correct numbers

### Cloud Testing

1. **Visit Your Live URL**
   - Example: `https://[your-app-name].streamlit.app`

2. **Test All Features**
   - ✅ Homepage loads
   - ✅ Can navigate between pages
   - ✅ Charts display correctly
   - ✅ Sliders and filters work
   - ✅ Data table updates with filters
   - ✅ No error messages

---

## ✅ Step 6: Update Submission Document

1. **Fill in Your Information**
   - Student's Full Name: [Your Name]
   - Candidate Registration Number: [Your ID]
   - School Name: [Your School]

2. **Update GitHub Links**
   - Repository URL: `https://github.com/YourUsername/IDAI104_[YourID]-[YourName]`

3. **Update Live App URL**
   - Streamlit URL: `https://[your-app-name].streamlit.app`

4. **Save Submission Document**
   - Save as PDF or DOCX as required
   - Include all links that work

---

## 📋 Folder Structure in GitHub

After uploading, your GitHub should look like:

```
IDAI104_12345-JohnSmith/
├── README.md                           # Main documentation
├── SUBMISSION_DOCUMENT.md              # Submission details
├── app.py                              # Main Streamlit app
├── requirements.txt                    # Python dependencies
├── elevator_sensor_data_cleaned.csv    # Clean dataset
│
├── STAGE_1_RESEARCH.md                # Research documentation
├── stage_2_data_cleaning.py           # Data cleaning script
├── stage_3_visualizations.py          # Visualization script
├── STAGE_4_INSIGHTS.py                # Insights script
│
├── viz_1_timeseries.png               # Time series chart
├── viz_2_histograms.png               # Distribution charts
├── viz_3_scatter.png                  # Correlation chart
├── viz_4_boxplot.png                  # Box plot chart
└── viz_5_heatmap.png                  # Heatmap chart
```

---

## 🔗 Important Links

| Item | Link |
|------|------|
| GitHub New Repo | https://github.com/new |
| GitHub Account | https://github.com |
| Streamlit Cloud | https://streamlit.io/cloud |
| Python Docs | https://docs.python.org |
| Streamlit Docs | https://docs.streamlit.io |

---

## ❓ Frequently Asked Questions

### Q: How do I update my code after deploying?

**A:** Make changes locally, then push to GitHub:
```bash
git add .
git commit -m "Update description"
git push origin main
```
Streamlit Cloud will automatically redeploy (updates live within 1-2 minutes).

### Q: Can graders see my private repository?

**A:** Make sure:
1. Repository is PUBLIC (not private)
2. OR add collaborator: ai.assignments@wacpinternational.org

### Q: How do I know if my deployment worked?

**A:** 
- Look for green checkmark ✓ on Streamlit Cloud dashboard
- Visit your URL - should show the app
- Check "View logs" for any errors

### Q: What if data file isn't loading?

**A:** Ensure `elevator_sensor_data_cleaned.csv` is:
- In the same folder as `app.py`
- Uploaded to GitHub
- Not in a subfolder

### Q: Can I use a different dataset?

**A:** Yes, but you must:
- Use same column names (ID, revolutions, humidity, vibration, x1-x5)
- Have similar number of records (100+)
- Update all 5 visualizations accordingly

### Q: How do I update requirements.txt?

**A:** List all Python packages you use:
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.10.0
```

---

## 📞 Troubleshooting Checklist

- ✅ GitHub repository created (public)
- ✅ All files uploaded to GitHub
- ✅ Access granted to ai.assignments@wacpinternational.org
- ✅ Streamlit Cloud account created
- ✅ App deployed successfully
- ✅ Live URL accessible
- ✅ All 5 visualizations working
- ✅ Data file loads correctly
- ✅ No error messages in logs
- ✅ Submission document completed

---

## 🎉 You're Ready!

Once you've completed all steps above, you're ready to submit:

1. ✅ Verify GitHub repository link works
2. ✅ Verify Streamlit Cloud app is live
3. ✅ Fill in submission document with links
4. ✅ Submit to course instructor

---

**Need Help?**
- Check README.md for detailed documentation
- Review app.py code for implementation details
- Check Streamlit Cloud logs for deployment errors
- Contact instructor for additional support

**Good luck with your submission! 🚀**
