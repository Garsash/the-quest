class Debug():
    printLog=[]
    counting={}
    def log(self,string):
        self.printLog.append(string)

    def clearLog(self):
        self.printLog=[]

    def print(self,clear=True):
        for x in self.counting.keys():
            if self.counting[x]["type"]=="tick":
                self.log(self.counting[x]["count"])
                self.resetCount(x)
        for x in self.printLog:
            print(x)
        if clear==True:
            self.clearLog()

    def beginCount(self,char,type="tick"):
        if not type in ["tick"]:
            raise ValueError(type, "is not a real counting type")
        self.counting[char]={"count":0, "type":"tick"}

    def resetCount(self,char):
        if not char in self.counting.keys():
            raise ValueError(char, "counter must be initialised")
        self.counting[char]["count"]=0

    def count(self, char, number=1):
        if not char in self.counting.keys():
            raise ValueError(char, "counter must be initialised")
        self.counting[char]["count"]+=number