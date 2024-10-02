import tkinter as tk
from PIL import ImageFont,Image,ImageTk
from tkinter import filedialog, ttk
import PyPDF2, string,json,random,PIL

class Buttons_and_Labels(ttk.Frame):
    def __init__(self, parent, path, function, col, row, frame, destroying=0, text='', bg='white'):
        super().__init__(master=parent)
        self.function = function
        self.path = path
        self.col = col
        self.row = row
        self.frame = frame
        self.destroying = destroying
        self.text = text
        self.bg = bg

    def create_label(self,len = 300):
        label = ttk.Label(self.frame, text=f'{self.text:>{screen_width}}', font=("Arial", 13),wraplength=len, background = self.bg,padding=10)
        label.grid(row=self.row, column=self.col, sticky='nsew', padx=5, pady=5)
        

    def create_button__columns(self,span = 1):
        self.frame.rowconfigure(self.row, weight=1)
        self.frame.columnconfigure((0, 1), weight=1, uniform='a')

        button = ttk.Button(self.frame, text=self.text, command=self.function)
        button.grid(row=self.row, column=self.col,columnspan=span, sticky='nsew', padx=5, pady=5)

    def create_regular_button(self):
        button = ttk.Button(self.frame, text=self.text, command=self.function)
        button.place(relx = self.col, rely = self.row)

    def check_button(self, question, inner_list, answer, dict_, checkbutton_states, span=1):
        def updating_good_answers():
            if x.get() == 1:
                inner_list.append(answer)
                dict_.update({question: inner_list})
                check_button.configure(selectcolor='green3')
            else:
                if answer in inner_list:
                    inner_list.remove(answer)
                dict_.update({question: inner_list})
                check_button.configure(selectcolor='red')

            checkbutton_states[(question, answer)] = x.get()
        x = tk.IntVar(value=checkbutton_states.get((question, answer), 0))

        check_button = tk.Checkbutton(self.frame, selectcolor='red', variable=x, onvalue=1, offvalue=0, command=updating_good_answers)
        check_button.grid(row=self.row, column=self.col, sticky='nsew', padx=5, pady=1)

        if x.get() == 1:
            check_button.configure(selectcolor='green3')
        else:
            check_button.configure(selectcolor='red')
            
    def create_text(self,width, height, max_chars=1000):
        if height == 1:
            text = tk.Text(self.frame, width=50, height=height, wrap='word', pady=5, bg=self.bg, undo=True)
        else:
            text = tk.Text(self.frame, width=self.how_many_letters_in_row(), height=height, wrap='word', pady=5, bg=self.bg, undo=True)
        text.insert('1.0', self.text)
        text.grid(row=self.row, column=self.col + 1, sticky='nsew', padx=3, pady=5)
        text.bind('<Control-z>', lambda e: text.edit_undo())
        
        def limit_characters(event=None):
            current_text = text.get("1.0", tk.END)
            if len(current_text) > max_chars:
                text.delete(f"1.{max_chars}", tk.END)
                
        text.bind("<KeyRelease>", limit_characters)
        
    def how_many_letters_in_row(self):
        global width_of_font
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
            bbox = font.getbbox('W')
            width_of_font = bbox[2] - bbox[0]
            how_many = screen_width // width_of_font
            return how_many
        except FileNotFoundError:
            font = ImageFont.truetype('/Library/Fonts/Arial.ttf',13)
            bbox = font.getbbox('W')
            width_of_font = bbox[2] - bbox[0]
            how_many = screen_width // width_of_font
            return how_many
        except OSError:
            error('Arial font cannot be found ')            
            
