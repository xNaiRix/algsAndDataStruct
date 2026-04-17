#include "CommandProcessor.h"

CommandProcessor::CommandProcessor()
    : commandHandlers{
          {"TurnOn", [this](std::istringstream& iss) { handleTurnOn(iss); }},
          {"TurnOff", [this](std::istringstream& iss) { handleTurnOff(iss); }},
          {"Info", [this](std::istringstream& iss) { handleInfo(iss); }},
          {"SelectChannel", [this](std::istringstream& iss) { handleSelectChannel(iss); }},
          {"SelectPreviousChannel", [this](std::istringstream& iss) { handleSelectPreviousChannel(iss); }},
          {"SetChannelName", [this](std::istringstream& iss) { handleSetChannelName(iss); }},
          {"DeleteChannelName", [this](std::istringstream& iss) { handleDeleteChannelName(iss); }},
          {"GetChannelName", [this](std::istringstream& iss) { handleGetChannelName(iss); }},
          {"GetChannelByName", [this](std::istringstream& iss) { handleGetChannelByName(iss); }}
      } {
}

std::string CommandProcessor::readRestOfLine(std::istringstream& iss) {
    std::string rest;
    std::getline(iss, rest);
    if (!rest.empty() && rest.front() == ' ') {
        rest.erase(0, 1);
    }
    return rest;
}

bool CommandProcessor::isNumber(const std::string& token) {
    if (token.empty()) {
        return false;
    }
    for (char c : token) {
        if (!std::isdigit(static_cast<unsigned char>(c))) {
            return false;
        }
    }
    return true;
}

void CommandProcessor::handleTurnOn(std::istringstream&) {
    tv.TurnOn();
}

void CommandProcessor::handleTurnOff(std::istringstream&) {
    tv.TurnOff();
}

void CommandProcessor::handleInfo(std::istringstream&) {
    tv.Info();
}

void CommandProcessor::handleSelectChannel(std::istringstream& iss) {
    std::string arg;
    iss >> arg;
    if (arg.empty()) {
        std::cout << "ERROR" << std::endl;
        return;
    }

    if (isNumber(arg)) {
        int channel = std::stoi(arg);
        tv.SelectChannel(channel);
    } else {
        tv.SelectChannel(arg);
    }
}

void CommandProcessor::handleSelectPreviousChannel(std::istringstream&) {
    tv.SelectPreviousChannel();
}

void CommandProcessor::handleSetChannelName(std::istringstream& iss) {
    int channel;
    iss >> channel;
    std::string name = readRestOfLine(iss);
    tv.SetChannelName(channel, name);
}

void CommandProcessor::handleDeleteChannelName(std::istringstream& iss) {
    std::string name = readRestOfLine(iss);
    tv.DeleteChannelName(name);
}

void CommandProcessor::handleGetChannelName(std::istringstream& iss) {
    int channel;
    iss >> channel;
    tv.GetChannelName(channel);
}

void CommandProcessor::handleGetChannelByName(std::istringstream& iss) {
    std::string name = readRestOfLine(iss);
    tv.GetChannelByName(name);
}

void CommandProcessor::processCommand(const std::string& line) {
    std::istringstream iss(line);
    std::string command;
    iss >> command;

    auto handlerIt = commandHandlers.find(command);
    if (handlerIt == commandHandlers.end()) {
        std::cout << "ERROR" << std::endl;
        return;
    }

    handlerIt->second(iss);
}
