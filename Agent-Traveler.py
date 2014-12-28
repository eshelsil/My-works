def get_float(text):
    try:
        return float(text)
    except:
        print "Try again"
        return get_float(raw_input("Enter a number: "))

def enter_places():
    places = []
    place = raw_input("First place's name (airport): ")
    while place not in ["", "NO", "no", "No", "0"]:
        x = get_float(raw_input("Place's x: "))
        y = get_float(raw_input("Place's y: "))
        places.append((place, x, y))
        place = raw_input("Next place's name (for finish type 'no'): ")
    return places

def find_dist(place1, place2):
    return ((place1[1] - place2[1]) ** 2 + (place1[2] - place2[2]) ** 2) ** 0.5

memo = {}
def save_result(func):
    def new_func(*args):
        try:
            return memo[args]
        except:
            memo[args] = func(*args)
            return memo[args]
    return new_func

@save_result
def find_best_choice(cur_place, goal, to_go, num_places, num_been):
    best = None
    for place in to_go:
        boy = Position(place, goal, list(to_go), num_places, num_been + 1)
        dist = boy.dist + find_dist(cur_place, place)
        if best == None or dist < best[0]:
            best = (dist, boy)
    return best
    
class Position(object):
    def __init__(self, cur_place, goal, to_go, num_places, num_been):
        self.place = cur_place
        to_go.remove(cur_place)
        if num_places == num_been:
            self.dist = 0
            self.best_choice = None
        else:
            if to_go == []:
                to_go = [goal]
            best = find_best_choice(cur_place, goal, tuple(to_go),\
                                          num_places, num_been)
            self.dist = best[0]
            self.best_choice = best[1]

def agent():
    places = enter_places()
    position = Position(places[0], places[0], places, len(places) + 1, 1)
    cur_pos = position
    road = []
    while cur_pos != None:
        road.append(cur_pos.place)
        cur_pos = cur_pos.best_choice
    travel_dist = position.dist
    print
    print "Shortest Road:"
    for place in road:
        print place[0], "(" + str(place[1]) + ", " + str(place[2]) + ")"
    print
    print "Travel Distance:", travel_dist

agent()
