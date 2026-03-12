## Pac-Man Submod for Monika After Story
## Play Pac-Man with Monika!

init -990 python in mas_submod_utils:
    Submod(
        author="Kiwi",
        name="PacMan Game",
        description="Play Pac-Man with Monika!",
        version="1.0.0"
    )

init -10 python:
    import store
    import random
    
    # Persistent variables
    if persistent._pacman_high_score is None:
        persistent._pacman_high_score = 0
    if persistent._pacman_games_played is None:
        persistent._pacman_games_played = 0
    
    # Game constants
    PACMAN_CELL_SIZE = 25
    PACMAN_COLS = 19
    PACMAN_ROWS = 21
    
    # Level themes - changes every 2000 points
    PACMAN_THEMES = [
        {
            'name': 'Classic',
            'wall': '#0000FF',      # Blue walls
            'bg': '#000000',        # Black background
            'dot': '#FFFF00',       # Yellow dots
            'pacman': '#FFFF00',    # Yellow Pac-Man
            'ghost_scared': '#0000FF'  # Blue when scared
        },
        {
            'name': 'Forest',
            'wall': '#228B22',      # Forest green walls
            'bg': '#0A3A0A',        # Dark green background
            'dot': '#90EE90',       # Light green dots
            'pacman': '#FFD700',    # Gold Pac-Man
            'ghost_scared': '#228B22'  # Green when scared
        },
        {
            'name': 'Ocean',
            'wall': '#1E90FF',      # Dodger blue walls
            'bg': '#000033',        # Dark blue background
            'dot': '#00FFFF',       # Cyan dots
            'pacman': '#FFA500',    # Orange Pac-Man
            'ghost_scared': '#1E90FF'  # Blue when scared
        },
        {
            'name': 'Sunset',
            'wall': '#FF4500',      # Orange-red walls
            'bg': '#2B0A0A',        # Dark red background
            'dot': '#FFD700',       # Gold dots
            'pacman': '#FF69B4',    # Hot pink Pac-Man
            'ghost_scared': '#FF4500'  # Orange when scared
        },
        {
            'name': 'Candy',
            'wall': '#FF1493',      # Deep pink walls
            'bg': '#1A0A1A',        # Dark purple background
            'dot': '#FF69B4',       # Hot pink dots
            'pacman': '#00FFFF',    # Cyan Pac-Man
            'ghost_scared': '#FF1493'  # Pink when scared
        },
        {
            'name': 'Neon',
            'wall': '#00FF00',      # Lime green walls
            'bg': '#0A0A0A',        # Almost black background
            'dot': '#FF00FF',       # Magenta dots
            'pacman': '#00FFFF',    # Cyan Pac-Man
            'ghost_scared': '#00FF00'  # Green when scared
        },
        {
            'name': 'Lava',
            'wall': '#8B0000',      # Dark red walls
            'bg': '#1A0000',        # Very dark red background
            'dot': '#FFA500',       # Orange dots
            'pacman': '#FFFF00',    # Yellow Pac-Man
            'ghost_scared': '#8B0000'  # Dark red when scared
        },
        {
            'name': 'Ice',
            'wall': '#87CEEB',      # Sky blue walls
            'bg': '#0A1A2A',        # Dark blue background
            'dot': '#E0FFFF',       # Light cyan dots
            'pacman': '#FFFFFF',    # White Pac-Man
            'ghost_scared': '#87CEEB'  # Sky blue when scared
        },
        {
            'name': 'Space',
            'wall': '#4B0082',      # Indigo walls
            'bg': '#000000',        # Black background
            'dot': '#FFFFFF',       # White dots (stars)
            'pacman': '#FFD700',    # Gold Pac-Man
            'ghost_scared': '#4B0082'  # Indigo when scared
        },
        {
            'name': 'Rainbow',
            'wall': '#FF00FF',      # Magenta walls
            'bg': '#0A0A1A',        # Very dark blue background
            'dot': '#FFFF00',       # Yellow dots
            'pacman': '#00FF00',    # Green Pac-Man
            'ghost_scared': '#FF00FF'  # Magenta when scared
        }
    ]
    
    # Maze layout (1 = wall, 0 = dot, 2 = power pellet, 3 = empty)
    PACMAN_MAZE = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
        [1,2,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,2,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,0,1,1,1,3,1,3,1,1,1,0,1,1,1,1],
        [1,1,1,1,0,1,3,3,3,3,3,3,3,1,0,1,1,1,1],
        [1,1,1,1,0,1,3,1,1,3,1,1,3,1,0,1,1,1,1],
        [3,3,3,3,0,3,3,1,3,3,3,1,3,3,0,3,3,3,3],
        [1,1,1,1,0,1,3,1,1,1,1,1,3,1,0,1,1,1,1],
        [1,1,1,1,0,1,3,3,3,3,3,3,3,1,0,1,1,1,1],
        [1,1,1,1,0,1,3,1,1,1,1,1,3,1,0,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
        [1,2,0,1,0,0,0,0,0,3,0,0,0,0,0,1,0,2,1],
        [1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
        [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
    
    class PacManGame:
        def __init__(self):
            self.pacman_x = 9
            self.pacman_y = 16
            self.direction = None  # 'up', 'down', 'left', 'right'
            self.next_direction = None
            self.score = 0
            self.dots_remaining = 0
            self.power_pellets_remaining = 0
            self.game_over = False
            self.won = False
            self.maze = []
            self.ghosts = []
            self.power_mode = False
            self.power_timer = 0
            self.level = 1
            self.theme = PACMAN_THEMES[0]
            
        def start(self):
            """Start a new game"""
            self.pacman_x = 9
            self.pacman_y = 16
            self.direction = None
            self.next_direction = None
            self.score = 0
            self.game_over = False
            self.won = False
            self.power_mode = False
            self.power_timer = 0
            self.level = 1
            self.theme = PACMAN_THEMES[0]
            
            # Copy maze
            self.maze = [row[:] for row in PACMAN_MAZE]
            
            # Count dots and power pellets
            self.dots_remaining = sum(row.count(0) for row in self.maze)
            self.power_pellets_remaining = sum(row.count(2) for row in self.maze)
            
            # Initialize ghosts
            self.ghosts = [
                {'x': 9, 'y': 9, 'color': '#FF0000', 'dir': 'left', 'respawn_timer': 0},   # Red (Blinky)
                {'x': 8, 'y': 10, 'color': '#FFB8FF', 'dir': 'up', 'respawn_timer': 0},    # Pink (Pinky)
                {'x': 9, 'y': 10, 'color': '#00FFFF', 'dir': 'down', 'respawn_timer': 0},  # Cyan (Inky)
                {'x': 10, 'y': 10, 'color': '#FFB852', 'dir': 'right', 'respawn_timer': 0} # Orange (Clyde)
            ]
        
        def update_level(self):
            """Update level based on score"""
            new_level = (self.score // 2000) + 1
            if new_level != self.level and new_level <= len(PACMAN_THEMES):
                self.level = new_level
                self.theme = PACMAN_THEMES[self.level - 1]
                
                # Check for victory at level 10
                if self.level == 10:
                    self.won = True
                    return True
                return True  # Level changed
            return False
        
        def respawn_dots(self):
            """Respawn all dots (not power pellets)"""
            for row_idx in range(PACMAN_ROWS):
                for col_idx in range(PACMAN_COLS):
                    # If it was originally a dot in the template, respawn it
                    if PACMAN_MAZE[row_idx][col_idx] == 0 and self.maze[row_idx][col_idx] == 3:
                        self.maze[row_idx][col_idx] = 0
                        self.dots_remaining += 1
        
        def set_direction(self, direction):
            """Set next direction"""
            self.next_direction = direction
        
        def can_move(self, x, y):
            """Check if position is valid"""
            if x < 0 or x >= PACMAN_COLS or y < 0 or y >= PACMAN_ROWS:
                return False
            return self.maze[y][x] != 1
        
        def update(self):
            """Update game state"""
            if self.game_over or self.won:
                return
            
            # Update power mode timer
            if self.power_mode:
                self.power_timer -= 1
                if self.power_timer <= 0:
                    self.power_mode = False
            
            # Try to change direction
            if self.next_direction:
                new_x, new_y = self.pacman_x, self.pacman_y
                if self.next_direction == 'up':
                    new_y -= 1
                elif self.next_direction == 'down':
                    new_y += 1
                elif self.next_direction == 'left':
                    new_x -= 1
                elif self.next_direction == 'right':
                    new_x += 1
                
                if self.can_move(new_x, new_y):
                    self.direction = self.next_direction
                    self.next_direction = None
            
            # Move Pac-Man
            if self.direction:
                new_x, new_y = self.pacman_x, self.pacman_y
                if self.direction == 'up':
                    new_y -= 1
                elif self.direction == 'down':
                    new_y += 1
                elif self.direction == 'left':
                    new_x -= 1
                elif self.direction == 'right':
                    new_x += 1
                
                # Wrap around
                if new_x < 0:
                    new_x = PACMAN_COLS - 1
                elif new_x >= PACMAN_COLS:
                    new_x = 0
                
                if self.can_move(new_x, new_y):
                    self.pacman_x = new_x
                    self.pacman_y = new_y
                    
                    # Eat dot
                    if self.maze[new_y][new_x] == 0:
                        self.maze[new_y][new_x] = 3
                        self.score += 10
                        self.dots_remaining -= 1
                        self.update_level()  # Check for level up
                        
                        if self.dots_remaining == 0:
                            self.won = True
                    
                    # Eat power pellet
                    elif self.maze[new_y][new_x] == 2:
                        self.maze[new_y][new_x] = 3
                        self.score += 50
                        self.power_mode = True
                        self.power_timer = 50  # 50 frames (about 7.5 seconds)
                        self.power_pellets_remaining -= 1
                        self.update_level()  # Check for level up
                        
                        # Respawn all dots when all power pellets are eaten
                        if self.power_pellets_remaining == 0:
                            self.respawn_dots()
                            # Reset power pellets
                            for row_idx in range(PACMAN_ROWS):
                                for col_idx in range(PACMAN_COLS):
                                    if PACMAN_MAZE[row_idx][col_idx] == 2:
                                        self.maze[row_idx][col_idx] = 2
                            self.power_pellets_remaining = sum(row.count(2) for row in self.maze)
            
            # Check collision with ghosts BEFORE moving them
            for ghost in self.ghosts:
                # Decrease respawn timer
                if ghost['respawn_timer'] > 0:
                    ghost['respawn_timer'] -= 1
                    continue  # Skip collision check while respawning
                
                if ghost['x'] == self.pacman_x and ghost['y'] == self.pacman_y:
                    if self.power_mode:
                        # Eat ghost
                        self.score += 200
                        ghost['x'] = 9
                        ghost['y'] = 9
                        ghost['respawn_timer'] = 20  # 20 frames of immunity
                    else:
                        # Game over
                        self.game_over = True
                        return
            
            # Move ghosts with improved AI
            for ghost in self.ghosts:
                # Don't move if respawning
                if ghost['respawn_timer'] > 0:
                    continue
                # Get possible directions
                possible_dirs = []
                for direction in ['up', 'down', 'left', 'right']:
                    gx, gy = ghost['x'], ghost['y']
                    if direction == 'up':
                        gy -= 1
                    elif direction == 'down':
                        gy += 1
                    elif direction == 'left':
                        gx -= 1
                    elif direction == 'right':
                        gx += 1
                    
                    # Check if position is valid AND no other ghost is there
                    if self.can_move(gx, gy):
                        # Check if another ghost is already at this position
                        ghost_collision = False
                        for other_ghost in self.ghosts:
                            if other_ghost is not ghost and other_ghost['x'] == gx and other_ghost['y'] == gy:
                                ghost_collision = True
                                break
                        
                        if not ghost_collision:
                            possible_dirs.append((direction, gx, gy))
                
                if possible_dirs:
                    if self.power_mode:
                        # Run away from Pac-Man when scared
                        best_dir = None
                        max_dist = -1
                        for direction, gx, gy in possible_dirs:
                            dist = abs(gx - self.pacman_x) + abs(gy - self.pacman_y)
                            if dist > max_dist:
                                max_dist = dist
                                best_dir = (direction, gx, gy)
                        if best_dir:
                            new_dir, new_x, new_y = best_dir
                        else:
                            new_dir, new_x, new_y = random.choice(possible_dirs)
                    else:
                        # Chase Pac-Man (70% of the time, otherwise random)
                        if random.random() < 0.7:
                            # Find direction that gets closer to Pac-Man
                            best_dir = None
                            min_dist = 999999
                            for direction, gx, gy in possible_dirs:
                                dist = abs(gx - self.pacman_x) + abs(gy - self.pacman_y)
                                if dist < min_dist:
                                    min_dist = dist
                                    best_dir = (direction, gx, gy)
                            if best_dir:
                                new_dir, new_x, new_y = best_dir
                            else:
                                new_dir, new_x, new_y = random.choice(possible_dirs)
                        else:
                            # Random movement
                            new_dir, new_x, new_y = random.choice(possible_dirs)
                    
                    ghost['dir'] = new_dir
                    ghost['x'] = new_x
                    ghost['y'] = new_y
            
            # Check collision with ghosts AFTER moving them too
            for ghost in self.ghosts:
                # Skip if respawning
                if ghost['respawn_timer'] > 0:
                    continue
                
                if ghost['x'] == self.pacman_x and ghost['y'] == self.pacman_y:
                    if self.power_mode:
                        # Eat ghost
                        self.score += 200
                        ghost['x'] = 9
                        ghost['y'] = 9
                        ghost['respawn_timer'] = 20  # 20 frames of immunity
                    else:
                        # Game over
                        self.game_over = True
    
    # Global game instance
    pacman_game = PacManGame()

# Main Pac-Man event - Register in game database
init 5 python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="mas_pacman_game",
            prompt="Pac-Man",
            unlocked=True
        ),
        code="GME",
        restartBlacklist=True
    )

label mas_pacman_game:
    python:
        pacman_game.start()
        persistent._pacman_games_played += 1
    
    call screen pacman_game_screen
    
    python:
        final_score = pacman_game.score
        if final_score > persistent._pacman_high_score:
            persistent._pacman_high_score = final_score
            new_high_score = True
        else:
            new_high_score = False
    
    python:
        max_level_reached = pacman_game.level
        theme_name = pacman_game.theme['name']
    
    if pacman_game.won:
        if max_level_reached >= 10:
            m 1wubso "Wait...{w=0.5} Did you just...?"
            m 3sub "YOU WON!!!"
            m 1hub "You reached level 10!"
            m 3hua "You beat all the themes and conquered Pac-Man!"
            m 1ekbsa "I'm so proud of you, [player]!"
            m 3hubfb "That was incredible to watch!"
            m 1eka "The ghosts got so fast at the end..."
            m 3eub "But you still made it through!"
            m 1hubfa "You're amazing~"
        else:
            m 1sub "Oh my gosh, [player]!"
            m 3hub "You beat the whole maze!"
            m 1hua "That's amazing!"
            m 3eka "You're really good at this!"
            if max_level_reached > 1:
                m 1eub "And you made it to the [theme_name] theme!"
    elif new_high_score:
        m 1hua "New high score!"
        m 3eub "You got [final_score] points!"
        if max_level_reached > 1:
            m 1hua "You reached level [max_level_reached] - the [theme_name] theme!"
        m 1eka "Great job, [player]!"
    elif final_score >= 2000:
        m 1hua "Nice job, [player]!"
        m 3eub "You scored [final_score] points!"
        if max_level_reached > 1:
            m 1eua "You got to see the [theme_name] theme!"
            m 3hub "Pretty cool, right?"
    else:
        m 1eka "You scored [final_score] points!"
        m 3eua "Those ghosts can be tricky!"
        m 1hua "Try to get 2000 points to see the next theme!"
    
    return

# Pac-Man game screen
screen pacman_game_screen():
    modal True
    
    # Update game every 0.15 seconds
    if not pacman_game.game_over and not pacman_game.won:
        timer 0.15 repeat True action Function(pacman_game.update)
    
    # Extract theme colors at the screen level
    python:
        theme_name = pacman_game.theme['name']
        theme_dot_color = pacman_game.theme['dot']
        theme_pacman_color = pacman_game.theme['pacman']
        theme_wall_color = pacman_game.theme['wall']
        theme_bg_color = pacman_game.theme['bg']
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 550
        ysize 680
        background "#000000"
        padding (10, 10)
        
        vbox:
            spacing 5
            xalign 0.5
            yalign 0.5
            
            # Score display
            hbox:
                spacing 10
                xalign 0.5
                
                frame:
                    background "#FFE6F4"
                    padding (8, 4)
                    text "Score: [pacman_game.score]" size 18 color "#000000" outlines []
                
                frame:
                    background "#FFE6F4"
                    padding (8, 4)
                    text "Level: [pacman_game.level]" size 18 color "#000000" outlines []
                
                frame:
                    background "#FFE6F4"
                    padding (8, 4)
                    text "[theme_name]" size 18 color "#000000" outlines []
                
                if pacman_game.power_mode:
                    frame:
                        background "#FFE6F4"
                        padding (8, 4)
                        text "POWER!" size 18 color "#000000" outlines []
            
            # Game area
            frame:
                xsize PACMAN_COLS * PACMAN_CELL_SIZE + 10
                ysize PACMAN_ROWS * PACMAN_CELL_SIZE + 10
                background Solid(theme_bg_color)
                
                vbox:
                    spacing 0
                    xalign 0.5
                    yalign 0.5
                    
                    # Draw maze
                    for row_idx in range(PACMAN_ROWS):
                        hbox:
                            spacing 0
                            for col_idx in range(PACMAN_COLS):
                                python:
                                    cell = pacman_game.maze[row_idx][col_idx]
                                    theme = pacman_game.theme
                                    
                                    if cell == 1:
                                        cell_color = theme['wall']  # Wall
                                    elif cell == 0:
                                        cell_color = theme['bg']  # Dot (will draw separately)
                                    elif cell == 2:
                                        cell_color = theme['bg']  # Power pellet
                                    else:
                                        cell_color = theme['bg']  # Empty
                                    
                                    # Extract theme colors for use in screen
                                    dot_color = theme['dot']
                                    pacman_color = theme['pacman']
                                    
                                    # Check if Pac-Man is here
                                    is_pacman = (col_idx == pacman_game.pacman_x and row_idx == pacman_game.pacman_y)
                                    
                                    # Check if ghost is here
                                    ghost_here = None
                                    ghost_color = None
                                    for ghost in pacman_game.ghosts:
                                        if ghost['x'] == col_idx and ghost['y'] == row_idx:
                                            ghost_here = ghost
                                            if pacman_game.power_mode:
                                                ghost_color = theme['ghost_scared']
                                            else:
                                                ghost_color = ghost['color']
                                            break
                                
                                frame:
                                    xysize (PACMAN_CELL_SIZE, PACMAN_CELL_SIZE)
                                    background Solid(cell_color)
                                    
                                    # Draw dot
                                    if cell == 0:
                                        frame:
                                            xalign 0.5
                                            yalign 0.5
                                            xysize (4, 4)
                                            background Solid(dot_color)
                                    
                                    # Draw power pellet
                                    elif cell == 2:
                                        frame:
                                            xalign 0.5
                                            yalign 0.5
                                            xysize (8, 8)
                                            background Solid(dot_color)
                                    
                                    # Draw Pac-Man
                                    if is_pacman:
                                        frame:
                                            xalign 0.5
                                            yalign 0.5
                                            xysize (18, 18)
                                            background Solid(pacman_color)
                                    
                                    # Draw ghost
                                    elif ghost_here:
                                        frame:
                                            xalign 0.5
                                            yalign 0.5
                                            xysize (18, 18)
                                            background Solid(ghost_color)
            
            # Controls and status
            hbox:
                spacing 15
                xalign 0.5
                
                if pacman_game.game_over or pacman_game.won:
                    vbox:
                        spacing 8
                        xalign 0.5
                        
                        if pacman_game.won:
                            if pacman_game.level >= 10:
                                frame:
                                    background "#FFE6F4"
                                    padding (12, 6)
                                    xalign 0.5
                                    text "YOU WON!!!" size 24 color "#000000" outlines []
                                frame:
                                    background "#FFE6F4"
                                    padding (12, 6)
                                    xalign 0.5
                                    text "LEVEL 10 COMPLETE!" size 18 color "#000000" outlines []
                            else:
                                frame:
                                    background "#FFE6F4"
                                    padding (12, 6)
                                    xalign 0.5
                                    text "YOU WIN!" size 24 color "#000000" outlines []
                        else:
                            frame:
                                background "#FFE6F4"
                                padding (12, 6)
                                xalign 0.5
                                text "GAME OVER" size 24 color "#000000" outlines []
                        
                        textbutton "Finish":
                            style "hkb_button"
                            xalign 0.5
                            action Return()
                
                if not pacman_game.game_over and not pacman_game.won:
                    textbutton "Quit":
                        style "hkb_button"
                        action Return()
    
    # Keyboard controls
    if not pacman_game.game_over and not pacman_game.won:
        key "K_UP" action Function(pacman_game.set_direction, 'up')
        key "K_DOWN" action Function(pacman_game.set_direction, 'down')
        key "K_LEFT" action Function(pacman_game.set_direction, 'left')
        key "K_RIGHT" action Function(pacman_game.set_direction, 'right')
        key "K_w" action Function(pacman_game.set_direction, 'up')
        key "K_s" action Function(pacman_game.set_direction, 'down')
        key "K_a" action Function(pacman_game.set_direction, 'left')
        key "K_d" action Function(pacman_game.set_direction, 'right')

# Stats
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_pacman_stats",
            category=['monika'],
            prompt="What's my Pac-Man high score?",
            pool=True,
            unlocked=True
        )
    )

label mas_pacman_stats:
    python:
        high_score = persistent._pacman_high_score
        games = persistent._pacman_games_played
    
    if games == 0:
        m 1eua "You haven't played Pac-Man with me yet, [player]."
        m 3eub "Want to give it a try?"
    else:
        m 1eua "Let me check..."
        m 3eub "Your high score is [high_score] points!"
        m 1hua "You've played [games] games total."
        
        if high_score > 2000:
            m 3hub "That's incredible!"
            m 1eka "You're a Pac-Man master!"
        elif high_score > 1000:
            m 1hua "That's really good!"
            m 3eua "You're getting the hang of it."
        else:
            m 1eka "Keep playing!"
            m 3eub "You'll get better at avoiding those ghosts."
    
    return
