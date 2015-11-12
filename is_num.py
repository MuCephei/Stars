import math

def isNumber(input):
    try:
        float(input)
        result = True
    except:
        result = False
    return result

def angle(input):
    #note that many other things are angles, this just cleans it up for you
    if isNumber(input):
        temp = input/(2*math.pi)
        temp -= int(temp)
        return(temp*2*math.pi)
    else:
        input = None
    return input