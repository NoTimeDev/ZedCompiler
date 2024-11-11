#include <iostream> 
#include <fstream> 
#include "nlohmann/json.hpp"
#include <string>
#include <cstdlib>
#include <cstring>

using json = nlohmann::json;

int main(int argc, char** argv){
    std::ifstream File("Build.json");
    if(!File.is_open()){
        std::cerr << "\033[91mError:\033[97m No Build File, Build Expects A \"Build.json\" File\033[0m" << std::endl;
        exit(1);
    }

    json Data;
    File >> Data;

    std::string Command = "";

    auto Compiler = Data.find("Compiler");
    if(Compiler == Data.end()){
        std::cerr << "\033[91mError:\033[97m No Compiler Specified\033[0m" << std::endl;
        exit(1);
    }
    Command+=*Compiler;
    
    auto Options = Data.find("Options");
    if(Options != Data.end()){
        for(auto i : *Options){
            Command.append(" ");
            Command.append(i);
        }
    }

    auto Files = Data.find("Files");
    if(Files != Data.end()){
        for(auto i : *Files){
            Command.append(" ");
            Command.append(i);
        }
    }


    auto Name = Data.find("Exe");
    if(Name == Data.end()){
        std::cerr << "\033[91mError:\033[97m No ExeName Specified\033[0m" << std::endl;
        exit(1);        
    } 

    Command.append(" -o ");
    Command.append(*Name);

    auto Flags = Data.find("Flags");
    if(Flags != Data.end()){
        for(auto i : *Flags){
            Command.append(" ");
            Command.append(i);
        }
    }

    system(Command.c_str());
}
