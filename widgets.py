import tkinter as tk
from tkinter import ttk
from hanzi2pinyin import hanzi2pinyin
class ExampleEditWidget(tk.Frame):
    def __init__(self, parent, label, finish_callback, example = None):
        tk.Frame.__init__(self, parent)

        self.example_label = tk.Label(self, text=label + ': ')
        self.example_entry = tk.Entry(self)
        self.example_entry.bind('<Return>', self.update_pronunciation)
        self.example_entry.bind('<FocusOut>', self.update_pronunciation)
        self.example_label.grid(column=0, row=0, sticky='w', pady=4, padx=(5,0))
        self.example_entry.grid(column=1, row=0, sticky='news', columnspan=4, padx=10, pady=4)

        self.example_pronunciation_label = tk.Label(self, text='pronunciation: ')
        self.example_pronunciation_entry = tk.Entry(self)
        self.example_pronunciation_label.grid(column=0, row=1, sticky='w', pady=4, padx=(5,0))
        self.example_pronunciation_entry.grid(column=1, row=1, sticky='news', columnspan=4, padx=10, pady=4)

        self.example_meaning_label = tk.Label(self, text='meaning: ')
        self.example_meaning_entry = tk.Entry(self)
        self.example_meaning_label.grid(column=0, row=2, sticky='w', pady=4, padx=(5,0))
        self.example_meaning_entry.grid(column=1, row=2, sticky='news', columnspan=4, padx=10, pady=4)
        self.example_meaning_entry.bind('<Return>', finish_callback)
        # self.example_entry.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.grid(column=0, row=4, columnspan=5, sticky="WE", pady=(5,2))
        if example is not None:
            self.set_example(example)

    def set_example(self, example):
        self.example_entry.insert(0, example['example']) 
        self.example_pronunciation_entry.insert(0, example['pronunciation']) 
        self.example_meaning_entry.insert(0, example['meaning']) 
    
    def get(self):
        return self.entry.get()

    def focus(self):
        self.example_entry.focus()
    
    def update_pronunciation(self, val):
        self.example_pronunciation_entry.delete(0, 'end')
        self.example_pronunciation_entry.insert(0, hanzi2pinyin(self.example_entry.get()))
        self.example_meaning_entry.focus()

    def get_example(self):
        return {
            'example': self.example_entry.get(),
            'pronunciation': self.example_pronunciation_entry.get(),
            'meaning': self.example_meaning_entry.get()
        }

class ExamplesWidget(tk.Frame):
    def __init__(self, parent, finish_callback):
        tk.Frame.__init__(self, parent)
        self.finish_callback = finish_callback
        self.example_widgets = []
        self.add_example_button = tk.Button(self, text='add example!', bd=0, fg="magenta", command=self.add_example)
        self.add_example_button.grid(column=0, row=0, pady=2, padx=5)
        example_widget = ExampleEditWidget(self, 'Example 1', finish_callback)
        example_widget.grid(column=0, row=1, columnspan=5,sticky='we', pady=5)
        self.example_widgets.append(example_widget)
        self.columnconfigure(1, weight=1)

    def get(self):
        return self.entry.get()
    
    def add_example (self):
        new_example = ExampleEditWidget(self, f'Example {len(self.example_widgets)+1}', self.finish_callback)
        new_example.grid(column=0, row=self.grid_size()[1], columnspan=5,sticky='we', pady=5)
        self.example_widgets.append(new_example)
        new_example.focus()

    def focus(self):
        if len(self.example_widgets) == 0:
            return
        self.example_widgets[0].focus()

    def get_examples(self):
        examples = []
        for w in self.example_widgets:
            examples.append(w.get_example())
        return examples

    def clear(self):
        for w in self.example_widgets:
            w.destroy()
        self.example_widgets = []
        self.add_example()

    def set_examples(self, w):
        if len(self.example_widgets) == 0:
            tk.messagebox.showerror(title='no example widget, something is wrong', message='you can close this program and restart.')
        if len(w.examples) == 0:
            return
        for i in  range(0, len(w.examples)):
            example = w.examples[i]
            if len(self.example_widgets) <=i:
                self.add_example()
            self.example_widgets[i].set_example(example)
        
