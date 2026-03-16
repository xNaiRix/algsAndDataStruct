#include <iostream>
#include <cmath>
#include <optional>
#include <numbers>
#include<stdexcept>
#include <format>

// Предварительные объявления
struct Point;
struct Vector;
struct Line;

// --- Вектор ---
struct Vector {
    double dx, dy;

    double length() const { return std::sqrt(dx * dx + dy * dy); }
    double atan2() const { return std::atan2(dy, dx) * 180.0 / std::numbers::pi; }

    Vector normalize() const {
        double len = length();
        return (len == 0.0) ? Vector{ 0, 0 } : Vector{ dx / len, dy / len };
    }

    // Вектор * Число
    Vector operator*(double scalar) const { return { dx * scalar, dy * scalar }; }
    // Вектор / Число
    Vector operator/(double scalar) const { return { dx / scalar, dy / scalar }; }

    // Оператор ~ (перпендикулярный вектор)
    Vector operator~() const { return { -dy, dx }; }

    // Оператор ^ (угол между векторами)
    double operator^(const Vector& other) const {
        double angle = atan2() - other.atan2();
        if (angle > 180.0) angle -= 360.0;
        if (angle < -180.0) angle += 360.0;
        return std::abs(angle);
    }
};

// Число * Вектор
inline Vector operator*(double scalar, const Vector& v) { return v * scalar; }
// Функция abs(Vector)
inline double abs(const Vector& v) { return v.length(); }

// --- Точка ---
struct Point {
    double x, y;

    // Точка - Точка = Вектор
    Vector operator-(const Point& other) const { return { x - other.x, y - other.y }; }
    // Точка - Вектор = Точка
    Point operator-(const Vector& v) const { return { x - v.dx, y - v.dy }; }
    // Точка + Вектор = Точка
    Point operator+(const Vector& v) const { return { x + v.dx, y + v.dy }; }

    // Оператор | будет возвращать линию, но Line еще не определен, 
    // поэтому определим методы ниже
    Line operator|(const Point& other) const;
    Line operator|(const Vector& dir) const;
};

// --- Линия ---
struct Line {
    Point p1, p2;
    double a, b, c;//ax + by + c = 0, (a,b) - нормаль к прямой, |c| - длина перпенд из (0,0) к прямой

    Line(Point p1, Point p2) : p1(p1), p2(p2) {
        Vector norm = Vector{ p2.y - p1.y, p1.x - p2.x }.normalize();
        a = norm.dx;
        b = norm.dy;
        c = -a * p1.x - b * p1.y;
    }

    // Пересечение прямых: Линия & Линия = optional<Точка>
    std::optional<Point> operator&(const Line& other) const {
        double det = a * other.b - other.a * b;
        if (std::abs(det) < 1e-9) return std::nullopt; // Параллельны
        return Point{
            (other.c * b - c * other.b) / det,
            (c * other.a - other.c * a) / det
        };
    }

    // Оператор ~ (нормаль прямой как вектор)
    Vector operator~() const { return { a, b }; }

    // Проверка принадлежности точки прямой (вместо Python-оператора `in`)
    bool contains(const Point& p) const {
        return std::abs(a * p.x + b * p.y + c) < 1e-5;
    }

    double length() const { return (p1 - p2).length(); }
};

// Функция abs(Line) - длина отрезка
inline double abs(const Line& l) { return l.length(); }

// Реализация методов создания линии (Точка | Точка) и (Точка | Вектор)
inline Line Point::operator|(const Point& other) const { return Line(*this, other); }
inline Line Point::operator|(const Vector& dir) const { return Line(*this, *this + dir); }

// --- Окружность ---
struct Circle {
    Point center;
    double radius;

    Circle(Point a, Point b, Point c) : center{ 0, 0 }, radius(0) {
        Point p = a + (b - a) / 2.0;
        Point q = b + (c - b) / 2.0;

        Line po = p | ~(a | b); // Серединный перпендикуляр к AB
        Line qo = q | ~(b | c); // Серединный перпендикуляр к BC

        if (auto intersection = po & qo; intersection) {
            center = *intersection;
            radius = abs(a - center);
        }
    }

    bool contains(const Point& p) const {
        return std::abs(abs(center - p) - radius) < 1e-5;
    }
};

