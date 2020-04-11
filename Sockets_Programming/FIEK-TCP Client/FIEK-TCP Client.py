import socket
import sys
import select


#serverName = 'localhost'
serverName = input(" Shenoni emrin e serverit: ")
#serverPort = 13000
Port = input(" Shenoni portin: ")
serverPort = int(Port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverName,serverPort))

while True:
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    var = input(" Zgjedhni njeren nga kerkesat: "+
        "\n\n -IPADDRESS\n -PORT\n -COUNT\n -REVERSE\n -PALINDROME\n -TIME\n -GAME\n -GFC\n" +
        " -CONVERT\n -STORAGE\n -HOST\n" +
        " -EXIT/ChangeServer\n\n-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-\n"
        +" -")


    var=var.strip()
    if len(var) > 128:
        # madhesia me e madhe qe mund te mirret eshte 128 byte
        print(" Kerkesa nuk mund te jete me e gjate se 128 karaktere!")
        continue
    if not var:
        print(" Ju lutem shenoni nje kerkese!")
        continue
    # mbyllet serveri pas kerkeses EXIT
    if var == "EXIT":
        s.close()
        break
    if var=="ChangeServer":
       
        print("\n-.-.-.-.-.-.- New Connection -.-.-.-.-.-.-")
        serverName = input(" Shenoni emrin e serverit: ") 
        Port = input(" Shenoni portin: ")
        serverPort = int(Port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serverName,serverPort))
        print("\n")

    # behet enkodimi i kerkeses dhe dergimi tek TCP serveri    
    s.sendall(str.encode(var))
    data = s.recv(1024)
    data = data.decode('utf-8')# dekodohet me utf-8
    print(data)
