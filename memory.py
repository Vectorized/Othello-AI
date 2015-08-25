def getMemoryUsedMB():
    try:
        import os, psutil
    except:
        return 0
    try:
        proc = psutil.Process(os.getpid())
        return proc.get_memory_info()[0] / float(2**20)
    except:
        try:
            proc = psutil.Process(os.getpid())
            return proc.get_memory()[0] / float(2**20)
        except:
            return 0
    return 0 
