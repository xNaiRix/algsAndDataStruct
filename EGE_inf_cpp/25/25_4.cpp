#include <iostream>
#include<vector>
#include<algorithm>
using namespace  std;
using ll = long long;
ll find_divs(long long n) {
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
    if (divs.size() ==4) {
        ll ans = 0;
        for (auto& c : divs) { ans += c;}
        return ans;
    }
    return -1;

}
int main() {
    setlocale(LC_ALL, "ru");
    ll start = 123456;//==2 разл натур дел, не считая числа и 1
    ll end = 1234560;
    vector<ll> a;
    for (long long i = start, cnt = 0; i <=end, cnt < 5; i++) {
        ll ans = find_divs(i);
        if (ans == -1) {
            continue;
        }
        a.push_back(ans);
        cout << i << "\n";// << ans << endl;
        ++cnt;
    }
    cout << endl;
    for (auto& c : a) {
        cout << c << "\n";
    }

}