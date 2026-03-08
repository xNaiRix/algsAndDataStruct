#include <iostream>
#include<vector>
#include<algorithm>
using namespace  std;

pair<int,int> find_divs(long long n) {
    vector<int> divs;
    long long i = 2;
    while (i*i < n) {
        if (n%i == 0) {
            divs.push_back(i);
            divs.push_back(n/i);
        }
        i += 1;
    }
    if (i*i == n) {
        divs.push_back(i);
    }
    if (divs.size() == 2) {
        return {divs[0], divs[1]};
    }
    return {-1, -1};

}
int main() {
    setlocale(LC_ALL, "ru");
    int start = 174457;//==2 разл натур дел, не считая числа и 1
    int end = 174505;
    vector<pair<int, int>> divs;
    for (long long i = start; i <end; i++) {
        pair<int, int> ans = find_divs(i);
        if (ans.first == -1 && ans.second == -1) {
            continue;
        }
        if (ans.first > ans.second) {
            swap(ans.first, ans.second);
        }
        divs.push_back(ans);
        //cout << ans.first << " " << ans.second << endl;
    }
    sort(divs.begin(), divs.end(), [](pair<int, int> a, pair<int, int> b) {
        return a.first*a.second < b.first*b.second;
    });
    for (auto [a,b] : divs) {
        cout<< a << endl;
    }
    cout << endl;
    for (auto [a,b] : divs) {
        cout<< b << endl;
    }


}