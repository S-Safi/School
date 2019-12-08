import math
import socket

class Signal:

    def __init__(self):
      self.xpos = 0
      self.ypos = 0
      self.windd = 0
      self.winds = 0
      self.fuel = 0

class Status:

  xpos = 0
  ypos = 0
  distancetravel = 0
  fuel = 100
  fpm = 0
  actualFuel = 0
  distancetoinit = 0

  def applySignal(self, signal):
      self.xpos = self.xpos + signal.xpos
      self.ypos = self.ypos + signal.ypos
      self.fuel = self.fuel - signal.fuel

  def accDistance(self, signal):
      self.distancetravel = self.distancetravel + math.sqrt(signal.xpos**2 +
                                                            signal.ypos**2)

  def disttoinit(self):
      self.distancetoinit = math.sqrt(self.xpos**2 + self.ypos**2)

  def calcAvgFuel(self):
      self.fpm = self.actualFuel / self.distancetravel

  def isEnoughFuel(self):
      estimateFuel = self.distancetoinit * self.fpm
      if estimateFuel > (4 / 5 * (255 - self.actualFuel)):
          print("Low Fuel Warning: return to base")

def parsePos(char1, char2):
    p1 = int(char1, 16)
    p2 = int(char2, 16)
    pfinal = p1 + (p2 / 16) - 8
    return pfinal

def parseDir(char1, char2):
    dHex = char1 + char2
    dInt = int(dHex, 16)
    dFinal = dInt * (360 / 255)
    return dFinal

def parseFuel(char1, char2):
    fHex = char1 + char2
    fInt = int(fHex, 16)
    fFinal = (fInt / 255) * 100
    return fFinal

def simpleParse(char1, char2):
    init = char1 + char2
    return int(init, 16)

status = Status()

s = socket.socket()
s.connect(('10.212.0.169', 50505))
buffer = ''
data = s.recv(512)
i = 0
buffer += data.decode('utf-8')
while buffer and i < len(buffer):
  data = s.recv(512)
  currentmsg = ''
  char = ''
  firstchar = buffer[i]
  buffer += data.decode('utf-8')
  while i < len(buffer) and char != '\n' and firstchar == 's':
      char = buffer[i]
      currentmsg += char
      i += 1
  signal = Signal()
  signal.xpos = parsePos(currentmsg[1], currentmsg[2])
  signal.ypos = parsePos(currentmsg[3], currentmsg[4])
  signal.windd = parseDir(currentmsg[5], currentmsg[6])
  signal.winds = parsePos(currentmsg[7], currentmsg[8])
  signal.fuel = parseFuel(currentmsg[9], currentmsg[10])
  status.actualFuel = status.actualFuel + simpleParse(currentmsg[9], currentmsg[10])
  status.applySignal(signal)
  status.accDistance(signal)
  status.disttoinit()
  status.calcAvgFuel()
  print("X: {xpos} Y: {ypos} F: {fuel_left} R: {fuel_rate}".format(xpos = round(status.xpos, 1), ypos = round(status.ypos, 1), fuel_left = round(status.fuel, 1), fuel_rate = round(status.fpm, 1)))
  status.isEnoughFuel()


