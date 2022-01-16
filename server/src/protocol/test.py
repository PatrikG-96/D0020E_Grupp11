from ProtocolParser import ProtocolParser

string = "AP1.0/LoginMessage/options[encoding:UTF-8];Message[username:patrik, password:password]"

ProtocolParser.parseProtocolString(string)