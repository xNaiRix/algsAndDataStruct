#include <iostream>
#include <vector>
#include <memory>
#include <array>
class Output {
    bool state = false;
    bool next_state = false;

    public:
        Output()=default;
        [[nodiscard]] bool get() const {
            return state;
        }
        void update() {
            state = next_state;
        }
        void set(bool next_state) {
            this->next_state = next_state;
        }
};
class Gate {
public:
    virtual ~Gate() = default;

    virtual void compute() = 0;

    virtual void update() = 0;
};
class OneOutputGate : public Gate {
protected:
    std::shared_ptr<Output> output;

public:
    OneOutputGate() {
        output = std::make_shared<Output>();
    }
    ~OneOutputGate() override = default;

    void update() override {
        output->update();
    }

    [[nodiscard]] std::weak_ptr<Output> get_output() {
        return output;
    }
};

class InputGate : public OneOutputGate {
public:
    void set(const bool val) {
        output->set(val);
        update();
    }

    void compute() override {
    }
};

class NotGate : public OneOutputGate {
    std::weak_ptr<Output> in;
public:
    void setInput(const std::weak_ptr<Output> &input) {
        in = input;
    }

    void compute() override {
        if (const auto p = in.lock()) {
            output->set(!p->get());
        }
    }
};

class AndGate : public OneOutputGate {
    std::weak_ptr<Output> in1, in2;
public:
    void setInputs(const std::weak_ptr<Output> &i1, const std::weak_ptr<Output> &i2) {
        in1 = i1;
        in2 = i2;
    }

    void compute() override {
        const auto p1 = in1.lock();
        const auto p2 = in2.lock();
        if (p1 && p2) {
            output->set(p1->get() && p2->get());
        }
    }
};

class OrGate : public OneOutputGate {
    std::weak_ptr<Output> in1, in2;
public:
    void setInputs(const std::weak_ptr<Output> &i1, const std::weak_ptr<Output>& i2) {
        in1 = i1;
        in2 = i2;
    }

    void compute() override {
        const auto p1 = in1.lock();
        const auto p2 = in2.lock();
        if (p1 && p2) {
           output->set(p1->get() || p2->get());
        }
    }
};

class Circuit {
    std::vector<std::shared_ptr<Gate>> gates;

public:
    template<typename T, typename... Args>
    std::shared_ptr<T> create(Args&&... args) {
        auto gate = std::make_shared<T>(std::forward<Args>(args)...);
        gates.push_back(gate);
        return gate;
    }

    void tick() {
        for (auto& g : gates) g->compute();
        for (auto& g : gates) g->update();
    }

    void simulate(const int ticks = 10) {
        for (int i = 0; i < ticks; ++i) {
            tick();
        }
    }
};

class NANDGate: public OneOutputGate {
    std::shared_ptr<AndGate> and_gate;
    std::shared_ptr<NotGate> out_nand;

    Circuit circuit = Circuit();
public:
    NANDGate() {
        and_gate = circuit.create<AndGate>();
        out_nand = circuit.create<NotGate>();
        out_nand->setInput(and_gate->get_output());
    }
    void setInputs(std::weak_ptr<Output> inA, std::weak_ptr<Output> inB) {
        and_gate->setInputs(inA, inB);
    }
    void compute() override {
        circuit.simulate(2);
        std::shared_ptr<Output> p = out_nand->get_output().lock();
        output->set( p->get());
    }

};

class XORGate: public OneOutputGate {// (A or B) and (A nand B)
    std::shared_ptr<AndGate> out_and;
    std::shared_ptr<OrGate> or_gate;
    std::shared_ptr<NANDGate> nand_gate;
    Circuit circuit = Circuit();
    public:
    XORGate() {
        out_and = circuit.create<AndGate>();
        nand_gate = circuit.create<NANDGate>();
        or_gate = circuit.create<OrGate>();
    }
    void setInputs(std::weak_ptr<Output> inA, std::weak_ptr<Output> inB) {
        or_gate->setInputs(inA, inB);
        nand_gate->setInputs(inA, inB);
        out_and->setInputs(or_gate->get_output(), nand_gate->get_output());
    }
    void compute() override {
        circuit.simulate(3);
        std::shared_ptr<Output> p = out_and->get_output().lock();
        output->set( p->get());
    }
};

