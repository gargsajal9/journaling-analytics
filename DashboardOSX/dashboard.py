import os
import json
import time, thread
from LogParser import parse
import subprocess32
import urllib
from collections import OrderedDict
import logging
import re
import datetime,requests
from summary import downloadTika
import summary
import cPickle as pickle

UNCATAGORISED_TAG='Untagged'
DASHBOARD_LOG_FILE = os.environ['HOME']+ "/Documents/OSXInstrumenterLogs/dashboard.log"
DASHBOARD_LOG_FOLDER=os.environ['HOME']+ "/Documents/OSXInstrumenterLogs/"
FILES_FILTER_LIST = ['.swp','.log','.pyc','.dat','.lck','.xcuserstate']
URL_FILTER_LIST=['localhost:5000','Safari.app','chrome://','topsites://']
UNITYID_ENV_VAR = 'UNITYID'
compliled_patterns = list()
DASHBOARD_VERSION="0.7"
DOCUMENT_UPLOAD_URL='http://las-goal-web.oscar.ncsu.edu:3000/api/docevent'

state=OrderedDict()
actions=[]


SKYLR_URL = "https://las-skylr-token.oscar.ncsu.edu/api/data/document/query"
SKYLR_GOALLIST_URL='https://las-journaling-token.oscar.ncsu.edu/shib/user'
SKYLE_UPDATE_URL = "https://las-skylr-token.oscar.ncsu.edu/api/data/document/add/split-task"
AUTH_TOKEN="6479b23519a262e696508e7b8b1156de33c56430072f94a3f6dd92b430c624d2"

startTime=(int(datetime.datetime.now().strftime("%s")) - 60*60*24*3)*1000
endTime=int(datetime.datetime.now().strftime("%s"))*1000

"""
def getEventsfromLog():
    with open(os.environ['HOME']+"/Documents/OSXInstrumenterLogs/console.log") as file:
        res=[]
        for line in file:
            e = parse(line)
            if e['type']=="event":
                jobj = json.loads(e['json'])
                a={}
                a['app']=jobj['content']['AppName']
                a['event']=jobj['content']['EvtDesc']
                #res.append([jobj['content']['AppName'],jobj['content']['EvtDesc']])
                res.append(a)
                #print (jobj['content']['AppName'],jobj['content']['EvtDesc'])
        return json.dumps(res)

"""

INSTRUMENTOR_LOG = os.environ['HOME']+ "/Documents/OSXInstrumenterLogs/console.log"

def startReading():
    f = open(INSTRUMENTOR_LOG, 'r')
    while True:
        line = ''
        while len(line) == 0 or line[-1] != '\n':
            tail = f.readline()
            if tail == '':
                time.sleep(0.1)          # avoid busy waiting
                # f.seek(0, io.SEEK_CUR) # appears to be unneccessary
                continue
            line += tail
        processLine(line)
    

def processLine(lines):
    #print lines
    #print "============================================="
    lines = lines.split('\n')
    for line in lines:
        #print line
        event = parse(line)
        if event:
            #print event
            updateState(event)


def updateState(event):

    if event['EvtType'] in ['FileAccessed','FileCreated','FileRenamed','FileModified']:
    #File event    
        #task = event['TaskName']   Not reading from the log
        fileName = event['EvtDesc'].replace('\/','/')
        app = event['AppName']
        eventType='file'

        if FilterFile(fileName):
            return
        if fileName==None or fileName=="" or fileName=="Application":
            return
        
        tasks = getAllTagsByFile(fileName)
        tasks.append(UNCATAGORISED_TAG)
        logging.info("File "+ fileName+ " udated at "+str(event['EvtTime']) )

    elif event['WebDomain'] !='Unknown' and event['WebDomain'] !='' and event['EvtDesc'] in ['Activated','CurrentDomain']:

        #task=event['TaskName']    Not reading from the log
        fileName=event['WebDomain']
        app = event['AppName']
        eventType='url'

        if UrlFilter(fileName):
            return

        tasks = getAllTagsByFile(fileName)
        tasks.append(UNCATAGORISED_TAG)
    else:
        return

    for task in tasks:
        if task not in state:
            state[task]=OrderedDict()
            state[task]['data']=OrderedDict()
        state[task]['data'][fileName]=({'AppName':app, 'EvtTime':event['EvtTime'], 'type':eventType})
        getCollaborateUsersForTaskFromSkylr(task)
        state[UNCATAGORISED_TAG]['collaborators'] = []
        SortSingleTask(task)
    SortAllTasks()

