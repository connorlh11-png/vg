## Pac-Man in Ren'Py 8.5.2
## Add this to your Ren'Py project's game folder

init python:
    import pygame
    import random
    
    class PacManGame(renpy.Displayable):
        def __init__(self):
            renpy.Displayable.__init__(self)
            
            # Game constants
            self.CELL_SIZE = 30
            self.WIDTH = 19
            self.HEIGHT = 21
            
            # Simple maze (1 = wall, 0 = pellet, 2 = power pellet, 3 = empty)
            self.maze = [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
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
                [1,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,2,1],
                [1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
                [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
                [1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
            
            # Copy maze for pellet tracking
            self.current_maze = [row[:] for row in self.maze]
            
            # Pac-Man
            self.pacman_x = 9
            self.pacman_y = 15
            self.direction = (0, 0)
            self.next_direction = (0, 0)
            
            # Ghosts
            self.ghosts = [
                {"x": 8, "y": 9, "color": "#FF0000", "dir": (1, 0)},  # Red (Blinky)
                {"x": 9, "y": 9, "color": "#FFB8FF", "dir": (-1, 0)}, # Pink (Pinky)
                {"x": 10, "y": 9, "color": "#00FFFF", "dir": (0, -1)}, # Cyan (Inky)
                {"x": 9, "y": 10, "color": "#FFB852", "dir": (0, 1)},  # Orange (Clyde)
            ]
            
            # Game state
            self.score = 0
            self.lives = 3
            self.game_over = False
            self.won = False
            self.powered_up = False
            self.power_timer = 0
            
            # Animation
            self.move_timer = 0
            self.move_delay = 0.15
            
        def can_move(self, x, y):
            """Check if position is walkable"""
            if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
                return False
            return self.maze[y][x] != 1
            
        def update_pacman(self, dt):
            """Update Pac-Man position"""
            # Try to change direction
            if self.next_direction != (0, 0):
                new_x = self.pacman_x + self.next_direction[0]
                new_y = self.pacman_y + self.next_direction[1]
                if self.can_move(new_x, new_y):
                    self.direction = self.next_direction
                    
            # Move in current direction
            new_x = self.pacman_x + self.direction[0]
            new_y = self.pacman_y + self.direction[1]
            
            if self.can_move(new_x, new_y):
                self.pacman_x = new_x
                self.pacman_y = new_y
                
                # Wrap around
                if self.pacman_x < 0:
                    self.pacman_x = self.WIDTH - 1
                elif self.pacman_x >= self.WIDTH:
                    self.pacman_x = 0
                    
                # Eat pellets
                cell = self.current_maze[self.pacman_y][self.pacman_x]
                if cell == 0:  # Regular pellet
                    self.score += 10
                    self.current_maze[self.pacman_y][self.pacman_x] = 3
                elif cell == 2:  # Power pellet
                    self.score += 50
                    self.current_maze[self.pacman_y][self.pacman_x] = 3
                    self.powered_up = True
                    self.power_timer = 5.0  # 5 seconds of power
                    
        def update_ghosts(self, dt):
            """Simple ghost AI"""
            for ghost in self.ghosts:
                # Random movement
                if random.random() < 0.3:  # 30% chance to change direction
                    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                    random.shuffle(directions)
                    for d in directions:
                        new_x = ghost["x"] + d[0]
                        new_y = ghost["y"] + d[1]
                        if self.can_move(new_x, new_y):
                            ghost["dir"] = d
                            break
                
                # Move ghost
                new_x = ghost["x"] + ghost["dir"][0]
                new_y = ghost["y"] + ghost["dir"][1]
                
                if self.can_move(new_x, new_y):
                    ghost["x"] = new_x
                    ghost["y"] = new_y
                else:
                    # Hit wall, try new direction
                    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                    random.shuffle(directions)
                    for d in directions:
                        new_x = ghost["x"] + d[0]
                        new_y = ghost["y"] + d[1]
                        if self.can_move(new_x, new_y):
                            ghost["dir"] = d
                            ghost["x"] = new_x
                            ghost["y"] = new_y
                            break
                            
        def check_collisions(self):
            """Check if Pac-Man hit a ghost"""
            for ghost in self.ghosts:
                if ghost["x"] == self.pacman_x and ghost["y"] == self.pacman_y:
                    if self.powered_up:
                        # Eat ghost
                        self.score += 200
                        ghost["x"] = 9
                        ghost["y"] = 9
                    else:
                        # Lose life
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over = True
                        else:
                            # Reset positions
                            self.pacman_x = 9
                            self.pacman_y = 15
                            self.direction = (0, 0)
                            
        def check_win(self):
            """Check if all pellets eaten"""
            for row in self.current_maze:
                if 0 in row or 2 in row:
                    return
            self.won = True
            
        def render(self, width, height, st, at):
            """Render the game"""
            render = renpy.Render(width, height)
            
            # Update game state
            if not self.game_over and not self.won:
                dt = st - self.move_timer
                if dt >= self.move_delay:
                    self.update_pacman(dt)
                    self.update_ghosts(dt)
                    self.check_collisions()
                    self.check_win()
                    self.move_timer = st
                    
                    # Update power-up timer
                    if self.powered_up:
                        self.power_timer -= dt
                        if self.power_timer <= 0:
                            self.powered_up = False
            
            # Draw maze
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    cell_x = x * self.CELL_SIZE
                    cell_y = y * self.CELL_SIZE
                    
                    cell = self.current_maze[y][x]
                    
                    if cell == 1:  # Wall
                        wall = renpy.render(Solid("#0000AA", xsize=self.CELL_SIZE, ysize=self.CELL_SIZE), width, height, st, at)
                        render.blit(wall, (cell_x, cell_y))
                    elif cell == 0:  # Pellet
                        pellet_size = 4
                        pellet = renpy.render(Solid("#FFFF00", xsize=pellet_size, ysize=pellet_size), width, height, st, at)
                        render.blit(pellet, (cell_x + self.CELL_SIZE//2 - 2, cell_y + self.CELL_SIZE//2 - 2))
                    elif cell == 2:  # Power pellet
                        pellet_size = 8
                        pellet = renpy.render(Solid("#FFFFFF", xsize=pellet_size, ysize=pellet_size), width, height, st, at)
                        render.blit(pellet, (cell_x + self.CELL_SIZE//2 - 4, cell_y + self.CELL_SIZE//2 - 4))
            
            # Draw Pac-Man
            pacman_size = 20
            pacman_color = "#FFFF00" if not self.powered_up else "#FFFFFF"
            pacman = renpy.render(Solid(pacman_color, xsize=pacman_size, ysize=pacman_size), width, height, st, at)
            render.blit(pacman, (self.pacman_x * self.CELL_SIZE + 5, self.pacman_y * self.CELL_SIZE + 5))
            
            # Draw ghosts
            for ghost in self.ghosts:
                ghost_size = 18
                ghost_color = "#0000FF" if self.powered_up else ghost["color"]
                ghost_render = renpy.render(Solid(ghost_color, xsize=ghost_size, ysize=ghost_size), width, height, st, at)
                render.blit(ghost_render, (ghost["x"] * self.CELL_SIZE + 6, ghost["y"] * self.CELL_SIZE + 6))
            
            # Draw UI
            ui_text = "Score: %d  Lives: %d" % (self.score, self.lives)
            if self.game_over:
                ui_text = "GAME OVER! Score: %d - Press R to restart" % self.score
            elif self.won:
                ui_text = "YOU WIN! Score: %d - Press R to restart" % self.score
                
            text_render = renpy.render(Text(ui_text, color="#FFFFFF", size=24), width, height, st, at)
            render.blit(text_render, (10, self.HEIGHT * self.CELL_SIZE + 10))
            
            renpy.redraw(self, 0)
            return render
            
        def event(self, ev, x, y, st):
            """Handle keyboard input"""
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    self.next_direction = (0, -1)
                elif ev.key == pygame.K_DOWN:
                    self.next_direction = (0, 1)
                elif ev.key == pygame.K_LEFT:
                    self.next_direction = (-1, 0)
                elif ev.key == pygame.K_RIGHT:
                    self.next_direction = (1, 0)
                elif ev.key == pygame.K_r:
                    # Restart game
                    self.__init__()
                elif ev.key == pygame.K_ESCAPE:
                    return True  # Exit game
                    
            raise renpy.IgnoreEvent()

# Define the game screen
screen pacman_game():
    add PacManGame()

# Label to start the game
label start_pacman:
    window hide
    call screen pacman_game
    return