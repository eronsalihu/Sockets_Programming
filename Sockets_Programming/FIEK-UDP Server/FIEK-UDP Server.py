import random
import socket
from datetime import datetime
import random
import shutil

serverPort=13000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 13000))
print(' Serveri u startua ne localhost: '+str(serverPort))
print(' -.-Serveri eshte i gatshem te pranoj kerkesa-.- ')

# METODAT 
#
#
#
def IPADDRESS(server_socket,addr):
    server_socket.sendto(str.encode(
            " IP adresa e klientit eshte: " + addr[0]), addr)

def PORT(server_socket,addr):
    server_socket.sendto(str.encode(
           " Klienti është duke përdorur portin: " + str(addr[1])), addr)

def PALINDROME(string):
    string_letters = [c for c in string.lower() if c.isalpha()]
    return (string_letters == string_letters[::-1])

def TIME(server_socket,addr):
    time=datetime.now().strftime(' %Y-%m-%d-%H:%M:%S')
    server_socket.sendto(str.encode(time),addr)

def GAME(server_socket,addr):
    srand=''
    for i in range(5):
        # gjenerimi i 5 numrave te rendomshem
        nrRandom=random.randint(1,35) 
        randString=" "+str(nrRandom)+" " 
        srand+=randString   
    server_socket.sendto(str.encode(srand),addr)

def CONVERT(server_socket, s, n):
    if(s == "cmToFeet"):
        server_socket.sendto(str.encode("%.2f" %(n/30.48)+" ft"),addr)
    elif(s == "FeetToCm"):
        server_socket.sendto(str.encode("%.2f" %(n*30.48)+" cm"),addr)
    elif(s == "kmToMiles"):
        server_socket.sendto(str.encode("%.2f" %(n / 1.609)+" miles"),addr)
    elif(s == "MileToKm"):
        server_socket.sendto(str.encode("%.2f" %(n * 1.609)+" km"),addr)

def GCF(a, b):
    if(b == 0):# nese b=0 at'here a shtypet
        return a
    else:
        return GCF(b, a % b)# shtypet shumezuesi i perbashket

def HOST(server_socket,addr):
    try:
        hostname = socket.gethostname()
        server_socket.sendto(str.encode(" Emri i hostit është: "+hostname),addr)
    except error:
        server_socket.sendto(str.encode(" Emri i hostit nuk dihet!"),addr)  
        
# funksion qe shfaq kerkesa e klientit e pastaj thirret te threading             
def operation_arr(request_arr, server_socket, addr):
    
    # metoda IPADRESA
    if(request_arr[0] == 'IPADDRESS'):
        IPADDRESS(server_socket,addr)

    # metoda PORT
    elif(request_arr[0] == 'PORT'):
       PORT(server_socket,addr)

    # metoda COUNT
    elif(request_arr[0] == 'COUNT'):
        try:
            s = ""
            s = s.join(request_arr[1:])  # ruajme fjaline ne nje string s
            count = 0
            zanoret = set("aeiouyAEIOUY\u00EB")# "aeiouyAEIOUY\u00EB" quhet RegEx i zanoreve
            bashketingelloret=0
            for letter in s:  # iterojme neper cdo shkronje te stringut
                if letter in zanoret:  # nese shkronja eshte zanore rritet count
                    count += 1
                else:
                    bashketingelloret = bashketingelloret+1  # numrojme bahketingellore
            server_socket.sendto(str.encode(
                " Teksti i pranuar përmban " + str(count) + " zanore dhe "+str(bashketingelloret)+" bashketingellore!"),addr)
        except IndexError:
            server_socket.sendto(str.encode(" Shenoni nje fjali pas kerkeses COUNT!"),addr)

    # metoda REVERSE
    elif (request_arr[0]=='REVERSE'):
        Sentence=' '.join(request_arr[1:])
        reversedS=Sentence[::-1]
        
        server_socket.sendto(str.encode(" "+reversedS),addr)

    # metoda PALINDROME
    elif (request_arr[0] == 'PALINDROME'):
        string=request_arr[1]
        
        if PALINDROME(string):
            server_socket.sendto(str.encode(" TRUE!"),addr)
        else:
            server_socket.sendto(str.encode(" FALSE!"),addr)

    # metoda TIME
    elif(request_arr[0] == 'TIME'):
        TIME(server_socket,addr)

    # metoda GAME
    elif(request_arr[0] == 'GAME'):
        GAME(server_socket,addr)
   
    # metoda CONVERT
    elif(request_arr[0] == 'CONVERT'):
        convert_option = " Convert Options:\n  -cmToFeet  \n  -FeetToCm  \n  -kmToMiles\n  -MileToKm"
        try:
            s = request_arr[1] # menyra e konvertimit
            n = float(request_arr[2])# vlera qe ka me u konvertu
            server_socket.sendto(str.encode(str(CONVERT(server_socket,s, n))), addr)
        except IndexError:
            server_socket.sendto(str.encode(
                " Ju lutem shenoni cka deshironi te konvertoni pastaj shifren! \n" + convert_option), addr)
        except ValueError:
            server_socket.sendto(str.encode(
                " Ju lutem shenoni cka deshironi te konvertoni pastaj shifren!\n "+convert_option ), addr)

    # metoda GCF
    elif (request_arr[0] == 'GCF'):
        a = int(request_arr[1]) # numri_pare
        b = int(request_arr[2]) # numri_dyte
        server_socket.sendto(str.encode(" "+str(GCF(a, b))),addr)

    # metoda STORAGE
    elif (request_arr[0] == 'STORAGE'):
        total, used, free = shutil.disk_usage("/")
        server_socket.sendto(str.encode(" Total: %d GiB" % (total // (2**30))+"\n Used: %d GiB" %
                             (used // (2**30))+"\n Free: %d GiB" % (free // (2**30))),addr)

    # metoda HOST
    elif(request_arr[0] == 'HOST'):
        HOST(server_socket,addr)

    else:
        server_socket.sendto(str.encode(" Shenoni njeren nga kerkesat!"), addr)

# pranimi i kerkesave te njepasnjeshme nga klientet
while True:
    kerkesa, addr = server_socket.recvfrom(1024)
    # pranohet komanda nga klienti dhe dekodohet me utf-8
    kerkesa = kerkesa.decode('utf-8') 
     # e ndajme komanden qe vje nga klienti dhe e ruajme ne forme te string array
    request_arr = kerkesa.split()
    operation_arr(request_arr, server_socket, addr)
