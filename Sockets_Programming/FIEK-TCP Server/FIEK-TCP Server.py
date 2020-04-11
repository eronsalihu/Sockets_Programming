import socket
import sys
from _thread import *
from datetime import datetime
import random
import shutil

host = ''
# porti 12000
serverPort = 13000

# krijimi i soketetit te serverit sipas TCP-protokollit
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # lidhja e portit te serverit dhe ip adreses me socketin e krijuar
    serverSocket.bind((host, serverPort))
except socket.error as e:
    print(str(e))

print(' Serveri u startua ne localhost: '+str(serverPort))
# serveri degjon lidhjet nga klientet
serverSocket.listen(10)
print(' -.-Serveri eshte i gatshem te pranoj kerkesa-.- ')

# METODAT 
#
#
#
def IPADDRESS(conn,addr):
    conn.send(str.encode(
            " IP adresa e klientit eshte: " + addr[0]))

def PORT(conn,addr):
    conn.send(str.encode(
           " Klienti është duke përdorur portin: " + str(addr[1])))

def PALINDROME(string):
    string_letters = [c for c in string.lower() if c.isalpha()]
    return (string_letters == string_letters[::-1])

def TIME(conn,addr):
    time=datetime.now().strftime(' %Y-%m-%d-%H:%M:%S')
    conn.send(str.encode(time))

def GAME(conn,addr):
    srand=''
    for i in range(5): 
        # gjenerimi i 5 numrave te rendomshem
        nrRandom=random.randint(1,35) 
        randString=" "+str(nrRandom)+" " 
        srand+=randString   
    conn.send(str.encode(srand))

def CONVERT(conn,s, n):
    
    if(s == "cmToFeet"):
        conn.send(str.encode(" "+"%.2f" %(n/30.48)+" ft"))
    elif(s == "FeetToCm"):
        conn.send(str.encode(" "+"%.2f" %(n*30.48)+" cm"))
    elif(s == "kmToMiles"):
        conn.send(str.encode(" "+"%.2f" %(n/1.609)+" miles"))
    elif(s == "MileToKm"):
        conn.send(str.encode(" "+"%.2f" %(n*1.609)+" km"))
        
def GCF(a, b):
    if(b == 0): # nese b=0 at'here a shtypet
        return a
    else:
        return GCF(b, a % b) # shtypet shumezuesi i perbashket

def HOST(conn,addr):
    try:
        hostname = socket.gethostname()
        conn.send(str.encode(" Emri i hostit është: "+hostname))
    except error:
        conn.send(str.encode(" Emri i hostit nuk dihet!"))
     
# funksion qe shfaq kerkesa e klientit e pastaj thirret te threading     
def operation_arr(request_arr, conn, addr):
    
    # metoda IPADRESA
    if(request_arr[0] == 'IPADDRESS'):
        IPADDRESS(conn,addr)
        
    # metoda PORT    
    elif(request_arr[0] == 'PORT'):
       PORT(conn,addr)
       

    # metoda COUNT
    elif(request_arr[0] == 'COUNT'):
        try:
            s = ""
            s = s.join(request_arr[1:])  # ruajme fjaline ne nje string s
            countz = 0
            zanoret = set("aeiouyAEIOUY\u00EB")# "aeiouy\u00EB" quhet RegEx i zanoreve
            bashketingelloret=0
            for letter in s:  # iterojme neper cdo shkronje te stringut
                if letter in zanoret:  # nese shkronja eshte zanore rritet count
                    countz += 1
                else:
                    bashketingelloret = bashketingelloret+1  # numrojme bahketingellore
            conn.send(str.encode(
                " Teksti i pranuar përmban " + str(countz) + " zanore dhe "+str(bashketingelloret)+" bashketingellore!"))
        except IndexError:
            conn.send(str.encode(" Shenoni nje fjali pas kerkeses COUNT!"))
   
    # metoda REVERSE
    elif (request_arr[0]=='REVERSE'):
        Sentence=' '.join(request_arr[1:])
        reversedS=Sentence[::-1]
        
        conn.send(str.encode(" "+reversedS))

    # metoda PALINDROME
    elif (request_arr[0] == 'PALINDROME'):
        string=request_arr[1]
        
        if PALINDROME(string):
            conn.send(str.encode(" TRUE!"))
        else:
            conn.send(str.encode(" FALSE!"))

    # metoda TIME
    elif(request_arr[0] == 'TIME'):
        TIME(conn,addr)

    # metoda GAME
    elif(request_arr[0] == 'GAME'):
        GAME(conn,addr)
   
    # metoda CONVERT
    elif(request_arr[0] == 'CONVERT'):
        convert_option = " Convert Options:\n  -cmToFeet  \n  -FeetToCm  \n  -kmToMiles\n  -MileToKm"
        try:
            s = request_arr[1] # menyra e konvertimit
            n = float(request_arr[2]) # vlera qe ka me u konvertu
            conn.send(str.encode(" "+str(CONVERT(conn,s, n))))
        except IndexError:
            conn.send(str.encode(
                " Ju lutem shenoni cka deshironi te konvertoni pastaj shifren! \n" + convert_option))
        except ValueError:
            conn.send(str.encode(
                " Ju lutem shenoni cka deshironi te konvertoni pastaj shifren!\n "+convert_option ))

    # metoda GCF
    elif (request_arr[0] == 'GCF'):
        a = int(request_arr[1]) # numri_pare
        b = int(request_arr[2]) # numri_dyte
        conn.send(str.encode(" "+str(GCF(a, b))))

    # metoda STORAGE
    elif (request_arr[0] == 'STORAGE'):
        total, used, free = shutil.disk_usage("/")
        conn.send(str.encode(" Total: %d GiB" % (total // (2**30))+"\n Used: %d GiB" %
                             (used // (2**30))+"\n Free: %d GiB" % (free // (2**30))))
        
    # metoda HOST
    elif(request_arr[0] == 'HOST'):
        HOST(conn,addr)

    else:
        conn.send(str.encode(" Shenoni njeren nga kerkesat!"))
    
# funksioni qe pranon kerkesat e definuara me lart nga klienti
def client_thread(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            request = data.decode('utf-8') # pranohet komanda nga klienti dhe dekodohet me utf-8
            request_arr = request.split() # e ndajme komanden qe vje nga klienti dhe e ruajme ne forme te string array
            
            try:
                operation_arr(request_arr, conn, addr)
            except IndexError:
                # nqs. nuk shkruhet asnjera nga metodat e percaktuara
                conn.send(str.encode(" Kerkesa nuk eshte valide!"))
        except OSError:
            conn.close()
    conn.close()

# pranimi i kerkesave te njepasnjeshme nga klientet
while True:
    # ky rresht ben qe serveri te "degjoj" per kerkesa nga klienti permes lidhjes TCP
    connectionSocket, addr = serverSocket.accept()

    print('Klienti u lidh ne serverin %s me port %s' % addr)

    # krijimi i nje procesi te ri (threadi te ri), me lidhjen e nje klienti te ri
    start_new_thread(client_thread, (connectionSocket, addr,))