from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import time
import os

Letter_Map = {
    'Α': 'a',
    'Ά': 'a',
    'Β': 'b',
    'Γ': 'g',
    'Δ': 'd',
    'Ε': 'e',
    'Έ': 'e',
    'Ζ': 'z',
    'Η': 'i',
    'Ή': 'i',
    'Θ': 'th',
    'Ι': 'i',
    'Ί': 'i',
    'Κ': 'k',
    'Λ': 'l',
    'Μ': 'm',
    'Ν': 'n',
    'Ξ': 'x',
    'Ο': 'o',
    'Ό': 'o',
    'Π': 'p',
    'Ρ': 'r',
    'Σ': 's',
    'ς': 's',
    'Τ': 't',
    'Υ': 'y',
    'Ύ': 'y',
    'Φ': 'f',
    'Χ': 'x',
    'Ψ': 'ps',
    'Ω': 'w',
    'Ώ': 'w'
}


class MainWindow(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.not_pressed = True
        self.changed = False
        self.root_directory = None
        self.original_names_list = None
        self.original_names = {}
        self.letter_map = Letter_Map.copy()
        self.path_entry()

    def init(self):
        start = time.time()
        self.root.title("Greek to Greeklish Rename")

        scrollbar = tk.Scrollbar(self.root, orient="vertical")
        self.original_names_list = tk.Listbox(self.root, width=50, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.original_names_list.yview)
        scrollbar.pack(side="right", fill="y")
        self.original_names_list.config(width=0)
        self.original_names_list.pack(fill="both", expand=True)

        Button(self.root, text="Rename to Greek", command=self.rename_to_original).pack(fill=X)

        for subdir, dirs, files in os.walk(self.root_directory):
            if files:
                for current_file_name in files:
                    current_folder_path = os.path.join(self.root_directory, subdir)
                    original_file_path = os.path.abspath(os.path.join(current_folder_path, current_file_name))
                    if os.path.exists(original_file_path):
                        name_changed_to_greeklish = self.name_change(current_file_name)
                        if self.changed:
                            renamed_file_path = current_folder_path + "\\" + name_changed_to_greeklish
                            os.rename(original_file_path, renamed_file_path)
                            self.original_names[name_changed_to_greeklish] = {'original_name': current_file_name}
                            self.original_names_list.insert('end', current_file_name + '  -->  ' + name_changed_to_greeklish)
                        self.changed = False
        self.root.deiconify()
        end = time.time()
        messagebox.showinfo('Rename to Greeklish', 'Completed in :  ' + str(end - start) + 'seconds.')

    def rename_to_original(self):
        if self.not_pressed:
            start = time.time()
            self.not_pressed = False
            self.original_names_list.delete(0, END)
            for subdir, dirs, files in os.walk(self.root_directory):
                if files:
                    for current_file_name in files:
                        current_folder_path = os.path.join(self.root_directory, subdir)
                        original_file_path = os.path.abspath(os.path.join(current_folder_path, current_file_name))
                        if os.path.exists(original_file_path) and current_file_name in self.original_names:
                            name_changed_to_greek = self.original_names.get(current_file_name).get('original_name')
                            renamed_file_path = current_folder_path + "\\" + name_changed_to_greek
                            os.rename(original_file_path, renamed_file_path)
                            self.original_names_list.insert('end', current_file_name + '  -->  ' + name_changed_to_greek)
            end = time.time()
            messagebox.showinfo('Rename to Greek', 'Completed in :  ' + str(end - start) + 'seconds.')

    def name_change(self, old_name):
        name_english = ''
        ext_position = old_name.rfind('.')
        extension = old_name[ext_position:]
        for letter in old_name[:ext_position]:
            self.letter_change(letter)
            en_letter = self.letter_change(letter)
            name_english += en_letter
        name_english += extension
        return name_english

    def letter_change(self, gr_letter):
        cap = False
        if gr_letter.istitle():
            cap = True
        en_letter = self.letter_map.get(gr_letter.title())
        if en_letter:
            self.changed = True
        else:
            en_letter = gr_letter
        if cap:
            en_letter = en_letter.title()
        return en_letter

    def path_entry(self):
        self.root.withdraw()
        self.root_directory = askdirectory()
        while not self.root_directory:
            pass
        self.init()


rt = Tk()
app = MainWindow(rt)
rt.mainloop()
