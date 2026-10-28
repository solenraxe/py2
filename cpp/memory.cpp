#include <string>
#include <map>
using namespace std;

map<string, string> vars = {{"sConsole", "Console:"}};

void createVar(string varN) {
    vars[varN] = "";
}

void setVar(string varN, string varVal) {
    vars[varN] = varVal;
}

string& getVar(string varN) {
    //if(!vars[varN]) {createVar(varN);};
    return vars[varN];
}