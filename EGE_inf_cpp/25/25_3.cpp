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
            if (i%2 == 0) {
                divs.push_back(i);
            }
            if ((n/i)%2 == 0) {
                divs.push_back(n/i);
            }
        }
        i += 1;
    }
    if (i*i == n && i%2 == 0) {
        divs.push_back(i);
    }
    if (divs.size() >=6) {
        ll ans = -1;
        for (auto& c: divs) {
            ans = max(ans, c);
        }
        return ans;
    }
    return -1;

}
int main() {
    setlocale(LC_ALL, "ru");
    int start = 977004;//==2 разл натур дел, не считая числа и 1
    int end = 977022;
    for (long long i = start; i <=end; i++) {
        ll ans = find_divs(i);
        if (ans == -1) {
            continue;
        }
        cout << i << " " << ans << endl;
    }

}