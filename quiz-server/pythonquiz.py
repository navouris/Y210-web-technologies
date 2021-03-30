import re
import os
import random
import datetime

total_questions = 5
class Quiz:
    allQuiz = {}
    def __init__(self, id, question, replies, correct):
        self.id = id
        self.question = question
        self.replies = replies
        self.correct = correct
        if not correct: print(id, replies); input() # error in input data
        Quiz.allQuiz[id] = self

    def calculate_score(self, reply):
        print(self.replies)
        if int(reply) == int(self.correct): return 1
        elif int(reply) == len(self.replies) + 1: return 0
        elif  0 < int(reply) < len(self.replies) + 1:
            return -1/len(self.replies)

    def __str__(self):
        out = "\n\nΕρώτηση ["+str(self.id)+"]\n"
        out += self.question.replace("<pre>", "----").replace("</pre>", "----")
        out += "Απαντήσεις:\n"
        for i,r in sorted(self.replies.items()):
            out += str(i)+"\t"+ r + "\n"
        # out += "Correct reply:" +str(self.correct)
        return out.strip("\n")

class Player:
    players = {}
    @staticmethod
    def load_players():
        if "players.txt" in os.listdir("."):
            print("loading players...")
            for line in open("players.txt", "r", encoding="utf-8"):
                # print(line)
                if line.startswith("Player:"):
                    p = Player(line.strip().split("\t")[-1], update=False)
                elif line.startswith("Game:"):
                    game = line.split("\t")
                    p.games[game[1]] = float(game[-1].strip())
        for i,p in Player.players.items():
            print(p)
    
    def __init__(self, name, update=True):
        self.name = name
        self.games = {}
        Player.players[name] = self
        if update: self.update_players()

    def new_game(self, score, update=True):
        self.games[datetime.datetime.now().strftime('%d-%m-%y %a %H:%M:%S')] = score
        if update: self.update_players()

    def update_players(self):
        # print("entering update players...")
        # print(Player.players)
        with open("players.txt", "w", encoding="utf-8") as file_out:
            for id,p in Player.players.items():
                file_out.write("\t".join(["Player:", p.name])+"\n")
                for g in p.games:
                    file_out.write("\t".join(["Game:", g, str(p.games[g])])+"\n")

    def __str__(self):
        out = "Παίκτης: "+self.name+"\n"
        if not self.games: out += "Δεν υπάρχουν προηγούμενες προσπάθειες"
        else: 
            out += "Προηγούμενες προσπάθειες:\n"
            for g in sorted(self.games):
                out += g + "\tscore: " + "{:.1f}%\n".format(self.games[g])
        return out


### interface to the quiz ################################

def load_quiz():
    ## φόρτωσε δεδομένα ερωτήσεων από εξωτερικό αρχείο
    id = None
    code = False
    replies = {}
    question = ""
    for line in open("questions.txt", "r", encoding="utf-8"):
        if not line.strip(): continue
        if line.startswith("Q"): 
            if id: Quiz(id, question, replies, correct)
            id = line.strip().strip(".")
            correct = None
            question = ""
            replies = {}
        elif re.findall("^[1-9]+?\.", line): # reply
            reply_number = int(line.split()[0].strip("."))
            if line.strip().endswith("***"):
                correct = reply_number
                line = line.strip().rstrip("***")
            reply_body = " ".join(line.split()[1:])
            replies[reply_number] = reply_body.strip()
        else:
            question += line
        
    ## load players
    Player.load_players()

def draw_questions():
    all_quiz_keys = list(Quiz.allQuiz.keys())
    random.shuffle(all_quiz_keys)
    return all_quiz_keys[:total_questions]

def show_question(id):
    if id in Quiz.allQuiz.keys():
        q = Quiz.allQuiz[id]
        return {"id": q.id, \
            "question": q.question, \
            "replies": {**q.replies, **{len(q.replies)+1: "Δεν γνωρίζω"}}, \
            "correct": q.correct}

def question_score(id, reply):
    q = Quiz.allQuiz[id]
    return q.calculate_score(reply)

def player_history(player):
    if player in Player.players.keys():
        return Player.players[player].__str__()
    else: return "Δεν υπάρχουν προηγούμενες προσπάθειες"

def save_game(name, score):
    player = Player.players[name] if (name in Player.players) \
        else Player(name, update=False)
    player.new_game( 100*score/total_questions )

#################################################

def play_quiz():
    name = None
    theQuestions =[]
    score = 0
    while True:
        if not name:
            name = input("Δώσε το όνομά σου:")
            if not name: break
        # player = Player.players[name] if (name in Player.players) else Player(name)
        # print(player)

        # select random questions
        theQuestions = draw_questions()
        # print(theQuestions);input()

        # ask the user one by one the questions
        for i,q in enumerate(theQuestions):
            while True:
                quizQuestion = Quiz.allQuiz[q]
                print("Ερώτηση {} από {}".format(i+1, len(theQuestions)))
                print(quizQuestion)
                # print(len(quizQuestion.replies), quizQuestion.replies)
                print(str(len(quizQuestion.replies)+1)+".\tΔεν γνωρίζω")
                answer = input("H απάντησή σας (x για έξοδο):")
                if (answer in "xXχΧ") or answer.isdigit() and 0<int(answer)<= len(quizQuestion.replies)+1:
                    break
            if answer in "xXχΧ": break # έξοδος από το παιχνίδι
            answer = quizQuestion.calculate_score(answer)
            if answer == 1:
                print("σωστή απάντηση")
            else: print("λάθος απάντηση, η σωστή απάντηση είναι η {}".format(quizQuestion.correct))
            score += answer
            print("To score είναι {:.1f}".format(score))
            input()
        
        # exit from game - save score
        print("Το συνολικό σκορ σας ήταν {:.1f} από {}".format(score, total_questions))
        # player.new_game( 100*score/total_questions )
        save_game(name, score)

        # ask player for new game
        reply = input("Θέλετε να παίξετε πάλι; (ναι/οχι)")
        # print('reply=', reply, reply.lower()[0] not in "νn" )
        if reply.lower()[0] not in "νn": break
        theQuestions =[]
        score = 0

if __name__ == "__main__":
    load_quiz()
    play_quiz()