def saveStateToDisk():
    with open("state","w") as stateFile:
        pickle.dump(state,stateFile)

def readStateFromDisk():
    if os.path.isfile("state"):
        with open("state","w") as stateFile:
            savedState=pickle.load(stateFile)
            state=savedState

def addToActions(actionTuple):
    global actions
    actions.append(actionTuple)
    with open(DASHBOARD_LOG_FOLDER+"dashboard-actions.dat","w") as actionsFile:
        pickle.dump(actions,actionsFile)

def readActions():
    global actions
    if os.path.isfile(DASHBOARD_LOG_FOLDER+"dashboard-actions.dat"):
        with open(DASHBOARD_LOG_FOLDER+"dashboard-actions.dat","rb") as actionsFile:
            actions=pickle.load(actionsFile)
            for action in actions:
                eventType = 'file' if action[3] is 1 else 'url'
                if action[2]==1:
                    if action[0] not in state:
                        state[action[0]]=OrderedDict()
                        state[action[0]]['data']=OrderedDict()
                    state[action[0]]['data'][action[1]]=({'AppName':None, 'EvtTime':action[4], 'type':eventType})
                    logging.info("Updated action for "+action[1])
                    SortSingleTask(action[0])
                else:
                    if action[0] in state:
                        if action[1] in state[action[0]]['data']:
                            del state[action[0]]['data'][action[1]]
                    SortSingleTask(action[0])       
        SortAllTasks()
    else:
        logging.info("No saved actions found")


def SortSingleTask(task):
    state[task]['data'] = OrderedDict(sorted(state[task]['data'].iteritems(), key=lambda x: x[1]['EvtTime'],reverse=True))

def SortAllTasks():
    global state
    #temp = OrderedDict( sorted(state.iteritems(), key=lambda i: next(i[1].iteritems())[1]['EvtTime'] , reverse=True))
    temp = sorted(state.iteritems(),cmp=StateSortComparator)
    #print temp
    #state = temp
    state = OrderedDict()
    for i in temp:
        state[i[0]]=i[1]
    #Untagged should be in the last
    if UNCATAGORISED_TAG in state:
        temp = state[UNCATAGORISED_TAG]
        del state[UNCATAGORISED_TAG]
        state[UNCATAGORISED_TAG] = temp


def StateSortComparator(task1,task2):
    #print task1
    #print task2

    try:
        if next(task1[1]['data'].iteritems())[1]['EvtTime'] > next(task2[1]['data'].iteritems())[1]['EvtTime']:
            return -1
        else:
            return 1
    except StopIteration:
        return 0


def printState():
    while True:
        time.sleep(5)
        for tag,files in state.items():
            files = files['data']
            print "Task:",tag
            for fileName,details in files.items():
                print fileName,details['AppName'],details['EvtTime']
            print '---------------------------------------------------'
        print "***********End of State***********"
        

def getState():
    return state;

def openFile(filepath):
    #filepath=urllib.unquote(filepath).decode('utf8') 
    filepath = filepath.replace(":","/")
    #subprocess32.Popen(['open',re.sub(" ","\ ",filepath)])
    subprocess32.Popen('open "'+filepath+'"', shell=True)

def openInBrowser(filepath):
    filepath = filepath.replace(":","/")
    #subprocess32.Popen(['open','-R',re.sub(" ","\ ",filepath)], shell=True)
    subprocess32.Popen('open -R "'+filepath+'"', shell=True)

def AddTag(filepath,tag):
    filepathWithColon=filepath
    filepath = filepath.replace(":","/")
    #subprocess32.call(['tracker-control','-f',filepath])
    subprocess32.Popen(['tag',"-a",tag,re.sub(" ","\ ",filepath)], shell=True)
    subprocess32.Popen('tag -a '+ tag +' "'+filepath+'"', shell=True)
    if tag not in state:
        state[tag]=OrderedDict()
        state[tag]['data']=OrderedDict()
    state[tag]['data'][filepath] = getFileDetailsByName(filepath)
    if filepath in state[UNCATAGORISED_TAG]:
    	del state[UNCATAGORISED_TAG]['data'][filepath]
    SortSingleTask(tag)
    SortAllTasks()
    updateEventsToSkylr("AddTask",filepathWithColon,tag)
    addToActions((tag,filepath,1,1,state[tag]['data'][filepath]['EvtTime']))

