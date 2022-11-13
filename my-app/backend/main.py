#Michael Lion Aguillon
import flask
import json
import multiprocessing
import glob

Application= flask.Flask(__name__)

@Application.before_first_request
def START():
    ServerStarted()

@Application.route("/", methods= ["GET", "POST"])
def Home():
    return flask.render_template("index.html")

#@Application.route("/", methods= ["POST"])
#def

def ServerStarted():
    ALLFILES= glob.glob("./Asteroids/*.csv")

    Manager= multiprocessing.Manager()
    ReturnDictionary= Manager.dict()

    print("Before Multiprocessing...")

    NumberofActiveProcesses= 0
    Processes= []
    for Index in range(len(ALLFILES)):
        if (NumberofActiveProcesses < 8):
            print("Multiprocessing...")
            
            DirectoryName= ALLFILES[Index][0:11]
            CurrentFileName= ALLFILES[Index][12:]
            CurrentFile= open(DirectoryName + "/" + CurrentFileName)
            Content= CurrentFile.read()

            CurrentProcess= multiprocessing.Process(target= RetreiveData, args= [Content])
            CurrentProcess.start()
            print("Process made!")

            Processes.append(CurrentProcess)
            NumberofActiveProcesses+= 1
        
        else:
            for CurrentProcess in Processes:
                CurrentProcess.join()
            NumberofActiveProcesses= 0

            print("Multiprocessing...")
            CurrentProcess= multiprocessing.Process(target= RetreiveData, args= ALLFILES[Index])
            CurrentProcess.start()
            print("Process made!")

            Processes.append(CurrentProcess)
            NumberofActiveProcesses+= 1
    for CurrentProcess in Processes:
        CurrentProcess.join()
    
    print("After Multiprocessing...")

    Output= open("Console.txt", "w")
    Output.write(str(ReturnDictionary))
    Output.close()

def RetreiveData(Content):
    ListofData= []
    CurrentMap= {}

    for Character in Content:
        Commas= 0
        Word= ""

        for Character in Content:
            if (Character == ','):
                Commas+= 1
            
            if (Commas == 1):
                CurrentMap["BIT_DEPTH"]= Word
                Word= ""
            
            elif (Commas == 2):
                CurrentMap["RATE_OF_PENETRATION"]= Word
                Word= ""
            
            elif (Commas == 3):
                CurrentMap["HOOK_LOAD"]= Word
                Word= ""
            
            elif (Commas == 4):
                CurrentMap["DIFFERENTIAL_PRESSURE"]= Word
                Word= ""
            
            elif (Commas == 5):
                CurrentMap["WEIGHT_ON_BIT"]= Word
                Word= ""
            
            elif (Commas == 6):
                CurrentMap["DRILL_BIT_ID"]= Word
                Word= ""
            
            elif (Character == '\n'):
                CurrentMap["DRILL_BIT_ID"]= Word
                Word= ""
                ListofData.append(CurrentMap)
                CurrentMap= {}
            
            else:
                Word+= Character
            Commas= 0
    if len(CurrentMap) > 0:
        ListofData.append(CurrentMap)

    return ListofData

if __name__ == '__main__':
    Application.run(debug= True, port= 5000)