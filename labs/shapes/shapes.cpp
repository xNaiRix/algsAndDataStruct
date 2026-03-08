#include <cmath>
#include <iostream>
#include <math.h>
#include <vector>
using namespace std;
class Shape {
public:
    float virtual get_area()=0;
    float virtual get_perimetr()=0;
    //virtual ~Shape() = default;
};
class Circle : public Shape {
    float r;
public:
    static const float pi;
    Circle(float r):r(r){}

    float get_area() override{
        return pi*r*r;
    }
    float get_perimetr() override {
        return pi*2*r;
    }
};
const float Circle::pi = 3.14;

class Rectangle : public Shape {
    float h;
    float d;
    public:
    Rectangle(float h, float d):h(h),d(d){}
    float get_area() override {
        return d*h;
    }
    float get_perimetr() override {
        return 2*(d+h);
    }
    virtual float get_diagonal() {
        return d*sqrt(2);
    }
};
class Square : public Rectangle {
    public:
    Square(float h):Rectangle(h,h){}
};
int main() {
    vector<Shape*> shapes;
    shapes.push_back(new Circle(10));
    shapes.push_back(new Rectangle(3, 10));
    shapes.push_back(new Square(20));
    float sum_area = 0;
    float sum_perim = 0;
    cout << dynamic_cast<Rectangle *>(shapes[0]);//->get_diagonal() << endl;
    for (auto shape : shapes) {
        sum_area += shape->get_area();
        sum_perim += shape->get_perimetr();
        delete shape;
    }
    cout << "Area: " << sum_area << endl;
    cout << "Perim: " << sum_perim << endl;
}