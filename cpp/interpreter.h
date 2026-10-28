#include <string>

namespace Extern {
    void runLine(std::string txt);
}

extern "C" void runLineC(const char* txt) {
    Extern::runLine(std::string(txt));
}