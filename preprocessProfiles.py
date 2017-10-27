
allprofiles = open('facebookprofiles.txt', 'r').read().split('\n')
numProfs = int(len(allprofiles) / 50)
profileGroups = []

for i in range(5):
    try:
        doneProfs = set(open('done_' + str(i) + '.txt', 'r').read().split('\n'))
    except Exception as e:
        print(e)
        doneProfs = set()
    remaining = set(allprofiles[int(numProfs * i) : int(numProfs * (i + 1))])
    remaining = remaining.difference(doneProfs)
    outfile = open('profiles_' + str(i) + '.txt', 'w')
    for p in remaining:
        outfile.write(p)
        outfile.write('\n')