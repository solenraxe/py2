#include <string>

namespace Extern {
    void runLine(std::string txt);
    std::string getConsole();
}

extern "C" void runLineC(const char* txt) {
    Extern::runLine(std::string(txt));
}

extern "C" const char* getConsoleC() {
    static std::string buffer;
    buffer = Extern::getConsole();
    return buffer.c_str();
}