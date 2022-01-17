# Importera protocolParser

string = "AP1.0/LoginMessage/options[encoding:UTF-8];Message[username:patrik, password:password]"
AlarmString = "AP1.0/AlarmMessage/options[encoding:UTF-8];Message[device_id:1003, alarm_id:404, alarm_flag:1]"

message = ProtocolParser.parseProtocolString(string)
secMsg = ProtocolParser.parseProtocolString(AlarmString)

print(message)
print(secMsg)

version = "AP1.0"
# ? Maybe split the hType into two parts ex: Alarm (Response/Message). Then concatinate 
hType = "AlarmMessage"
options = "encoding:UTF-8"
mType = "Message"
params = "device_id:1003, alarm_id:404, alarm_flag:1"


def createProtocolString(version, hType, options, mType, params):
    protString = f"{version}/{hType}/options[{options}];{mType}[{params}]"
    return protString

print(createProtocolString(version, hType, options, mType, params))