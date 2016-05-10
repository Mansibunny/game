#ECOO-q1.py
data = open("DATA12.txt")

for q in range(10):
    w=data.readline()
    num=int(data.readline())
    w=(w.replace("\n","")).split(" ")
    passed=0

    for i in range(num):

        marks=data.readline()    
        marks=(marks.replace("\n","")).split(" ")
        fin=eval(w[0]+"*0.01*"+marks[0])+eval(w[1]+"*0.01*"+marks[1])+eval(w[2]+"*0.01*"+marks[2])+eval(w[3]+"*0.01*"+marks[3])
        if fin>=50:
            passed+=1
                
    print(passed)    
