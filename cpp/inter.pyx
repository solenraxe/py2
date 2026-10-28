cdef extern from "interpreter.h":
    void runLineC(const char* txt)

def runL(str txt):
    cdef bytes text = txt.encode("utf-8")
    runLineC(<const char*>text)