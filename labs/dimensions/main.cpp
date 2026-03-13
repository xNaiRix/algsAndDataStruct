#include <iostream>
#include <string>
#include<format>

class Dimension
{
    int m;
    int l;
    int t;
    friend std::ostream& operator<<(
        std::ostream& out, const Dimension& dim);
 public:
    Dimension(int m, int l, int t):
     m(m), l(l), t(t){}
    Dimension()=default;
    
    
    static bool equalDimension(
        const Dimension& a, const Dimension& b)
    {
        return a.m == b.m &&
             a.l == b.l && a.t == b.t;
    }
    const bool operator== (const Dimension& other) const{
        return this->m == other.m &&
             this->l == other.l && this->t == other.t;
    } 

    const bool operator!= (const Dimension& other) const{
        return !((*this) == other);
    } 

    static Dimension multiplyDimension (
        const Dimension& a, const Dimension& b)
    {
        Dimension result;
        result.m = a.m + b.m;
        result.l = a.l + b.l;
        result.t = a.t + b.t;
        return result;
    }
    Dimension operator* (const Dimension& other) const{
        Dimension result;
        result.m = this->m + other.m;
        result.l = this->l + other.l;
        result.t = this->t + other.t;
        return result;
    } 

    static Dimension divideDimension(
        const Dimension& a, const Dimension& b)
    {
        Dimension result;
        result.m = a.m - b.m;
        result.l = a.l - b.l;
        result.t = a.t - b.t;
        return result;
    }
    Dimension operator/ (const Dimension& other) const{
        Dimension result;
        result.m = this->m - other.m;
        result.l = this->l - other.l;
        result.t = this->t - other.t;
        return result;
    } 

};
std::ostream& operator<<(
        std::ostream& out, const Dimension& dim){
            out << "M^" << dim.m
                      << " L^" << dim.l
                      << " T^" << dim.t;
        return out;
}

class Quantity;

class Unit
{
    std::string name;// короткое имя: "m", "kg", "s"
    Dimension dim;
    double factor;// коэффициент перевода в SI
    friend class Quantity;
 public:
    Unit() = default;
    Unit(std::string name,
         const Dimension& dim,
         double factor = 1.):
         name(name), factor(factor), dim(dim){}
    template<typename T>
    T calcValueSi(const T& value) const {
        return value * this->factor;
    }

};

class Quantity
{
    double valueSI;   // значение в СИ -- в будущем: другие представления числе - через базовый класс?
    Dimension dim;    // размерность

    friend std::ostream& operator<<(
        std::ostream& out, const Quantity& q);
 public:
    Quantity() = default;
    Quantity(double valueSI,
         const Dimension& dim):
         valueSI(valueSI), dim(dim){}
    Quantity(double value,
        const Unit& unit):
    valueSI(unit.calcValueSi(value)), dim(unit.dim){}
    std::string printWithDim(const Unit& unit) const{
        if (this->dim != unit.dim)
        {
            return "Ошибка: величину нельзя вывести"
              " в этой единице!";
        }

        double value = this->valueSI / unit.factor;
        return std::format("{} {}", value, unit.name);
    }


    Quantity operator-() const{
        double new_valueSI = -this->valueSI;
        Dimension new_dim = this->dim;
        return Quantity(new_valueSI, new_dim);
    }
    const Quantity& operator+() const{
        return (*this);
    }
        Quantity operator+(const Quantity& other ) const{
        if (this->dim != other.dim)
        {
            std::cout << "Ошибка: нельзя складывать"
            " величины разных размерностей!" << std::endl;
            exit(1);
        }

        double new_valueSI = this->valueSI + other.valueSI;
        Dimension new_dim = this->dim;
        return Quantity(new_valueSI, new_dim);
    }
    Quantity operator-(const Quantity& other ) const{
        return (*this) + (-other);
    }
    Quantity& operator+=(const Quantity& other ){
        (*this) = (*this) + other;
        return (*this);
    }
    Quantity& operator-=(const Quantity& other ){
        (*this) += (-other);
        return (*this);
    }

