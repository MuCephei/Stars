import math

def isNumber(input):
    try:
        float(input)
        result = True
    except:
        result = False
    return result

def isAngle(input):
    if isNumber(input):
        while(input > 2*math.pi):
            input -= math.pi*2
        while(input < 0):
            input += math.pi*2
    else:
        input = None
    return input