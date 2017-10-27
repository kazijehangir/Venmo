import json
import re

def validDate(date):
    # return Bool
    # date: String
    # Valid dates: 
    # July 16 at 11:42am
    # 13 mins
    # 4 hrs
    # July 16, 2016 at 11:42am 
    pattern1 = r'\w+ [0-9]+ at [0-9]+:[0-9]+[am|pm].*'
    pattern2 = r'[0-9]+ mins.*'
    pattern3 = r'[0-9]+ hrs.*'
    pattern4 = r'\w+ [0-9]+, [0-9]+ at [0-9]+:[0-9]+[am|pm].*'
    if re.match(pattern1, date) or re.match(pattern2, date) or re.match(pattern3, date) or re.match(pattern4, date):
        # print('Accepted date:', date)
        return True
    # print('Rejecting date: ', date)
    return False

allposts = {}
for i in range(5):
    print('Opening posts_' + str(i) + '.json')
    profs = open('posts_' + str(i) + '.json', 'r').read().strip().split('\n')
    for prof in profs:
        try:
            # print('JSON loading: ', prof.strip())
            prof = json.loads(prof.strip())
            # print('JSON: ', prof)
            for k in prof.keys():
                allposts[k] = prof[k] 
        except Exception as e:
            continue

allPostsOutput = open('allPosts.json', 'w')
json.dump(allposts, allPostsOutput)
print('Got ', len(allposts.keys()), ' profiles.')

filtered = {}
existed = 0
for prof in allposts.keys():
    found = False
    for post in allposts[prof]:
        if post['text'] or validDate(post['date']):
            found = True
    if found:
        filtered[prof] = allposts[prof]
    if len(allposts[prof]):
        existed += 1

print('Profiles with non-empty posts: ',existed)
print('Filtered profiles: ', len(filtered.keys()))

outputFiltered = open('filteredPosts.json', 'w')
json.dump(filtered, outputFiltered)

