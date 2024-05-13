class settings():
    def __init__(self):
        self.screen_width = 1366
        self.screen_height = 768

        self.ship_speed = 1.5
        self.ship_limit = 3
        self.bg_color = (22, 14, 61)
        
        self.bullet_speed = 1.5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (255, 0, 255)
        self.bullet_allowed = 5
        
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1 right, -1 left

        self.alien_points = 50
        