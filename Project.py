import tkinter as tk
import random

class TicTacToe:
    def __init__(self, master):
        self.last_move = None
        self.master = master
        self.master.title("Tic Tac Toe")
        self.ai_mode = "Normal"
        self.ai_difficulty = "Medium"  # Default difficulty
        self.ai_starts = False
        self.move_history = []
        self.memo = {}
        self.create_intro_screen()

    def create_intro_screen(self):
        for w in self.master.winfo_children():
            w.destroy()

        f = tk.Frame(self.master, bg="lightgrey", padx=20, pady=20)
        f.pack(fill=tk.BOTH, expand=True)

        tk.Label(f, text="Welcome to Tic Tac Toe!", font=("Arial", 24, "bold"),
                 fg="black", bg="lightgrey", pady=10).pack()

        instructions = (
            "How to Play:\n"
            "- The game is played on a 3x3 grid.\n"
            "- You are 'X', and the AI is 'O'.\n"
            "- Take turns placing your marker in an empty square.\n"
            "- The goal is to form a line of three markers horizontally, vertically, or diagonally.\n\n"
            "Select Mode:\n"
            "- Normal Mode: AI uses a heuristic-based strategy with varying difficulty levels.\n"
            "- Unbeatable Mode: AI uses the Minimax algorithm to never lose."
        )
        tk.Label(f, text=instructions, font=("Arial", 14),
                 fg="black", bg="lightgrey", justify=tk.LEFT, wraplength=400).pack(pady=10)

        tk.Button(f, text="Normal Mode", font=("Arial", 14), bg="lightblue",
                  command=self.create_normal_mode_selection).pack(pady=5)
        tk.Button(f, text="Unbeatable Mode", font=("Arial", 14), bg="lightblue",
                  command=self.create_unbeatable_mode_start_selection).pack(pady=5)

        # Removed Algorithms button from the home screen

    def create_normal_mode_selection(self):
        for w in self.master.winfo_children():
            w.destroy()
        f = tk.Frame(self.master, bg="lightgrey", padx=20, pady=20)
        f.pack(fill=tk.BOTH, expand=True)

        tk.Label(f, text="Normal Mode - Select Difficulty", font=("Arial", 20, "bold"),
                 fg="black", bg="lightgrey").pack(pady=10)
        for lvl in ["Easy", "Medium", "Hard"]:
            tk.Button(f, text=lvl, font=("Arial", 14), bg="lightgreen",
                      command=lambda l=lvl: self.set_normal_mode_difficulty(l)).pack(pady=5)
        tk.Button(f, text="Back", font=("Arial", 12), bg="grey", fg="white",
                  command=self.create_intro_screen).pack(pady=10)

    def set_normal_mode_difficulty(self, difficulty):
        self.ai_difficulty = difficulty
        self.create_normal_mode_start_selection()

    def create_normal_mode_start_selection(self):
        for w in self.master.winfo_children():
            w.destroy()
        f = tk.Frame(self.master, bg="lightgrey", padx=20, pady=20)
        f.pack(fill=tk.BOTH, expand=True)

        tk.Label(f, text=f"Normal Mode - {self.ai_difficulty} Difficulty",
                 font=("Arial", 20, "bold"), fg="black", bg="lightgrey").pack(pady=10)
        tk.Label(f, text="Who should start first?", font=("Arial", 14),
                 fg="black", bg="lightgrey").pack(pady=10)
        tk.Button(f, text="You Start", font=("Arial", 14), bg="lightblue",
                  command=lambda: self.set_mode_and_start("Normal", False)).pack(pady=5)
        tk.Button(f, text="AI Starts", font=("Arial", 14), bg="lightblue",
                  command=lambda: self.set_mode_and_start("Normal", True)).pack(pady=5)
        tk.Button(f, text="Back", font=("Arial", 12), bg="grey", fg="white",
                  command=self.create_normal_mode_selection).pack(pady=10)

    def create_unbeatable_mode_start_selection(self):
        for w in self.master.winfo_children():
            w.destroy()
        f = tk.Frame(self.master, bg="lightgrey", padx=20, pady=20)
        f.pack(fill=tk.BOTH, expand=True)

        tk.Label(f, text="Unbeatable Mode", font=("Arial", 20, "bold"),
                 fg="black", bg="lightgrey").pack(pady=10)
        tk.Label(f, text="Who should start first?", font=("Arial", 14),
                 fg="black", bg="lightgrey").pack(pady=10)
        tk.Button(f, text="You Start", font=("Arial", 14), bg="lightblue",
                  command=lambda: self.set_mode_and_start("Unbeatable", False)).pack(pady=5)
        tk.Button(f, text="AI Starts", font=("Arial", 14), bg="lightblue",
                  command=lambda: self.set_mode_and_start("Unbeatable", True)).pack(pady=5)
        tk.Button(f, text="Back", font=("Arial", 12), bg="grey", fg="white",
                  command=self.create_intro_screen).pack(pady=10)

    def set_mode_and_start(self, mode, ai_starts):
        self.ai_mode = mode
        self.ai_starts = ai_starts
        self.move_history = []
        self.memo = {}
        self.create_game_board()

    def create_game_board(self):
        # Initialize AI's first move state
        self.ai_first_move_done = False  # This ensures the AI knows whether it has made its first random move.

        self.board = [[None] * 3 for _ in range(3)]
        for w in self.master.winfo_children():
            w.destroy()

        main_frame = tk.Frame(self.master, bg="white")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        g = tk.Frame(main_frame, bg="white")
        g.pack(fill=tk.BOTH, expand=True)

        bf = tk.Frame(g, bg="white")
        bf.pack(pady=10)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                b = tk.Button(bf, text='', font=('Arial', 20), height=2, width=5, bg="lightgrey",
                              command=lambda x=i, y=j: self.player_move(x, y))
                b.grid(row=i, column=j, padx=5, pady=5)
                row.append(b)
            self.buttons.append(row)

        self.status_label = tk.Label(g, text="Your turn!", font=("Arial", 14), bg="white")
        self.status_label.pack(pady=10)

        self.possible_moves_frame = tk.Frame(self.master, bg="white", padx=20)
        self.possible_moves_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        tk.Label(self.possible_moves_frame, text="Possible Moves", font=("Arial", 16), bg="white").pack(pady=10)

        if self.ai_starts:
            self.status_label.config(text="AI is thinking...")
            self.master.after(500, self.ai_move)

    def player_move(self, i, j):
        if self.board[i][j] is None and not self.terminal(self.board):
            self.board[i][j] = "X"
            self.buttons[i][j].config(text="X", state=tk.DISABLED, bg="lightblue")
            self.move_history.append(("Player", i, j))
            self.last_move = (i, j)  # Update the last move

            # Update possible moves right after the move
            self.update_possible_moves()

            if self.terminal(self.board):
                self.end_game()
            else:
                self.status_label.config(text="AI is thinking...")
                self.master.after(500, self.ai_move)

    def ai_move(self):
        if not self.terminal(self.board):
            move = self.normal_ai_move() if self.ai_mode == "Normal" else self.unbeatable_ai_move()
            self.last_move = move  # Store the last move made by the AI

            # Update possible moves right after the AI move
            self.update_possible_moves()

            if self.terminal(self.board):
                self.end_game()
            else:
                self.status_label.config(text="Your turn!")

    # ------------------- NORMAL MODE AI (Heuristic with Difficulty Levels) -------------------
    def normal_ai_move(self):
        move = self.find_heuristic_move()
        if move:
            self.board[move[0]][move[1]] = "O"
            self.buttons[move[0]][move[1]].config(text="O", state=tk.DISABLED, bg="lightcoral")
            self.move_history.append(("AI", move[0], move[1]))
        else:
            # Fallback to random move if no heuristic move found (shouldn't occur)
            self.random_ai_move()

    def find_heuristic_move(self):
        difficulty_probability = {
            "Easy": 0.3,
            "Medium": 0.5,
            "Hard": 0.8
        }
        prob = difficulty_probability[self.ai_difficulty]
        if random.random() > prob:
            return self.random_choice_move()

        # If AI can win in the next move, take it
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "O"
                    if self.winner(self.board) == "O":
                        self.board[i][j] = None
                        return (i, j)
                    self.board[i][j] = None

        #If player can win in the next move, block it
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "X"
                    if self.winner(self.board) == "X":
                        self.board[i][j] = None
                        return (i, j)
                    self.board[i][j] = None

        # Take the center if available
        if self.board[1][1] is None:
            return (1, 1)

        #Take one of the corners if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = []
        for corner in corners:
            row = corner[0]
            column = corner[1]
            if self.board[row][column] is None:
                available_corners.append(corner)

        #Take one of the edges
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_edges = []
        for edge in edges:
            row = edge[0]
            column = edge[1]
            if self.board[row][column] is None:
                available_edges.append(edge)
        if available_edges:
            return random.choice(available_edges)
        return None

    def random_choice_move(self):
        cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]
        return random.choice(cells) if cells else (None, None)

    def random_ai_move(self):
        move = self.random_choice_move()
        if move != (None, None):
            self.board[move[0]][move[1]] = "O"
            self.buttons[move[0]][move[1]].config(text="O", state=tk.DISABLED, bg="lightcoral")
            self.move_history.append(("AI", move[0], move[1]))

    def update_possible_moves(self):
        # Destroy all current widgets in the frame to refresh the list
        for widget in self.possible_moves_frame.winfo_children():
            widget.destroy()

        # Create a label for 'Possible Moves'
        tk.Label(self.possible_moves_frame, text="Possible Moves", font=("Arial", 16), bg="lightblue").pack(pady=10)

        # Iterate through the board and display possible moves
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    move_label = tk.Label(self.possible_moves_frame, text=f"Move to ({i + 1}, {j + 1})",
                                          font=("Arial", 14), bg="white")
                    move_label.pack()

    # ------------------- UNBEATABLE AI (Minimax) -------------------
    def unbeatable_ai_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    self.board[i][j] = "O"
                    sc = self.minimax(self.serialize_board(self.board), False)
                    self.board[i][j] = None
                    if sc > best_score:
                        best_score = sc
                        best_move = (i, j)
        if best_move:
            i, j = best_move
            self.board[i][j] = "O"
            self.buttons[i][j].config(text="O", state=tk.DISABLED, bg="lightcoral")
            self.move_history.append(("AI", i, j))

    def minimax(self, board, maximizing):
        if board in self.memo: return self.memo[board]
        w, _ = self.get_winner_and_line(board)
        if w == "O": return 1
        if w == "X": return -1
        if self.is_board_full(board): return 0

        if maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        nb = [list(r) for r in board]
                        nb[i][j] = "O"
                        sc = self.minimax(self.serialize_board(nb), False)
                        best = max(best, sc)
            self.memo[board] = best
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        nb = [list(r) for r in board]
                        nb[i][j] = "X"
                        sc = self.minimax(self.serialize_board(nb), True)
                        best = min(best, sc)
            self.memo[board] = best
            return best



    # ------------- WINNER DETECTION WITH WINNING LINE -------------
    def get_winner_and_line(self, board):
        lines = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)], [(2, 0), (1, 1), (0, 2)]
        ]
        for line in lines:
            vals = [board[i][j] for (i, j) in line]
            if vals == ["X", "X", "X"]:
                return ("X", line)
            if vals == ["O", "O", "O"]:
                return ("O", line)
        return (None, None)

    def winner(self, b):
        w, _ = self.get_winner_and_line(b)
        return w

    def is_board_full(self, b):
        return all(cell is not None for row in b for cell in row)

    def terminal(self, b):
        return self.winner(b) is not None or self.is_board_full(b)

    def serialize_board(self, b):
        return tuple(tuple(r) for r in b)

    def end_game(self):
        w, line = self.get_winner_and_line(self.board)
        msg = "It's a tie!" if w is None else f"{w} wins!"
        self.status_label.config(text=msg)

        # ---------- HIGHLIGHT THE WINNING LINE ----------
        if w and line:  # There's a winner and we have that line
            for (i, j) in line:
                self.buttons[i][j].config(bg="yellow")

        self.post_game_analysis()

        for row in self.buttons:
            for b in row:
                b.config(state=tk.DISABLED)

        # Create a frame to hold both buttons
        buttons_frame = tk.Frame(self.master)
        buttons_frame.pack(pady=20)

        # Play Again Button
        tk.Button(buttons_frame, text="Play Again", font=("Arial", 14), bg="lightblue",
                  command=self.reset_game).grid(row=0, column=0, padx=10)

        # Algorithms Button
        tk.Button(buttons_frame, text="Algorithms", font=("Arial", 14), bg="lightblue",
                  command=self.create_algorithms_screen).grid(row=0, column=1, padx=10)  # Kept Algorithms button here

    def post_game_analysis(self):
        w = self.winner(self.board)
        txt = ("Game Analysis:\n" + (f"{w} won the game.\n" if w else "It's a tie.\n")
               + "Move History with Feedback:\n")
        for idx, (p, i, j) in enumerate(self.move_history):
            txt += f"{p} moved to ({i + 1}, {j + 1}) - {self.analyze_move(idx)}\n"
        tk.Label(self.master, text=txt, font=("Arial", 12), bg="white", justify=tk.LEFT).pack(pady=10)

    def analyze_move(self, idx):
        if idx < 3:
            return random.choice(["Good start!", "Nice placement!", "Consider the center!"])
        elif idx < 6:
            return random.choice(["You're controlling more space.", "Think combos!", "Strategic move."])
        return random.choice(["Critical moment!", "Watch next move!", "Tight game!"])

    def reset_game(self):
        for w in self.master.winfo_children():
            w.destroy()
        self.create_intro_screen()

    # ------------------ Algorithms Screens ------------------
    def create_algorithms_screen(self):
        for w in self.master.winfo_children():
            w.destroy()

        f = tk.Frame(self.master, bg="lightgrey", padx=20, pady=20)
        f.pack(fill=tk.BOTH, expand=True)

        # Title
        tk.Label(f, text="Algorithm Explanation", font=("Arial", 24, "bold"), fg="black", bg="lightgrey",
                 pady=10).pack()
        # Explanation Content
        if self.ai_mode == "Normal":
            explanation = (
                "Normal Mode Algorithm\n\n"
                "Easy Difficulty:\n"
                "- Behavior: 30% heuristic, 70% random moves.\n"
                "- Effect: Makes the AI less predictable and easier to beat.\n\n"
                "Medium Difficulty:\n"
                "- Behavior: 50% heuristic, 50% random moves.\n"
                "- Effect: Offers a balanced challenge with equal strategy and unpredictability.\n\n"
                "Hard Difficulty:\n"
                "- Behavior: 90% heuristic, 10% random moves.\n"
                "- Effect: Highly strategic and challenging to beat.\n\n"
                "Heuristic Strategy Details:\n"
                "1. Win if Possible: The AI will take a winning move if available.\n"
                "2. Block Opponent's Win: If the player is about to win, the AI blocks their move.\n"
                "3. Center Control: The AI prioritizes taking the center square for strategic advantage.\n"
                "4. Corner Priority: It prefers corners to maximize winning opportunities.\n"
                "5. Fallback to Edges: If no corners are available, edges are selected.\n\n"
                "This adaptive approach ensures that the AI plays intelligently, offering varying levels of challenge."
            )
        elif self.ai_mode == "Unbeatable":
            explanation = (
                "Unbeatable Mode Algorithm\n\n"
                "Minimax Algorithm:\n"
                "- The AI evaluates all possible game outcomes recursively.\n"
                "- Scores are assigned:\n"
                "  - AI Win: +1\n"
                "  - Player Win: -1\n"
                "  - Tie: 0\n"
                "- Ensures optimal moves that maximize the AI's minimum gain.\n\n"
                "Memoization:\n"
                "- Stores previously evaluated board states to speed up calculations and avoid redundant processing.\n\n"
                "Outcome:\n"
                "The Unbeatable AI will always win or force a tie, ensuring it cannot lose."
            )
        else:
            explanation = "Unknown Mode."

        # Display Explanation Text
        tk.Label(f, text=explanation, font=("Arial", 14), fg="black", bg="white", justify=tk.LEFT, wraplength=600,
                 padx=10, pady=10).pack(pady=10)
        # Back Button
        tk.Button(f, text="Return", font=("Arial", 14, "bold"), bg="grey", fg="white", command=self.create_intro_screen
                  ).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()