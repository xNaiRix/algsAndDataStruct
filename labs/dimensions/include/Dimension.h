#pragma once
#include <ostream>
class Dimension
{
    int m;
    int l;
    int t;
    int i;
    friend std::ostream& operator<<(
        std::ostream& out, const Dimension& dim);
 public:
    Dimension(int m, int l, int t, int i=0);
    Dimension()=default;
    const bool operator== (const Dimension& other) const;
    const bool operator!= (const Dimension& other) const;
    Dimension operator* (const Dimension& other) const;
    Dimension operator/ (const Dimension& other) const;

};
std::ostream& operator<<(
        std::ostream& out, const Dimension& dim);
