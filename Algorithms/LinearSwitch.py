from Utils.ValueCalc import calcTable
from Utils.switch import switch


def LinearSwitch(arrangement):
    for i in range(len(arrangement)):
        preValue = calcTable(arrangement[i])[0]
        for j in range(len(arrangement[i])):
            switch(arrangement, (i,j), (i,(j+1)%len(arrangement[i])))
