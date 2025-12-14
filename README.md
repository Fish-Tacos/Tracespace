# Trace Space

**Visualizing the Internet's Consciousness**

Trace Space transforms social media data into living, breathing 3D organisms. Watch information patterns emerge, pulse, and evolve in real-time as the internet's collective consciousness shifts.

Built using Donald Hoffman's Interface Theory of Perception as a theoretical framework.

---

## 🎯 What It Does

Trace Space creates a hierarchical visualization of information:

- **Sub-components**: Individual data sources (BlueSky posts, Reddit threads, etc.) appear as pulsing organisms
- **Components**: Aggregated patterns (Social Media consciousness) emerge from sub-components
- **Entity**: The complete "Internet Consciousness" emerges at the highest level

Each organism's properties reveal information patterns:
- **Size** = Engagement volume
- **Color** = Sentiment (red=negative, green=neutral, blue=positive)
- **Position** = Topic similarity (organisms with similar topics cluster together)
- **Pulse rate** = Velocity of change

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/tracespace.git
cd tracespace

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python run.py

# Start web server
python server.py
```

Then open your browser to `http://localhost:5000`

---

## 📁 Project Structure

```
tracespace/
├── core/                       # Core system components
│   ├── organism.py            # Base organism data structure
│   ├── aggregator.py          # Statistical aggregation logic
│   └── data_manager.py        # Tiered storage (hot/warm/cold)
│
├── subcomponents/             # Data source connectors
│   ├── base.py               # Abstract base class
│   └── bluesky_top10.py      # BlueSky trending posts
│
├── components/                # Mid-level aggregators
│   └── social_media.py       # Aggregates social sub-components
│
├── entity/                    # Top-level aggregators
│   └── internet_consciousness.py  # Complete information space
│
├── visualization/             # Web frontend
│   ├── index.html            # Three.js 3D display
│   └── data/                 # Served visualization data
│
├── data/                      # Tiered data storage
│   ├── hot/                  # Last 30 days (fast access)
│   ├── warm/                 # 30 days - 2 years (compressed)
│   └── cold/                 # Archive (>2 years)
│
├── config.py                  # System configuration
├── run.py                     # Main pipeline orchestrator
├── server.py                  # Flask web server
└── requirements.txt           # Python dependencies
```

---

## 🎨 How It Works

### 1. Data Fetching
Every hour, sub-components fetch data from their sources:
- BlueSky API for trending posts
- (Future: Reddit, Hacker News, Twitter, etc.)

### 2. NLP Processing
Each data item is processed:
- **Topic extraction**: TF-IDF + PCA to determine 3D position
- **Sentiment analysis**: Word-based sentiment → RGB color
- **Engagement metrics**: Likes/reposts/replies → organism size
- **Velocity**: Rate of change → pulse speed

### 3. Hierarchical Aggregation
Using statistical methods:
- **Sub-components → Component**: Average position, sum engagement, weighted color
- **Component → Entity**: Same aggregation at higher level

### 4. Visualization
Three.js renders organisms in 3D:
- Organisms pulse at different rates
- Similar topics cluster together
- Users can interact (hover for details, click for full info)
- Auto-refreshes every 60 seconds

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
FETCH_LIMIT = 10              # Posts per sub-component
REFRESH_INTERVAL = 3600       # Seconds between updates (1 hour)
DATA_HOT_RETENTION_DAYS = 30  # Keep uncompressed for 30 days
VISUALIZATION_PORT = 5000      # Web server port
```

---

## 📊 Data Storage

Trace Space uses tiered storage to manage data growth:

- **Hot** (0-30 days): Uncompressed JSON, fast access
- **Warm** (30 days - 2 years): Compressed, slower access
- **Cold** (>2 years): Archived

Automatic cleanup prevents disk space issues.

---

## 🛠️ Adding New Sub-Components

To add a new data source:

1. Create a new class extending `SubComponentBase`
2. Implement `fetch_raw_data()` and `process_to_organisms()`
3. Add to component in `run.py`

Example:

```python
# subcomponents/reddit_hot.py
from subcomponents.base import SubComponentBase

class RedditHot(SubComponentBase):
    def __init__(self):
        super().__init__(name="Reddit Hot")
    
    def fetch_raw_data(self):
        # Fetch from Reddit API
        pass
    
    def process_to_organisms(self, raw_data):
        # Convert to Organism objects
        pass
```

---

## 🧠 Theoretical Framework

Trace Space is inspired by **Donald Hoffman's Interface Theory of Perception**:

- **Conscious agents** perceive and act on information
- **Composition**: Agents combine into higher-order agents
- **Emergent properties**: Meta-patterns arise from aggregation

In Trace Space:
- Each organism = conscious agent
- Aggregation = agent composition
- Visualization = making consciousness visible

---

## 🎯 Roadmap

### Phase 1 (Current) - MVP
- [x] BlueSky sub-component
- [x] Statistical aggregation
- [x] 3D visualization
- [x] Tiered data storage

### Phase 2 - Expansion
- [ ] Add Reddit sub-component
- [ ] Add Hacker News sub-component
- [ ] Pattern detection (clusters, correlations)
- [ ] Historical comparison mode

### Phase 3 - Platform
- [ ] User accounts
- [ ] Custom sub-components
- [ ] Plugin marketplace
- [ ] Freemium model ($5/month for advanced features)

---

## 📝 License

MIT License - see LICENSE file

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See `CONTRIBUTING.md` for guidelines.

---

## 📧 Contact

Built by Fish-Tacos

- GitHub: [@Fish-Tacos](https://github.com/Fish-Tacos)
- Email: mrfishypantsdude@gmail.com 
---

## 🙏 Acknowledgments

- **Donald Hoffman** for Interface Theory of Perception
- **BlueSky** for open API access
- The open-source community

---

**Live long and prosper.** 🖖
