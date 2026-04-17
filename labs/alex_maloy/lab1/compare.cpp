#include <iostream>
#include<fstream>
#include<string>
int main(int argc, char** argv){
    std::string filepath1, filepath2;
    try{
        filepath1 = argv[1];
        filepath2 = argv[2];
    }catch(std::exception){
        std::cout << "There are less then 2 files" << std::endl;
        return 1;
    }
    std::fstream f1, f2;
    f1.open(filepath1, std::ios::in);
    f2.open(filepath2, std::ios::in);
    bool equal = true;
    int i = 1;
    if (f1.is_open() && f2.is_open()){
        std::string line1, line2;
        while (std::getline(f1, line1))
        {
            if (! std::getline(f2, line2)|| !(line1 == line2)){
                equal = false;
                break;
            }
            ++i;
        }
        if (std::getline(f2, line2)){
            equal = false;
        }

    } 
    f1.close();
    f2.close();
    if (equal){
        std::cout << "Files are equal";
    } else {
        std::cout << "Files are different. Line number is " << i <<  std::endl;
        return 1;
    }
}