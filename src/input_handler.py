import pygame

class InputHandler:
    def __init__(self):
        pass
    
    def handle_name_input(self, event, input_text):
        """Handle name input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_text.strip():
                    return input_text.strip(), True  # name, should_start
            elif event.key == pygame.K_BACKSPACE:
                return input_text[:-1], False
            else:
                if len(input_text) < 15:  # Limit name length
                    return input_text + event.unicode, False
        return input_text, False
    
    def handle_paddle_movement(self, paddle):
        """Handle continuous paddle movement input"""
        keys = pygame.key.get_pressed()
        mouse_y = pygame.mouse.get_pos()[1]
        
        # Keyboard controls
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            paddle.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            paddle.move_down()
        
        # Mouse controls (optional)
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            paddle_center = paddle.y + paddle.height // 2
            if mouse_y < paddle_center - 10:
                paddle.move_up()
            elif mouse_y > paddle_center + 10:
                paddle.move_down()
    
    def handle_game_over_input(self, event):
        """Handle game over screen input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "restart"
            elif event.key == pygame.K_ESCAPE:
                return "quit"
        return None
