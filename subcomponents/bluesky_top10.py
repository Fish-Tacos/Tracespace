"""
BlueSky Sub-Component
Fetches top posts from BlueSky and converts to organisms
"""

import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from typing import List, Dict

import config
from subcomponents.base import SubComponentBase
from core.organism import Organism, Position, Color


class BlueSkyTop10(SubComponentBase):
    """
    BlueSky trending posts sub-component
    Fetches top 10 posts by engagement from BlueSky's "what's hot" feed
    """
    
    def __init__(self):
        super().__init__(name="BlueSky Top 10")
        self.api_base = config.BLUESKY_API_BASE
        self.feed_uri = config.BLUESKY_FEED_URI
        self.vectorizer = TfidfVectorizer(
            max_features=config.NLP_MAX_FEATURES,
            stop_words='english'
        )
    
    def fetch_raw_data(self) -> List[Dict]:
        """Fetch top posts from BlueSky API"""
        endpoint = f"{self.api_base}/app.bsky.feed.getFeed"
        
        params = {
            'feed': self.feed_uri,
            'limit': config.FETCH_LIMIT
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            posts = []
            for item in data.get('feed', [])[:config.FETCH_LIMIT]:
                post = item.get('post', {})
                
                # Extract engagement metrics
                like_count = post.get('likeCount', 0)
                repost_count = post.get('repostCount', 0)
                reply_count = post.get('replyCount', 0)
                
                posts.append({
                    'text': post.get('record', {}).get('text', ''),
                    'author': post.get('author', {}).get('handle', 'unknown'),
                    'likes': like_count,
                    'reposts': repost_count,
                    'replies': reply_count,
                    'total_engagement': like_count + repost_count + reply_count,
                    'timestamp': post.get('record', {}).get('createdAt', ''),
                    'uri': post.get('uri', '')
                })
            
            return posts
            
        except Exception as e:
            print(f"[{self.name}] Error fetching data: {e}")
            return []
    
    def process_to_organisms(self, raw_data: List[Dict]) -> List[Organism]:
        """Convert BlueSky posts to Organism objects"""
        if not raw_data:
            return []
        
        # Extract text for NLP processing
        texts = [post['text'] for post in raw_data]
        
        # Calculate 3D positions based on topic similarity
        positions = self._calculate_positions(texts)
        
        # Create organisms
        organisms = []
        for i, post in enumerate(raw_data):
            # Calculate sentiment color
            color = self._calculate_sentiment(post['text'])
            
            # Calculate size (log scale for engagement)
            size = self._calculate_size(post['total_engagement'])
            
            # Calculate velocity (placeholder for now - will be improved with historical data)
            velocity = min(post['total_engagement'] / 100, 1.0)
            
            organism = Organism(
                organism_id=f"bluesky_{i}",
                position=positions[i],
                size=size,
                color=color,
                velocity=velocity,
                text=post['text'][:200],  # Truncate for display
                metadata={
                    'author': post['author'],
                    'engagement': post['total_engagement'],
                    'likes': post['likes'],
                    'reposts': post['reposts'],
                    'replies': post['replies'],
                    'uri': post['uri'],
                    'source': 'bluesky'
                }
            )
            organisms.append(organism)
        
        return organisms
    
    def _calculate_positions(self, texts: List[str]) -> List[Position]:
        """
        Calculate 3D positions based on topic similarity using PCA
        Similar topics cluster together in 3D space
        """
        if len(texts) < 2:
            # Not enough data for PCA, return origin
            return [Position(0, 0, 0) for _ in texts]
        
        try:
            # Vectorize texts using TF-IDF
            vectors = self.vectorizer.fit_transform(texts)
            
            # Reduce to 3D using PCA
            n_components = min(3, len(texts))
            pca = PCA(n_components=n_components)
            positions_3d = pca.fit_transform(vectors.toarray())
            
            # Normalize to range [-POSITION_RANGE, POSITION_RANGE]
            if positions_3d.std() > 0:
                positions_3d = (positions_3d - positions_3d.mean(axis=0)) / (positions_3d.std(axis=0) + 1e-6)
                positions_3d *= config.POSITION_RANGE
            
            # Pad to 3D if needed
            if n_components < 3:
                padding = np.zeros((len(texts), 3 - n_components))
                positions_3d = np.hstack([positions_3d, padding])
            
            # Convert to Position objects
            return [Position(x=float(pos[0]), y=float(pos[1]), z=float(pos[2])) 
                    for pos in positions_3d]
            
        except Exception as e:
            print(f"[{self.name}] Position calculation error: {e}")
            # Fallback: random positions
            return [Position(
                x=np.random.randn() * config.POSITION_RANGE,
                y=np.random.randn() * config.POSITION_RANGE,
                z=np.random.randn() * config.POSITION_RANGE
            ) for _ in texts]
    
    def _calculate_sentiment(self, text: str) -> Color:
        """
        Simple sentiment analysis using word lists
        Returns RGB color where:
        - R (red) = negative sentiment
        - G (green) = neutral
        - B (blue) = positive sentiment
        """
        positive_words = [
            'good', 'great', 'amazing', 'awesome', 'love', 'excellent',
            'wonderful', 'fantastic', 'best', 'beautiful', 'perfect', 'happy',
            'excited', 'brilliant', 'outstanding', 'superb'
        ]
        negative_words = [
            'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible',
            'disappointing', 'poor', 'stupid', 'wrong', 'fail', 'sad',
            'angry', 'frustrated', 'annoying', 'pathetic'
        ]
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        total = pos_count + neg_count + 1
        
        # Map to RGB
        # Positive = more blue, Negative = more red, Neutral = more green
        r = neg_count / total  # Red for negative
        g = (1 - (pos_count + neg_count) / total)  # Green for neutral
        b = pos_count / total  # Blue for positive
        
        # Normalize and add baseline color so organisms aren't black
        base = 0.2
        r = base + (1 - base) * r
        g = base + (1 - base) * g
        b = base + (1 - base) * b
        
        return Color(r=float(r), g=float(g), b=float(b))
    
    def _calculate_size(self, engagement: int) -> float:
        """
        Calculate organism size from engagement
        Uses log scale to prevent huge size differences
        """
        # Log scale with minimum size
        size = np.log1p(engagement) + 1
        
        # Clamp to configured range
        size = max(config.ORGANISM_MIN_SIZE, min(config.ORGANISM_MAX_SIZE, size))
        
        return float(size)
