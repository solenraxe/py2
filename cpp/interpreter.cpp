#include <string>
#include <vector>
#include <map>
#include <functional>
#include <sstream>
#include <iostream>

using CmdFunc = std::function<void(const std::vector<std::string>&)>;
std::map<std::string, CmdFunc> commands;

void runPrint(const std::vector<std::string>& args) {
    std::cout << "Hello World!!" << '\n';
}

void runVar(const std::vector<std::string>& args) {
    std::cout << "Run Var" << '\n';
}

std::vector<std::string> splitString(std::string str, const char splitter) {
    std::vector<std::string> result;
    std::string current;
    int strSize = str.size();
    for(int i=0; i<strSize; i++) {
        if(str[i] == splitter) {
            if(current != "") {
                result.push_back(current);
                current = "";
            }
            continue;
        }
        current += str[i];
    }
    if(current.size() != 0) {
        result.push_back(current);
    }
    return result;
}

namespace Extern {
    void runLine(std::string txt) {
        auto args = splitString(txt, ' ');

        if (args.empty() || (txt.size() >= 2 && (txt.substr(0, 2) == "- " || txt.substr(0, 2) == "#"))) {
            return;
        }

        if(commands.count(args[0])) {
            commands[args[0]](args);
        } else {
            runVar(args);
        }
    }
}

int main() {
    commands["print"] = runPrint;
}