class Making_Windows():
    def __init__(self):
        self.main_frame = None
        self.canvas = None
        self.frame_content = None
        
    def making_canvas(self,window):

        self.main_frame = ttk.Frame(window)
        self.main_frame.pack(fill='both', expand=True)

        self.frame = ttk.Frame(self.main_frame)
        self.frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side='left', fill='both', expand=True)
        
        self.frame_content = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_content, anchor='nw')
        if window == root:
            
            self.frame_content.config(width=screen_width, height=screen_height)
            self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.sync_scroll)
            self.scrollbar.pack(side='right', fill='y')
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.adjust_canvas_scrollregion()
            self.canvas.bind_all('<MouseWheel>', self.block_up_scroll)
            
        return self.frame_content
    
    def set_background_image(self, window, image_path):  
        image = Image.open(image_path)
        size = (screen_width,screen_height)
        image = image.resize(size)  
        photo = ImageTk.PhotoImage(image)  
        label = tk.Label(window, image=photo)  
        label.pack(fill="both", expand=True)  
        label.image = photo
        
    def block_up_scroll(self, event):
        if self.canvas.yview()[0] <= 0 and event.delta > 0:
            return "break"
        self.canvas.yview_scroll(-int(event.delta / 60), "units")

    def adjust_canvas_scrollregion(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def start_button(self):    
        reading_file_button = Buttons_and_Labels(root, '', self.reading_file, 0.5, 0.5, self.frame_content, destroying = 1, text='New Test')
        reading_file_button.create_regular_button()    

    def sync_scroll(self, *args):
        self.canvas.yview(*args)

    def scroll_to_top(self):
        self.canvas.yview_moveto(0)

    def reading_file(self):
        global dict_questions ,list_of_dict,frame_content
        self.canvas.filename = filedialog.askopenfilename(initialdir='/data', title='Select a file', filetypes=(('pdf files', '*.pdf'),)) 
        file_path = self.canvas.filename
        list_of_dict = []
        one_answer = ''
        longer_line = ''
        question = 0
        answears = []
        el_before = ''
        list_of_answers = []
        empty_dict = {}
        try:
            with open(file_path, 'rb') as pdf:
                reader = PyPDF2.PdfReader(pdf, strict=False)
                list_pdf_text = []
                lines_pdf_text = ''
                dict_questions = {}
                inner_list = []
                for page in reader.pages:
                    content = page.extract_text()
                    list_pdf_text.append(content)
                for i in range(len(list_pdf_text)):      
                    lines_pdf_text = list_pdf_text[i]
                    lines_pdf_text = lines_pdf_text.split('\n')
                    for line in lines_pdf_text:
                        line = line.strip()
                        if line:
                            if line[0] in string.digits and question == 0:
                                question = 1
                            if question == 1:
                                longer_line += line
                            else:
                                answears.append(line)
                            if line[-1] == '?' or line[-1] == ':' and question == 1:
                                if answears:
                                    for an in answears:
                                        for el in an[::-1]:
                                            one_answer += el
                                            if el_before == ')' or el_before == '.' and el == an[0]:
                                                list_of_answers.append(one_answer[::-1])
                                                one_answer = ''
                                            el_before = el
                                if list_of_answers:
                                    for el in list_of_answers:
                                        inner_list.append(el)
                                        list_of_answers = []
                                inner_list = []
                                dict_questions.update({(longer_line):inner_list})
                                
                                longer_line = ''
                                question = 0
                                answears = []
                for an in answears:
                    for el in an[::-1]:
                        one_answer += el
                        if el_before == ')' or el_before == '.':
                            list_of_answers.append(one_answer[::-1])
                            one_answer = ''
                        el_before = el
                if list_of_answers:
                    for el in list_of_answers:
                        inner_list.append(el)      
            i = 0
            list_of_dict.append(empty_dict)
            for k,w in dict_questions.items():
                i += 1 
                empty_dict.update({k:w})
                if i % 5 == 0:
                    empty_dict = {}
                    list_of_dict.append(empty_dict)
            if list_of_dict == [{}]:
                error('Cannot make test from this file ')
            else:
                for widget in frame_content.winfo_children():
                    widget.destroy()
                creating_test()
                self.adjust_canvas_scrollregion() 
        except FileNotFoundError:
            pass
        
# Main functions
def front_page():
    global page_nr
    page_nr = 0
    for widget in frame_content.winfo_children():
        widget.destroy()
    window.set_background_image(frame_content, "main_bg.png")
    window.start_button()
    play = Buttons_and_Labels(root, '',load_saves, 0.5, 0.4, frame_content, text='Play')
    play.create_regular_button()
    window.adjust_canvas_scrollregion()
 
def creating_test():
    global page_nr, line
    i = 0
    line = 0
    for k in list_of_dict[page_nr]:
        inner_list = []
        text = Buttons_and_Labels(root, '', empty_f, 1, line, frame_content, text=k, bg='SkyBlue1')
        text.create_text(180,4)
        line += 1
        for w in list_of_dict[page_nr][k]:
            text = Buttons_and_Labels(root, '', empty_f, 1, line, frame_content, text=w, bg='azure')
            button = Buttons_and_Labels(root, '', empty_f, 0, line, frame_content, text=str(i+1), bg = 'white')
            button.check_button(k, inner_list, str(w), good_answerws_dict, checkbutton_states_maker)
            text.create_text(180,4)
            line += 1
            i += 1
    if page_nr != len(list_of_dict)-2:        
        next_page = Buttons_and_Labels(root, '',lambda: next_page_f(creating_test), 3, line, frame_content, text='next page')
        next_page.create_button__columns()
    if page_nr > 0:    
        previous_page = Buttons_and_Labels(root, '',lambda: previous_page_f(creating_test), 0, line, frame_content, text='previous page')
        previous_page.create_button__columns()
    if page_nr == len(list_of_dict)-2:
        end_edits = Buttons_and_Labels(root, '',saving_page, 3, line, frame_content, text='end edits')
        end_edits.create_button__columns()
    window.adjust_canvas_scrollregion()

def game_f():
    global page_nr, line
    for widget in frame_content.winfo_children():
        widget.destroy()
    i = 0
    for k in list_of_dict[page_nr]:
        inner_list = []
        label = Buttons_and_Labels(root, '', empty_f, 3, line, frame_content, text=k, bg='SkyBlue1')
        label.create_label(len = screen_width-screen_width*0.2)
        line += 1
        for w in list_of_dict[page_nr][k]:
            label = Buttons_and_Labels(root, '', empty_f, 3, line, frame_content, text=w, bg='azure')
            button = Buttons_and_Labels(root, '', empty_f, 0, line, frame_content, text=str(i+1), bg = 'white')
            button.check_button(k, inner_list, str(w), players_answers_dict,checkbutton_states_game)
            label.create_label(len = screen_width-screen_width*0.2)
            line += 1
            i += 1
    line += 1
    if page_nr != len(list_of_dict)-1:        
        next_page = Buttons_and_Labels(root, '', lambda: next_page_f(game_f), 4, line, frame_content, text='next page')
        next_page.create_button__columns()
    if page_nr > 0:    
        previous_page = Buttons_and_Labels(root, '', lambda: previous_page_f(game_f), 0, line, frame_content, text='previous page')
        previous_page.create_button__columns()
    if page_nr == len(list_of_dict)-1:
        end_game = Buttons_and_Labels(root, '',end_game_f, 4, line, frame_content, text='end')
        end_game.create_button__columns()
    window.adjust_canvas_scrollregion()

def check_answers():
    global page_nr, line,score,score_text
    for widget in frame_content.winfo_children():
        widget.destroy()
    i = 0
    window.scroll_to_top()
    dict_of_colors = colors()
    score_text = f'{score/number_of_questions:^{screen_width}}\n{str(score/number_of_questions*100)+'%':^{screen_width}}'
    score_label = Buttons_and_Labels(root, '', empty_f, 3, line, frame_content,bg ='RosyBrown1' ,text=score_text)
    score_label.create_label(len = screen_width-screen_width*0.2)
    line += 1    
    for k in list_of_dict[page_nr]:
        label = Buttons_and_Labels(root, '', empty_f, 3, line, frame_content, text=k, bg='SkyBlue1')
        label.create_label(len = screen_width-screen_width*0.2)
        line += 1
        i_0 = 0

        for w in list_of_dict[page_nr][k]:
            label = Buttons_and_Labels(root, '', empty_f, 3, line, frame_content, text=w, bg=dict_of_colors[k][i_0])
            label.create_label(len = screen_width-screen_width*0.2)
            line += 1
            i += 1
            i_0 +=1
    line += 1
    if page_nr != len(list_of_dict)-1:        
        next_page = Buttons_and_Labels(root, '', lambda: next_page_f(check_answers), 4, line, frame_content, text='next page')
        next_page.create_button__columns()
    if page_nr > 0:    
        previous_page = Buttons_and_Labels(root, '', lambda: previous_page_f(check_answers), 0, line, frame_content, text='previous page')
        previous_page.create_button__columns()
    if page_nr == len(list_of_dict)-1:
        end = Buttons_and_Labels(root, '', front_page, 4, line, frame_content, text='end')
        end.create_button__columns()
    window.adjust_canvas_scrollregion()   
    
#Subfunctions     
    #front page subfunction
def load_saves():
    def load_file(file):
        global list_of_dict, good_answerws_dict,dict_questions,longest_text
        with open(file.strip(),'r',encoding = 'utf-8') as json_file, open(f'{file.strip()}_answers','r',encoding = 'utf-8') as json_file_answers:
            dict_questions_json = json_file.read()
            good_answerws_dict_json = json_file_answers.read()
            list_of_dict = json.loads(dict_questions_json)
            good_answerws_dict = json.loads(good_answerws_dict_json)
            dict_questions = {}
            for dict in list_of_dict: 
                for k,w in dict.items():
                    dict_questions.update({k:w})

            chose_how_many_q()

    for widget in frame_content.winfo_children():
        widget.destroy()  
    line = 0
    with open('saves.txt','r') as saves:
        for file in saves:
            file_button = Buttons_and_Labels(root, '',lambda f = file: load_file(f), 0,line, frame_content, text=file)
            file_button.create_button__columns()
            line += 1
    previous_page = Buttons_and_Labels(root, '',front_page, 0, line, frame_content, text='previous page')
    previous_page.create_button__columns()
    window.adjust_canvas_scrollregion()
  

    #Creating_test subfunction
def saving_page():
    def saving_file():
        global page_nr
        for widget in frame_content.winfo_children():
            if isinstance(widget,tk.Text):
                name = widget.get('1.0',tk.END).strip()
        list_of_dict_json = json.dumps(list_of_dict,ensure_ascii = False)
        good_answerws_dict_json = json.dumps(good_answerws_dict,ensure_ascii = False)
        try:
            with open(f'{name}','w',encoding='UTF-8') as json_file, open(f'{name}_answers','w',encoding='UTF-8') as json_file_answers, open('saves','a',encoding='UTF-8') as saves:
                json_file.write(list_of_dict_json)
                json_file_answers.write(good_answerws_dict_json)
                saves.write(f'{name}\n')
            page_nr = 0
            for widget in frame_content.winfo_children():
                widget.destroy()
            front_page()
        except OSError:
            error('A file name cannot contain these characters: \\ / : * ? " < > |.')
    global page_nr
    page_nr += 1    
    for widget in frame_content.winfo_children():
        widget.destroy()
    label_name_your_file = Buttons_and_Labels(root, '', empty_f, 0, 1, frame_content, text='Your\'s save name:',bg = 'SystemButtonFace')
    text = Buttons_and_Labels(root, '', empty_f, 0, 1, frame_content, text='')
    save_button = Buttons_and_Labels(root, '', saving_file, 0, 2, frame_content, text='save')
    text.create_text(50,1,max_chars = 250)
    label_name_your_file.create_label()
    save_button.create_button__columns()
    window.adjust_canvas_scrollregion()
    previous_page = Buttons_and_Labels(root, '',lambda: previous_page_f(creating_test), 0, 3, frame_content, text='previous page')
    previous_page.create_button__columns()   
 
    #Game_f subfunction
def end_game_f():
    global page_nr
    page_nr = 0
    check_answers()
    
    #Check answears subfuntion
def colors():
    global score
    dict_of_colors = {}
    i = 0
    score = 0
    while i <len(list_of_dict):
        for k in list_of_dict[i]:
            inner_list = []
            for w in list_of_dict[i][k]:
                if k in players_answers_dict and k in good_answerws_dict:
                    if w in players_answers_dict[k] and w in good_answerws_dict[k]:
                        inner_list.append('lawn green')
                    elif w in players_answers_dict[k] and w not in good_answerws_dict[k]:
                        inner_list.append('orange red')
                    elif w in good_answerws_dict[k] and w not in players_answers_dict[k]:
                        inner_list.append('light goldenrod')
                    else:
                        inner_list.append('azure')

                elif k in good_answerws_dict and w in good_answerws_dict[k]:
                    inner_list.append('gold')                
                else:
                    inner_list.append('azure')
            score +=1 if 'orange red' not in inner_list and 'light goldenrod' not in inner_list and 'lawn green' in inner_list else 0
            dict_of_colors.update({k:inner_list})
        i+=1

    return dict_of_colors

    #load_saves subfunction
def chose_how_many_q():
    global toplvl
    toplvl = tk.Toplevel(root)
    top_window = Making_Windows()
    top_frame_content = top_window.making_canvas(toplvl)
    how_many_questions_quater  = Buttons_and_Labels(toplvl, '',lambda: start_game_and_making_list_of_q(len(dict_questions)//4), 0,line, top_frame_content, text=str(len(dict_questions)//4))
    how_many_questions_quater.create_button__columns()
    how_many_questions_half = Buttons_and_Labels(toplvl, '',lambda: start_game_and_making_list_of_q(len(dict_questions)//2), 1,line, top_frame_content, text=str(len(dict_questions)//2))
    how_many_questions_half.create_button__columns()
    how_many_questions_all = Buttons_and_Labels(toplvl, '',lambda: start_game_and_making_list_of_q(len(dict_questions)), 2,line, top_frame_content, text=str(len(dict_questions)))
    how_many_questions_all.create_button__columns()
    
    #First game_f call
def start_game_and_making_list_of_q(i):
    global list_of_dict,number_of_questions
    empty_dict = {}
    list_of_dict = []
    i_0 = i/5
    number_of_questions = 0
    while i_0 > 0:
        key = random.choice(list(dict_questions.keys()))
        if not any(key in d for d in list_of_dict):
            w = dict_questions[key]
            empty_dict.update({key: w})
            number_of_questions +=1
            if len(empty_dict) % 5 == 0:
                i_0 -= 1 
                list_of_dict.append(empty_dict)
                empty_dict = {} 
    toplvl.destroy()
    game_f()
   
    #Subfunctios of many functions    
def empty_f():
    pass 

def error(text):
    toplvl = tk.Toplevel(root)
    toplvl.geometry('300x150')
    top_window = Making_Windows()
    top_frame_content = top_window.making_canvas(toplvl)
    label = Buttons_and_Labels(toplvl, '', empty_f, 0, 1, top_frame_content, text=text,bg = 'SystemButtonFace')
    label.create_label()
    
def next_page_f(function):
    global page_nr
    saving_changes_on_page() if function == creating_test else None
    if page_nr < len(list_of_dict):
        page_nr += 1
        for widget in frame_content.winfo_children():
            widget.destroy()
        function()
        window.scroll_to_top()

def previous_page_f(function):
    global page_nr
    saving_changes_on_page() if function == creating_test else None
    if page_nr>0:
        page_nr -= 1
        for widget in frame_content.winfo_children():
            widget.destroy()
        function()
        window.scroll_to_top()
        
        #subfunction of previous/next_page_f
def saving_changes_on_page():
    global page_nr 
    new_dict = {}
    list_of_answers = []
    key = None 
    for widget in frame_content.winfo_children():
        if isinstance(widget, tk.Text):
            var = widget.get('1.0', tk.END).strip()
            if var and var[0] in string.digits:
                if key is not None:
                    new_dict[key] = list_of_answers
                key = var 
                list_of_answers = [] 
            else:
                list_of_answers.append(var)
    if key is not None:
        new_dict[key] = list_of_answers
    list_of_dict[page_nr] = new_dict
    

# setup
score = 0
score_text = 0
number_of_questions = 1
checkbutton_states_maker = {}
checkbutton_states_game = {}
list_of_dict = []
list_of_files = []
dict_questions = {}
line = 1
page_nr = 0
good_answerws_dict = {}
players_answers_dict = {}

try:
    file  = open('saves.txt','x')
    file.close()
except FileExistsError:
    pass       

root = tk.Tk()
root.state('zoomed')    
root.title('Test Maker')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#window background

window = Making_Windows()
frame_content = window.making_canvas(root)

front_page()
root.mainloop()
