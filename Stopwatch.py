


from tkinter import *
import time

class StopWatch(Frame):  
    # Executes a stop watch frame widget.                                                                 
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
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
        # Stopwatch Label 
        title = Label(self, text='Stopwatch', font=('Arial', 10))
        title.pack(fill=X, expand=NO, pady=1, padx=2)
        
        watch = Label(self, textvariable=self.timestr, font=('Arial', 16), bg=('black'), fg=('white'))
        self._setTime(self._elapsedtime)
        watch.pack(fill=X, expand=NO, pady=3, padx=2)
        
        name = Label(self, text= '           hours            minutes          seconds         centisec.       ', font=('Arial', 4), fg='white', bg='black')
        name.pack(fill='x', expand='no')

        lap = Label(self, text='Laps')
        lap.pack(fill=X, expand=NO, pady=4, padx=2)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.listbox = Listbox(self,selectmode=EXTENDED, height = 5, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
   
    def _update(self): 
         # update stopwatch function in order to make changes on stopwatch every seconds elapsed time.
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        # Set the time string to Hours:Minutes:Seconds:Hundreths
        hours = int(elap/3600.0)
        minutes = int(elap/60.0)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d:%02d' % (hours, minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        # Set the time string to Hours:Minutes:Seconds:Hundreths 
        hours = int(elap/3600.0)
        minutes = int(elap/60.0)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d:%02d' % (hours, minutes, seconds, hseconds)
        
    def Start(self):                         
        # Start the stopwatch, ignore if running.
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        # Stop the stopwatch, ignore if stopped. 
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
         # Reset the stopwatch. Reset function is use to set the watch to zero  """
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.laps = []   
        self.lapmod2 = self._elapsedtime
        self._setTime(self._elapsedtime)
        self.listbox.delete(0, END)

    def Lap(self):
        # Makes a lap, only if the watch starts running.
        tempo = self._elapsedtime - self.lapmod2
        if self._running:
            self.laps.append(self._setLapTime(tempo))
            self.listbox.insert(END, self.laps[-1])
            self.listbox.yview_moveto(1)
            self.lapmod2 = self._elapsedtime
                       
    def storing(self):
        # Get the name of the timer and create a file to store the laps
        file = str(self.e.get()) + ' - '
        with open(file + self.today + '.txt', 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8')))
            
def main():
    root = Tk()
    root.wm_attributes("-topmost", 1)      #always on top - might do a button for it
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='Start', height=3, width=4, fg=('green'), bg=('black'), command=sw.Start).pack(side=LEFT)
    Button(root, text='Stop', height=3, width=4, fg=('red'), bg=('black'), command=sw.Stop).pack(side=LEFT)
    Button(root, text='Lap', height=3, width=4, fg=('yellow'), bg=('black'), command=sw.Lap).pack(side=LEFT)
    Button(root, text='Reset', height=3, width=4, fg=('cyan'), bg=('black'), command=sw.Reset).pack(side=LEFT)
    
    root.mainloop()

if __name__ == '__main__':
    
