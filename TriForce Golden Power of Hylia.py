import re
import math

def checkAndConvert(value):
    if(not(isinstance(value,str))):
        return None
    value = value.strip()
    
    if(len(value)==0):
        return None

    neg = 1
    if(value[0] == "-"):
        neg = -1
        value = value[1:]

    out = 0
    t = -1
    for v in value:
        if(t>=0):
            t += 1
        if(v==" "):
            return None
        if(v=="."):
            if(t==-1):
                t=0
                continue
            else:
                return None
        if("0"<=v and v<="9"):
            out = out*10 + int(v)
        else:
            return None
    
    if(t==-1):
        return neg*out
    return neg*out/(10**t)

def superscript(n):
    out = ""
    while(n>0):
        v = n%10
        if(v==1):
            out = "\u00b9" + out
        elif(v==2 or v==3):
            out = chr(ord("\u00b0")+v) + out
        else:
            out = chr(ord("\u2070")+v) + out
        n //= 10
    return out

def mkTerm(coeff, deg):
    if (deg==0):
        return("" +str(abs(coeff))+ "")
    elif (coeff == 1 or coeff == -1):
        if(deg==1):
            return("x")
        else:
            sub = superscript(deg)
            return("x" +str(sub)+ "")
    else:    
        if(deg==1):
            return("" +str(abs(coeff))+ "x")
        else:
            sub = superscript(deg)
            return("" +str(abs(coeff))+ "x" +str(sub)+ "")

def formatPoly(coeffs):
    out = ""
    last = coeffs[-1]
    rounded = [round(item, 2) for item in coeffs]
    for i in range(len(rounded)):
        if (coeffs[i]!=0):
            out = (mkTerm(rounded[i],i)) + out
            if coeffs[i] < 0:
                out = " - " + out
            else:
                out = " + " + out
    for i in range(len(coeffs)):
        if last < 0:
            out = re.sub(' - ', '-', out, 1)
            break 
        else:
            out = out[3:]
            break 
    return out

def calculate(coeffs, x):
    out = [None]*(len(coeffs))
    out1 = []
    for i in range(len(coeffs)):
        if (i == 0):
            out[i] = coeffs[i]
        if (i == 1):
            out[i] = coeffs[i] * x
        if (i > 1):
            out[i] = coeffs[i] * (x**i)
    out1 = sum(out)
    return out1

def zeros(coeffs):
    out = None
    if (len(coeffs) == 1):
        if coeff[0] == 0:
            out = "INF"
        else:
            out
    if (len(coeffs) == 2):
        out = -(coeffs[0]) / (coeffs[1])
    if (len(coeffs) == 3):
        a = coeffs[2]
        b = coeffs[1]
        c = coeffs[0]
        d = (b**2) - (4*a*c)
        if (d>0):
            solA = (-b - math.sqrt(d))//(2*a)
            solB = (-b + math.sqrt(d))//(2*a)
            out = [solA, solB]
        if (d==0):
            solA = (-b - math.sqrt(d))//(2*a)
            out = [solA]
        if (d<0):
            out = []
    return out

def calculateAll(coeffs, values):
    out = []
    for v in values:
        out += [(v,calculate(coeffs,v))]
    return out

def mapToIndex(points, startX, startY):
    pts = []
    out = []
    sortedOut = []
    for i in range(len(points)):
        if (points[i][0] >= startX and points[i][0] <= (startX+20) and points[i][1] <= startY and points[i][1] >= (startY-20)):
            pts += [points[i]]
    for i in range(len(pts)):
        col = (pts[i][0]) - startX
        row = ((pts[i][1]) * 20 - (startY * 20))
        out += [(abs(row) + (col))]
        sortedOut = sorted(out)
    return sortedOut

def setupAxis(graph, startX, startY):
    out = ""
    for i in range(20):
        for j in range(18):
            if(i == abs(startY)):
                out += "–"*abs(startX)+"+"+ "–"*(20-abs(startX)-1)
                break
            if(j == abs(startX)-1):
                out += graph[i*20+j]+"|"
            if(j>=0):
                out += graph[i*20+j]
    return out
    
def addToGraph(graph, points, symbol):
    newGraph = ""
    k = 0
    for i in range(20):
        for j in range(20):
            if (k < len(points) and i*20+j == points[k]):
                newGraph += symbol
                k+=1
            else:
                newGraph += graph[i*20+j]             
    return newGraph
    
def printGraph(graph):
    for i in range(20):
        for j in range(20):
            print(graph[i*20+j],end=" ")
        print()

g = "·"*400
g = setupAxis(g, -9, 15)
eq = []
sym = "@#$%&"
#printGraph(g)


print("(1) Add Polynomial")
print("(2) Remove Polynomial")
print("(3) Change Window Corner")
print("(4) Determine Zeros")
print("(5) Determine Intersections between")
print("(6) EXIT\n")

while(True):
    choice = 0
    while(True):
        option = input("Enter your option number: ")
        print("\n")
        if(option.isnumeric()):
            choice = int(option)
            break
    if (choice == 1):
        degree = 0
        while(True):
            num = input("What is the degree of the polynomial? ")
            print("\n")
            if(num.isnumeric()):
                degree = int(num)
                break
        poly = [None]*(degree + 1)
        i = 0
        while (i<len(poly)):
            coefficient = 0
            while(True):
                num2 = input("Enter the term of degree "+str(i)+": ")
                print("\n")
                coefficient = checkAndConvert(num2)
                if(num2==None):
                    print("...enter only integer or decimal point numbers\n\n")
                else:
                    break
            poly[i] = coefficient
            i += 1
        startX = -9 #
        startY = 15 #
        startX1 = startX
        values = [None]*20
        values[0] = startX
        i = 1
        while (i<len(values)):
            while(True):
                startX1 += 1
                values[i] = startX1
                break 
            i += 1
        eq += [poly]
        g = "·"*400
        g = setupAxis(g, startX, startY)
        for i in range(len(eq)):
            e = eq[i]
            points = calculateAll(e,values)
            loc = mapToIndex(points, startX, startY)
            g = addToGraph(g, loc, sym[i])
        printGraph(g)
        print("\n")
    if (choice == 2):
        break
    if (choice == 3):
        break
    if (choice == 4):
        break
    if (choice == 5):
        print("The polynomials are currently")
        for i in range(len(eq)):
            polyStr = formatPoly(eq[i])
            print("("+str(i)+") "+str(polyStr)+" ")
        print("\n")
        a = 0 
        while(True):
            choose = input("Choose the two polynomials to determine intersection with: ")
            print("\n")
            if(a.isnumeric()):
                choose = int(a)
                break
            
    if (choice == 6):
        break 
