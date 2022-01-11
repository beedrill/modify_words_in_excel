from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from widgets import ExamplesWidget
from excel_handler import init_open, get_word_by_id, save_word, Word
root = None
word_id_entry = None
word_content_entry = None
word_pronunciation_entry = None
word_part_entry = None
word_meaning_entry = None
examples_widget = None
next_button = None
previous_button = None
current_word = None

def previous():
    id = word_id_entry.get()
    id = str(int(id) - 1)
    w = get_word_by_id(id)
    load_word(w)
    examples_widget.focus()

def next():
    current_word.word_content = word_content_entry.get()
    current_word.pronunciation = word_pronunciation_entry.get()
    current_word.meaning = word_meaning_entry.get()
    current_word.part = word_part_entry.get()
    current_word.examples = examples_widget.get_examples()
    x = save_word(current_word)
    if x != 0:
        return 1
    id = word_id_entry.get()
    id = str(int(id) + 1)
    w = get_word_by_id(id)
    load_word(w)
    examples_widget.focus()

def clear():
    global current_word
    word_id_entry.delete(0, "end")
    word_content_entry.delete(0, "end")
    word_pronunciation_entry.delete(0, "end")
    word_part_entry.delete(0, "end")
    word_meaning_entry.delete(0, "end")
    current_word = None
    examples_widget.clear()

def load_word(w):
    global current_word
    clear()
    if w is None:
        return
    word_id_entry.insert(0, w.id)
    word_content_entry.insert(0, w.word_content)
    word_pronunciation_entry.insert(0, w.pronunciation)
    word_part_entry.insert(0, w.part)
    word_meaning_entry.insert(0, w.meaning)
    current_word = w
    examples_widget.set_examples(w)


def updateWithId():
    w = get_word_by_id(word_id_entry.get())
    load_word(w)
    examples_widget.focus()


def open_file():
    fn = fd.askopenfilename(filetypes=[("Excel files", ".xlsx .xls")], initialdir='.')
    w = init_open(fn)
    load_word(w)

def setup_gui():
    global root
    global word_id_entry
    global word_content_entry
    global word_pronunciation_entry
    global word_part_entry
    global examples_widget
    global word_meaning_entry
    global next_button
    global previous_button
    # setup window
    root = Tk()
    root.title('Chinese Vocabulary Editting')
    
    #setup menu bar
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=open_file)
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    # setup main layout
    Label(root, text = 'word id:').grid(column = 0, row = 1, pady=2, padx=5)
    word_id_entry = Entry(root, width=10)
    word_id_entry.grid(column = 1, row = 1, pady=2, padx=10)
    word_id_entry.bind('<Return>', lambda x:updateWithId())
    Button(root, text='update word!', bd=0, fg="magenta", command=updateWithId).grid(column=2, row=1, pady=2, padx=5)
    Label(root, text = 'word content:').grid(column = 3, row = 1, pady=2, padx=5)
    word_content_entry = Entry(root, width=10)
    word_content_entry.grid(column = 4, row = 1, pady=2, padx=10)
    Label(root, text = 'pronunciation:').grid(column = 0, row = 2, pady=2, padx=5)
    word_pronunciation_entry = Entry(root, width=10)
    word_pronunciation_entry.grid(column = 1, row = 2, pady=2, padx=10)
    Label(root, text = 'part:').grid(column = 3, row = 2, pady=2, padx=5)
    word_part_entry = Entry(root, width=10)
    word_part_entry.grid(column = 4, row = 2, pady=2, padx=10)
    Label(root, text = 'meaning:').grid(column = 0, row = 3, pady=2, padx=5)
    word_meaning_entry = Entry(root)
    word_meaning_entry.grid(column = 1, row = 3, pady=2, padx=10, columnspan=4, sticky=N+S+W+E)
    # separator
    separator = ttk.Separator(root, orient='horizontal')
    separator.grid(column=0, row=4, columnspan=5, sticky="WE", pady=10)
    # examples
    examples_widget = ExamplesWidget(root, lambda _: next())
    examples_widget.grid(column=0, row=5, columnspan=5, sticky="WE", pady=5)
    # navigation button
    previous_button = Button(root, text='previous', command=previous)
    previous_button.grid(column=3, row=6, sticky="WE", padx=6, pady=(2,10))
    next_button = Button(root, text='next', command=next)
    next_button.grid(column=4, row=6, sticky="WE", padx=6, pady=(2,10))
    root.mainloop()

if __name__ == '__main__':
    setup_gui()
