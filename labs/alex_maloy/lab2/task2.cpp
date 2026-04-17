#include <string>
#include<iostream>
#include <vector>
std::string TrimBlanks(std::string const& str){
    std::string new_str = "";
    int first = -1;
    for(int i = 0; i < str.length(); ++i){
        if (str[i] == ' '){ first = i;}
        else {
            break;
        }
    }
    if (first == -1) {return str;}
    int last = str.length();

    for(int i = str.length() - 1; i >=0; --i){
        if (str[i] == ' '){ last = i;}
        else{
            break;
        }
    }
    for(int i = first + 1; i < last; ++i){
        new_str.push_back(str[i]); 
    }
    return new_str;
}
bool test(){
    std::vector<std::string> strings {"hello", " hello", "   hello", "hello ", "hello    ",
         " hello ", "     hello", " hello     ",
        " hello my frined", "hello my frined ", " hello my friend ", "   hello my friend", "hello my friend    ",
        "   hello my friend    "};
    bool fl = true;
        for(auto& str: strings){
            std::string new_str = TrimBlanks(str);
            std::cout << new_str << ' ';
            if (new_str.length() != 0 && (new_str[0] == ' ' || new_str.back() == ' ')){
                fl = false;
                //std::cout << "WRONG ON:" << str << " RESULT IS:" << new_str << "\n"; 
            }

        }
        return fl;
    
}
int main(){
    std::string str;
    // std::getline(std::cin, str);
    // str = TrimBlanks(str);
    // std::cout << str;
    std::cout << test();
}