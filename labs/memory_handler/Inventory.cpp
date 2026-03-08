#include <iostream>
#include <exception>
#include <format>
class Inventory{
    int* data;
    int size;
    int capacity;
    friend std::ostream& operator<< (std::ostream& out, const Inventory& obj);
public:
    Inventory(int capacity = 5): 
    capacity(capacity), size(0){
        data = new int[capacity];
    }
    Inventory(const Inventory& other): 
    capacity(other.capacity), size(other.size){
        this->data = new int[this->capacity];
        for (size_t i = 0; i < this->size; ++i){
            this->data[i] = other.data[i];
        }
    }

    ~Inventory(){
        delete[] data;
    }
    Inventory& operator=(const Inventory& other){
        if (this == &other){
            return *this;
        }
        delete[] this->data;
        this->size = other.size;
        this->capacity = other.capacity;
        this->data = new int[this->capacity];
        for (size_t i = 0; i < this->size; ++i){
            this->data[i] = other.data[i];
        }
        return *this;
    }

    int& operator[] (int index){
        if (index >= size){
            throw std::out_of_range(
                    "Inventory out of range."
                );
        }
        return *(data + index);
    }

    void add(int newItem){
        if (size == capacity){
            int * newData = new int[capacity*2];
            for(size_t i = 0; i < size; ++i){
                newData[i] = data[i];
            }
            delete[] data;
            data = newData;
            capacity*=2;
        }
        
        data[size++] = newItem;
    }

    void clear(){
        size = 0;//по-хорошему надо делать data = nullptr
        // и везде проверять на nullptr
        //но это надо менять всё!
    }
    void print();
};
std::ostream& operator<< (std::ostream& out, const Inventory& obj){
    for(size_t i = 0; i < obj.size; ++i){
        out << *(obj.data + i);
        if( i + 1 != obj.size){
            out << ' ';
        }
    }
    return out;
}
void Inventory::print(){
    std::cout << (*this) << std::endl;
}
int main() {
    Inventory arthur(2);
    arthur.add(10); // Золото
    arthur.add(20); // Зелье
    arthur.add(30); // Меч (тут массив расширится)

    std::cout << "Arthur's inventory: ";
    arthur.print();

    // Тест конструктора копирования
    Inventory lancelot = arthur; 
    lancelot.add(99); // Даем Ланселоту уникальный предмет

    std::cout << "Lancelot's inventory: ";
    lancelot.print();

    Inventory merlin(10);
    merlin.add(777); // Посох
    
    // Тест оператора присваивания
    merlin = arthur; 

    std::cout << "Merlin's inventory (copied from Arthur): ";
    merlin.print();
    
    // Проверка независимости:
    std::cout << "Original Arthur remains unchanged: ";
    arthur.print();

    std::cout << "Success! No crashes!" << std::endl;
    return 0;
}