def RemoveTag(filepath,tag):
    filepathWithColon=filepath
    filepath = filepath.replace(":","/")
    #subprocess32.Popen(['tag',"-r",tag,re.sub(" ","\ ",filepath)], shell=True)
    subprocess32.Popen('tag -r '+ tag +' "'+filepath+'"', shell=True)
    EvtTime = state[tag]['data'][filepath]['EvtTime']
    del state[tag]['data'][filepath]
    updateEventsToSkylr("RemoveTask",filepathWithColon,tag)
    addToActions((tag,filepath,0,1,EvtTime))

def RemoveTagURL(url,tag):
    EvtTime = state[tag]['data'][url]['EvtTime']
    temp=state[tag]['data'][url]
    del state[tag]['data'][url]
    updateEventsToSkylr("RemoveTask",url,tag)
    addToActions((tag,url,0,0,EvtTime))

def AddTagURL(url,tag):
    if tag not in state:
        state[tag] = OrderedDict()
        state[tag]['data'] = OrderedDict()
    state[tag]['data'][url]=getFileDetailsByName(url)
    if url in state[UNCATAGORISED_TAG]['data']:
    	del state[UNCATAGORISED_TAG]['data'][url]
    SortSingleTask(tag)
    SortAllTasks()
    updateEventsToSkylr("AddTask",url,tag)
    addToActions((tag,url,1,0,state[tag]['data'][url]['EvtTime']))

def getFileDetailsByName(filename):
    for task,allTags in state.iteritems():
        filelist = allTags['data']
        if filename in filelist:
            return filelist[filename]
    logging.warn(filename+" not found")
    return False

def getAllTagsByFile(filename):
    ret=[]
    for task,allTags in state.iteritems():
        filelist = allTags['data']
        if filename in filelist:
            ret.append(task)
    try:
        ret.remove(UNCATAGORISED_TAG)
    except:pass
    return ret # empty list if file not in state

def clearTag(tag):
    global state
    if tag in state:
        del state[tag]

def getUnity():
    if UNITYID_ENV_VAR in os.environ:
        return os.environ[UNITYID_ENV_VAR]

def openAll(tag):
    listOfURLs=[]
    if tag in state:
        for item,desc in state[tag]['data'].iteritems():
            if desc['type']=='file':
                filepath=item
                filepath = filepath.replace(":","/")
                #subprocess32.Popen(['open',re.sub(" ","\ ",filepath)], stderr=subprocess32.STDOUT, shell=True)
                subprocess32.Popen('open "'+filepath+'"', shell=True)
            else:
                listOfURLs.append(item)
    ret={}
    ret['listOfURLs']=listOfURLs
    return ret


def getURLsFromSkylr():
    global startTime,endTime
    headers = {'Content-Type':'application/json', 'AuthToken':AUTH_TOKEN}
    data= {"type":"find","query":{'data.UserId':os.environ[UNITYID_ENV_VAR], 'data.ProjId':"journaling-chrome", 'data.EvtTime':{'$gte':startTime,'$lte':endTime}}}
    startTime=endTime
    endTime=int(datetime.datetime.now().strftime("%s"))*1000
    #print data['query']['data.EvtTime']
    try:
        r = requests.post(SKYLR_URL,data=json.dumps(data),headers=headers)
        response = json.loads(r.text)
    except:
        logging.warn("HTTP connection ( for fetching URLs ) to Skylr failed")
        return   
    for i in response['data']:
        event = i['data']
        #print event
        if 'WebURL' in event and 'TaskName' in event:
            if event['WebURL'].startswith('http') and event['TaskName']!="":
                updateStateURL(state,event['WebURL'],formatTask(event['TaskName']),event['EvtTime'])


def getCollaborateUsersForTaskFromSkylr(task):
    taskList = task.split("_")
    headers = {'Content-Type':'application/json', 'AuthToken':AUTH_TOKEN}
    data= {"type":"find","query":{'data.TaskName':taskList, 'data.ProjId':"journaling-ubuntu"}}
    try:
        r = requests.post(SKYLR_URL,data=json.dumps(data),headers=headers)
        response = json.loads(r.text)
        allUsers = []
        for i in response['data']:
            if i:
                event = i['data']
                if 'UserId' in event:
                    allUsers.append(event['UserId'])

        allUsers = set(allUsers)
        if os.environ[UNITYID_ENV_VAR] in allUsers:
            allUsers.remove(os.environ[UNITYID_ENV_VAR])

        state[task]['collaborators'] = list(allUsers)
    except:
        logging.warn("HTTP connection ( for fetching URLs ) to Skylr failed for task "+task)
        return

