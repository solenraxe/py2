cdef extern from "interpreter.h":
    void runLineC(const char* txt)
    cdef const char* getConsoleC()

def runL(str txt):
    cdef bytes text = txt.encode("utf-8")
    runLineC(<const char*>text)

def getCons():
    result = getConsoleC()
    r = <bytes>result
    return r