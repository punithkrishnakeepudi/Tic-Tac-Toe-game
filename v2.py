import pygame
import sys
import random
import math
from enum import Enum
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOARD_SIZE = 400
CELL_SIZE = BOARD_SIZE // 3
BOARD_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


class GameState(Enum):
    MENU = 1
    MODE_SELECT = 2
    DIFFICULTY_SELECT = 3
    NAME_INPUT = 4
    PLAYING = 5
    GAME_OVER = 6


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Player:
    """Represents a player with name and symbol"""

    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.score = 0


class AI:
    """AI player with different difficulty levels"""

    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.symbol = 'O'

    def get_move(self, board: List[List[str]], player_symbol: str = 'X') -> Tuple[int, int]:
        """Get AI move based on difficulty"""
        if self.difficulty == Difficulty.EASY:
            return self._get_random_move(board)
        elif self.difficulty == Difficulty.MEDIUM:
            return self._get_medium_move(board, player_symbol)
        else:  # HARD
            return self._get_minimax_move(board, player_symbol)

    def _get_random_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Get random available move"""
        available_moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    available_moves.append((i, j))
        return random.choice(available_moves) if available_moves else (0, 0)

    def _get_medium_move(self, board: List[List[str]], player_symbol: str) -> Tuple[int, int]:
        """Medium difficulty: Block player wins, otherwise random"""
        # First, try to block player from winning
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    # Try this move
                    board[i][j] = player_symbol
                    if self._check_winner(board) == player_symbol:
                        board[i][j] = ''  # Undo
                        return (i, j)
                    board[i][j] = ''  # Undo

        # If no blocking needed, make random move
        return self._get_random_move(board)

    def _get_minimax_move(self, board: List[List[str]], player_symbol: str) -> Tuple[int, int]:
        """Hard difficulty: Use minimax algorithm"""
        best_score = -math.inf
        best_move = (0, 0)

        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = self.symbol
                    score = self._minimax(board, 0, False, player_symbol)
                    board[i][j] = ''

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move

    def _minimax(self, board: List[List[str]], depth: int, is_maximizing: bool, player_symbol: str) -> int:
        """Minimax algorithm implementation"""
        winner = self._check_winner(board)

        if winner == self.symbol:
            return 10 - depth
        elif winner == player_symbol:
            return depth - 10
        elif self._is_board_full(board):
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = self.symbol
                        score = self._minimax(board, depth + 1, False, player_symbol)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = player_symbol
                        score = self._minimax(board, depth + 1, True, player_symbol)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def _check_winner(self, board: List[List[str]]) -> Optional[str]:
        """Check if there's a winner"""
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != '':
                return row[0]

        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
                return board[0][col]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
            return board[0][2]

        return None

    def _is_board_full(self, board: List[List[str]]) -> bool:
        """Check if board is full"""
        for row in board:
            for cell in row:
                if cell == '':
                    return False
        return True


