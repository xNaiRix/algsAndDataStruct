#include <iostream>
#include <cmath>


class Vector2D{
    double x,y;
    friend std::ostream& operator<<(
        std::ostream&, const Vector2D&);
    friend std::istream& operator>>(
        std::istream&, Vector2D&);
    public:
        Vector2D():x(0), y(0){}
        Vector2D(double x, double y): x(x),y(y){}
        Vector2D(const Vector2D& other): 
        x(other.x), y(other.y){}

        Vector2D operator-() const{
            return Vector2D(-this->x, -this->y);
        }
        Vector2D operator+() const{
            return Vector2D(*this);
        }

        Vector2D operator+(const Vector2D& other) const{
            return Vector2D(
                other.x + this->x,
                other.y + this->y
            );
        }
        Vector2D& operator+=(const Vector2D& other){
            (*this) = (*this) + other;
            return *this;
        }
        Vector2D operator-(const Vector2D& other) const{
            return *this + (-other);
        }
        Vector2D& operator-=(const Vector2D& other){
            (*this) += -other; 
            return *this;
        }

        Vector2D operator*(const double other) const{
            return Vector2D(
                other * this->x,
                other * this->y
            );
        }
        Vector2D& operator*=(const double other){
            (*this) = (*this) * other;
            return *this;
        }

        double operator*(const Vector2D& other) const{
            return other.x * this->x + other.y + this->y;
        }

        double operator^(const Vector2D& other) const{
            return other.y * this->x - other.x + this->y;
        }//cross product

        //cmp
        bool operator==(const Vector2D&other) const{
            return (this->x == other.x) &&  
            (this->y == other.y);
        }
        bool operator!=(const Vector2D&other) const{
            return !(*this == other);
        }

        double length_2()const{
            return (*this)*(*this);
        }
        double length()const{
            return std::sqrt(this->length());
        }
};


std::ostream& operator<<(
    std::ostream& out, const Vector2D& obj
){
    out<<"( " << obj.x << ", " << obj.y << " )"; 
    return out;
} 

std::istream& operator>>(
    std::istream& in, Vector2D& obj
){
    in >> obj.x >> obj.y; 
    return in;
} 

Vector2D operator* (double num, const Vector2D& v){
    return v * num;
}

int main() {
    Vector2D playerPos(10.0, 5.0);
    Vector2D velocity(2.5, -1.0);
    float time = 2.0;

    // Считаем новую позицию: Позиция + (Скорость * Время)
    Vector2D newPos = playerPos + (velocity * time);

    std::cout << "Start position: " << playerPos << std::endl;
    std::cout << "Velocity: " << velocity << std::endl;
    std::cout << "Position after 2 seconds: " << newPos << std::endl;

    Vector2D target(15.0, 3.0);
    if (newPos == target) {
        std::cout << "Target reached!" << std::endl;
    } else {
        std::cout << "Missed the target." << std::endl;
    }

    return 0;
}