#include <iostream>
#include<fstream>
#include<string>
int main(int argc, char** argv){
    std::string filepath, text;
    try{
        filepath = argv[1];
        text = argv[2];
    }catch(std::exception){
        std::cout << "There are no file or no text to find" << std::endl;
        return 1;
    }
    std::fstream f;
    f.open(filepath, std::ios::in);
    int i = 1;
    bool found = false;
    if (f.is_open()){
        std::string line
        while (std::getline(f, line))
        {
            if(line == text)
            ++i;
        }

    } 
    f.close();
}