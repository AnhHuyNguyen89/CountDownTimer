class Task():
    def __init__(self, name, hours, minutes, seconds, remainingTime = -1):
        self.name = name
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.remainingTime = remainingTime

    def getName(self):
        return self.name

    def getHours(self):
        return self.hours

    def getMinutes(self):
        return self.minutes

    def getSeconds(self):
        return self.seconds

    def getRemainingTime(self):
        return self.remainingTime

    def setRemainingTime(self, newTime):
        self.remainingTime = newTime

    def string(self):
        stringInformation = str(self.name) 
        return stringInformation
