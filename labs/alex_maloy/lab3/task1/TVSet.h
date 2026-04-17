#ifndef TVSET_H
#define TVSET_H

#include <iostream>
#include <string>
#include <map>
#include <sstream>

class TVSet {
private:
    bool isOn = false;
    int currentChannel = 1;
    int previousChannel = 1;
    std::map<int, std::string> channelNames;
    std::map<std::string, int> nameToChannel;

    std::string trim(const std::string& str);
    std::string normalizeName(const std::string& name);

public:
    void TurnOff();
    void TurnOn();
    void SelectChannel(int channel);
    void SelectChannel(const std::string& name);
    void SelectPreviousChannel();
    void Info();
    void SetChannelName(int channel, const std::string& name);
    void DeleteChannelName(const std::string& name);
    void GetChannelName(int channel);
    void GetChannelByName(const std::string& name);

    bool IsOn();
    int GetCurrentChannel();
    int GetPreviousChannel();
};

#endif