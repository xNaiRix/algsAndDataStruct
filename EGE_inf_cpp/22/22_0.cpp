#include <iostream>
#include <vector>
#include <algorithm>
#include <set>
#include <map>
#include <fstream>
#include<sstream>

using namespace std;
int main() {
    ifstream input("D:\\Sirius\\Informatics\\4sem\\EGE_inf_cpp\\22\\table.txt");
    map<int, pair<int, vector<int>>> d;
    string s;
    while (input) {
        getline(input, s);
        int i, t;
        vector<int> z;
        stringstream buffer(s);
        int z_el;
        char symb;
        buffer >> i >> t;
        while (buffer) {
            buffer >> z_el >> symb;
            z.push_back(z_el);
        }
        d[i] = make_pair(t, z);
    }
    set<int> verts, depends;
    for (auto [key, value] : d) {
        verts.insert(key);
    }
    for (auto [key, value] : d) {
        for (auto& c : value.second) {
            depends.insert(c);
        }
    }
    set<int> diff;
    set_difference(verts.begin(), verts.end(), depends.begin(), depends.end(),
        inserter(diff, diff.begin()));
    set <pair<int, int>> r;
    for (int i: diff) {
        r.insert(make_pair(d[i].first, i));
    }
    bool fl = false;
    pair<int, int> mn_el;
    for (const auto& [d_i0, i]: r) {
        if ( !fl) {
            fl = true;
            mn_el = make_pair(d_i0, i);
        }
        if (d_i0 == mn_el.first) {
            if (-i <= mn_el.second ) {
                mn_el = make_pair(d_i0, i);
            }
        }
        else if (d_i0 < mn_el.first) {
            mn_el = make_pair(d_i0, i);
        }
    }
    cout << mn_el.first << ' ' << mn_el.second;
}