#include <iostream>
#include<vector>
#include<algorithm>
using namespace  std;
using ll = long long;
pair<ll, ll> find_divs(long long n) {
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
    ll sum = 0;
    for (auto& c : divs) { sum += c;}
    if (sum > 460000) {
        return {divs.size(), sum};
    }
    return {-1,-1};

}
int main(){
    setlocale(LC_ALL, "ru");
    ll start = 135790;
    ll end = 163229;
    vector<ll> a;
    for (long long i = start, cnt = 0; i <=end, cnt < 5; i++) {
        pair<ll, ll> ans = find_divs(i);
        if (ans == make_pair((ll)-1, (ll)-1)) continue;
        a.push_back(ans.second);
        cout << ans.first<< "\n";// << ans.second << endl;
        ++cnt;
    }

    cout << endl;
    for (auto& c : a) {
        cout << c << "\n";
    }
}
