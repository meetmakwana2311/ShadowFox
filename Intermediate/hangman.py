import tkinter as tk
from tkinter import messagebox, font
import random
import string
import threading
import time

class HangmanGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hangman Game")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Game variables
        self.words_with_hints = {
            'PYTHON': 'A popular programming language named after a snake',
            'COMPUTER': 'Electronic device used for processing data',
            'HANGMAN': 'The name of this word guessing game',
            'KEYBOARD': 'Input device with keys for typing',
            'PROGRAMMING': 'The process of creating computer software',
            'ALGORITHM': 'Step-by-step procedure for solving a problem',
            'DATABASE': 'Organized collection of structured information',
            'INTERNET': 'Global network connecting millions of computers',
            'SOFTWARE': 'Programs and applications that run on computers',
            'HARDWARE': 'Physical components of a computer system',
            'ARTIFICIAL': 'Made by humans rather than occurring naturally',
            'INTELLIGENCE': 'The ability to acquire and apply knowledge',
            'MACHINE': 'Device that performs work using power',
            'LEARNING': 'The process of acquiring new knowledge or skills',
            'NETWORK': 'System of interconnected computers or devices',
            'DEVELOPER': 'Person who creates software applications',
            'FRAMEWORK': 'Platform for developing software applications',
            'DEBUGGING': 'Process of finding and fixing bugs in code',
            'VARIABLE': 'Storage location with an associated name',
            'FUNCTION': 'Block of code designed to perform a task'
        }
        
        self.word = ""
        self.hint = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 7  # Classic hangman with 7 stages
        
        # Classic 7-stage hangman progression
        self.hangman_stages = [
            "",  # 0 wrong guesses
            # 1. Gallows
            "  +-------+\n  |       |\n  |        \n  |        \n  |        \n  |        \n  |        \n===========",  # 1
            # 2. Head
            "  +-------+\n  |       |\n  |       O\n  |        \n  |        \n  |        \n  |        \n===========",  # 2
            # 3. Body
            "  +-------+\n  |       |\n  |       O\n  |       |\n  |       |\n  |        \n  |        \n===========",  # 3
            # 4. Left arm
            "  +-------+\n  |       |\n  |       O\n  |      /|\n  |       |\n  |        \n  |        \n===========",  # 4
            # 5. Right arm
            "  +-------+\n  |       |\n  |       O\n  |      /|\\\n  |       |\n  |        \n  |        \n===========",  # 5
            # 6. Left leg
            "  +-------+\n  |       |\n  |       O\n  |      /|\\\n  |       |\n  |      / \n  |        \n===========",  # 6
            # 7. Right leg (Game Over)
            "  +-------+\n  |       |\n  |       O\n  |      /|\\\n  |       |\n  |      / \\\n  |    DEAD!\n===========",  # 7
        ]
        
        # Falling hangman animation stages
        self.falling_stages = [
            "  +-------+\n  |       |\n  |        \n  |       O\n  |      /|\\\n  |      / \\\n  |    DEAD!\n===========",
            "  +-------+\n  |       |\n  |        \n  |        \n  |       O\n  |      /|\\\n  |    DEAD!\n===========",
            "  +-------+\n  |       |\n  |        \n  |        \n  |        \n  |       O\n  |    DEAD!\n===========",
            "  +-------+\n  |       |\n  |        \n  |        \n  |        \n  |        \n  |   O DEAD!\n==========="
        ]
        
        self.celebration_active = False
        self.game_over = False
        self.setup_ui()
        self.new_game()
        
    def setup_ui(self):
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg='#16213e', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_font = font.Font(family="Arial", size=32, weight="bold")
        title_label = tk.Label(header_frame, text=" HANGMAN CHAMPION ", font=title_font, 
                              bg='#16213e', fg='#00ff88')
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left panel for hangman
        left_panel = tk.Frame(main_container, bg='#0f1419', relief='raised', bd=3)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Hangman title
        hangman_title = tk.Label(left_panel, text=" GALLOWS", font=("Arial", 16, "bold"),
                                bg='#0f1419', fg='#ff6b6b')
        hangman_title.pack(pady=10)
        
        # Hangman display with larger size and better alignment
        hangman_font = font.Font(family="Courier", size=16, weight="bold")
        self.hangman_label = tk.Label(left_panel, text="", font=hangman_font, 
                                     bg='#0f1419', fg='#ff6b6b', justify='left')
        self.hangman_label.pack(expand=True, pady=20)
        
        # Wrong guesses display
        self.wrong_label = tk.Label(left_panel, text="", font=("Arial", 14, "bold"), 
                                   bg='#0f1419', fg='#ff4757')
        self.wrong_label.pack(pady=10)
        
        # Right panel for game
        right_panel = tk.Frame(main_container, bg='#0f1419', relief='raised', bd=3)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Word section
        word_section = tk.Frame(right_panel, bg='#0f1419')
        word_section.pack(fill='x', pady=20, padx=20)
        
        word_title = tk.Label(word_section, text="🔤 MYSTERY WORD", font=("Arial", 16, "bold"),
                             bg='#0f1419', fg='#4834d4')
        word_title.pack()
        
        # Much larger word display
        word_font = font.Font(family="Arial", size=28, weight="bold")
        self.word_label = tk.Label(word_section, text="", font=word_font, 
                                  bg='#0f1419', fg='#00d2d3', pady=15)
        self.word_label.pack()
        
        # Hint section
        hint_section = tk.Frame(right_panel, bg='#2c2c54', relief='sunken', bd=2)
        hint_section.pack(fill='x', pady=10, padx=20)
        
        hint_title = tk.Label(hint_section, text=" HINT", font=("Arial", 14, "bold"),
                             bg='#2c2c54', fg='#ffa502')
        hint_title.pack(pady=5)
        
        self.hint_label = tk.Label(hint_section, text="", font=("Arial", 12), 
                                  bg='#2c2c54', fg='#f1f2f6', wraplength=350, pady=10)
        self.hint_label.pack()
        
        # Guessed letters section
        guessed_section = tk.Frame(right_panel, bg='#0f1419')
        guessed_section.pack(fill='x', pady=10, padx=20)
        
        self.guessed_label = tk.Label(guessed_section, text="", font=("Arial", 12), 
                                     bg='#0f1419', fg='#a4b0be', wraplength=350)
        self.guessed_label.pack()
        
        # Input section
        input_section = tk.Frame(right_panel, bg='#0f1419')
        input_section.pack(pady=20)
        
        input_label = tk.Label(input_section, text=" Enter your guess:", 
                              font=("Arial", 14, "bold"), bg='#0f1419', fg='#f1f2f6')
        input_label.pack()
        
        self.entry = tk.Entry(input_section, font=("Arial", 18), width=8, justify='center',
                             bg='#2f3542', fg='#f1f2f6', insertbackground='#00d2d3',
                             relief='flat', bd=5)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda e: self.make_guess())
        
        # Buttons
        buttons_frame = tk.Frame(right_panel, bg='#0f1419')
        buttons_frame.pack(pady=15)
        
        guess_btn = tk.Button(buttons_frame, text=" GUESS", command=self.make_guess,
                             bg='#00d2d3', fg='#0f1419', font=("Arial", 14, "bold"), 
                             width=12, height=2, relief='flat', cursor='hand2')
        guess_btn.pack(side='left', padx=10)
        
        new_game_btn = tk.Button(buttons_frame, text="🔄 NEW GAME", command=self.new_game,
                                bg='#5f27cd', fg='white', font=("Arial", 14, "bold"), 
                                width=12, height=2, relief='flat', cursor='hand2')
        new_game_btn.pack(side='left', padx=10)
        
        # Alphabet section
        alphabet_frame = tk.Frame(self.root, bg='#1a1a2e')
        alphabet_frame.pack(pady=20)
        
        alphabet_title = tk.Label(alphabet_frame, text="🔤 ALPHABET BOARD", 
                                 font=("Arial", 16, "bold"), bg='#1a1a2e', fg='#00ff88')
        alphabet_title.pack(pady=10)
        
        # Create alphabet buttons with better styling
        self.letter_buttons = {}
        letters_container = tk.Frame(alphabet_frame, bg='#1a1a2e')
        letters_container.pack()
        
        # First row: A-M
        row1_frame = tk.Frame(letters_container, bg='#1a1a2e')
        row1_frame.pack(pady=5)
        for letter in 'ABCDEFGHIJKLM':
            btn = tk.Button(row1_frame, text=letter, width=4, height=2,
                           command=lambda l=letter: self.guess_letter(l),
                           bg='#2f3542', fg='#f1f2f6', font=("Arial", 12, "bold"),
                           relief='flat', cursor='hand2',
                           activebackground='#57606f', activeforeground='white')
            btn.pack(side='left', padx=2, pady=2)
            self.letter_buttons[letter] = btn
        
        # Second row: N-Z
        row2_frame = tk.Frame(letters_container, bg='#1a1a2e')
        row2_frame.pack(pady=5)
        for letter in 'NOPQRSTUVWXYZ':
            btn = tk.Button(row2_frame, text=letter, width=4, height=2,
                           command=lambda l=letter: self.guess_letter(l),
                           bg='#2f3542', fg='#f1f2f6', font=("Arial", 12, "bold"),
                           relief='flat', cursor='hand2',
                           activebackground='#57606f', activeforeground='white')
            btn.pack(side='left', padx=2, pady=2)
            self.letter_buttons[letter] = btn
            
    def new_game(self):
        """Start a new game"""
        word_hint_pair = random.choice(list(self.words_with_hints.items()))
        self.word = word_hint_pair[0]
        self.hint = word_hint_pair[1]
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.celebration_active = False
        self.game_over = False
        
        # Reset alphabet buttons
        for btn in self.letter_buttons.values():
            btn.configure(state='normal', bg='#2f3542', fg='#f1f2f6')
        
        self.update_display()
        self.entry.focus()
        
    def make_guess(self):
        """Process a guess from the entry field"""
        guess = self.entry.get().upper().strip()
        self.entry.delete(0, tk.END)
        
        if len(guess) != 1 or guess not in string.ascii_uppercase:
            self.show_custom_message(" Invalid Input", "Please enter a single letter!", "warning")
            return
        
        self.guess_letter(guess)
        
    def guess_letter(self, letter):
        """Process a letter guess"""
        if letter in self.guessed_letters:
            self.show_custom_message(" Already Guessed", f"You already guessed '{letter}'!", "info")
            return
        
        self.guessed_letters.add(letter)
        
        # Update button appearance
        if letter in self.letter_buttons:
            if letter in self.word:
                self.letter_buttons[letter].configure(state='disabled', bg='#2ed573', fg='white')
            else:
                self.letter_buttons[letter].configure(state='disabled', bg='#ff4757', fg='white')
        
        if letter not in self.word:
            self.wrong_guesses += 1
        
        self.update_display()
        self.check_game_status()
        
    def update_display(self):
        """Update all display elements"""
        # Update word display with spacing
        display_word = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                display_word += letter + "  "
            else:
                display_word += "_  "
        self.word_label.config(text=display_word.strip())
        
        # Update hint
        self.hint_label.config(text=self.hint)
        
        # Update wrong guesses counter
        remaining = self.max_wrong_guesses - self.wrong_guesses
        self.wrong_label.config(text=f" Wrong: {self.wrong_guesses}/{self.max_wrong_guesses}\n Lives: {remaining}")
        
        # Update hangman drawing
        stage_index = min(self.wrong_guesses, len(self.hangman_stages) - 1)
        self.hangman_label.config(text=self.hangman_stages[stage_index])
        
        # Update guessed letters
        if self.guessed_letters:
            correct_letters = [l for l in sorted(self.guessed_letters) if l in self.word]
            wrong_letters = [l for l in sorted(self.guessed_letters) if l not in self.word]
            
            display_text = ""
            if correct_letters:
                display_text += f" Correct: {', '.join(correct_letters)}"
            if wrong_letters:
                if display_text:
                    display_text += "\n"
                display_text += f" Wrong: {', '.join(wrong_letters)}"
            
            self.guessed_label.config(text=display_text)
        else:
            self.guessed_label.config(text="")
            
    def check_game_status(self):
        """Check if the game is won or lost"""
        if self.game_over:
            return
            
        # Check win condition
        if all(letter in self.guessed_letters for letter in self.word):
            self.game_over = True
            if self.wrong_guesses == 0:
                # Perfect game - trigger celebration
                self.show_celebration()
                self.show_custom_message(" PERFECT VICTORY!", 
                                       f"INCREDIBLE! You guessed '{self.word}' with NO wrong guesses!\n\n"
                                       f" Perfect Score: 100%\n You are a Hangman CHAMPION!", 
                                       "celebration")
            else:
                self.show_custom_message(" Victory!", 
                                       f"Congratulations! You won!\n\n"
                                       f"Word: {self.word}\n"
                                       f"Wrong guesses: {self.wrong_guesses}/{self.max_wrong_guesses}\n"
                                       f"Score: {((self.max_wrong_guesses - self.wrong_guesses) / self.max_wrong_guesses * 100):.0f}%", 
                                       "success")
            self.disable_all_buttons()
            # Auto start new game after 3 seconds
            self.root.after(3000, self.new_game)
            
        # Check lose condition
        elif self.wrong_guesses >= self.max_wrong_guesses:
            self.game_over = True
            self.disable_all_buttons()
            # Show falling animation first
            self.show_falling_hangman()
            # Then show game over message and start new game
            self.root.after(2000, lambda: self.show_game_over_and_restart())
    
    def show_celebration(self):
        """Show celebration animation for perfect games"""
        self.celebration_active = True
        
        def animate_celebration():
            colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7', '#a55eea']
            original_bg = self.root.cget('bg')
            
            for _ in range(15):  # Flash for 3 seconds
                if not self.celebration_active:
                    break
                color = random.choice(colors)
                self.root.configure(bg=color)
                self.root.update()
                time.sleep(0.2)
                self.root.configure(bg=original_bg)
                self.root.update()
                time.sleep(0.2)
            
            self.root.configure(bg=original_bg)
        
        # Run celebration in a separate thread
        celebration_thread = threading.Thread(target=animate_celebration)
        celebration_thread.daemon = True
        celebration_thread.start()
    
    def show_falling_hangman(self):
        """Animate the hangman falling down"""
        def animate_fall():
            for stage in self.falling_stages:
                if self.game_over:  # Only animate if game is still over
                    self.hangman_label.config(text=stage)
                    self.root.update()
                    time.sleep(0.5)
        
        # Run falling animation in a separate thread
        fall_thread = threading.Thread(target=animate_fall)
        fall_thread.daemon = True
        fall_thread.start()
    
    def show_game_over_and_restart(self):
        """Show game over message and restart"""
        if self.game_over:  # Only show if game is still over
            self.show_custom_message(" Game Over!", 
                                   f"The hangman fell down!\n\n"
                                   f"The word was: {self.word}\n"
                                   f"Starting new game... ", 
                                   "failure")
            # Auto start new game after message
            self.root.after(1000, self.new_game)
    
    def show_custom_message(self, title, message, msg_type):
        """Show custom styled message boxes"""
        if msg_type == "celebration":
            messagebox.showinfo(title, message)
        elif msg_type == "success":
            messagebox.showinfo(title, message)
        elif msg_type == "failure":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
            
    def disable_all_buttons(self):
        """Disable all letter buttons"""
        for btn in self.letter_buttons.values():
            btn.configure(state='disabled')
        self.celebration_active = False
            
    def run(self):
        """Start the game"""
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = HangmanGame()
    game.run()