class RStriggerGate: public Gate {
    Circuit circuit = Circuit();
    std::shared_ptr<NANDGate> nand1;
    std::shared_ptr<NANDGate> nand2;
    std::shared_ptr<Output> q_output;
    std::shared_ptr<Output> not_q_output;

    public:
    RStriggerGate() {
        q_output = std::make_shared<Output>();
        not_q_output = std::make_shared<Output>();
        nand1 = circuit.create<NANDGate>();
        nand2 = circuit.create<NANDGate>();
    }
    void setInputs(std::weak_ptr<Output> notS, std::weak_ptr<Output> notR) {
        nand1->setInputs(notS, nand2->get_output());
        nand2->setInputs(notR, nand1->get_output());
    }
    void compute() override {
        circuit.simulate();
        std::shared_ptr<Output> q = nand1->get_output().lock();
        std::shared_ptr<Output> not_q = nand2->get_output().lock();
        q_output->set( q->get());
        not_q_output->set( not_q->get());
    }
    [[nodiscard]] std::weak_ptr<Output> get_q_output() {
        return q_output;
    }
    [[nodiscard]] std::weak_ptr<Output> get_not_q_output() {
        return not_q_output;
    }
    void update() override {
        q_output->update();
        not_q_output->update();
    }
};

class Accumulator2Gate: public Gate {
  Circuit circuit = Circuit();
    std::shared_ptr<XORGate> xor_gate;//единицы
    std::shared_ptr<AndGate> and_gate;//десятки
    std::shared_ptr<Output> s_output;//единицы
    std::shared_ptr<Output> p_output;//десятки

    public:
    Accumulator2Gate() {
        p_output = std::make_shared<Output>();
        s_output = std::make_shared<Output>();
        xor_gate = circuit.create<XORGate>();
        and_gate = circuit.create<AndGate>();
    }
    void setInputs(std::weak_ptr<Output> in1, std::weak_ptr<Output> in2) {
        xor_gate->setInputs(in1, in2);
        and_gate->setInputs(in1, in2);
    }
    void compute() override {
        circuit.simulate(2);
        std::shared_ptr<Output> s = xor_gate->get_output().lock();
        std::shared_ptr<Output> p = and_gate->get_output().lock();
        p_output->set( p->get());
        s_output->set( s->get());
    }
    [[nodiscard]] std::weak_ptr<Output> get_p_output() {
        return p_output;
    }
    [[nodiscard]] std::weak_ptr<Output> get_s_output() {
        return s_output;
    }
    void update() override {
        p_output->update();
        s_output->update();
    }

};


class Accumulator3Gate: public Gate {
    Circuit circuit = Circuit();
    std::shared_ptr<Accumulator2Gate> accumulator1;
    std::shared_ptr<Accumulator2Gate> accumulator2;
    std::shared_ptr<Accumulator2Gate> accumulator3;
    std::shared_ptr<Output> s_output;
    std::shared_ptr<Output> p_output;


public:
    Accumulator3Gate() {
        //p(a,b) - бит переноса от суммы a+b
        //s(a,b) - бит единиц от суммы a+b
        p_output = std::make_shared<Output>();//p(a,b,c) = s( p(a,b), p( s(a,b), c) )
        //p=1 если (p(a,b) = 1 XOR (p(s(a,b), c) = 1, тк одновременно быть не могут
        s_output = std::make_shared<Output>();//s(a+b+c) = s(s(a+b) + c)
        accumulator1 = circuit.create<Accumulator2Gate>();//a+b
        accumulator2 = circuit.create<Accumulator2Gate>();//S(a+b) + c
        accumulator3 = circuit.create<Accumulator2Gate>();//P(a+b) + P(S(a+b) + c)

    }
    void setInputs(std::weak_ptr<Output> in1, std::weak_ptr<Output> in2, std::weak_ptr<Output> in3) {
        accumulator1->setInputs(in1, in2);
        accumulator2->setInputs((accumulator1->get_s_output()).lock(), in3);
        accumulator3->setInputs((accumulator1->get_p_output()).lock(), (accumulator2->get_p_output()).lock());
    }
    void compute() override {
        circuit.simulate(3);
        std::shared_ptr<Output> s = (accumulator2->get_s_output()).lock();
        std::shared_ptr<Output> p = (accumulator3->get_s_output()).lock();
        p_output->set( p->get());
        s_output->set( s->get());
    }
    [[nodiscard]] std::weak_ptr<Output> get_p_output() {
        return p_output;
    }
    [[nodiscard]] std::weak_ptr<Output> get_s_output() {
        return s_output;
    }
    void update() override {
        p_output->update();
        s_output->update();
    }
};