void Eyler(){
    Point A{ -150, -150 };
    Point B = A + Vector{ 400, 0 };
    Point C = B + Vector{ -70, 300 };

    // Строим прямые/отрезки
    Line AB = A | B;
    Line BC = B | C;
    Line AC = A | C;

    // Основания медиан
    Point L = B + (C - B) / 2.0;
    Point M = A + (B - A) / 2.0;
    Point N = A + (C - A) / 2.0;

    Line CM = C | M;
    Line BN = B | N;
    Point D = (CM & BN).value(); // Точка пересечения медиан (Центроид)

    // Центр описанной окружности
    Line OM = M | ~AB;
    Line ON = N | ~AC;
    Point O = (OM & ON).value();

    // Основания высот
    Point E = (AB & (C | ~AB)).value();
    Point F = (AC & (B | ~AC)).value();
    Line CE = C | E;
    Line BF = B | F;
    Point H = (CE & BF).value(); // Точка пересечения высот (Ортоцентр)

    // Окружность Эйлера (окружность 9 точек)
    Circle c9(E, M, N);
    Point P = c9.center; // Центр окружности Эйлера

    // Прямая Эйлера
    Line OH = O | H;

    // Вывод результатов
    std::cout << std::boolalpha;
    std::cout << "D in OH: " << OH.contains(D) << "\n"; // Лежит ли центроид на прямой Эйлера
    std::cout << "P in OH: " << OH.contains(P) << "\n"; // Лежит ли центр окр. Эйлера на прямой
    std::cout << "L in c9: " << c9.contains(L) << "\n"; // Лежит ли основание медианы на окр. Эйлера

    std::cout << "\nДлины сторон:\n";
    std::cout << std::format("AB = {:.1f}\n", abs(AB));
    std::cout << std::format("AC = {:.1f}\n", abs(AC));
    std::cout << std::format("BC = {:.1f}\n", abs(BC));

    // Вычисляем углы
    double ang_ABC = (A - B) ^ (C - B);
    double ang_BAC = (C - A) ^ (B - A);
    double ang_ACB = (B - C) ^ (A - C);

    std::cout << std::format("\n<ABC + <BCA + <CAB = {:.1f} + {:.1f} + {:.1f} = {:.0f} = 180\n",
        ang_ABC, ang_ACB, ang_BAC,
        (ang_ABC + ang_BAC + ang_ACB));
}
void fourPointsOnCircle(Point A, Point B, Point C, Point D){
    Line AB = A|B;
    Line CD = C|D;
    std::optional<Point> O_opt = AB & CD;
    if (!O_opt){
        std::swap (A, C);
        AB = A|B;
        CD = C|D;
        O_opt = AB & CD;
        if (!O_opt){
            std::swap (A, D);
            AB = A|B;
            CD = C|D;
            O_opt = AB & CD;
            std::cout << "\nPoints A becomes C, C becomes D, D becomes A to not be parallel\n";
            if (!O_opt){
                throw std::invalid_argument("Bad points");
            }
        }
        else{
            std::cout << "\nPoints A and C changed there order to not be parallel\n";
        }

    }
    Point O = O_opt.value(); // O - точка пересечения
    Line AO = A|O;
    Line OB = O|B;
    Line OC = O|C;
    Line OD = O|D;
    std::cout << std::boolalpha;
    std::cout << "AO/OC = " << AO.length() / OC.length();
    std::cout << "\nOD/OB = " << OD.length() / OB.length();
    double d = AO.length() / OC.length() - OD.length() / OB.length();
    std::cout << "\ndict = " << d << '\n';
    Circle circle {A,B,C};
    std::cout << "\ncircle (ABC) contains D: " << circle.contains(D);
    std::cout <<  "\n\nTheorem about 4 points on circle is correct: " << 
         ((std::abs(d) < 1e-5 ) == circle.contains(D))
         << std::endl<<std::endl<<std::endl;


}
int main() {
    // Вершины треугольника
    Point A = Point(0,50);
    Point B = Point(50,0);
    Point C = Point(40,30);
    Point D = Point(40,-30);
    std::cout << "\n==============LAB===============\n";
    fourPointsOnCircle(A,B,C,D);
    fourPointsOnCircle(A,B,B,D);
    fourPointsOnCircle(A,B,B,C);
    A = {0, 100};
    fourPointsOnCircle(A,B,C,D);
    A = {50,60};
    fourPointsOnCircle(A,B,C,D);
    fourPointsOnCircle(B,A,C,D);
    return 0;
}