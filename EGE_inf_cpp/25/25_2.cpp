#include <iostream>
#include<vector>
#include<algorithm>
using namespace  std;
using ll = long long;
ll find_divs(long long n) {
    vector<ll> divs;
    long long i = 2;
    while (i*i < n) {
        if (n%i == 0) {
            if (i%100 == 14 && i!= 14) {
                divs.push_back(i);
            }
            if ((n/i)%100 == 14 && (n/i)!= 14) {
                divs.push_back(n/i);
            }

        }

        ++i;
    }
    if (i*i == n) {
        if (n%i == 0 && i%100 == 14 && i!= 14) {
            divs.push_back(i);
        }
    }
    if (not divs.empty()){
        ll ans = n;
        for (auto& c : divs) {ans= min(ans,c);}
        return ans;
    }
    return -1;
}


int main() {
    setlocale(LC_ALL, "ru");
    ll start = 800000;
    ll end = 2000000;
    int cnt = 0;
    for (long long i = start, cnt = 0; i <end, cnt < 5; i++) {
        ll ans = find_divs(i);
        if (ans == -1) {
            continue;
        }
        ++cnt;
        cout << i << " " << ans << endl;
    }


}