template<int n>
//a2a1a0 + b2b1b0 = c3c2c1c0
//c0 = s(a0,b0,0)
//c1 = s(a1,b1,p(a0,b0,c))
//...
class Accumulator2NumberNBitsGate: public Gate {
    Circuit circuit = Circuit();
    std::shared_ptr<InputGate> input_zero;
    std::array<std::shared_ptr<Accumulator3Gate>, n> accumulators;
    std::array<std::shared_ptr<Output>, n + 1> output_bits;//0 бит - младший
    public:
    Accumulator2NumberNBitsGate() {
        for (int i = 0; i < n + 1; i++) {
            output_bits[i] = std::make_shared<Output>();
        }
        input_zero = circuit.create<InputGate>();
        input_zero->set(0);
        for (auto& accum : accumulators) {
            accum =  circuit.create<Accumulator3Gate>();
        }


    }
    void setInputs(const std::array<std::weak_ptr<Output>, n>& in1,
                    const std::array<std::weak_ptr<Output>, n>& in2) {
        accumulators[0]->setInputs(in1[0], in2[0],  input_zero->get_output());
        for (int i = 1; i < n; ++i) {
            accumulators[i]->setInputs(
                accumulators[i - 1]->get_p_output(),
                in1[i],
                in2[i]
            );
        }

    }

