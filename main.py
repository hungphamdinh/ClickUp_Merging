# main.py

import tkinter as tk
from gui.gui import GitMergeToolkitGUI

def main():
    root = tk.Tk()
    app = GitMergeToolkitGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
