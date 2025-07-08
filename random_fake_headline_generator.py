import random
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from fpdf import FPDF

class FakeHeadlineGenerator:
    def __init__(self):
        self.subjects = {
            "Politics": ["Prime Minister", "Opposition Leader", "Rickshaw Drivers", "Group of monkeys"],
            "Entertainment": ["Ali Zafar", "Mahira Sharma", "Sara", "Babar Azam"],
            "Food": ["Hungry Kid", "MasterChef", "Samosa Vendor", "Burger Lover"]
        }
        self.actions = ["Launches", "Dances with", "Eats", "Sings to", "Cancels", "Declares war on",
                        "Orders", "Celebrates", "Wishes", "Blames"]
        self.places_things = ["Quaid-e-Azam Mausoleum", "Shahrah-e-Faisal", "Plate of samosas", 
                              "Burger", "Hat", "Courtroom", "Cricket Stadium", "University Canteen"]
        self.history = []
        self.favorites = []

    def generate_headline(self, category=None):
        category = category or random.choice(list(self.subjects.keys()))
        subject = random.choice(self.subjects[category])
        action = random.choice(self.actions)
        place_thing = random.choice(self.places_things)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headline = f"[{timestamp}] Breaking News: {subject} {action} {place_thing}"
        self.history.append({"timestamp": timestamp, "category": category, "headline": headline})
        return headline

    def save_history_txt(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for item in self.history:
                f.write(item["headline"] + "\n")

    def save_history_pdf(self, path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Generated Headlines", ln=True, align='C')
        pdf.ln(10)
        for item in self.history:
            pdf.multi_cell(0, 10, item["headline"])
        pdf.output(path)

    def save_history_json(self, path="headline_history.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)

class FakeHeadlineApp:
    def __init__(self, root):
        self.generator = FakeHeadlineGenerator()
        self.root = root
        self.root.title("Pro Fake Headline Generator")
        self.root.geometry("800x600")

        # Theme colors
        self.light_mode = {"bg": "#f0f0f0", "fg": "#000000", "text_bg": "#ffffff", "text_fg": "#000000"}
        self.dark_mode = {"bg": "#2d2d2d", "fg": "#ffffff", "text_bg": "#1e1e1e", "text_fg": "#ffffff"}
        self.current_theme = self.light_mode

        self.setup_ui()

    def setup_ui(self):
        self.theme_var = tk.BooleanVar()
        theme_check = tk.Checkbutton(self.root, text="Dark Mode", variable=self.theme_var, command=self.toggle_theme)
        theme_check.pack(pady=3)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        self.setup_main_tab()
        self.setup_favorites_tab()
        self.setup_search_tab()
        self.apply_theme()

    def setup_main_tab(self):
        self.tab_main = tk.Frame(self.notebook)
        self.notebook.add(self.tab_main, text="📰 Headlines")

        top = tk.Frame(self.tab_main)
        top.pack(pady=5)

        tk.Label(top, text="Category:").grid(row=0, column=0, padx=5)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(top, textvariable=self.category_var, state="readonly",
                                              values=["Any", "Politics", "Entertainment", "Food"])
        self.category_dropdown.set("Any")
        self.category_dropdown.grid(row=0, column=1)

        tk.Label(top, text="Count:").grid(row=0, column=2, padx=5)
        self.count_entry = tk.Entry(top, width=5)
        self.count_entry.insert(0, "3")
        self.count_entry.grid(row=0, column=3)

        tk.Button(top, text="Generate", command=self.generate_headlines).grid(row=0, column=4, padx=5)

        self.text_area = tk.Text(self.tab_main, height=20)
        self.text_area.pack(pady=10)

        bottom = tk.Frame(self.tab_main)
        bottom.pack()

        tk.Button(bottom, text="Add to Favorites", command=self.add_to_favorites).pack(side="left", padx=10)
        tk.Button(bottom, text="Export TXT", command=self.export_txt).pack(side="left", padx=10)
        tk.Button(bottom, text="Export PDF", command=self.export_pdf).pack(side="left", padx=10)
        tk.Button(bottom, text="Clear", command=self.clear_main_text).pack(side="left", padx=10)

    def setup_favorites_tab(self):
        self.tab_fav = tk.Frame(self.notebook)
        self.notebook.add(self.tab_fav, text="⭐ Favorites")

        self.fav_text = tk.Text(self.tab_fav, height=25)
        self.fav_text.pack(padx=10, pady=10, fill="both")

    def setup_search_tab(self):
        self.tab_search = tk.Frame(self.notebook)
        self.notebook.add(self.tab_search, text="🔍 Search")

        search_frame = tk.Frame(self.tab_search)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Go", command=self.search_headlines).pack(side="left")

        self.search_results = tk.Text(self.tab_search, height=25)
        self.search_results.pack(padx=10, pady=10, fill="both")

    def toggle_theme(self):
        self.current_theme = self.dark_mode if self.theme_var.get() else self.light_mode
        self.apply_theme()

    def apply_theme(self):
        theme = self.current_theme
        widgets = [self.root, self.tab_main, self.tab_fav, self.tab_search,
                   self.text_area, self.fav_text, self.search_results]

        for widget in widgets:
            widget.config(bg=theme["bg"])
            if isinstance(widget, tk.Text):
                widget.config(fg=theme["text_fg"], bg=theme["text_bg"])

    def generate_headlines(self):
        self.text_area.insert(tk.END, "\n--- Generated ---\n")
        try:
            count = int(self.count_entry.get())
            if count < 1 or count > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter count 1–10")
            return

        cat = self.category_var.get()
        cat = None if cat == "Any" else cat

        for _ in range(count):
            headline = self.generator.generate_headline(cat)
            self.text_area.insert(tk.END, headline + "\n")

        self.generator.save_history_json()

    def clear_main_text(self):
        self.text_area.delete("1.0", tk.END)

    def export_txt(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            self.generator.save_history_txt(path)
            messagebox.showinfo("Saved", "Headlines exported as TXT.")

    def export_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if path:
            self.generator.save_history_pdf(path)
            messagebox.showinfo("Saved", "Headlines exported as PDF.")

    def add_to_favorites(self):
        selected_text = self.text_area.get("sel.first", "sel.last")
        if selected_text:
            self.generator.favorites.append(selected_text)
            self.fav_text.insert(tk.END, selected_text + "\n")
        else:
            messagebox.showinfo("No Selection", "Please select a headline to add to favorites.")

    def search_headlines(self):
        keyword = self.search_var.get().lower()
        self.search_results.delete("1.0", tk.END)

        if not keyword:
            return

        found = [h["headline"] for h in self.generator.history if keyword in h["headline"].lower()]
        if not found:
            self.search_results.insert(tk.END, "No matches found.")
        else:
            for item in found:
                self.search_results.insert(tk.END, item + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FakeHeadlineApp(root)
    root.mainloop()