class Button:
    """Simple button class for UI"""

    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int] = LIGHT_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
        self.is_hovered = False
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen: pygame.Surface):
        """Draw button on screen"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class InputBox:
    """Input box for player names"""

    def __init__(self, x: int, y: int, width: int, height: int, placeholder: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = ""
        self.placeholder = placeholder
        self.font = pygame.font.Font(None, 24)
        self.active = False

    def handle_event(self, event: pygame.event.Event):
        """Handle input events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen: pygame.Surface):
        """Draw input box"""
        color = LIGHT_GRAY if self.active else WHITE
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        display_text = self.text if self.text else self.placeholder
        text_color = BLACK if self.text else GRAY
        text_surface = self.font.render(display_text, True, text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class GameManager:
    """Main game manager class"""

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.state = GameState.MENU
        self.board = [['', '', ''] for _ in range(3)]
        self.current_player = 'X'
        self.game_mode = None  # 'single' or 'two_player'
        self.difficulty = None
        self.winner = None
        self.winning_line = None

        # Players
        self.player1 = None
        self.player2 = None
        self.ai = None

        # UI Elements
        self.buttons = {}
        self.input_boxes = {}
        self.fonts = {
            'title': pygame.font.Font(None, 48),
            'large': pygame.font.Font(None, 36),
            'medium': pygame.font.Font(None, 24),
            'small': pygame.font.Font(None, 18)
        }

        # Animation
        self.animation_timer = 0
        self.cell_hover = None

        # Sound effects (placeholders - add actual sound files)
        self.sounds = {
            'move': None,  # pygame.mixer.Sound('move.wav')
            'win': None,  # pygame.mixer.Sound('win.wav')
            'click': None  # pygame.mixer.Sound('click.wav')
        }

        self.setup_ui()

    def setup_ui(self):
        """Setup UI elements for different states"""
        # Menu buttons
        self.buttons['start'] = Button(350, 250, 100, 50, "Start Game", GREEN)
        self.buttons['exit'] = Button(350, 320, 100, 50, "Exit", RED)

        # Mode selection buttons
        self.buttons['single'] = Button(300, 200, 200, 50, "Single Player", BLUE)
        self.buttons['two_player'] = Button(300, 270, 200, 50, "Two Player", ORANGE)
        self.buttons['back'] = Button(50, 50, 80, 40, "Back", GRAY)

        # Difficulty buttons
        self.buttons['easy'] = Button(300, 180, 200, 50, "Easy", GREEN)
        self.buttons['medium'] = Button(300, 250, 200, 50, "Medium", YELLOW)
        self.buttons['hard'] = Button(300, 320, 200, 50, "Hard", RED)

        # Game over buttons
        self.buttons['play_again'] = Button(250, 450, 120, 50, "Play Again", GREEN)
        self.buttons['main_menu'] = Button(400, 450, 120, 50, "Main Menu", BLUE)

        # Input boxes
        self.input_boxes['player1'] = InputBox(300, 200, 200, 30, "Player 1 Name")
        self.input_boxes['player2'] = InputBox(300, 250, 200, 30, "Player 2 Name")
        self.input_boxes['single_player'] = InputBox(300, 200, 200, 30, "Your Name")

    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle UI events based on current state
            if self.state == GameState.MENU:
                self.handle_menu_events(event)
            elif self.state == GameState.MODE_SELECT:
                self.handle_mode_select_events(event)
            elif self.state == GameState.DIFFICULTY_SELECT:
                self.handle_difficulty_select_events(event)
            elif self.state == GameState.NAME_INPUT:
                self.handle_name_input_events(event)
            elif self.state == GameState.PLAYING:
                self.handle_game_events(event)
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_events(event)

    def handle_menu_events(self, event):
        """Handle menu events"""
        if self.buttons['start'].handle_event(event):
            self.play_sound('click')
            self.state = GameState.MODE_SELECT
        elif self.buttons['exit'].handle_event(event):
            self.running = False

    def handle_mode_select_events(self, event):
        """Handle mode selection events"""
        if self.buttons['single'].handle_event(event):
            self.play_sound('click')
            self.game_mode = 'single'
            self.state = GameState.DIFFICULTY_SELECT
        elif self.buttons['two_player'].handle_event(event):
            self.play_sound('click')
            self.game_mode = 'two_player'
            self.state = GameState.NAME_INPUT
        elif self.buttons['back'].handle_event(event):
            self.play_sound('click')
            self.state = GameState.MENU

    def handle_difficulty_select_events(self, event):
        """Handle difficulty selection events"""
        if self.buttons['easy'].handle_event(event):
            self.play_sound('click')
            self.difficulty = Difficulty.EASY
            self.state = GameState.NAME_INPUT
        elif self.buttons['medium'].handle_event(event):
            self.play_sound('click')
            self.difficulty = Difficulty.MEDIUM
            self.state = GameState.NAME_INPUT
        elif self.buttons['hard'].handle_event(event):
            self.play_sound('click')
            self.difficulty = Difficulty.HARD
            self.state = GameState.NAME_INPUT
        elif self.buttons['back'].handle_event(event):
            self.play_sound('click')
            self.state = GameState.MODE_SELECT

    def handle_name_input_events(self, event):
        """Handle name input events"""
        if self.game_mode == 'single':
            self.input_boxes['single_player'].handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.input_boxes['single_player'].text.strip():
                    self.start_single_player_game()
        else:
            self.input_boxes['player1'].handle_event(event)
            self.input_boxes['player2'].handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if (self.input_boxes['player1'].text.strip() and
                        self.input_boxes['player2'].text.strip()):
                    self.start_two_player_game()

        if self.buttons['back'].handle_event(event):
            self.play_sound('click')
            if self.game_mode == 'single':
                self.state = GameState.DIFFICULTY_SELECT
            else:
                self.state = GameState.MODE_SELECT

    def handle_game_events(self, event):
        """Handle game playing events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.winner is None:
                self.handle_board_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_board_hover(event.pos)

    def handle_game_over_events(self, event):
        """Handle game over events"""
        if self.buttons['play_again'].handle_event(event):
            self.play_sound('click')
            self.reset_game()
        elif self.buttons['main_menu'].handle_event(event):
            self.play_sound('click')
            self.reset_to_menu()

    def handle_board_click(self, pos: Tuple[int, int]):
        """Handle clicks on the game board"""
        x, y = pos
        if BOARD_X <= x <= BOARD_X + BOARD_SIZE and BOARD_Y <= y <= BOARD_Y + BOARD_SIZE:
            col = (x - BOARD_X) // CELL_SIZE
            row = (y - BOARD_Y) // CELL_SIZE

            if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '':
                self.make_move(row, col)

    def handle_board_hover(self, pos: Tuple[int, int]):
        """Handle mouse hover over board"""
        x, y = pos
        if BOARD_X <= x <= BOARD_X + BOARD_SIZE and BOARD_Y <= y <= BOARD_Y + BOARD_SIZE:
            col = (x - BOARD_X) // CELL_SIZE
            row = (y - BOARD_Y) // CELL_SIZE
            if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '':
                self.cell_hover = (row, col)
            else:
                self.cell_hover = None
        else:
            self.cell_hover = None

    def make_move(self, row: int, col: int):
        """Make a move on the board"""
        if self.board[row][col] == '' and self.winner is None:
            self.board[row][col] = self.current_player
            self.play_sound('move')

            # Check for winner
            self.check_game_over()

            if self.winner is None:
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'

                # AI move if single player mode
                if self.game_mode == 'single' and self.current_player == 'O':
                    self.make_ai_move()

    def make_ai_move(self):
        """Make AI move"""
        if self.ai and self.winner is None:
            row, col = self.ai.get_move(self.board)
            pygame.time.wait(500)  # Small delay for better UX
            self.board[row][col] = 'O'
            self.play_sound('move')
            self.check_game_over()
            if self.winner is None:
                self.current_player = 'X'

    def check_game_over(self):
        """Check if game is over"""
        # Check rows
        for i, row in enumerate(self.board):
            if row[0] == row[1] == row[2] and row[0] != '':
                self.winner = row[0]
                self.winning_line = ('row', i)
                self.handle_game_end()
                return

        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] and self.board[0][j] != '':
                self.winner = self.board[0][j]
                self.winning_line = ('col', j)
                self.handle_game_end()
                return

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '':
            self.winner = self.board[0][0]
            self.winning_line = ('diag', 0)
            self.handle_game_end()
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '':
            self.winner = self.board[0][2]
            self.winning_line = ('diag', 1)
            self.handle_game_end()
            return

        # Check for draw
        if all(self.board[i][j] != '' for i in range(3) for j in range(3)):
            self.winner = 'Draw'
            self.handle_game_end()

    def handle_game_end(self):
        """Handle game end"""
        self.play_sound('win')

        # Update scores
        if self.winner == 'X':
            self.player1.score += 1
        elif self.winner == 'O':
            if self.game_mode == 'single':
                pass  # AI doesn't need score
            else:
                self.player2.score += 1

        self.state = GameState.GAME_OVER

    def start_single_player_game(self):
        """Start single player game"""
        name = self.input_boxes['single_player'].text.strip()
        self.player1 = Player(name, 'X')
        self.ai = AI(self.difficulty)
        self.state = GameState.PLAYING
        self.current_player = 'X'

    def start_two_player_game(self):
        """Start two player game"""
        name1 = self.input_boxes['player1'].text.strip()
        name2 = self.input_boxes['player2'].text.strip()
        self.player1 = Player(name1, 'X')
        self.player2 = Player(name2, 'O')
        self.state = GameState.PLAYING
        self.current_player = 'X'

    def reset_game(self):
        """Reset game for new round"""
        self.board = [['', '', ''] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.winning_line = None
        self.state = GameState.PLAYING

    def reset_to_menu(self):
        """Reset to main menu"""
        self.reset_game()
        self.state = GameState.MENU
        self.game_mode = None
        self.difficulty = None
        self.player1 = None
        self.player2 = None
        self.ai = None

        # Clear input boxes
        for input_box in self.input_boxes.values():
            input_box.text = ""

    def play_sound(self, sound_name: str):
        """Play sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

    def draw(self):
        """Main draw method"""
        self.screen.fill(WHITE)

        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.MODE_SELECT:
            self.draw_mode_select()
        elif self.state == GameState.DIFFICULTY_SELECT:
            self.draw_difficulty_select()
        elif self.state == GameState.NAME_INPUT:
            self.draw_name_input()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        """Draw main menu"""
        title = self.fonts['title'].render("Tic-Tac-Toe", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        self.buttons['start'].draw(self.screen)
        self.buttons['exit'].draw(self.screen)

    def draw_mode_select(self):
        """Draw mode selection screen"""
        title = self.fonts['large'].render("Select Game Mode", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        self.buttons['single'].draw(self.screen)
        self.buttons['two_player'].draw(self.screen)
        self.buttons['back'].draw(self.screen)

    def draw_difficulty_select(self):
        """Draw difficulty selection screen"""
        title = self.fonts['large'].render("Select Difficulty", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        self.buttons['easy'].draw(self.screen)
        self.buttons['medium'].draw(self.screen)
        self.buttons['hard'].draw(self.screen)
        self.buttons['back'].draw(self.screen)

    def draw_name_input(self):
        """Draw name input screen"""
        if self.game_mode == 'single':
            title = self.fonts['large'].render("Enter Your Name", True, BLACK)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
            self.screen.blit(title, title_rect)

            self.input_boxes['single_player'].draw(self.screen)

            instruction = self.fonts['medium'].render("Press Enter to start", True, GRAY)
            instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, 280))
            self.screen.blit(instruction, instruction_rect)
        else:
            title = self.fonts['large'].render("Enter Player Names", True, BLACK)
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
            self.screen.blit(title, title_rect)

            self.input_boxes['player1'].draw(self.screen)
            self.input_boxes['player2'].draw(self.screen)

            instruction = self.fonts['medium'].render("Press Enter to start", True, GRAY)
            instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, 320))
            self.screen.blit(instruction, instruction_rect)

        self.buttons['back'].draw(self.screen)

    def draw_game(self):
        """Draw game screen"""
        # Draw title
        title = self.fonts['large'].render("Tic-Tac-Toe", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)

        # Draw current turn
        if self.winner is None:
            if self.current_player == 'X':
                current_text = f"{self.player1.name}'s Turn (X)"
            else:
                if self.game_mode == 'single':
                    current_text = "AI's Turn (O)"
                else:
                    current_text = f"{self.player2.name}'s Turn (O)"

            turn_surface = self.fonts['medium'].render(current_text, True, BLACK)
            turn_rect = turn_surface.get_rect(center=(WINDOW_WIDTH // 2, 70))
            self.screen.blit(turn_surface, turn_rect)

        # Draw board
        self.draw_board()

        # Draw scores
        self.draw_scores()

    def draw_board(self):
        """Draw the game board"""
        # Draw grid lines
        for i in range(1, 3):
            # Vertical lines
            pygame.draw.line(self.screen, BLACK,
                             (BOARD_X + i * CELL_SIZE, BOARD_Y),
                             (BOARD_X + i * CELL_SIZE, BOARD_Y + BOARD_SIZE), 3)
            # Horizontal lines
            pygame.draw.line(self.screen, BLACK,
                             (BOARD_X, BOARD_Y + i * CELL_SIZE),
                             (BOARD_X + BOARD_SIZE, BOARD_Y + i * CELL_SIZE), 3)

        # Draw board border
        pygame.draw.rect(self.screen, BLACK, (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE), 3)

        # Draw hover effect
        if self.cell_hover and self.winner is None:
            row, col = self.cell_hover
            hover_rect = pygame.Rect(BOARD_X + col * CELL_SIZE + 2,
                                     BOARD_Y + row * CELL_SIZE + 2,
                                     CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(self.screen, LIGHT_GRAY, hover_rect)

        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                if self.board[row][col] != '':
                    self.draw_symbol(row, col, self.board[row][col])

        # Draw winning line
        if self.winning_line:
            self.draw_winning_line()

    def draw_symbol(self, row: int, col: int, symbol: str):
        """Draw X or O symbol"""
        center_x = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
        center_y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

        if symbol == 'X':
            # Draw X
            margin = 30
            pygame.draw.line(self.screen, RED,
                             (center_x - margin, center_y - margin),
                             (center_x + margin, center_y + margin), 8)
            pygame.draw.line(self.screen, RED,
                             (center_x + margin, center_y - margin),
                             (center_x - margin, center_y + margin), 8)
        elif symbol == 'O':
            # Draw O
            pygame.draw.circle(self.screen, BLUE, (center_x, center_y), 40, 8)

    def draw_winning_line(self):
        """Draw winning line animation"""
        if not self.winning_line:
            return

        # Animate winning line with pulsing effect
        self.animation_timer += 1
        alpha = int(128 + 127 * math.sin(self.animation_timer * 0.1))
        color = (*GREEN, alpha) if self.animation_timer % 60 < 30 else (*YELLOW, alpha)

        line_type, index = self.winning_line

        if line_type == 'row':
            start_x = BOARD_X + 10
            end_x = BOARD_X + BOARD_SIZE - 10
            y = BOARD_Y + index * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.line(self.screen, color[:3], (start_x, y), (end_x, y), 6)

        elif line_type == 'col':
            x = BOARD_X + index * CELL_SIZE + CELL_SIZE // 2
            start_y = BOARD_Y + 10
            end_y = BOARD_Y + BOARD_SIZE - 10
            pygame.draw.line(self.screen, color[:3], (x, start_y), (x, end_y), 6)

        elif line_type == 'diag':
            if index == 0:  # Main diagonal
                start_pos = (BOARD_X + 10, BOARD_Y + 10)
                end_pos = (BOARD_X + BOARD_SIZE - 10, BOARD_Y + BOARD_SIZE - 10)
            else:  # Anti-diagonal
                start_pos = (BOARD_X + BOARD_SIZE - 10, BOARD_Y + 10)
                end_pos = (BOARD_X + 10, BOARD_Y + BOARD_SIZE - 10)
            pygame.draw.line(self.screen, color[:3], start_pos, end_pos, 6)

    def draw_scores(self):
        """Draw player scores"""
        if not self.player1:
            return

        # Player 1 score
        score_text = f"{self.player1.name}: {self.player1.score}"
        score_surface = self.fonts['medium'].render(score_text, True, BLACK)
        self.screen.blit(score_surface, (50, 150))

        # Player 2 or AI score
        if self.game_mode == 'two_player' and self.player2:
            score_text = f"{self.player2.name}: {self.player2.score}"
            score_surface = self.fonts['medium'].render(score_text, True, BLACK)
            self.screen.blit(score_surface, (50, 180))
        elif self.game_mode == 'single':
            ai_wins = sum(1 for _ in range(10)) - self.player1.score  # Placeholder for AI wins
            score_text = f"AI: {ai_wins if ai_wins > 0 else 0}"
            score_surface = self.fonts['medium'].render(score_text, True, BLACK)
            self.screen.blit(score_surface, (50, 180))

    def draw_game_over(self):
        """Draw game over screen"""
        # Draw the game board in background
        self.draw_game()

        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Draw result text
        if self.winner == 'Draw':
            result_text = "It's a Draw!"
            color = ORANGE
        elif self.winner == 'X':
            result_text = f"{self.player1.name} Wins!"
            color = GREEN
        else:  # winner == 'O'
            if self.game_mode == 'single':
                result_text = "AI Wins!"
            else:
                result_text = f"{self.player2.name} Wins!"
            color = GREEN

        result_surface = self.fonts['large'].render(result_text, True, color)
        result_rect = result_surface.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(result_surface, result_rect)

        # Draw final scores
        if self.game_mode == 'two_player':
            score_text = f"{self.player1.name}: {self.player1.score}  |  {self.player2.name}: {self.player2.score}"
        else:
            ai_score = 0  # Placeholder - you might want to track this
            score_text = f"{self.player1.name}: {self.player1.score}  |  AI: {ai_score}"

        score_surface = self.fonts['medium'].render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, 350))
        self.screen.blit(score_surface, score_rect)

        # Draw buttons
        self.buttons['play_again'].draw(self.screen)
        self.buttons['main_menu'].draw(self.screen)

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def main():
    """Main function to start the game"""
    try:
        game = GameManager()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()