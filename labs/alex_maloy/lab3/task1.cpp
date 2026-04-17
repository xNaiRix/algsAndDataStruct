#include <iostream>
#include <string>
#include <map>
#include <sstream>
#include <algorithm>
#include <cctype>

class TVSet {
private:
    bool isOn = false;
    int currentChannel = 1;
    int previousChannel = 1;
    std::map<int, std::string> channelNames;
    std::map<std::string, int> nameToChannel;

    std::string trim(const std::string& str) {
        size_t first = str.find_first_not_of(" \t");
        if (first == std::string::npos) return "";
        size_t last = str.find_last_not_of(" \t");
        return str.substr(first, last - first + 1);
    }

    std::string normalizeName(const std::string& name) {
        std::string trimmed = trim(name);
        if (trimmed.empty()) return "";
        // Remove extra spaces
        std::string result;
        bool space = false;
        for (char c : trimmed) {
            if (c == ' ') {
                if (!space) {
                    result += c;
                    space = true;
                }
            } else {
                result += c;
                space = false;
            }
        }
        return result;
    }

public:
    void TurnOff() {
        if (isOn) {
            isOn = false;
            std::cout << "TV is turned off" << std::endl;
        } else {
            std::cout << "ERROR" << std::endl;
        }
    }

    void TurnOn() {
        if (!isOn) {
            isOn = true;
            std::cout << "TV is turned on" << std::endl;
        } else {
            std::cout << "ERROR" << std::endl;
        }
    }

    void SelectChannel(int channel) {
        if (!isOn) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        if (channel < 1 || channel > 99) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        previousChannel = currentChannel;
        currentChannel = channel;
        std::cout << "Channel switched to: " << channel << std::endl;
    }

    void SelectChannel(const std::string& name) {
        if (!isOn) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        auto it = nameToChannel.find(name);
        if (it == nameToChannel.end()) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        previousChannel = currentChannel;
        currentChannel = it->second;
        std::cout << "Channel switched to: " << name << std::endl;
    }

    void SelectPreviousChannel() {
        if (!isOn || previousChannel == currentChannel) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        currentChannel = previousChannel;
        std::cout << "Switched to previous channel" << std::endl;
    }

    void Info() {
        if (!isOn) {
            std::cout << "TV is turned off" << std::endl;
            return;
        }
        std::cout << "TV is turned on" << std::endl;
        std::cout << "Channel is: " << currentChannel << std::endl;
        for (const auto& pair : channelNames) {
            std::cout << pair.first << " - " << pair.second << std::endl;
        }
    }

    void SetChannelName(int channel, const std::string& name) {
        if (!isOn || channel < 1 || channel > 99) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        std::string normName = normalizeName(name);
        if (normName.empty()) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        // If name already used, remove old association
        auto it = nameToChannel.find(normName);
        if (it != nameToChannel.end()) {
            channelNames.erase(it->second);
        }
        // If channel had name, remove from nameToChannel
        auto cit = channelNames.find(channel);
        if (cit != channelNames.end()) {
            nameToChannel.erase(cit->second);
        }
        channelNames[channel] = normName;
        nameToChannel[normName] = channel;
        std::cout << "Channel name set: " << channel << " - " << normName << std::endl;
    }

    void DeleteChannelName(const std::string& name) {
        if (!isOn) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        std::string normName = normalizeName(name);
        auto it = nameToChannel.find(normName);
        if (it == nameToChannel.end()) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        channelNames.erase(it->second);
        nameToChannel.erase(it);
        std::cout << "Channel name deleted: " << normName << std::endl;
    }

    void GetChannelName(int channel) {
        if (!isOn || channel < 1 || channel > 99) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        auto it = channelNames.find(channel);
        if (it == channelNames.end()) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        std::cout << "Channel " << channel << " name: " << it->second << std::endl;
    }

    void GetChannelByName(const std::string& name) {
        if (!isOn) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        std::string normName = normalizeName(name);
        auto it = nameToChannel.find(normName);
        if (it == nameToChannel.end()) {
            std::cout << "ERROR" << std::endl;
            return;
        }
        std::cout << "Channel for name " << normName << ": " << it->second << std::endl;
    }
};

int main() {
    TVSet tv;
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        std::string command;
        iss >> command;
        if (command == "TurnOn") {
            tv.TurnOn();
        } else if (command == "TurnOff") {
            tv.TurnOff();
        } else if (command == "Info") {
            tv.Info();
        } else if (command == "SelectChannel") {
            std::string arg;
            iss >> arg;
            if (arg.empty()) {
                std::cout << "ERROR" << std::endl;
                continue;
            }
            // Check if arg is number
            bool isNumber = true;
            for (char c : arg) {
                if (!std::isdigit(c)) {
                    isNumber = false;
                    break;
                }
            }
            if (isNumber) {
                int channel = std::stoi(arg);
                tv.SelectChannel(channel);
            } else {
                tv.SelectChannel(arg);
            }
        } else if (command == "SelectPreviousChannel") {
            tv.SelectPreviousChannel();
        } else if (command == "SetChannelName") {
            int channel;
            std::string name;
            iss >> channel;
            std::getline(iss, name);
            name = name.substr(1); // remove leading space
            tv.SetChannelName(channel, name);
        } else if (command == "DeleteChannelName") {
            std::string name;
            std::getline(iss, name);
            name = name.substr(1);
            tv.DeleteChannelName(name);
        } else if (command == "GetChannelName") {
            int channel;
            iss >> channel;
            tv.GetChannelName(channel);
        } else if (command == "GetChannelByName") {
            std::string name;
            std::getline(iss, name);
            name = name.substr(1);
            tv.GetChannelByName(name);
        } else {
            std::cout << "ERROR" << std::endl;
        }
    }
    return 0;
}