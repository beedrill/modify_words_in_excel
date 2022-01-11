import xlrd
import xlwt
from xlutils.copy import copy
import tkinter
import traceback
file_path = None
row_count = None

ID = 0
WORD_CONTENT = 1
PRONUNCIATION = 2
MEANING = 3
WORDBOOK = 4
PART = 5
EXAMPLE1 = 6 # column num of example 1

class Word:
    def __init__(self, row, id, word_content, pronunciation, meaning, wordbook, part, examples = None):
        self.examples = examples if examples is not None else []
        self.id = id
        self.word_content = word_content
        self.pronunciation = pronunciation
        self.meaning = meaning
        self.wordbook = wordbook
        self.part = part
        self.row = row

    @staticmethod
    def fromRow(row, idx):
        w = Word(
            idx, row[ID].value, row[WORD_CONTENT].value, row[PRONUNCIATION].value, row[MEANING].value, row[WORDBOOK].value, row[PART].value
        )
        i = EXAMPLE1
        examples = []
        while i < len(row) and len(row[i].value) > 0:
            examples.append({
                'example': row[i].value,
                'pronunciation': row[i+1].value,
                'meaning': row[i+2].value
            })
            i += 3
        # print(examples)
        w.examples = examples
        return w
    def __str__(self):
        return self.word_content


def get_sheet ():
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_index(0)
    return sheet

def init_open(filename):
    global file_path 
    global row_count
    file_path = filename
    sheet = get_sheet()
    row_count = sheet.nrows
    for i in range(1, row_count):
        if len(sheet.cell(i, EXAMPLE1).value) == 0:
            return Word.fromRow(sheet.row(i), i)

def get_word_by_id(id):
    sheet = get_sheet()
    for i in range(1, row_count):
        if sheet.cell(i, ID).value == id:
            return Word.fromRow(sheet.row(i), i)

def save_word(w):
    try:
        rb = xlrd.open_workbook(file_path)
        wb = copy(rb)
        w_sheet = wb.get_sheet(0)
        w_sheet.write(w.row, WORD_CONTENT, w.word_content)
        w_sheet.write(w.row, PRONUNCIATION, w.pronunciation)
        w_sheet.write(w.row, MEANING, w.meaning)
        w_sheet.write(w.row, PART, w.part)
        for j in range(0, len(w.examples)):
            example = w.examples[j]
            print(example)
            w_sheet.write(w.row, EXAMPLE1 + j*3, example['example'])
            w_sheet.write(w.row, EXAMPLE1 + j*3 + 1, example['pronunciation'])
            w_sheet.write(w.row, EXAMPLE1 + j*3 + 2, example['meaning'])
        wb.save(file_path)
        return 0
    except Exception as e:
        print(traceback.format_exc())
        tkinter.messagebox.showerror(title='Unable to modify the file', message=str(e))
        return 1
