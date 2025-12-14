"""
Test Trace Space with Mock Data
Generates fake organism data to test visualization without API access
"""

import json
import random
from datetime import datetime
from pathlib import Path

def generate_mock_data():
    """Generate realistic mock organism data"""
    
    # Mock BlueSky posts
    mock_posts = [
        {"text": "Just shipped our new AI feature! So excited to see what people build with it.", "author": "techfounder", "likes": 342, "reposts": 89, "replies": 67},
        {"text": "Hot take: The future of computing is not in the cloud, it's in local-first software.", "author": "devthoughts", "likes": 567, "reposts": 234, "replies": 123},
        {"text": "Our team just hit 1M users! Thank you all for the amazing support 🎉", "author": "startup_ceo", "likes": 892, "reposts": 156, "replies": 201},
        {"text": "AI agents are getting really good at coding. Just had Claude help me debug a nasty race condition.", "author": "engineer_mike", "likes": 445, "reposts": 98, "replies": 87},
        {"text": "The intersection of consciousness and computation is fascinating. Hoffman's work is mind-bending.", "author": "philo_coder", "likes": 234, "reposts": 67, "replies": 45},
        {"text": "Deployed to production on a Friday. Living dangerously 😎", "author": "devops_guru", "likes": 678, "reposts": 201, "replies": 134},
        {"text": "Just finished reading 'The Case Against Reality'. My perception of reality will never be the same.", "author": "curious_mind", "likes": 189, "reposts": 45, "replies": 32},
        {"text": "Why does every SaaS product now have an AI chatbot? Sometimes I just want a simple FAQ page.", "author": "ux_designer", "likes": 523, "reposts": 167, "replies": 98},
        {"text": "Breakthrough in quantum error correction! This could be the path to practical quantum computers.", "author": "quantum_researcher", "likes": 756, "reposts": 289, "replies": 156},
        {"text": "Remember when websites were just HTML and CSS? Those were simpler times...", "author": "old_school_dev", "likes": 412, "reposts": 123, "replies": 89}
    ]
    
    # Generate sub-components
    subcomponents = []
    for i, post in enumerate(mock_posts):
        total_engagement = post['likes'] + post['reposts'] + post['replies']
        
        # Sentiment analysis (simple mock)
        sentiment_score = (post['likes'] - post['replies'] * 0.3) / total_engagement
        if sentiment_score > 0.3:
            color = {'r': 0.3, 'g': 0.4, 'b': 0.8}  # Positive = blue
        elif sentiment_score < -0.1:
            color = {'r': 0.8, 'g': 0.3, 'b': 0.3}  # Negative = red
        else:
            color = {'r': 0.4, 'g': 0.7, 'b': 0.4}  # Neutral = green
        
        # Position (topic clustering simulation)
        position = {
            'x': random.uniform(-5, 5),
            'y': random.uniform(-5, 5),
            'z': random.uniform(-5, 5)
        }
        
        # Size based on engagement
        import math
        size = math.log1p(total_engagement) / 2 + 0.5
        
        subcomp = {
            'id': f'bluesky_{i}',
            'position': position,
            'size': size,
            'color': color,
            'velocity': min(total_engagement / 500, 1.0),
            'text': post['text'],
            'metadata': {
                'author': post['author'],
                'engagement': total_engagement,
                'likes': post['likes'],
                'reposts': post['reposts'],
                'replies': post['replies'],
                'source': 'bluesky'
            }
        }
        subcomponents.append(subcomp)
    
    # Generate component (aggregate of sub-components)
    avg_x = sum(s['position']['x'] for s in subcomponents) / len(subcomponents)
    avg_y = sum(s['position']['y'] for s in subcomponents) / len(subcomponents)
    avg_z = sum(s['position']['z'] for s in subcomponents) / len(subcomponents)
    
    total_engagement = sum(s['metadata']['engagement'] for s in subcomponents)
    
    component = {
        'id': 'social_media_component',
        'position': {'x': avg_x, 'y': avg_y, 'z': avg_z},
        'size': math.log1p(total_engagement) + 1,
        'color': {'r': 0.5, 'g': 0.6, 'b': 0.5},
        'velocity': 0.5,
        'text': f'Composite of {len(subcomponents)} organisms',
        'metadata': {
            'child_count': len(subcomponents),
            'total_engagement': total_engagement,
            'aggregate_method': 'statistical'
        },
        'children': subcomponents
    }
    
    # Generate entity (top level)
    entity = {
        'id': 'internet_consciousness_entity',
        'position': {'x': avg_x, 'y': avg_y, 'z': avg_z},
        'size': math.log1p(total_engagement) + 2,
        'color': {'r': 0.4, 'g': 0.5, 'b': 0.6},
        'velocity': 0.3,
        'text': f'Composite of 1 components',
        'metadata': {
            'child_count': 1,
            'total_engagement': total_engagement,
            'aggregate_method': 'statistical'
        },
        'components': [component]
    }
    
    # Complete data structure
    data = {
        'timestamp': datetime.now().isoformat(),
        'entity': entity,
        'components': [component],
        'subcomponents': subcomponents,
        'stats': {
            'total_organisms': len(subcomponents),
            'component_count': 1,
            'total_engagement': total_engagement
        }
    }
    
    return data

def main():
    """Generate mock data and save for visualization"""
    print("="*60)
    print("TRACE SPACE - MOCK DATA GENERATOR")
    print("="*60)
    
    # Generate data
    data = generate_mock_data()
    
    # Save to visualization directory
    viz_dir = Path('visualization/data')
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = viz_dir / 'latest.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Generated mock data:")
    print(f"   - {data['stats']['total_organisms']} organisms")
    print(f"   - Total engagement: {data['stats']['total_engagement']:,}")
    print(f"   - Saved to: {output_file}")
    print("\n" + "="*60)
    print("Now run: python server.py")
    print("Then open: http://localhost:5000")
    print("="*60)

if __name__ == "__main__":
    main()
