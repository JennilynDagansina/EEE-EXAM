from tkinter import *
from tkinter import messagebox
import time


class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self.window = parent
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.lapstr = StringVar()
        self.e = 0
        self.listbox = 0
        self.makeWidgets()
        self.laps = []
        self.lapmod2 = 0
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
        
    def makeWidgets(self):                         
        """ Stopwatch Label """
        title = Label(self, text='Stopwatch', font=('Arial', 20))
        title.pack(fill=X, expand=YES, pady=1, padx=2)
        
        watch = Label(self, textvariable=self.timestr, font=('Arial', 32), bg=('black'), fg=('white'))
        self._setTime(self._elapsedtime)
        watch.pack(fill=X, expand=YES, pady=3, padx=2)
        
        name = Label(self, text= '            hours          minutes        seconds       centisec.       ', font=('Arial', 8), fg='white', bg='black')
        name.pack(fill='x', expand='yes')

        lap = Label(self, text='Laps')
        lap.pack(fill=X, expand=YES, pady=4, padx=2)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.listbox = Listbox(self,selectmode=EXTENDED, height = 8, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
   
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Hours:Minutes:Seconds:Hundreths """
        hours = int(elap/3600.0)
        minutes = int(elap/60.0)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours, minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        """ Set the time string to Hours:Minutes:Seconds:Hundreths """
        hours = int(elap/3600.0)
        minutes = int(elap/60.0)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d:%02d' % (hours, minutes, seconds, hseconds)
        
    def Start(self):                         
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.laps = []   
        self.lapmod2 = self._elapsedtime
        self._setTime(self._elapsedtime)
        self.listbox.delete(0, END)
        
    def ExitApp(self):
        MsgBox = messagebox.askquestion ('Exit App','Really Quit?',icon = 'error')
        if MsgBox == 'yes':
           self.window.destroy()
        else:
            messagebox.showinfo('Welcome Back','Welcome back to the App')

    def Lap(self):
        '''Makes a lap'''
        tempo = self._elapsedtime - self.lapmod2
        if self._running:
            self.laps.append(self._setLapTime(tempo))
            self.listbox.insert(END, self.laps[-1])
            self.listbox.yview_moveto(1)
            self.lapmod2 = self._elapsedtime
                       
    def storing(self):
        '''Get the name of the timer and create a file to store the laps'''
        file = str(self.e.get()) + ' - '
        with open(file + self.today + '.txt', 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8', font=('Arial', 20))))
            
def main():
    root = Tk()
    root.wm_attributes("-topmost", 1)      #always on top - might do a button for it
    root.geometry('485x450')
    sw = StopWatch(root)
    sw.pack(side=TOP)


    Button(root, text='Start', height=5, width=12, fg=('green'), command=sw.Start).pack(fill=X, expand=YES, pady=3, padx=2, side=LEFT, anchor=CENTER)
    Button(root, text='Stop', height=5, width=12, fg=('red'), command=sw.Stop).pack(fill=X, expand=YES, pady=3, padx=2, side=LEFT, anchor=CENTER)
    Button(root, text='Lap', height=5, width=12, fg=('black'), command=sw.Lap).pack(fill=X, expand=YES, pady=3, padx=2, side=LEFT, anchor=CENTER)
    Button(root, text='Reset', height=5, width=12, fg=('black'), command=sw.Reset).pack(fill=X, expand=YES, pady=3, padx=2, side=LEFT, anchor=CENTER)
    Button(root, text='Exit App',height=3, width=12, command=sw.ExitApp).pack(fill=X, expand=NO, pady=3, padx=2,anchor=CENTER, side=LEFT)
    
    root.mainloop()

if __name__ == '__main__':
    main()
    