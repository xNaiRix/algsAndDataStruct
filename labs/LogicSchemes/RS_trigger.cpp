#include <iostream>
#include <vector>
#include <memory>
//#include <iomanip>
#include <windows.h> // для кодировки

// Базовый класс логического элемента
class Gate {
protected:
    bool state = false;
    bool next_state = false;

public:
    virtual ~Gate() = default;

    // Вычисляет новое состояние на основе текущих входов
    virtual void compute() = 0;

    // Применяет вычисленное состояние (имитация такта времени)
    virtual void update() {
        state = next_state;
    }

    // Возвращает текущее значение на выходе
    [[nodiscard]] bool get() const {
        return state;
    }
};

// --- Входной сигнал ---
class InputGate : public Gate {
public:
    void set(bool val) {
        next_state = val;
        update(); // Входы обновляются мгновенно
    }

    void compute() override {
        // Входной сигнал не зависит от других элементов
    }
};

// --- Элемент NOT ---
class NotGate : public Gate {
    std::weak_ptr<Gate> in;
public:
    void setInput(std::shared_ptr<Gate> input) {
        in = input;
    }

    void compute() override {
        if (auto p = in.lock()) {
            next_state = !p->get();
        }
    }
};

// --- Элемент AND ---
class AndGate : public Gate {
    std::weak_ptr<Gate> in1, in2;
public:
    void setInputs(std::shared_ptr<Gate> i1, std::shared_ptr<Gate> i2) {
        in1 = i1;
        in2 = i2;
    }

    void compute() override {
        auto p1 = in1.lock();
        auto p2 = in2.lock();
        if (p1 && p2) {
            next_state = p1->get() && p2->get();
        }
    }
};

// --- Элемент OR ---
class OrGate : public Gate {
    std::weak_ptr<Gate> in1, in2;
public:
    void setInputs(std::shared_ptr<Gate> i1, std::shared_ptr<Gate> i2) {
        in1 = i1;
        in2 = i2;
    }

    void compute() override {
        auto p1 = in1.lock();
        auto p2 = in2.lock();
        if (p1 && p2) {
            next_state = p1->get() || p2->get();
        }
    }
};

// --- Класс Схемы (Circuit) ---
// Управляет всеми элементами и обеспечивает тактирование
class Circuit {
    std::vector<std::shared_ptr<Gate>> gates;

public:
    // Фабричный метод для создания элементов
    template<typename T, typename... Args>
    std::shared_ptr<T> create(Args&&... args) {
        auto gate = std::make_shared<T>(std::forward<Args>(args)...);
        gates.push_back(gate);
        return gate;
    }

    // Один такт симуляции
    void tick() {
        for (auto& g : gates) g->compute();
        for (auto& g : gates) g->update();
    }

    // Прогоняем симуляцию N тактов до стабилизации сигналов
    void simulate(int ticks = 10) {
        for (int i = 0; i < ticks; ++i) {
            tick();
        }
    }
};


// ==========================================
// ДЕМОНСТРАЦИЯ
// ==========================================
class NANDGate: public Gate{
    std::shared_ptr<InputGate> inA;
    std::shared_ptr<InputGate> inB;
    std::shared_ptr<AndGate> and_gate;
    std::shared_ptr<NotGate> out_nand;

    Circuit circuit = Circuit();
public:
    NANDGate() {
        and_gate = circuit.create<AndGate>();
        out_nand = circuit.create<NotGate>();
        out_nand->setInput(and_gate);
    }
    void setInputs(std::shared_ptr<Gate> inA, std::shared_ptr<Gate> inB) {
        and_gate->setInputs(inA, inB);
    }
    void compute() override {
        circuit.simulate(2);
        next_state = out_nand->get();
    }

};

class RStriggerGate: public Gate {
    Circuit circuit = Circuit();
    std::shared_ptr<NANDGate> nand1;
    std::shared_ptr<NANDGate> nand2;

