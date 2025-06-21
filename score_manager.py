import json
import os

class ScoreManager:
    def __init__(self, filename="high_scores.json"):
        self.filename = filename
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def add_high_score(self, name, score):
        """Add a new high score"""
        self.high_scores.append({"name": name, "score": score})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        self.save_high_scores()
    
    def get_high_scores(self):
        """Get the list of high scores"""
        return self.high_scores
