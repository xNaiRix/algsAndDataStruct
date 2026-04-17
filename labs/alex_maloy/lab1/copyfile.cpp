#include <iostream>
#include<fstream>
#include<string>
int main(int argc, char** argv){
    std::string filepath1, filepath2;
    try{
        filepath1 = argv[1];
        filepath2 = argv[2];
    }catch(std::exception){
        std::cout << "There is no input or no output file" << std::endl;
        return 1;
    }
    std::fstream in, out;
    in.open(filepath1, std::ios::in);
    out.open(filepath2, std::ios::out | std::ios::trunc);
    if (in.is_open() && out.is_open()){
        std::string line;
        while (std::getline(in, line))
        {
            out << line << std::endl;
        }

    } 
    in.close();
    out.close();
    std::cout << "\n\n\nFile has been written" << std::endl;
}