from protocol.ProtocolParser import ProtocolParser


string = "AP1.0/LoginMessage/options[encoding:UTF-8];Message[username:patrik, password:password]"
AlarmString = "AP1.0/AlarmMessage/options[encoding:UTF-8];Message[device_id:1003, alarm_id:404, alarm_flag:1]"

message = ProtocolParser.parseProtocolString(string)
secMsg = ProtocolParser.parseProtocolString(AlarmString)

print(message)
print(secMsg)