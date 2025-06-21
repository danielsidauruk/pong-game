import random

class AIPlayer:
    def __init__(self, paddle, difficulty=0.8):
        self.paddle = paddle
        self.difficulty = difficulty  # 0.0 to 1.0, higher is harder
        
    def update(self, ball):
        # AI follows the ball with some imperfection
        paddle_center = self.paddle.y + self.paddle.height // 2
        ball_y = ball.y
        
        # Add some randomness to make AI beatable
        if random.random() < self.difficulty:
            if ball_y < paddle_center - 10:
                self.paddle.move_up()
            elif ball_y > paddle_center + 10:
                self.paddle.move_down()
