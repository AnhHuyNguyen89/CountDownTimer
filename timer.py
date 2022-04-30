from tkinter import *
from tkinter import filedialog
from task import *
import tkinter.messagebox
import datetime as dt
import time
import csv


# App Class
class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Countdown Timer')
        self.geometry('1000x350')
        self.resizable(False, False)
        self.listOfTasks = []
        self.currentTaskIndex = 0
        self._paused = False
        self.restartIndex = 0

        # Configure grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.create_widgets()
    

    # Creates all needed widgets for the GUI
    def create_widgets(self):

        # Menu bar
        self.menuBar = Menu(self)
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label='Import', command=self.importCSV)
        self.fileMenu.add_command(label='Export', command=self.exportCSV)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        self.config(menu=self.menuBar)

        # Timer frame
        self.timerFrame = LabelFrame(self, text='Timer', labelanchor='n', borderwidth=2, width=500, height=280)
        self.timerFrame.grid(row=0, column=0, rowspan=2, sticky='n', padx= 20)
        self.timerFrame.grid_propagate(False)

        self.timerFrame.columnconfigure(0, weight=1)
        self.timerFrame.columnconfigure(1, weight=1)
        self.timerFrame.columnconfigure(2, weight=1)
        self.timerFrame.rowconfigure(0, weight=1)
        self.timerFrame.rowconfigure(1, weight=1)

        # Timer label
        self.timerLabel = Label(self.timerFrame,text="00:00:00",font=("",50))
        self.timerLabel.grid(column=0, row = 0, columnspan=3)

        startButtonImage = PhotoImage(file="Timer-Images/Play1.png")
        stopButtonImage = PhotoImage(file="Timer-Images/stop.png")
        restartButtonImage = PhotoImage(file="Timer-Images/restart.png")
        nextButtonImage = PhotoImage(file="Timer-Images/next.png")

        # Timer buttons
        self.startButton = Button(self.timerFrame, text='Start', command=self.startTimer, image=startButtonImage, border=0)
        self.startButton.grid(column=0, row = 1)
        self.startButton.Image=startButtonImage

        self.stopButton = Button(self.timerFrame, text='Stop', command=self.stopTimer, image=stopButtonImage, border=0)
        self.stopButton.grid(column=1, row = 1)
        self.stopButton.Image=stopButtonImage

        self.restartButton = Button(self.timerFrame, text='Skip', command=self.skipTimer, image=nextButtonImage, border=0)
        self.restartButton.grid(column=2, row = 1)
        self.restartButton.Image=nextButtonImage

        # Task frame
        self.taskFrame = LabelFrame(self, text='Tasks', labelanchor='n', borderwidth=2, width=500, height=100)
        self.taskFrame.grid(row=0, column=1, rowspan=2, padx= 20, sticky="n")
        self.taskFrame.grid_propagate(False)

        # Presents the task box
        self.taskLabel = Label(self.taskFrame, text='Task',width=10)
        self.taskLabel.grid(row=0, column=0)

        # Gets the task box information
        self.task = Entry(self.taskFrame, width=10)
        self.task.grid(row=1, column=0, padx= 10)

        # Spinbox can increase and decrease the time for the hours
        self.hourInput = Spinbox(self.taskFrame, from_= 0, to= 24, incr = 1, width ="10")
        self.hourInput.grid(row=1, column=1)

        # Hour task box 
        self.hourLabel = Label(self.taskFrame, text=u'Hours', font=('', 11))
        self.hourLabel.grid(row=0, column=1)
      
        # Spinbox can increase and decrease the time for the minutes
        self.minuteInput = Spinbox(self.taskFrame, from_ = 0, to = 59, incr = 1, width="10")
        self.minuteInput.grid(row=1, column=2)
       
        # Minute task box
        self.minuteLabel = Label(self.taskFrame,text=u'Minutes',font=('', 11))
        self.minuteLabel.grid(row=0, column=2)
        
        # Spinbox can increase and decrease the time for the seconds
        self.secondInput = Spinbox(self.taskFrame, from_ = 0, to = 99, incr = 1, width="10")
        self.secondInput.grid(row=1, column=3)
       
        # Second task box
        self.secondLabel = Label(self.taskFrame,text=u'Seconds',font=('', 11))
        self.secondLabel.grid(row=0, column=3)

        # Add task button to add a new task
        taskButton = Button(self.taskFrame, text='Add Task', command=self.addTask)
        taskButton.grid(row = 1, column=4)

        # Extend the time to the current task
        self.updateButton = Button(self.taskFrame, text='Extend', command=self.updateTimer)
        self.updateButton.grid(column=4, row = 4)

        # Restarts the tasks
        self.restartTasks = Button(self.taskFrame, text='Restart Tasks', command=self.restartTasks)
        self.restartTasks.grid(row=1, column=5)

        # Task box frame
        self.taskFrame = LabelFrame(self, text='Tasks', labelanchor='n', borderwidth=2, width=500, height=100)
        self.taskFrame.grid(row=1, column=1, rowspan=2, padx= 20, sticky="n")
        self.taskFrame.grid_propagate(False)

        # Total time
        self.totalTimeLabel = Label(self.taskFrame,text="Total Time: 00:00:00")
        self.totalTimeLabel.pack()

        # Task box to hold tasks
        self.tasksListbox = tkinter.Listbox(self.taskFrame, height=10, width=80)
        self.tasksListbox.pack()

        # Add the current datetime by Anh Huy Nguyen
        self.w = Label(text=f"{dt.datetime.now():%a, %b %d %Y}", fg="black", font=("helvetica", 12)).place(x=20, y = 295)
        def clock():
            clockTime = time.strftime('%H:%M:%S %p')
            currTimeLabel.config(text = clockTime)
            currTimeLabel.after(1000,clock)

        currTimeLabel = Label( font ='helvetica 12', text = '')
        currTimeLabel.place(x = 150 , y = 295)
        clock()
       

    # Adds the current task to a list of tasks and also added to the entry box.
    def addTask(self):
        newTask = self.taskMaker()
        new_entry = self.stringFormat()

        #Adding to the listbox if there is a name and some time input
        if newTask.name != "" and (newTask.hours != "0" or newTask.minutes != "0" or newTask.seconds != "0"):
            self.listOfTasks.append(newTask)
            self.tasksListbox.insert(tkinter.END, new_entry)  
            self.totalTimeLabel.config(text='Total Time: ' + self.calcTotalTaskTime())
            
        #Display a warning message when above requirements havent been met
        else:
            tkinter.messagebox.showwarning(title="Warning!", message="You must enter a task!")
            

    # Skip the task to the next task
    def skipTimer(self):
        self.listOfTasks[self.currentTaskIndex].setRemainingTime(-1)
        self.timerLabel.configure(text='00:00:00')
        

    # Update the time of the current task.
    def updateTimer(self):
        tmpTask = self.taskMaker()
        self.listOfTasks[self.currentTaskIndex].hours = int(self.listOfTasks[self.currentTaskIndex].hours) + \
            int(tmpTask.hours)

        self.listOfTasks[self.currentTaskIndex].minutes = int(self.listOfTasks[self.currentTaskIndex].minutes) + \
            int(tmpTask.minutes)

        self.listOfTasks[self.currentTaskIndex].seconds = int(self.listOfTasks[self.currentTaskIndex].seconds) + \
            int(tmpTask.seconds)

        self.listOfTasks[self.currentTaskIndex].remainingTime = int(self.listOfTasks[
            self.currentTaskIndex].remainingTime) + self.secondsConverter(tmpTask.hours, tmpTask.minutes, tmpTask.seconds)

        self.tasksListbox.delete(self.currentTaskIndex)

        strNewTask = "Task:" + \
            self.listOfTasks[self.currentTaskIndex].name + "   Hours:" + \
            str(self.listOfTasks[self.currentTaskIndex].hours) + \
            "   Minutes:" + \
            str(self.listOfTasks[self.currentTaskIndex].minutes) + \
            "   Seconds:" + \
            str(self.listOfTasks[self.currentTaskIndex].seconds)
            
        self.tasksListbox.insert(self.currentTaskIndex, strNewTask)
        
         
    # Gets all the input values from the user and makes a task object
    def taskMaker(self):
        taskName = self.task.get()
        hours = self.hourInput.get()
        minutes = self.minuteInput.get()
        seconds = self.secondInput.get()
        newTask = Task(taskName, hours, minutes, seconds, -1)

        return newTask

    # Converts time into seconds
    def secondsConverter(self, hours, minutes, seconds):
        intHours = int(hours)
        intMinutes = int(minutes)
        intSeconds = int(seconds)

        self.converted = (intHours * 3600) + (intMinutes * 60) + intSeconds

        return self.converted 


    # Restarts the tasks
    def restartTasks(self):
        self.restartIndex = 0
        self.currentTaskIndex = 0

        while self.restartIndex < len(self.listOfTasks):
            self.listOfTasks[self.restartIndex].setRemainingTime(-1)
            self.restartIndex += 1

        self.startTimer()


    # Stop current task timer
    def stopTimer(self):
        self._paused = True

   
    #Loops through the list of task objects to display the count down for each one
    def startTimer(self):
        if self._paused ==  True:
            self._paused =  False

        if self.currentTaskIndex < len(self.listOfTasks):

            if self.listOfTasks[self.currentTaskIndex].getRemainingTime() > -1:
                self.updateClock()

            else:
                hours = self.listOfTasks[self.currentTaskIndex].getHours()
                minutes =  self.listOfTasks[self.currentTaskIndex].getMinutes()
                seconds =  self.listOfTasks[self.currentTaskIndex].getSeconds()
                self.listOfTasks[self.currentTaskIndex].setRemainingTime(self.secondsConverter(hours, minutes, seconds))

                self.updateClock()


    #Formats the task into a string to be presented in the listbox
    def stringFormat(self):
        taskName= self.task.get()
        hours = self.hourInput.get()
        minutes = self.minuteInput.get()
        seconds = self.secondInput.get()

        stringconcat = "Task:" + str(taskName) + "   Hours:"+ str(hours) + "   Minutes:" + str(minutes) + "   Seconds:" + str(seconds)

        return stringconcat


    # Updates the clock after 1 second until time is up
    def updateClock(self):
        TimeInProgress = self.listOfTasks[self.currentTaskIndex].getRemainingTime()

        if self._paused == True:
                self.listOfTasks[self.currentTaskIndex].setRemainingTime(TimeInProgress)

        elif TimeInProgress > -1:
            mins,secs = divmod(TimeInProgress,60)
            tempHour = 0

            if mins>59:
                tempHour, mins = divmod(mins,60)

            timeformat = "{0:02d}:".format(tempHour)+("{0:02d}:{1:02d}".format(mins,secs))
            
            self.timerLabel.configure(text=timeformat)
            self.listOfTasks[self.currentTaskIndex].setRemainingTime(TimeInProgress - 1)
            self.after(1000, self.updateClock)
                
        else:
            tkinter.messagebox.showinfo("Time Countdown", "Time's up!")

            self.currentTaskIndex += 1
            self.startTimer()


    # Provides a dialog box to import a csv file
    def importCSV(self):
        self.tasksListbox.delete(0, END)
        self.listOfTasks = []
        
        filePath = filedialog.askopenfilename(filetypes=(('csv', '.csv'),), defaultextension=(('csv', '*.csv'),))

        with open(filePath, 'r') as f:
            reader = csv.reader(f)

            for row in reader:
                self.listOfTasks.append(Task(row[0], row[1], row[2], row[3]))
        
        for task in self.listOfTasks:
            newEntry = "Task:" + str(task.getName()) + "   Hours:"+ str(task.getHours()) + "   Minutes:" + str(task.getMinutes()) + "   Seconds:" + str(task.getSeconds())
            self.tasksListbox.insert(tkinter.END, newEntry)
        
        self.totalTimeLabel.config(text='Total Time: ' + self.calcTotalTaskTime())
    

    # Provides a dialog box to export tasks to a csv file
    def exportCSV(self):
        filePath = filedialog.asksaveasfilename(filetypes=(('csv', '.csv'),), defaultextension=(('csv', '*.csv'),))

        try:
            with open(filePath, 'w', newline='') as f:
                writer = csv.writer(f)

                for task in self.listOfTasks:
                    writer.writerow([task.getName(), task.getHours(), task.getMinutes(), task.getSeconds()])

        except BaseException as e:
            print('BaseException:', filePath)

        else:
            tkinter.messagebox.showinfo("Export", "Tasks exported successfully!")

    
    # Calculates the total time and returns it in string format by Robbie Benson
    def calcTotalTaskTime(self):
        totalHours = 0
        totalMinutes = 0
        totalSeconds = 0

        # Get total times
        for task in self.listOfTasks:
            totalHours += int(task.getHours())
            totalMinutes += int(task.getMinutes())
            totalSeconds += int(task.getSeconds())

        # Convert to neede format
        totalMinutes,totalSeconds = divmod(totalSeconds,60)

        if totalMinutes>59:
            totalHours, totalMinutes = divmod(totalMinutes,60)

        totalTime = "{0:02d}:".format(totalHours)+("{0:02d}:{1:02d}".format(totalMinutes,totalSeconds))

        return totalTime
    

# Main
if __name__ == '__main__':
    app = App()
    app.mainloop()