    public:
    RStriggerGate() {
        nand1 = circuit.create<NANDGate>();
        nand2 = circuit.create<NANDGate>();
    }
    void setInputs(std::shared_ptr<Gate> notS, std::shared_ptr<Gate> notR) {
        nand1->setInputs(notS, nand2);
        nand2->setInputs(notR, nand1);
    };
    void compute() override {
        circuit.simulate();
        next_state = nand1->get();//Это Q
    }

};
void demoCombinationalCircuit() {
    std::cout << "=== Комбинационная схема: XOR (Исключающее ИЛИ) ===\n";
    // XOR строится как: (A AND NOT B) OR (NOT A AND B)

    Circuit circuit;

    auto A = circuit.create<InputGate>();
    auto B = circuit.create<InputGate>();

    auto notA = circuit.create<NotGate>(); notA->setInput(A);
    auto notB = circuit.create<NotGate>(); notB->setInput(B);

    auto and1 = circuit.create<AndGate>(); and1->setInputs(A, notB);
    auto and2 = circuit.create<AndGate>(); and2->setInputs(notA, B);

    auto outXor = circuit.create<OrGate>(); outXor->setInputs(and1, and2);

    std::cout << "Таблица истинности:\n";
    std::cout << " A | B | Output (XOR)\n";
    std::cout << "---+---+-------------\n";

    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            A->set(i);
            B->set(j);
            circuit.simulate(5); // 5 тактов достаточно для прохождения сигнала через 3 слоя
            std::cout << " " << i << " | " << j << " |      " << outXor->get() << "\n";
        }
    }
    std::cout << "\n";
}

void demoSequentialCircuit() {
    std::cout << "=== Последовательностная схема: RS-триггер ===\n";
    // RS-триггер на базе элементов NOR (НЕ-ИЛИ).
    // Так как у нас есть OR и NOT, мы соберем NOR из них.
    // Q     = NOT( OR(R, Q_inv) )
    // Q_inv = NOT( OR(S, Q) )

    Circuit circuit;

    auto S = circuit.create<InputGate>();
    auto R = circuit.create<InputGate>();

    auto or1 = circuit.create<OrGate>();
    auto not1 = circuit.create<NotGate>(); // Выход Q

    auto or2 = circuit.create<OrGate>();
    auto not2 = circuit.create<NotGate>(); // Выход Q_inv (инверсный)

    // Подключаем перекрестную обратную связь
    or1->setInputs(R, not2);
    not1->setInput(or1);

    or2->setInputs(S, not1);
    not2->setInput(or2);

    auto printState = [&]() {
        std::cout << "Входы [S=" << S->get() << ", R=" << R->get() << "] -> "
            << "Выходы [Q=" << not1->get() << ", Q_inv=" << not2->get() << "]\n";
        };

    // 1. Устанавливаем триггер (Set)
    std::cout << "1. Подаем Set (S=1, R=0)\n";
    S->set(1); R->set(0);
    circuit.simulate();
    printState();

    // 2. Режим хранения
    std::cout << "2. Режим хранения (S=0, R=0)\n";
    S->set(0); R->set(0);
    circuit.simulate();
    printState();

    // 3. Сбрасываем триггер (Reset)
    std::cout << "3. Подаем Reset (S=0, R=1)\n";
    S->set(0); R->set(1);
    circuit.simulate();
    printState();

    // 4. Снова режим хранения
    std::cout << "4. Режим хранения (S=0, R=0)\n";
    S->set(0); R->set(0);
    circuit.simulate();
    printState();
}

int main() {
    // Устанавливаем кодировку ввода и вывода в консоли на UTF-8
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);
    //
    // demoCombinationalCircuit();
    // demoSequentialCircuit();
    Circuit circuit;
    std::shared_ptr<InputGate> inputR, inputS;
    std::shared_ptr<RStriggerGate> RStrigger;
    inputR = circuit.create<InputGate>();
    inputS = circuit.create<InputGate>();
    RStrigger = circuit.create<RStriggerGate>();
    RStrigger->setInputs(inputS, inputR);
    inputS->set(!1);
    inputR->set(!0);
    circuit.simulate(1);
    std::cout << "set " << RStrigger->get() << "\n";

    inputS->set(!0);
    inputR->set(!0);
    circuit.simulate(1);
    std::cout << "memory " << RStrigger->get() << "\n";

    inputR->set(!1);
    inputS->set(!0);
    circuit.simulate(1);
    std::cout << "reset " << RStrigger->get() << "\n";

    inputS->set(!0);
    inputR->set(!0);
    circuit.simulate(1);
    std::cout << "memory " << RStrigger->get() << "\n";

    // NAND = circuit.create<NANDGate>();
    // NAND->setInputs(inputR, inputS);
    // for (int i = 0; i < 2; ++i) {
    //     for (int j = 0; j < 2; ++j) {
    //         inputR->set(i);
    //         inputS->set(j);
    //         circuit.simulate(1);
    //         std::cout <<i << ' ' << j << ' ' <<  NAND->get() << "\n";
    //     }
    // }

    return 0;
}