    void compute() override {
        circuit.simulate(n);
        for (int i = 0; i < n; ++i) {
            output_bits[i]->set(accumulators[i]->get_s_output().lock()->get());
        }
        output_bits.back()->set(accumulators.back()->get_p_output().lock()->get());
    }
    [[nodiscard]] std::array<std::weak_ptr<Output>, n + 1> get_output_number() const {
        std::array<std::weak_ptr<Output>, n + 1> res;
        for (int i = 0; i < n + 1; ++i) {
            res[i] = output_bits[i];
        }
        return res;
    }
    [[nodiscard]] std::weak_ptr<Output> get_output_bit(const int i) const {
        if (i < 0 || i >= n + 1) {
            throw std::out_of_range("While trying to get output bit in Accumulator2NumberNBitsGate");
        }
        return output_bits[i];
    }
    void update() override {
        for (const auto& bit : output_bits) {
            bit->update();
        }
    }
};
void checkRSTriggerGate() {
    Circuit circuit;
    std::shared_ptr<InputGate> inputNotR, inputNotS;
    std::shared_ptr<RStriggerGate> RStrigger;
    inputNotR = circuit.create<InputGate>();
    inputNotS = circuit.create<InputGate>();
    RStrigger = circuit.create<RStriggerGate>();
    RStrigger->setInputs((inputNotS->get_output()).lock(), (inputNotR->get_output()).lock());
    inputNotS->set(!1);
    inputNotR->set(!0);
    circuit.simulate(1);
    std::cout << "set: Q=" << ((RStrigger->get_q_output()).lock())->get() <<
        " notQ=" << ((RStrigger->get_not_q_output()).lock())->get() << "\n";


    inputNotS->set(!0);
    inputNotR->set(!0);
    circuit.simulate(1);
    std::cout << "memory: Q=" << ((RStrigger->get_q_output()).lock())->get() <<
        " notQ=" << ((RStrigger->get_not_q_output()).lock())->get() << "\n";

    inputNotR->set(!1);
    inputNotS->set(!0);
    circuit.simulate(1);
    std::cout << "reset: Q=" << ((RStrigger->get_q_output()).lock())->get() <<
        " notQ=" << ((RStrigger->get_not_q_output()).lock())->get() << "\n";

    inputNotS->set(!0);
    inputNotR->set(!0);
    circuit.simulate(1);
    std::cout << "memory: Q=" << ((RStrigger->get_q_output()).lock())->get() <<
        " notQ=" << ((RStrigger->get_not_q_output()).lock())->get() << "\n";
}
void checkAccumulator2Gate() {
    Circuit circuit;
    std::shared_ptr<InputGate> input1, input2;
    std::shared_ptr<Accumulator2Gate> accumulator;
    input1 = circuit.create<InputGate>();
    input2 = circuit.create<InputGate>();
    accumulator = circuit.create<Accumulator2Gate>();
    accumulator->setInputs((input1->get_output()).lock(), (input2->get_output()).lock());
    std::cout << "a b p s\n";
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            input1->set(i);
            input2->set(j);
            circuit.simulate(1);
            std::cout <<i << ' ' << j << ' ' <<  (accumulator->get_p_output()).lock()->get() << ' '<<
             (accumulator->get_s_output()).lock()->get() << "\n";
        }
    }
}
void checkAccumulator3Gate() {
    Circuit circuit;
    std::shared_ptr<InputGate> input1, input2, input3;
    std::shared_ptr<Accumulator3Gate> accumulator;
    input1 = circuit.create<InputGate>();
    input2 = circuit.create<InputGate>();
    input3 = circuit.create<InputGate>();
    accumulator = circuit.create<Accumulator3Gate>();
    accumulator->setInputs((input1->get_output()).lock(),
                            (input2->get_output()).lock(),
                            (input3->get_output()).lock());
    std::cout << "a b c\tp s\n";
    for (int i = 0; i < 2; ++i) {
        for (int j = 0; j < 2; ++j) {
            for (int k = 0; k < 2; ++k) {
                input1->set(i);
                input2->set(j);
                input3->set(k);
                circuit.simulate(1);
                std::cout <<i << ' ' << j << ' ' << k << '\t' <<
                 (accumulator->get_p_output()).lock()->get() << ' '<<
                 (accumulator->get_s_output()).lock()->get() << "\n";
            }
        }
    }
}


void checkAccumulator2NumNBitGate() {
    constexpr int n = 6;
    Circuit circuit;
    std::vector<std::shared_ptr<InputGate>> num1;
    std::vector<std::shared_ptr<InputGate>> num2;
    for (int i = 0; i < n; i++) {
        num1.push_back(circuit.create<InputGate>());
        num2.push_back(circuit.create<InputGate>());
    }
    std::shared_ptr<Accumulator2NumberNBitsGate<n>> accumulator;
    accumulator = circuit.create<Accumulator2NumberNBitsGate<n>>();

    std::array<std::weak_ptr<Output>, n> outputs1, outputs2;
    for (int i = 0; i < n; i++) {
        outputs1[i] = num1[i]->get_output();
        outputs2[i] = num2[i]->get_output();
    }
    accumulator->setInputs(outputs1, outputs2);
    for (int i = 0; i < (1<<n); ++i) {//(1<<n = 8)
        for (int j = 0; j < (1<<n); ++j) {
            for (int k = 0; k < n; k++) {
                num1[k]->set((i >> k) & 1);
                num2[k]->set((j >> k) & 1);
            }
            circuit.simulate(2);
            std::cout << i << '+' << j << " " << '\t' << "=  ";
            int sum = 0;
            for (int k = n; k >=0; --k) {
                int cur = accumulator->get_output_bit(k).lock()->get();
                sum = sum*2+cur;
                std::cout <<  cur;
            }
            std::cout <<' ' << '|' << ' ' << sum <<  '\n';
            if (i + j != sum) {
                std::cout << " WHAT ARE HELL\n";
            }
        }
    }
}
int main() {
    setlocale(LC_ALL,"ru");
    checkAccumulator2NumNBitGate();

    return 0;
}