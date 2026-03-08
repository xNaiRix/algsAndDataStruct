#include <iostream>
struct Player {
    int x = 1;
    int y = 1;
    int hp = 100;
    int gold = 0;
};
class Cell{
    protected:
        virtual char getSymbol() const = 0;
        virtual void onStep(Player& p) = 0;
        virtual bool canWalk() const { return true;}
        virtual ~Cell() {}
};

class Floor : public Cell {
public:
    Floor() = default;
    char getSymbol() const override { return '.'; }
    void onStep(Player& p) override { 
        // Ничего не происходит, просто стоим
    }
};

class Wall : public Cell {
public:
    Wall() = default;
    char getSymbol() const override { return '#'; }
    virtual bool canWalk()  const override { return false;}
    void onStep(Player& p) override {}
};

class Gold : public Cell {
private:
bool isCollected = false;
public:
    char getSymbol() const override {
        if (isCollected) return '.';
        return '$'; 
    }
    void onStep(Player& p) override {
        if (!isCollected){
            p.gold += 10;
        }
    }
};

class Map{
    Cell* grid[10][10];
    Map(){
        for(int i = 0; i < 10; ++i){
            grid[i][0] = new Wall();
            if (i != 0){
                grid[0][i] = new Wall();
                grid[9][i] = new Wall();
                if (i != 9){
                    grid[i][9] = new Wall();
                }
            }
        }
        for(int i = 1; i < 9; ++i){
            for (int j = 1; j < 9; ++j){
                grid[i][j] = new Floor();
            }
        }
    }
};