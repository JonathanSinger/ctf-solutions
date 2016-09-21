#Jonathan Singer TW:@jonathansinger
#my crap solution, but it works
#multiple everything by 100 so you dont work in floats
#iterate through the array and remove each amount
#solve over and over until you win!

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('misc.chal.csaw.io', 8000)
s.connect(server_address)

monies = [1000000,500000,100000,50000,10000,5000,2000,1000,500,100,50,25,10,5,1]

last = 0

while True:
  data = s.recv(100).splitlines()
  if 'flag' in data: break
  clean = data[0].replace('$','')
  coins = int(clean.replace('.',''))
  #print coins
  #print data[1]

  for x in monies:
    if (x == 1): last = 1
    if ((coins / x) >= 1):
        ss = str(coins / x)
        s.sendall(ss+"\n")
        #print ss
        coins = coins - (coins / x * x)
        if (last == 0): data = s.recv(20)
        else: data = s.recv(9)
    else:
        ss = "0\n"
        s.sendall(ss)
        #print "0"
        if (last == 0): data = s.recv(20)
        else: data = s.recv(9)

  if (data != "correct!\n"): break
  #print "NEXT"
  last = 0

print s.recv(200)
s.close()
