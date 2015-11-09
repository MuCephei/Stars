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
        temp = input/(2*math.pi)
        temp -= int(temp)
        return(temp*2*math.pi)
    else:
        input = None
    return input