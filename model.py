import time, threading, os
    

class MutiThreadReadLog(object):
    def __init__(self, parent, filename, **kwargs):
        self.parent = parent
        self.filename = filename
        self.kwargs = kwargs
        self.threads = []
        
        
        
    def readLog(self):
        count = len(self.threads)
        print(count)
        hasread = 0
        while True:
            time.sleep(0.1)
            if not os.path.exists(self.filename):
                continue
            with open(self.filename, 'r') as file:
                print('hasread1:'+str(hasread))
                file.seek(hasread)
                self.parent.displaylog(file.read())
                hasread = file.tell()
                print('hasread2:'+str(hasread))

            for i in range(len(self.threads)):
                if not self.threads[i].is_alive():
                    count -= 1 
                print('count:'+str(count))
                if count == 1:                
                    #剩下的这个进程为读日志线程
                    return self.parent.displaylog("导数已成功完成，日志读取也即将结束!!")                
                  
            
    def start(self):
        for k in self.kwargs:
            if k.startswith('thread'):   
                t1 = threading.Thread(target=self.kwargs[k])
                self.threads.append(t1)
        t2 = threading.Thread(target=self.readLog)
        self.threads.append(t2)                

  
        for t in self.threads:
                t.setDaemon(True)
                t.start()           
            

if __name__ == "__main__":        
    #starttime = datetime.datetime.now()
    #total_row = len(os.listdir(outdir))
    #endtime = datetime.datetime.now()
    #print u"速度：" + str(total_row / (1 if (endtime - starttime).seconds == 0 else (endtime - starttime).seconds)) + u"张/秒"
    print("goo.....")
