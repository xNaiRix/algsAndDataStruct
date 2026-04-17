#include <iostream>
#include<vector>
#include <algorithm>
#include<iomanip>
#include<numeric>
#include<exception>
void ReadNumbers(std::vector<float>& arr){
    float x;
    while (std::cin>>x){
        arr.push_back(x);
    }
    if (std::cin.eof()){}
    else if (std::cin.fail()) {
        std::cout << "ERROR" << std::endl;
        std::cin.clear();
        exit(0);
    }
}
void ProcessNumbers(std::vector<float>& arr){
    float sum = std::accumulate(arr.begin(), arr.end(), 0.0f,
                     [](float acc, float x)
                        { return x > 0 ? x + acc : acc;});
    int count_positive = std::count_if(arr.begin(), arr.end(),
        [](float x) { return x > 0; }
    );
    float average = 0.;
    if (count_positive != 0){
        average = sum/count_positive;
    }
    for(auto& c : arr){ c += average;}
    std::sort(arr.begin(), arr.end());
}
void PrintSortedNumbers(std::vector<float>& arr){
    std::cout << std::fixed << std::setprecision(3);
    for(float& c:arr){
        std::cout << c << ' ';
    }
}

int main(){
    std::vector<float> arr;
    ReadNumbers(arr);
    ProcessNumbers(arr);
    PrintSortedNumbers(arr);


    
}