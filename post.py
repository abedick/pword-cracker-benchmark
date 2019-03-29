import ast

def main():

    sizes = [100,500,1000,5000,10000,50000]
    ltr = ["a","b","c", "d"]

    trials = {}
    for x in sizes:
        for y in ltr:
            trials[str(x)+"-"+y] = {}

    for i in range(2,73):
        r =  getResult("data/"+str(i)+".txt")

        if len(r) == 13:

            inter = ast.literal_eval(r[8].strip())
            
            hashType = "md5"
            if inter[1] == "2":
                hashType = "sha1"
            elif inter[1] == "3":
                hashType = "lm"

            trials[inter[0]][hashType] = {
                "john-dict": float(r[0].strip()),
                "hcat-dict": float(r[6].strip()),
                "john-brute": float(r[4].strip()),
                "hcat-brute": float(r[2].strip())
            }
        
        else:
            print("error; data/"+str(i)+".txt")

    algo = 'john-brute'
    for t in trials:
        try:
            print(t+","+str(trials[t]["md5"][algo])+","+str(trials[t]["sha1"][algo])+","+str(trials[t]["lm"][algo]))
        except:
             a = 5

def getResult(file):
    f = open(file)
    g = f.readlines()
    return g

main()