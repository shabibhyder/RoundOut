import tkinter as tk
from tkinter import messagebox
import math

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        # Add a new node to the end of the circular linked list
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def remove(self, node):
        # Remove a node from the circular linked list
        if self.head == node:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = self.head.next
            self.head = self.head.next
        else:
            temp = self.head
            prev = None
            while temp.next != self.head:
                prev = temp
                temp = temp.next
                if temp == node:
                    prev.next = temp.next

    def get_length(self):
        # Get the length of the circular linked list
        length = 0
        temp = self.head
        while temp:
            length += 1
            temp = temp.next
            if temp == self.head:
                break
        return length

class CountingOutGameGUI:
    def __init__(self, root):
        # Initialize the GUI for the counting-out game
        self.root = root
        self.root.title("Counting Out Game")
        
        # Initialize variables to store values entered by the user
        self.N = tk.IntVar()
        self.K = tk.IntVar()
        
        # Create labels and entry widgets for user input
        self.label_N = tk.Label(root, text="Enter N:")
        self.entry_N = tk.Entry(root, textvariable=self.N)
        self.label_N.pack()
        self.entry_N.pack()
        
        self.label_K = tk.Label(root, text="Enter K:")
        self.entry_K = tk.Entry(root, textvariable=self.K)
        self.label_K.pack()
        self.entry_K.pack()
        
        # Create canvas for displaying players and game status
        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()
        
        # Create text widget for displaying game messages
        self.text_widget = tk.Text(root, height=10, width=40)
        self.text_widget.pack()
        
        # Create buttons for starting and eliminating players from the game
        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack()
        
        self.eliminate_button = tk.Button(root, text="Eliminate", command=self.eliminate_player)
        self.eliminate_button.pack()

        # Initialize variables to store player information
        self.players = None
        self.current_player = None
        self.player_icons = []
        self.player_boxes = []

    def start_game(self):
        # Start the game with user-defined parameters
        n = self.N.get()
        k = self.K.get()
        
        # Validate user input
        if not (1 < n < 12 and k >= 1):
            messagebox.showinfo("Invalid Input", "Allowed values for N: 1 < N < 12, K >= 1")
            return

        # Clear the canvas and create player representations
        self.canvas.delete("all")
        self.players = CircularLinkedList()
        box_width = 30  # Width of the boxes
        box_height = 30  # Height of the boxes
        for i in range(n):
            x = 200 + 150 * math.cos(2 * math.pi * i / n)
            y = 200 + 150 * math.sin(2 * math.pi * i / n)
            player_box = self.canvas.create_rectangle(x - box_width / 2, y - box_height / 2,
                                                       x + box_width / 2, y + box_height / 2,
                                                       outline='black', width=2)
            player_icon = self.canvas.create_text(x, y, text=str(i), font=("Arial", 12))
            self.player_icons.append(player_icon)
            self.player_boxes.append(player_box)
            self.players.append(i)

        # Set the current player to the head of the list
        self.current_player = self.players.head
        self.start_button.config(state="disabled")
        self.text_widget.insert(tk.END, f"Game started. N={n} K={k}\n")

    def eliminate_player(self):
        # Eliminate a player from the game
        if self.players.get_length() == 1:
            winner = self.players.head.data
            messagebox.showinfo("Game Over", f"Winner is Player {winner}")
            self.reset_game()
            return

        # Find the player to be eliminated based on the counting rule
        for _ in range(self.K.get() - 1):
            self.current_player = self.current_player.next

        eliminated_player = self.current_player
        self.current_player = self.current_player.next
        self.players.remove(eliminated_player)
        self.canvas.delete(self.player_icons[eliminated_player.data])
        self.canvas.delete(self.player_boxes[eliminated_player.data])
        self.text_widget.insert(tk.END, f"Player {eliminated_player.data} eliminated.\n")

        # If only one player remains, declare the winner and reset the game
        if self.players.get_length() == 1:
            winner = self.players.head.data
            messagebox.showinfo("Game Over", f"Winner is Player {winner}")
            self.reset_game()

    def reset_game(self):
        # Reset the game 
        self.canvas.delete("all")
        self.player_icons = []
        self.player_boxes = []
        self.players = None
        self.current_player = None
        self.start_button.config(state="normal")
        self.text_widget.delete(1.0, tk.END)

if __name__ == "__main__":
    # Create the main application window and start it.
    root = tk.Tk()
    app = CountingOutGameGUI(root)
    root.mainloop()
