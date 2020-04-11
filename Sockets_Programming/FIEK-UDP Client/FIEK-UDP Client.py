import time
import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
#serverName = 'localhost';
serverName = input(" Shenoni emrin e serverit: ")
#serverPort = 13000;
Port = input(" Shenoni portin: ")
serverPort = int(Port)
addr = (serverName, serverPort)

while 1:
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    var = input(" Zgjedhni njeren nga kerkesat: \n\n IPADDRESS\n PORT\n COUNT\n REVERSE\n PALINDROME\n TIME\n GAME\n GCF\n" +
                " CONVERT\n STORAGE\n HOST\n" +
                " EXIT/ChangeServer\n\n-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-\n"
                +" -")
    if not var:
        print(" Ju lutem shenoni njeren nga kerkesat!")
        continue
    if var == "EXIT":
        # mbyllet serveri pas kerkeses EXIT
        client_socket.close()
        break
    if var=="ChangeServer":       
        
        print("\n-.-.-.-.-.-.-.- New Connection -.-.-.-.-.-.-.-")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.settimeout(1.0)
        serverName = input(" Shenoni emrin e serverit: ")
        Port = input(" Shenoni portin: ")
        serverPort = int(Port)
        addr = (serverName, serverPort)
        print("\n")
    client_socket.sendto(var.encode(), addr)
    try:
        data, server = client_socket.recvfrom(1024)
        # dekodohet me utf-8
        data = data.decode('utf-8')
        print(data)
    except socket.timeout:
        print('REQUEST TIMED OUT')
    finally:
        print("\n-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