def updateStateURL(state,url,task,time):
    if 'localhost:5000' in url:
        return
    if task not in state:
        state[task]=OrderedDict()
        state[task]['data']=OrderedDict()
    state[task]['data'][url]=({'AppName':"", 'EvtTime':time, 'type':'url'})
    SortSingleTask(task)
    SortAllTasks()

def formatTask(task):
    if task[0]==os.environ[UNITYID_ENV_VAR]:
        task.pop(0)
    return "_".join(task)


def fetchAndUpdateURLs():
    while(True):
        getURLsFromSkylr()
        time.sleep(10)

def updateEventsToSkylr(evtType,filepath,taskName):
    headers = {'Content-Type':'application/json', 'AuthToken':AUTH_TOKEN}
    evtTime=int(datetime.datetime.now().strftime("%s"))*1000
    data={"content":{"WebDomain":"Unknown","ProjId":"journaling-ubuntu","SysId":"Ubuntu 14.04.2 LTS","NetAddr":"::1","UserId":os.environ[UNITYID_ENV_VAR],"EvtTime":evtTime,"WebQuery":"Unknown","EvtType":evtType,"EvtDesc":filepath,"TaskDesc":"None","TaskName":taskName,"AppName":"JournalingDashboard","ProjVer":DASHBOARD_VERSION}}
    try:
        data=json.dumps(data)
        logging.info("Sending an event to Skylr")
        logging.info(data)
        r = requests.post(SKYLE_UPDATE_URL,data=data,headers=headers)
        logging.info("Skylr Event Update response "+r.text)
    except Exception, e:
        logging.warn("HTTP connection to Skylr failed")        

def updateGoalList():
    headers = { 'AuthToken':AUTH_TOKEN}
    try:
        logging.info("Fetching Goal list from Skylr")
        r = requests.get(SKYLR_GOALLIST_URL,headers=headers)
        #print r.text
        response = json.loads(r.text)
        goals = response['goals']
        with open('public/CSC591_advancedalgos_tasks.json','w') as goalfile:
            goalfile.write()
    except Exception,e:
        logging.warn("HTTP connection to Skylr failed")

def uploadDocument(filepath,task):
    ret={}
    ret['userid'] = os.environ[UNITYID_ENV_VAR]
    content = summary.getFileContents(filepath)
    if content==None: return None
    ret['filepath']=filepath
    ret['task']=task
    ret['content']=content

    # Todo: test this
    response = requests.post(DOCUMENT_UPLOAD_URL,data=json.dumps(ret),headers = {'Content-Type':'application/json'})
    #print 
    #print json.dumps(ret)   

    return True if response.text=='success' else False
    

def initDashboard():
    if UNITYID_ENV_VAR not in os.environ:
        print "Error: Please set the",UNITYID_ENV_VAR,"environment variable."
        exit(1)
    downloadTika()
    logging.basicConfig(format='%(asctime)s  %(levelname)s: %(funcName)s() -   %(message)s',filename=DASHBOARD_LOG_FILE, filemode='w', level=logging.DEBUG)
    thread.start_new_thread(startReading,())
    #time.sleep(2)
    #thread.start_new_thread(fetchAndUpdateURLs,())
    #fetchAndUpdateURLs()
    print "Dashboard server running..."
    #thread.start_new_thread(printState,())
    time.sleep(3)
    readActions()


def FilterFile(file):
    for pattern in FILES_FILTER_LIST:
        if file.endswith(pattern):
            logging.info("Filtered "+ file +" for " + pattern)
            return True
    return False

def UrlFilter(url):
    for pattern in URL_FILTER_LIST:
        if pattern in url:
            logging.info("Filtered "+ url +" for " + pattern)
            return True
    return False


if __name__ =="__main__":
    #thread.start_new_thread(printState,())
    #thread.start_new_thread(startReading,())
    #startReading()
    #openFile("%2Fhome%2Fpreems%2FDownloads%2FCOURSE-SCHEDULE.01.05.2015.pdf")
    updateGoalList()
    
