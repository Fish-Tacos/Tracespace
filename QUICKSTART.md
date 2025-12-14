# Trace Space - Quick Start Guide

## 🚀 Get It Running in 5 Minutes

### Step 1: Install Dependencies
```bash
cd tracespace
pip install -r requirements.txt
```

### Step 2: Generate Test Data (For Testing Without API)
```bash
python generate_mock_data.py
```

This creates visualization data with 10 mock organisms.

### Step 3: Start Web Server
```bash
python server.py
```

### Step 4: Open Browser
Navigate to: **http://localhost:5000**

You should see:
- 10 pulsing organisms (sub-components)
- 1 larger organism at their center (component)
- 1 massive organism at the core (entity)

### Step 5: Interact
- **Drag mouse**: Rotate view
- **Scroll**: Zoom in/out
- **Hover**: See post details

---

## 🔄 Using Real Data (When You Have Network Access)

### Run the Full Pipeline
```bash
python run.py
```

This will:
1. Fetch real data from BlueSky API
2. Process it with NLP (topic extraction, sentiment analysis)
3. Generate organisms at all 3 levels
4. Save to `visualization/data/latest.json`

### Set Up Hourly Auto-Refresh (Optional)

**On Mac/Linux (cron):**
```bash
# Edit crontab
crontab -e

# Add this line (runs every hour at :00)
0 * * * * cd /path/to/tracespace && /usr/bin/python3 run.py
```

**On Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 1 hour
4. Action: Start program = `python`
5. Arguments: `run.py`
6. Start in: `/path/to/tracespace`

---

## 📁 Project Structure Overview

```
tracespace/
├── config.py              # System settings (API keys, refresh rate, etc.)
├── run.py                 # Main pipeline (fetch → process → aggregate)
├── server.py              # Web server (Flask)
├── generate_mock_data.py  # Test data generator
│
├── core/                  # Core system
│   ├── organism.py        # Organism data structure
│   ├── aggregator.py      # Statistical aggregation
│   └── data_manager.py    # Tiered storage
│
├── subcomponents/         # Data sources
│   ├── base.py            # Abstract base class
│   └── bluesky_top10.py   # BlueSky connector
│
├── components/            # Mid-level aggregators
│   └── social_media.py    # Aggregates sub-components
│
├── entity/                # Top-level aggregator
│   └── internet_consciousness.py
│
└── visualization/         # Web frontend
    ├── index.html         # Main page
    ├── tracespace.js      # Three.js visualization
    └── data/              # Served data files
```

---

## 🎨 Customization

### Change Refresh Rate
Edit `config.py`:
```python
REFRESH_INTERVAL = 3600  # Seconds (3600 = 1 hour)
```

### Change Number of Posts Fetched
Edit `config.py`:
```python
FETCH_LIMIT = 10  # Increase for more organisms
```

### Change Visualization Port
Edit `config.py`:
```python
VISUALIZATION_PORT = 5000  # Use different port
```

---

## 🐛 Troubleshooting

### "No data available" Error
**Solution:** Run `python generate_mock_data.py` first to create test data.

### BlueSky API Errors
**Cause:** Network restrictions or API rate limits.
**Solution:** Use mock data for testing, or check API status.

### "Port 5000 already in use"
**Solution:** Change port in `config.py` or kill process using port 5000.

### Organisms Not Pulsing
**Cause:** Browser doesn't support WebGL.
**Solution:** Use modern browser (Chrome, Firefox, Edge).

---

## 📊 Understanding the Visualization

### Colors
- **Red**: Negative sentiment posts
- **Green**: Neutral sentiment posts  
- **Blue**: Positive sentiment posts

### Size
- Larger = More engagement (likes + reposts + replies)

### Position
- Organisms with similar topics cluster together
- Uses PCA to reduce topic vectors to 3D coordinates

### Pulse Rate
- Faster = Higher velocity of change

---

## 🚢 Deploying to GitHub

### Initialize Git Repository
```bash
cd tracespace
git init
git add .
git commit -m "Initial commit - Trace Space v1.0"
```

### Create GitHub Repository
1. Go to github.com/new
2. Name: `tracespace`
3. Description: "Visualizing the Internet's Consciousness"
4. Public
5. Don't initialize with README (you already have one)

### Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/tracespace.git
git branch -M main
git push -u origin main
```

---

## 🎯 Next Steps

### Week 1: Get It Working
- [x] Generated mock data
- [ ] Run server and view visualization
- [ ] Test with real BlueSky API (when you have network)

### Week 2: Add Features
- [ ] Add Reddit sub-component
- [ ] Add Hacker News sub-component
- [ ] Improve sentiment analysis

### Week 3: Launch
- [ ] Create demo video
- [ ] Post to Hacker News
- [ ] Post to r/dataisbeautiful
- [ ] Update README with screenshots

---

## 📞 Support

If you hit issues:

1. Check the console output for errors
2. Verify all dependencies installed: `pip list | grep -E "requests|numpy|scikit|flask"`
3. Test with mock data first before real API

---

**Live long and prosper.** 🖖
