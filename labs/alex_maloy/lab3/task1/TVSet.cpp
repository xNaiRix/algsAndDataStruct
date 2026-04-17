#include "TVSet.h"

std::string TVSet::trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \t");
    if (first == std::string::npos) return "";
    size_t last = str.find_last_not_of(" \t");
    return str.substr(first, last - first + 1);
}

std::string TVSet::normalizeName(const std::string& name) {
    std::string trimmed = trim(name);
    if (trimmed.empty()) return "";
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

void TVSet::TurnOff() {
    if (isOn) {
        isOn = false;
        std::cout << "TV is turned off" << std::endl;
    } else {
        std::cout << "ERROR" << std::endl;
    }
}

void TVSet::TurnOn() {
    if (!isOn) {
        isOn = true;
        std::cout << "TV is turned on" << std::endl;
    } else {
        std::cout << "ERROR" << std::endl;
    }
}

void TVSet::SelectChannel(int channel) {
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

void TVSet::SelectChannel(const std::string& name) {
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

void TVSet::SelectPreviousChannel() {
    if (!isOn || previousChannel == currentChannel) {
        std::cout << "ERROR" << std::endl;
        return;
    }
    currentChannel = previousChannel;
    std::cout << "Switched to previous channel" << std::endl;
}

void TVSet::Info() {
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

void TVSet::SetChannelName(int channel, const std::string& name) {
    if (!isOn || channel < 1 || channel > 99) {
        std::cout << "ERROR" << std::endl;
        return;
    }
    std::string normName = normalizeName(name);
    if (normName.empty()) {
        std::cout << "ERROR" << std::endl;
        return;
    }
    auto it = nameToChannel.find(normName);
    if (it != nameToChannel.end()) {
        channelNames.erase(it->second);
    }
    auto cit = channelNames.find(channel);
    if (cit != channelNames.end()) {
        nameToChannel.erase(cit->second);
    }
    channelNames[channel] = normName;
    nameToChannel[normName] = channel;
    std::cout << "Channel name set: " << channel << " - " << normName << std::endl;
}

void TVSet::DeleteChannelName(const std::string& name) {
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

void TVSet::GetChannelName(int channel) {
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

void TVSet::GetChannelByName(const std::string& name) {
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

bool TVSet::IsOn() { return isOn; }
int TVSet::GetCurrentChannel() { return currentChannel; }
int TVSet::GetPreviousChannel() { return previousChannel; }