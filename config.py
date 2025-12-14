"""
Trace Space Configuration
All system settings in one place
"""

# API Settings
BLUESKY_API_BASE = "https://public.api.bsky.app/xrpc"
BLUESKY_FEED_URI = "at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot"

# Data Settings
DATA_HOT_DIR = "data/hot"
DATA_WARM_DIR = "data/warm"
DATA_COLD_DIR = "data/cold"
DATA_HOT_RETENTION_DAYS = 30
DATA_WARM_RETENTION_DAYS = 730  # 2 years

# Processing Settings
FETCH_LIMIT = 10  # Number of posts to fetch per sub-component
REFRESH_INTERVAL = 3600  # Seconds between fetches (1 hour)
NLP_MAX_FEATURES = 50  # TF-IDF feature limit
POSITION_RANGE = 5  # Organisms positioned in [-5, 5] range

# Visualization Settings
VISUALIZATION_PORT = 5000
AUTO_REFRESH_SECONDS = 60

# Organism Display Settings
ORGANISM_MIN_SIZE = 0.5
ORGANISM_MAX_SIZE = 5.0
ORGANISM_PULSE_SPEED_MIN = 0.5
ORGANISM_PULSE_SPEED_MAX = 2.0

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "tracespace.log"
