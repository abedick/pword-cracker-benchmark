import ast



def main():
    # print("post")

    sizes = [100,500,1000,5000,10000,50000]
    ltr = ["a","b","c", "d"]

    trials = {}
    for x in sizes:
        for y in ltr:
            trials[str(x)+"-"+y] = {}


    # print(trials)
    # t = ["1","2","3"]
    # tests = []
    # for x in trials:
    #     for y in t:
    #         tests.append(x + ":" + y)
    # # print(tests)


    i = 2

    for i in range(2,73):
        r =  getResult("data/"+str(i)+".txt")

        if len(r) == 13:

            
            # print("data/"+str(i)+".txt")
            # print()

            inter = ast.literal_eval(r[8].strip())
            
            hashType = "md5"
            if inter[1] == "2":
                hashType = "sha1"
            elif inter[1] == "3":
                hashType = "lm"

            # print(inter[0])
            trials[inter[0]][hashType] = {
                "john-dict": float(r[0].strip()),
                "hcat-dict": float(r[6].strip()),
                "john-brute": float(r[4].strip()),
                "hcat-brute": float(r[2].strip())
            }
            # print("\tjohn-dict\t" + r[0].strip())
            # print("\thcat-dict\t" + r[6].strip())
            # print("\tjohn-brut\t" + r[4].strip())
            # print("\thcat-brut\t" + r[2].strip())
        
        else:
            print("error; data/"+str(i)+".txt")
        # for x in r:
        #     print(x.strip())

    # print(trials)

    algo = 'john-brute'
    for t in trials:
        # print(t)

        try:
            print(t+","+str(trials[t]["md5"][algo])+","+str(trials[t]["sha1"][algo])+","+str(trials[t]["lm"][algo]))
        except:
             a = 5

        # for a in trials[t]:
        #     print("\t"+a.ljust(5)+" "+str(trials[t][a]['hcat-brute']))
        # # print("\t", trials[t])

def getResult(file):
    f = open(file)
    g = f.readlines()
    return g

main()