    Quantity operator*(const Quantity& other ) const{
        Quantity result;
        result.valueSI = this->valueSI * other.valueSI;
        result.dim = this->dim * other.dim;
        return result;
    }
    Quantity operator/(const Quantity& other ) const{
         if (other.valueSI == 0)
        {
            std::cout << "Ошибка: деление на ноль!" 
            << std::endl;
            exit(1);
        }
        Quantity result;
        result.valueSI = this->valueSI / other.valueSI;
        result.dim = this->dim / other.dim;
        return result;
    }
    Quantity& operator*= (const Quantity& other) {
        (*this) = (*this) * other;
        return (*this);
    }
    Quantity& operator/= (const Quantity& other) {
        (*this) = (*this) / other;
        return (*this);
    }


};

std::ostream& operator<<(
        std::ostream& out, const Quantity& q){
            out << q.valueSI << ' '
                <<  q.dim;
        return out;
    }

void tests(){
    Unit meter = Unit("m", Dimension(0, 1, 0), 1.0);
    Unit centimeter = Unit("cm", Dimension(0, 1, 0), 0.01);
    Unit second = {"s", Dimension(0, 0, 1), 1.0};
    Unit kilogramm = {"kg", Dimension(1, 0, 0), 1.0};
    Unit meters_in_second = {"m/s", Dimension(0, 1, -1)};
    Unit meters_in_second_in_second = 
        {"m/s^2", Dimension(0, 1, -2)};
    Unit newtons = {"N", Dimension(1, 1, -2)};
    Unit meter_cub = {"m^3", Dimension(0, 3, 0)};
    Unit kilogramms_in_meter_cub = 
        {"kg/m^3", Dimension(1, -3, 0)};
    std::cout <<std::endl << "2 m + 30 cm = " << 
    (Quantity(2., meter) + Quantity(30, centimeter)).
    printWithDim(meter);

    // std::cout <<std::endl << "2 kg + 3s = " << 
    // (Quantity(2., kilogramm) + Quantity(3., second)).
    // printWithDim(second);

    std::cout <<std::endl << "100 m / 20 s = " << 
    (Quantity(100., meter) / Quantity(20, second)).
    printWithDim(meters_in_second);

    std::cout <<std::endl << "10 m/s / 2 s = " << 
    (Quantity(10., meters_in_second) / Quantity(2, second)).
        printWithDim(meters_in_second_in_second);

    std::cout <<std::endl << "2 kg *  5 m/s^2 = " << 
    (Quantity(2., kilogramm) * 
        Quantity(5, meters_in_second_in_second)).
        printWithDim(newtons);

    std::cout <<std::endl << "4 kg /  0.002 m^3 = " << 
    (Quantity(4., kilogramm) /
        Quantity(0.002, meter_cub)).
        printWithDim(kilogramms_in_meter_cub);//
    
    std:: cout << std::endl<<"Tests done! Also need to"
            " check answers";

}
int main() {
    setlocale(LC_ALL, "ru");
    Unit meter = Unit("m", Dimension(0, 1, 0), 1.0);
    Unit centimeter = Unit("cm", Dimension(0, 1, 0), 0.01);
    Unit second = {"s", Dimension(0, 0, 1), 1.0};
    Unit kilogramm = {"kg", Dimension(1, 0, 0), 1.0};

    Quantity a = Quantity(2.0, meter);
    Quantity b = Quantity(200.0, centimeter);

    Quantity s = Quantity(100.0, meter);
    Quantity t = Quantity(20.0, second);
    Quantity v = s / t;

    std::cout<< "s: " << s << std::endl;
    std::cout<< "t: " << t << std::endl;
    std::cout<< "v: " << v << std::endl;
    // std::cout << a << std::endl; // 2
    // std::cout << b << std::endl; // 2

    Quantity x = Quantity(250.0, Unit("cm", Dimension(0,1,0), 0.01));
    std::cout << x.printWithDim( Unit("m", Dimension(0,1,0), 1.0));// 2.5 m

    tests();

    return 0;
}
