from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import sys
from collections import deque

# Constants
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600
GRID_SIZE = 30
CELL_SIZE = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

pygame.init()

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_wall = False
        self.is_start = False
        self.is_end = False

    def draw(self, screen):
        if self.is_wall:
            pygame.draw.rect(screen, WHITE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if self.is_start:
            pygame.draw.circle(screen, GREEN, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
        if self.is_end:
            pygame.draw.circle(screen, RED, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(i, j) for j in range(rows)] for i in range(cols)]

    def draw(self, screen):
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

    def solve_with_bfs(self, screen, clock, drawer):
        start = None
        end = None
        for row in self.grid:
            for cell in row:
                if cell.is_start:
                    start = cell
                if cell.is_end:
                    end = cell

        if not start or not end:
            print("No start or end defined!")
            return iter([])  # Return an empty iterator

        visited = [[False for _ in range(self.rows)] for _ in range(self.cols)]
        queue = deque([(start.x, start.y)])
        prev = {(start.x, start.y): None}

        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        found = False

        while queue and not found:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            x, y = queue.popleft()
            current_cell = self.grid[x][y]
            visited[x][y] = True

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows and not visited[nx][ny]:
                    neighbor = self.grid[nx][ny]
                    if not neighbor.is_wall:
                        prev[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
                        visited[nx][ny] = True

                    if neighbor.is_end:
                        found = True
                        break

            # Draw the maze and grid
            self.draw(screen)
            drawer.draw_grid()

            # Draw the visited cells
            for i in range(self.cols):
                for j in range(self.rows):
                    if visited[i][j]:
                        pygame.draw.rect(screen, PURPLE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            pygame.display.flip()
            clock.tick(60)

        if found:
            path = []
            x, y = end.x, end.y
            while (x, y) != (start.x, start.y):
                path.append((x, y))
                x, y = prev[(x, y)]
            path.reverse()

            for x, y in path:
                pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                self.draw(screen)
                drawer.draw_grid()
                pygame.display.flip()
                clock.tick(60)

            waiting_for_click = True
            while waiting_for_click:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting_for_click = False
        return found
    
    def solve_with_dfs(self, screen, clock, drawer):
        start = None
        end = None
        for row in self.grid:
            for cell in row:
                if cell.is_start:
                    start = cell
                if cell.is_end:
                    end = cell

        if not start or not end:
            print("No start or end defined!")
            return False

        visited = [[False for _ in range(self.rows)] for _ in range(self.cols)]
        stack = [(start.x, start.y)]
        prev = {(start.x, start.y): None}

        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        found = False

        while stack and not found:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            x, y = stack.pop()
            current_cell = self.grid[x][y]
            if visited[x][y]:
                continue
            visited[x][y] = True

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows and not visited[nx][ny]:
                    neighbor = self.grid[nx][ny]
                    if not neighbor.is_wall:
                        prev[(nx, ny)] = (x, y)
                        stack.append((nx, ny))

                    if neighbor.is_end:
                        found = True
                        break

            # Draw the maze and grid
            self.draw(screen)
            drawer.draw_grid()

            # Draw the visited cells
            for i in range(self.cols):
                for j in range(self.rows):
                    if visited[i][j]:
                        pygame.draw.rect(screen, PURPLE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            pygame.display.flip()
            clock.tick(60)

        if found:
            path = []
            x, y = end.x, end.y
            while (x, y) != (start.x, start.y):
                path.append((x, y))
                x, y = prev[(x, y)]
            path.reverse()

            for x, y in path:
                pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                self.draw(screen)
                drawer.draw_grid()
                pygame.display.flip()
                clock.tick(60)
        return found
    

    def solve_with_dijkstra(self, screen, clock, drawer):
        start = None
        end = None
        for row in self.grid:
            for cell in row:
                if cell.is_start:
                    start = cell
                if cell.is_end:
                    end = cell

        if not start or not end:
            print("No start or end defined!")
            return False

        visited = [[False for _ in range(self.rows)] for _ in range(self.cols)]
        distances = [[float('inf') for _ in range(self.rows)] for _ in range(self.cols)]
        distances[start.x][start.y] = 0
        prev = {(start.x, start.y): None}

        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        found = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            min_distance = float('inf')
            x, y = -1, -1
            for i in range(self.cols):
                for j in range(self.rows):
                    if not visited[i][j] and distances[i][j] < min_distance:
                        min_distance = distances[i][j]
                        x, y = i, j
            if x == -1:
                break

            visited[x][y] = True
            if self.grid[x][y].is_end:
                found = True
                break

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cols and 0 <= ny < self.rows and not visited[nx][ny] and not self.grid[nx][ny].is_wall:
                    alt = distances[x][y] + 1
                    if alt < distances[nx][ny]:
                        distances[nx][ny] = alt
                        prev[(nx, ny)] = (x, y)

            # Draw the maze and grid
            self.draw(screen)
            drawer.draw_grid()

            # Draw the visited cells
            for i in range(self.cols):
                for j in range(self.rows):
                    if visited[i][j]:
                        pygame.draw.rect(screen, PURPLE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            pygame.display.flip()
            clock.tick(60)

        if found:
            path = []
            x, y = end.x, end.y
            while (x, y) != (start.x, start.y):
                path.append((x, y))
                x, y = prev[(x, y)]
            path.reverse()

            for x, y in path:
                pygame.draw.rect(screen, YELLOW, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                self.draw(screen)
                drawer.draw_grid()
                pygame.display.flip()
                clock.tick(60)
        return found


class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                if self.action:
                    self.action()

class MazeDrawer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Drawer")
        self.clock = pygame.time.Clock()
        self.maze = Maze(GRID_SIZE, GRID_SIZE)
        self.drawing_mode = "wall"
        self.show_algo_buttons = False
        self.showing_path = False
        self.buttons = [
            Button(620, 50, 100, 40, "Wall", WHITE, self.set_wall_mode),
            Button(620, 100, 100, 40, "Start", GREEN, self.set_start_mode),
            Button(620, 150, 100, 40, "End", RED, self.set_end_mode),
            Button(620, 200, 100, 40, "Remove", BLUE, self.remove_walls),
            Button(620, 250, 100, 40, "Solve", YELLOW, self.toggle_algo_buttons),
            Button(620, 300, 100, 40, "BFS", BLUE, self.solve_with_bfs),
            Button(620, 350, 100, 40, "DFS", BLUE, self.solve_with_dfs),
            Button(620, 400, 100, 40, "Dijkstra", BLUE, self.solve_with_dijkstra),
            Button(620, 450, 100, 40, "A*", BLUE, self.solve_with_a_star)
        ]

    def set_wall_mode(self):
        self.drawing_mode = "wall"

    def set_start_mode(self):
        self.drawing_mode = "start"

    def set_end_mode(self):
        self.drawing_mode = "end"

    def remove_walls(self):
        for row in self.maze.grid:
            for cell in row:
                cell.is_wall = False

    def solve_with_bfs(self):
        self.maze.solve_with_bfs(self.screen, self.clock, self)
        self.showing_path = True

    def solve_with_dfs(self):
        self.maze.solve_with_dfs(self.screen, self.clock, self)
        self.showing_path = True

    def solve_with_dijkstra(self):
        self.maze.solve_with_dijkstra(self.screen, self.clock, self)
        self.showing_path = True

    def solve_with_a_star(self):
        pass  # TODO: Implement A*

    def toggle_algo_buttons(self):
        self.show_algo_buttons = not self.show_algo_buttons

    def draw_grid(self):
        for x in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (SCREEN_HEIGHT, y))

    def interpolate_points(self, p1, p2):
        """Return a list of points that interpolate between p1 and p2"""
        points = []
        x1, y1 = p1
        x2, y2 = p2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return points

    def handle_drawing(self, x, y, button, previous_pos=None):
        if x >= SCREEN_HEIGHT:
            return
        col, row = x // CELL_SIZE, y // CELL_SIZE
        cells_to_fill = [(col, row)]

        if previous_pos:
            prev_col, prev_row = previous_pos
            cells_to_fill += self.interpolate_points((prev_col, prev_row), (col, row))

        for c, r in cells_to_fill:
            if button == 1:  # Left mouse button
                if self.drawing_mode == "wall":
                    self.maze.grid[c][r].is_wall = True
                elif self.drawing_mode == "start":
                    for grid_row in self.maze.grid:
                        for cell in grid_row:
                            cell.is_start = False
                    self.maze.grid[c][r].is_start = True
                elif self.drawing_mode == "end":
                    for grid_row in self.maze.grid:
                        for cell in grid_row:
                            cell.is_end = False
                    self.maze.grid[c][r].is_end = True
            elif button == 3:  # Right mouse button
                if self.drawing_mode == "wall":
                    self.maze.grid[c][r].is_wall = False
                elif self.drawing_mode == "start":
                    self.maze.grid[c][r].is_start = False
                elif self.drawing_mode == "end":
                    self.maze.grid[c][r].is_end = False

    def run(self):
        running = True
        previous_mouse_pos = None
        while running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                    if self.showing_path:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.showing_path = False
                            continue
                    buttons = pygame.mouse.get_pressed()
                    if buttons[0] or buttons[2]:
                        mx, my = pygame.mouse.get_pos()
                        if mx < SCREEN_HEIGHT:
                            button = 1 if buttons[0] else 3
                            if previous_mouse_pos:
                                self.handle_drawing(mx, my, button, previous_mouse_pos)
                            else:
                                self.handle_drawing(mx, my, button)
                            previous_mouse_pos = (mx // CELL_SIZE, my // CELL_SIZE)
                else:
                    previous_mouse_pos = None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.handle_event(event)

            self.maze.draw(self.screen)
            self.draw_grid()
            for i, button in enumerate(self.buttons):
                if i <= 4 or self.show_algo_buttons:
                    button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

app = MazeDrawer()
app.run()
