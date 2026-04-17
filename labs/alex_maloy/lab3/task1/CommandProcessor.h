#ifndef COMMANDPROCESSOR_H
#define COMMANDPROCESSOR_H

#include "TVSet.h"
#include <functional>
#include <map>
#include <sstream>
#include <string>

class CommandProcessor {
private:
    using CommandHandler = std::function<void(std::istringstream&)>;

    TVSet tv;
    std::map<std::string, CommandHandler> commandHandlers;

    static std::string readRestOfLine(std::istringstream& iss);
    static bool isNumber(const std::string& token);

    void handleTurnOn(std::istringstream& iss);
    void handleTurnOff(std::istringstream& iss);
    void handleInfo(std::istringstream& iss);
    void handleSelectChannel(std::istringstream& iss);
    void handleSelectPreviousChannel(std::istringstream& iss);
    void handleSetChannelName(std::istringstream& iss);
    void handleDeleteChannelName(std::istringstream& iss);
    void handleGetChannelName(std::istringstream& iss);
    void handleGetChannelByName(std::istringstream& iss);

public:
    CommandProcessor();
    void processCommand(const std::string& line);
    TVSet& getTV() { return tv; }
};

#endif