import os
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, font, messagebox

from nudeny import Classify, Detect

file_array = []
nude_images = []
sexy_images = []
safe_images = []
invalid_images = []

def classify(pbar, pbar_label):
    ## IMPLEMENT NUDENY API HERE
    global file_array
    global nude_images
    global sexy_images
    global safe_images
    global invalid_images

    classify = Classify()
    response = classify.imageClassify(paths=file_array)
    # print(response['Prediction'])

    for index, prediction in enumerate(response['Prediction']):
        if prediction['class'] == 'nude':
            nude_images.append(file_array[index])
        elif prediction['class'] == 'sexy':
            sexy_images.append(file_array[index])
        elif prediction['class'] == 'safe':
            safe_images.append(file_array[index])
        elif prediction['class'] == 'invalid':
            invalid_images.append(file_array[index])

    nude_count.set(len(nude_images))
    sexy_count.set(len(sexy_images))
    safe_count.set(len(sexy_images))
    invalid_count.set(len(invalid_images))

    ## PROGRESS BAR
    pbar.stop()
    pbar.grid_forget()
    pbar_label.grid_forget()

def censor(pbar,pbar_label):
    ## IMPLEMENT NUDENY API HERE
    global nude_images

    if len(nude_images) == 0:
        messagebox.showerror(message="There's no nude image to censor")
        pbar.stop()
        pbar.grid_forget()
        pbar_label.grid_forget()
        return

    detect = Detect()
    try:
        response = detect.censorExposed(paths=nude_images, save_path=str(SAVE_DIR.get()))   
    except Exception as e:
        messagebox.showerror(message=str(e))

    # Without save_path
    # try:
    #     response = detect.censorExposed(paths=nude_images)
    #     print(response)   
    # except Exception as e:
    #     messagebox.showerror(message=str(e))
    

    ## PROGRESS BAR
    pbar.stop()
    pbar.grid_forget()
    pbar_label.grid_forget()

def delete():
    ## IMPLEMENT NUDENY API HERE
    global nude_images

    if len(nude_images) == 0:
        messagebox.showerror(message="There's no nude image to delete")
        return

    for nude_image in nude_images:
        try:
            os.remove(nude_image)
            print(f"File {nude_image} has been deleted")
        except Exception as e:
            print(f"Error deleting file {nude_image}: {str(e)}")

def classify_button_click():
    pbar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=400, mode='indeterminate')
    pbar.grid(column=0, row=9, columnspan=4)
    pbar.step(5)
    pbar_label = ttk.Label(mainframe, text="Getting Results...")
    pbar_label.grid(column=0, row=10, columnspan=4)
    thread = threading.Thread(target=classify, args=(pbar,pbar_label,))
    thread.start()
    pbar.start(10)

def censor_button_click():
    pbar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=400, mode='indeterminate')
    pbar.grid(column=0, row=9, columnspan=4)
    pbar.step(5)
    pbar_label = ttk.Label(mainframe, text="Getting Results...")
    pbar_label.grid(column=0, row=10, columnspan=4)
    thread = threading.Thread(target=censor, args=(pbar,pbar_label,))
    thread.start()
    pbar.start(10)


def get_dir():
    DIR.set(filedialog.askdirectory())
    files = os.listdir(DIR.get())
    global file_array
    # Store the list of files in an array
    
    # Get a list of all files in the directory
    files = os.listdir(DIR.get())

    # Store the list of files in the global file_array
    file_array = []
    
    for file in files:
        file_array.append(os.path.join(DIR.get(), file))
    total_count.set(len(file_array))
    nude_count.set("")
    sexy_count.set("")
    safe_count.set("")
    invalid_count.set("")


def get_save_dir():
    SAVE_DIR.set(filedialog.askdirectory())


root = Tk()
root.title("Nudeny Automation")

mainframe = ttk.Frame(root, padding="50 50 50 50")
mainframe.grid(column=0, row=0)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


