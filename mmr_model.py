import random
import statistics

class Player:

    def __init__(self, id, real_mmr, mmr=1000):
        self.id = id
        self.mmr = mmr
        self.real_mmr = real_mmr
        self.matches_played = 0
    
    def __str__(self):
        return 'id: ' + str(self.id) + ', MMR:' + str(self.mmr) + ', REAL MMR:' + str(self.real_mmr)


    def play(self, other):
        result = random.uniform(-1, 1)
        dif = self.real_mmr - other.real_mmr
        summ = (self.real_mmr + other.real_mmr)
        threshold = dif/summ
        
        if result > threshold:
            return 0
        else:
            return 1
delta_list = []
def change_mmr(p1, p2, score):
    #typical win/lose k1
    std_delta = 15
    k1 = 1
    winner = score[0] - score[1] > 0
    if not winner:
        k1 = -k1
    
    #mmr difference factor k2
    max_diff = 500
    dif = p1.mmr - p2.mmr
    if dif > max_diff:
        dif = max_diff
    if dif < -max_diff:
        dif = -max_diff
    if winner:
        k2 = 1 - (dif/(max_diff*2))
    else:
        k2 = 1 + (dif/(max_diff*2))

    #ft length factor k3
    ft_max = 10
    ft_min = 3
    ft_len = max(score)
    k3 = 1 + (ft_len - ft_min)/(ft_max - ft_min)/10

    #mmr difference factor k4
    score_dif = abs(score[0] - score[1])
    if score_dif > 2:
        k4 = 1 + score_dif/(ft_len*4)
    else:
        k4 = 1


    delta = int(std_delta*k1*k4*k3)
    delta_list.append(abs(delta))
    p1.mmr = p1.mmr + delta
    p2.mmr = p2.mmr - delta
    return abs(delta)


def simulate(p1, p2, size, debug=False):
    wr = 0
    for i in range(0, size+1):    
        wins = 0
        matches = 0
        ft = int(random.uniform(3,11))
        while wins < ft and matches - wins < ft:
            matches += 1
            wins += p1.play(p2)
        if wins == ft:
            wr += 1
        delta1 = change_mmr(p1, p2, [wins, matches-wins])
        if debug:
            print('********* Match ', i, 'FT: ', ft,  ' *********')  
            print('score: ' + str(wins) + ':' + str(matches-wins))
            print('delta: ', abs(delta1))
            print('p1 mmr: ', p1.mmr)
            print('p2 mmr: ', p2.mmr)
            
    if debug:
        print('Win rate: ', wr/size)
        print('p1 mmr: ', p1.mmr)
        print('p2 mmr: ', p2.mmr)


players = []
mmr_list = []
size = 30


for i in range(10):
    players.append(Player(i, 500))

for i in range(10,20):
    players.append(Player(i, 500*2))

for i in range(20,30):
    players.append(Player(i, 500*3))

    
#for i in range(30):
 #   players.append(Player(i, 500 + (i+1)*100))

for i in range(len(players)):
    for k in range(i+1, len(players)):
        simulate(players[i], players[k], size)
    mmr_list.append((players[i].mmr, players[i].real_mmr))

print(mmr_list)


print(statistics.stdev(delta_list))
print(statistics.mean(delta_list))

print(max(delta_list))

print(min(delta_list))




def generate_deltas(ft):
    p1 = Player(1, 1000)
    p2 = Player(2, 1000)
    str_to_write = ''
    for i in range(ft):
        delta = change_mmr(p1,p2,[i, ft])
        str_to_write += str(ft) + ','
        str_to_write += str(i) + ':' + str(ft) + ','
        str_to_write += str(delta) + '\n'
    return str_to_write


str_to_write = 'ft,score, delta\n'
for i in range(3, 11):
    str_to_write+=generate_deltas(i)

f = open('ft_delta_data.csv', 'w')
f.write(str_to_write)
f.close()


