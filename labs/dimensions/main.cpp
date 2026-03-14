#include <iostream>
#include <string>
#include<format>
#include <map>
#include <stdexcept>

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
    
    const bool operator== (const Dimension& other) const{
        return this->m == other.m &&
             this->l == other.l && this->t == other.t;
    } 

    const bool operator!= (const Dimension& other) const{
        return !((*this) == other);
    } 
    Dimension operator* (const Dimension& other) const{
        Dimension result;
        result.m = this->m + other.m;
        result.l = this->l + other.l;
        result.t = this->t + other.t;
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
    friend std::ostream& operator<< (std::ostream& out, const Unit& unit);
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
    std::string getName()const {return this->name;}


};
std::ostream& operator<<
    (std::ostream& out, const Unit& unit){
        out << unit.getName();
        return out;
}

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
    std::string valueWithDim(const Unit& unit) const{
        if (this->dim != unit.dim)
        {
            throw std::logic_error("Ошибка: величину нельзя вывести"
              " в этой единице!");
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
            throw std::logic_error("Нельзя складывать"
            " величины разных размерностей!");
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
            throw std::runtime_error("Деление на ноль!");
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

class UnitsMapCollection: public std::map<std::string, Unit>{
    void insertUnit(const Unit& unit){
        (*this)[unit.getName()] = unit;
    }
    public:
    void initUnits(){
        this->insertUnit(Unit("m", Dimension(0, 1, 0), 1.0));
        this->insertUnit(Unit("cm", Dimension(0, 1, 0), 0.01));
        this->insertUnit(Unit("s", Dimension(0, 0, 1), 1.0));
        this->insertUnit(Unit("kg", Dimension(1, 0, 0), 1.0));
        this->insertUnit(Unit("m/s", Dimension(0, 1, -1)));
        this->insertUnit(Unit("m/s^2", Dimension(0, 1, -2)));
        this->insertUnit(Unit("N", Dimension(1, 1, -2)));
        this->insertUnit(Unit("m^3", Dimension(0, 3, 0)));
        this->insertUnit(Unit("kg/m^3", Dimension(1, -3, 0)));
    }
    
};
UnitsMapCollection units;

void tests(){
    std::cout <<std::endl << "2 m + 30 cm = " << 
    (Quantity(2., units.at("m")) + Quantity(30, units.at("cm"))).
    valueWithDim(units.at("m"));

    // std::cout <<std::endl << "2 kg + 3s = " << 
    // (Quantity(2., units.at("kg")) + Quantity(3., units.at("s"))).
    // valueWithDim(units.at("s"));

    std::cout <<std::endl << "100 m / 20 s = " << 
    (Quantity(100., units.at("m")) / 
        Quantity(20, units.at("s"))).
    valueWithDim(units.at("m/s"));

    std::cout <<std::endl << "10 m/s / 2 s = " << 
    (Quantity(10., units.at("m/s")) / 
        Quantity(2, units.at("s"))).
        valueWithDim(units.at("m/s^2"));

    std::cout <<std::endl << "2 kg *  5 m/s^2 = " << 
    (Quantity(2., units.at("kg")) * 
        Quantity(5, units.at("m/s^2"))).
        valueWithDim(units["N"]);

    std::cout <<std::endl << "4 kg /  0.002 m^3 = " << 
    (Quantity(4., units.at("kg")) /
        Quantity(0.002, units.at("m^3"))).
        valueWithDim(units.at("kg/m^3"));//
    
    std:: cout << std::endl<<"Tests done! Also need to"
            " check answers\n";

}
void run(){
    std::string unitName;
    double value;

    std::cout << "Введите значение: ";
    std::cin >> value;

    std::cout << "Введите единицу: ";
    std::cin >> unitName;
    try {
    Unit u = units.at(unitName);
    Quantity q {value, u};
    std::cout << q;
    }
    catch (const std::exception& e){
        std::cout << "Ошибка " << e.what() << std::endl;
    }
}

int main() {
    setlocale(LC_ALL, "ru");
    units.initUnits();

    tests();
    run();

    return 0;
}