DIR = StringVar()
ttk.Button(mainframe, text='Open Directory', command=get_dir, width=20).grid(column=0, row=0, sticky=W)
ttk.Entry(mainframe, textvariable=DIR, state=DISABLED, width=70).grid(column=1, row=0, sticky=W, columnspan=3)

SAVE_DIR = StringVar()
ttk.Button(mainframe, text="Save Directory", command=get_save_dir, width=20).grid(column=0, row=1, sticky=W)
ttk.Entry(mainframe, textvariable=SAVE_DIR, state=DISABLED, width=70).grid(column=1, row=1, sticky=W, columnspan=3)

highlightFont = font.Font(family='Helvetica', name='appHighlightFont', size=16, weight='bold')
ttk.Label(mainframe, text="",).grid(column=0, row=2)
ttk.Label(mainframe, text="Total File(s): ", font=highlightFont).grid(column=0, row=3, sticky=W)
ttk.Label(mainframe, text="Nude Image(s): ", font=highlightFont).grid(column=0, row=4, sticky=W)
ttk.Label(mainframe, text="Sexy Image(s): ", font=highlightFont).grid(column=0, row=5, sticky=W)
ttk.Label(mainframe, text="Safe Image(s): ", font=highlightFont).grid(column=0, row=6, sticky=W)
ttk.Label(mainframe, text="Non-Image(s): ", font=highlightFont).grid(column=0, row=7, sticky=W)
ttk.Label(mainframe, text="", ).grid(column=0, row=8, sticky=W)

total_count = StringVar()
total = ttk.Label(mainframe, textvariable=total_count, font=highlightFont)
total.grid(column=1, row=3, sticky=W)

nude_count = StringVar()
nude = ttk.Label(mainframe, textvariable=nude_count, font=highlightFont)
nude.grid(column=1, row=4, sticky=W)

sexy_count = StringVar()
sexy = ttk.Label(mainframe, textvariable=sexy_count, font=highlightFont)
sexy.grid(column=1, row=5, sticky=W)

safe_count = StringVar()
safe = ttk.Label(mainframe, textvariable=safe_count, font=highlightFont)
safe.grid(column=1, row=6, sticky=W)

invalid_count = StringVar()
invalid = ttk.Label(mainframe, textvariable=invalid_count, font=highlightFont)
invalid.grid(column=1, row=7, sticky=W)


style = ttk.Style()
style.theme_use('alt')
style.configure("Classify.TButton", background="green", foreground="white", font=("Arial", 16))
style.configure("Censor.TButton", background="blue", foreground="white", font=("Arial", 16))
style.configure("Delete.TButton", background="red", foreground="white", font=("Arial", 16))

# create the buttons with the updated styles
ttk.Button(mainframe, text="Classify", padding="70 30", style="Classify.TButton", command=classify_button_click).grid(column=0, row=11, columnspan=2, sticky=NW)
ttk.Button(mainframe, text="Censor", padding="70 30", style="Censor.TButton", command=censor_button_click).grid(column=2, row=11, columnspan=2, sticky=NE)
ttk.Label(mainframe, text="", anchor=W, width=15).grid(column=0, row=12, sticky=W)
ttk.Button(mainframe, text="Delete", padding="70 30", style="Delete.TButton", command=delete).grid(column=0, row=13, columnspan=4)


root.mainloop()




# mainframe = widget.Frame(root, padding="100 100 100 0")
# mainframe.grid(column=0, row=0)
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# feet = StringVar()
# feet_entry = widget.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=1, row=5)

# meters = StringVar()
# test = widget.Label(mainframe, textvariable=meters)
# test.grid(column=1, row=2, sticky=(W, E))


# widget.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# widget.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# widget.Label(mainframe, text="is equivalent to").grid(column=0, row=2, sticky=E)
# widget.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# for child in mainframe.winfo_children(): 
#     child.grid_configure(padx=10, pady=10)

# feet_entry.focus()
# root.bind("<Return>", calculate)

# root.mainloop()

