import tkinter
from tkinter.filedialog import askdirectory
import os
import os.path
import time
import ems_to_csv_3
import sys
import threading


class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')


class MyGui(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.dir_opt = options = {}
        self.directory = ''
        options['initialdir'] = os.path.join(os.path.expanduser('~'), "Documents")
        options['mustexist'] = True
        options['parent'] = parent
        options['title'] = 'This is a title'

        self.working_dir_var = tkinter.StringVar()
        self.working_dir_label_var = tkinter.StringVar()
        self.select_button = tkinter.Button(self, text="Choose Source Directory",
                                       command=self.on_select_button_click)
        self.select_button.grid(column=0, row=0, sticky='NW', padx=10, pady=10)

        self.generate_button = tkinter.Button(self, text="Convert xml to csv",
                                       command=self.on_generate_button_click)
        self.generate_button.grid(column=1, row=0, sticky='NE', padx=10, pady=10)

        self.text_box = tkinter.Text(self.parent, wrap='word', height=28, width=50)
        self.text_box.grid(column=0, row=2, columnspan=2, sticky='NSWE', padx=5, pady=5)
        sys.stderr = StdoutRedirector(self.text_box)
        self.active_thread = None
        self.var_1 = tkinter.IntVar()
        self.var_2 = tkinter.IntVar()

        self.initialize()

    def initialize(self):
        self.grid()

        self.working_dir_var.set("Select working directory")

        label = tkinter.Label(self, textvariable=self.working_dir_label_var,
                              anchor="w", fg="white", bg="blue")
        label.grid(column=0, row=1, columnspan=2, sticky='EW', padx=10, pady=10)
        self.working_dir_label_var.set("Please select working directory with xml files to convert to csv")

        # todo use these check box elements to pass boolean info to your script
        # tkinter.Checkbutton(self, text="Not Used 1", variable=self.var_1).grid(row=3, sticky='W')
        # tkinter.Checkbutton(self, text="Not Used 2", variable=self.var_2).grid(row=4, sticky='W')

        self.generate_button['state'] = 'disabled'
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.minsize(width=1000, height=600)
        self.update()
        self.geometry(self.geometry())       

    def on_select_button_click(self):
        if not self.active_thread or not self.active_thread.is_alive():
            self.directory = askdirectory()
            if self.directory:
                os.chdir(self.directory)
                self.working_dir_label_var.set(self.directory)
                with open("thisisatest.txt", 'w') as f:
                    print(self.directory, file=f)
                # print("You clicked the select button")
                self.generate_button['state'] = 'normal'

    def on_generate_button_click(self):
        if not self.active_thread or not self.active_thread.is_alive():
            # self.generate_button['state'] = 'disabled'
            # self.select_button['state'] = 'disabled'
            # ib_report = ib.IbDetails()
            print("Starting...", file=sys.stderr)

            # todo uncomment the check box elements above to pass boolean info to your script
            if self.var_1.get():
                var_1 = True
            else:
                var_1 = False
            if self.var_2.get():
                var_2 = True
            else:
                var_2 = False

            self.active_thread = threading.Thread(target=ems_to_csv_3.main, args=[[], False])
            self.active_thread.start()
            # time.sleep(1)
            # os.system("start " + os.path.join(self.directory, "thisisatest.txt"))
            # os.system("start " + os.path.join(self.directory, ib_report.get_ib_report_name()))
            # print("You clicked the generate button")
            # self.generate_button['state'] = 'normal'
            # self.select_button['state'] = 'normal'

if __name__ == "__main__":
    app = MyGui(None)
    app.title('EMS Parser')
    app.mainloop()
