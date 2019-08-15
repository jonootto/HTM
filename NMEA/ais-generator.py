#!/usr/bin/python

import math

CharTable =[["0", "@", "000000"], ["1", "A", "000001"], ["2", "B", "000010"], ["3", "C", "000011"], ["4", "D", "000100"], ["5", "E", "000101"],
            ["6", "F", "000110"], ["7", "G", "000111"], ["8", "H", "001000"], ["9", "I", "001001"], [":", "J", "001010"], [";", "K", "001011"],
            ["<", "L", "001100"], ["=", "M", "001101"], [">", "N", "001110"], ["?", "O", "001111"], ["@", "P", "010000"], ["A", "Q", "010001"],
            ["B", "R", "010010"], ["C", "S", "010011"], ["D", "T", "010100"], ["E", "U", "010101"], ["F", "V", "010110"], ["G", "W", "010111"],
            ["H", "X", "011000"], ["I", "Y", "011001"], ["J", "Z", "011010"], ["K", "[", "011011"], ["L", "\\", "011100"], ["M", "]", "011101"],
            ["N", "^", "011110"], ["O", "_", "011111"], ["P", " ", "100000"], ["Q", "!", "100001"], ["R", "\"", "100010"], ["S", "#", "100011"],
            ["T", "$", "100100"], ["U", "%", "100101"], ["V", "&", "100110"], ["W", "'", "100111"], ["`", "(", "101000"], ["a", ")", "101001"],
            ["b", "*", "101010"], ["c", "+", "101011"], ["d", ",", "101100"], ["e", "-", "101101"], ["f", ".", "101110"], ["g", "/", "101111"],
            ["h", "0", "110000"], ["i", "1", "110001"], ["j", "2", "110010"], ["k", "3", "110011"], ["l", "4", "110100"], ["m", "5", "110101"],
            ["n", "6", "110110"], ["o", "7", "110111"], ["p", "8", "111000"], ["q", "9", "111001"], ["r", ":", "111010"], ["s", ";", "111011"],
            ["t", "<", "111100"], ["u", "=", "111101"], ["v", ">", "111110"], ["w", "?", "111111"]]

PT = "AIVDM"
CHAN = "A"
MT = '000001'
RI = '00'
FILL = '000000'
NS = 5


def Invert(BinStr):     # Oh shit! I'm a lame programmer and can't find a function to swap bits in binary!
    return BinStr.replace("0", "A").replace("1", "0").replace("A", "1")

def convert(val,bits): # This magic function converts dec to bin in right format
    if (val < 0 ):
        val = -val
        val = (str(bin(~val)))[3:].zfill(bits)
        val = Invert (val)
    else:
        val = (str(bin(val)))[2:].zfill(bits)
    return val

def checksum(s):
    c = 0
    for ch in s:
        c ^= ord(ch)
    c = hex(c).upper()[2:]
    return c

def GenAis(PT, CHAN, MT, RI, MMSI, NS, ROT, SOG, PA, LON, LAT, COG, HDG, TS, FILL, CommState):
    # Preparing Variables
    MMSI = str((bin(MMSI)))[2:].zfill(30)
    NS = str((bin(NS)))[2:].zfill(4)
    SOG = str((bin(round(SOG*10))))[2:].zfill(10)
    LON = round(LON*600000)
    LAT = round(LAT*600000)
    COG = round(COG*10)

    # Converting Vars to bin
    LON = convert(LON,28)
    LAT = convert(LAT,27)
    HDG = convert(HDG,9)
    COG = convert(COG,12)
    ROT = convert(ROT,8)
    TS  = convert(TS,6)
    CommState = convert(CommState,19)

    MESSAGE_BIN = MT + RI + MMSI + NS + ROT + SOG + PA + LON + LAT + COG + HDG + TS + FILL + CommState
 #   print (MESSAGE_BIN)

    MESSENC = ""
    LEN = 28 #28 6-byte words = 168 bits
    P = 0
    # Starting encoding binary string to 6-byte word:
    while P <= LEN:
        TMPSTR = MESSAGE_BIN[(6*P):(6*P+6)]
        # print (TMPSTR)
        P += 1
        for PAIR in CharTable:
            if PAIR[2] == TMPSTR:
                MESSENC += PAIR[0]
#    print (MESSENC)
    MESSAIS = (PT + ',1,1,,' + CHAN + ',' + MESSENC + ',0')
    # CS = '4E'
    CS = checksum(MESSAIS)
    return ("!" + MESSAIS + '*' + CS)

# So here the program starts

MMSI = 366730000
PA = '0'
LON = -122.39253
LAT = 37.803803
HDG = 511
COG = 51.3
SOG = 20.8
ROT = 128
ACC = 0
TS = 50
CommState = 67427

print (GenAis(PT, CHAN, MT, RI, MMSI, NS, ROT, SOG, PA, LON, LAT, COG, HDG, TS, FILL, CommState))