#include <iostream>
#include <random> 
#include <ctime>  
#include <memory>
struct Player {
    int x = 1;
    int y = 1;
    int hp = 100;
    int gold = 0;
    bool hasKey = false;
};
class Cell{
    public:
        virtual char getSymbol() const = 0;
        virtual void onStep(Player& p) = 0;
        virtual bool canWalk(const Player& p) const
         { return true;}
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
    virtual bool canWalk(const Player& p)  const override 
    { return false;}
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
            isCollected = true;
        }
    }
};

class Trap : public Cell {
public:
    char getSymbol() const override {
        return '^'; 
    }
    void onStep(Player& p) override {
        p.hp -= 20;
    }
};

class Door: public Cell {
    bool isOpened = false;
    public:
    virtual bool canWalk(const Player& p) const override{
        return isOpened || p.hasKey;
    } 
    void onStep(Player& p) override{
        if (!isOpened){
            p.hasKey = false;
            isOpened = true;
        }
    }
    char getSymbol() const override{
        if (!isOpened){
        return 'D';
        }
        return '.';
    }
};

class Key: public Cell {
  private:
    bool isCollected = false;
  public:
    void onStep(Player& p) override{
        if (!isCollected){
            p.hasKey = true;
            isCollected = true;
        }
    }
    char getSymbol() const override{
        if (!isCollected){
            return 'K';
        }
        return '.';
    }
};

class Map{
    std::unique_ptr<Cell> grid[10][10];
public:
    Map(){
        for(int i = 0; i < 10; ++i){
            grid[i][0] = std::make_unique<Wall>();
            if (i != 0){
                grid[0][i] = std::make_unique<Wall>();
                grid[9][i] = std::make_unique<Wall>();
                if (i != 9){
                    grid[i][9] = std::make_unique<Wall>();
                }
            }
        }
        for(int i = 1; i < 9; ++i){
            for (int j = 1; j < 9; ++j){
                int chance = std::rand() % 100;
                if (chance < 10) {
                    grid[i][j] = std::make_unique<Gold>();
                }
                else if (chance < 25) {
                    grid[i][j] = std::make_unique<Trap>();
                }
                else if (chance < 35) {
                    grid[i][j] = std::make_unique<Door>();
                }
                else if (chance < 40) {
                    grid[i][j] = std::make_unique<Key>();
                }
                else {
                    grid[i][j] = std::make_unique<Floor>();
                }
            }
        }
    }

    void draw(const Player& p) const {
        for (int i = 0; i < 10; ++i){
            for(int j = 0; j < 10; ++j){
                if (i == p.x && j == p.y){
                    std::cout << '@';
                }else{
                    std:: cout << grid[i][j]->getSymbol();
                }
            }
            std::cout<<std::endl;
        }
    }
    
    void movePlayer(Player& p, int dx, int dy){
    int nx = p.x + dx;
    int ny = p.y + dy;
    if (nx >= 0 && nx < 10 &&
        ny >= 0 && ny < 10 &&
        grid[nx][ny]->canWalk(p)){
            p.x = nx;
            p.y = ny;
            grid[nx][ny]->onStep(p);
        }
    }

};

int main() {
    std::srand(std::time(nullptr));
    Player player;
    Map gameMap;
    char input;

    while (player.hp > 0) {
        system("cls");

        std::cout << "HP: " << player.hp << " | Gold: " << 
        player.gold << " | hasKEY: " <<player.hasKey << "\n";
        gameMap.draw(player);
        std::cout << "Move (w/a/s/d) and press Enter: ";
        std::cin >> input;

        if (input == 'w') gameMap.movePlayer(player, -1, 0);
        if (input == 's') gameMap.movePlayer(player, 1, 0);
        if (input == 'a') gameMap.movePlayer(player, 0, -1);
        if (input == 'd') gameMap.movePlayer(player, 0, 1);
        if (input == 'q') break; // Выход
    }

    std::cout << "Game Over!\n";
    std::cin>>input;
    return 0;
}