//#pragma once
#include"Dimension.h"

Dimension::Dimension(int m, int l, int t, int i):
     m(m), l(l), t(t), i(i){}
    
const bool Dimension::operator== (const Dimension& other) const{
    return this->m == other.m &&
        this->l == other.l && this->t == other.t;
} 

const bool Dimension::operator!= (const Dimension& other) const{
    return !((*this) == other);
} 

Dimension Dimension::operator* (const Dimension& other) const{
    Dimension result;
    result.m = this->m + other.m;
    result.l = this->l + other.l;
    result.t = this->t + other.t;
    return result;
} 


Dimension Dimension::operator/ (const Dimension& other) const{
    Dimension result;
    result.m = this->m - other.m;
    result.l = this->l - other.l;
    result.t = this->t - other.t;
    return result;
} 

std::ostream& operator<<(
        std::ostream& out, const Dimension& dim){
            out << "M^" << dim.m
                      << " L^" << dim.l
                      << " T^" << dim.t;
        return out;
}