from ui.nsk_roster_app import NSKRosterApp
import tkinter as tk
from ttkbootstrap import Style

if __name__ == "__main__":
    root = tk.Tk()
    style = Style(theme="darkly")
    app = NSKRosterApp(root)
    root.mainloop()
