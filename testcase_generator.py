import tkinter as tk
import numpy as np

class MatrixGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = np.zeros((rows, cols), dtype=int)
        
        self.root = tk.Tk()
        self.root.title("Matrix Generator")
        self.output = "output_1"
        
        self.buttons = []
        for i in range(rows):
            row_buttons = []
            for j in range(cols):
                button = tk.Button(self.root, text="", width=2, height=1,
                                   command=lambda x=i, y=j: self.toggle_block(x, y))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        
        generate_button = tk.Button(self.root, text="Generate Matrix", command=self.generate_matrix)
        quit_button = tk.Button(self.root, text="Reset", command=self.reset)
        generate_button.grid(row=rows, columnspan=cols)
        quit_button.grid(row=rows+1, columnspan=cols + 1)
    
    def toggle_block(self, row, col):
        if self.matrix[row, col] == 0:
            self.matrix[row, col] = -1
            self.buttons[row][col].config(bg="black")
        else:
            self.matrix[row, col] = 0
            self.buttons[row][col].config(bg="white")
    
    def generate_matrix(self):
        with open(self.output + '.txt', 'w') as f:
            f.write(f"{self.rows} {self.cols} inf inf\n")
            for i in range (self.rows):
                for j in range (self.cols):
                    f.write(str(self.matrix[i][j]))
                    f.write(" ")
                f.write("\n")
                
        self.output = self.output[:-1] + str(int(self.output[-1])+1)
        
    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i, j] = 0    
                self.buttons[i][j].config(bg="white")
                
    def run(self):
        self.root.mainloop()
        
def main():
    generator = MatrixGenerator(20, 20)
    generator.run()
    
if __name__ == '__main__':
    main()