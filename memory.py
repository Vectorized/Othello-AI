def getMemoryUsedMB():
    try:
        import os, psutil
        proc = psutil.Process(os.getpid())
        return proc.get_memory_info()[0] / float(2**20)
    except:
        return 0
