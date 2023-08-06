#coding=utf8
import Queue
import threading
import contextlib
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ExcutorMgr(threading.Thread):
    def __init__(self,cnt=1,name=''):
        threading.Thread.__init__(self) 
        self.thread_stop = False
        self.name = name
        self.q=Queue.Queue()
        if cnt <= 0:
            cnt = 1
            self.thredList = []
            self.thredList.append(Excutor("#0"))
            self.curCnt = 1
        else:
            self.cnt = cnt
            self.curCnt = 0
            self.thredList = []
        self.index=0
        self.start()
    def run(self):
        while not self.thread_stop:             
            if self.q.qsize()>0:
                executor = self.getAvalExecutor()
                if executor != None:
                    job = self.q.get()                    
                    executor.execute(job)

            time.sleep(0.1)

    def wait(self):
        while not self.thread_stop:
            time.sleep(0.1)
            jobclear = False
            executorRunning = False
            if self.q.qsize() == 0:
                jobclear = True
            for i in range(0,self.curCnt):
                if self.thredList[i].isExecuting:
                    executorRunning = True
            if jobclear and not executorRunning:
                break
        self.stop()

    def stop(self):     
        for i in range(0,self.curCnt):
            self.thredList[i].stop()
        self.thread_stop = True 

    def getAvalExecutor(self):
        executor = None
        for i in range(0,self.curCnt):
            if not self.thredList[i].isExecuting:
                executor = self.thredList[i]
                # print dir(executor)
                # print 'find one thread execute'
                break
        if executor == None:
            if self.curCnt < self.cnt:
                self.thredList.append(Excutor("#%d"%self.curCnt))
                self.curCnt+=1
                executor = self.thredList[self.curCnt-1]
                # print 'new thread execute'            
        return executor


    def execute(self,job):
        self.q.put(job)
        
    def toString(self):
        ret = 'ExcutorMgr(%s) now has %d Executors'%(self.name,self.curCnt)

        for i in range(0,self.curCnt):
            executor = self.thredList[i]
            ret += '\n\t%s'%(executor.toString())
        return ret

class Job(object):
    def __init__(self, func, params):    
        self.func = func
        self.params = params
    def call(self):
        return self.func(self.params)
class Excutor(threading.Thread):

    def __init__(self,name=''):
        threading.Thread.__init__(self) 
        self.thread_stop = False
        self.job = None        
        self.name = name
        self.isExecuting = False#for executormgr
        self.isRunning = False#for executor
        self.start()

    def execute(self,job):
        self.isExecuting = True
        self.job = job

    def run(self): #Overwrite run() method, put what you want the thread do here 
        while not self.thread_stop: 
            if not self.isRunning and self.job != None:
                self.isRunning = True
                res = self.job.call()
                self.isRunning = False
                self.job = None
                self.isExecuting = False
                

            time.sleep(0.1) 

    def stop(self): 
        self.thread_stop = True 
        self._Thread__stop()

    def toString(self):
        show  = 'no'
        if  self.isRunning :
            show = 'has'
        return "executor(%s) now running %s jobs"%(self.name,show)


def test2(t):
    print 'sleep start'
    time.sleep(t)
    print 'sleep over'

def test():
    startTime = time.time()
    t = ExcutorMgr(4,"mgr")
    
    t.execute(Job(test2,4))
    t.execute(Job(test2,4))
    
    t.execute(Job(test2,4))
    t.execute(Job(test2,4))
    t.execute(Job(test2,4))
    t.execute(Job(test2,4))
    t.execute(Job(test2,4))
    time.sleep(1)
    print t.toString()
    t.stop() 
    # t.wait()
    print 'task done',time.time() - startTime


# test()