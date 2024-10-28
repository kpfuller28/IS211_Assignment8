import random
import time

class PlayerFactory:
    @staticmethod
    def createPlayer(playerType, name):
        if playerType == 'human':
            return Player(name)
        elif playerType == 'computer':
            return ComputerPlayer(name)

class Player:
    def __init__(self, name):
        self.name   = name
        self.score = 0
        self.turnScore = 0
        self.gameWins = 0

    def hold(self):
        self.score += self.turnScore
        self.resetTurnScore()

    def resetTurnScore(self):
        self.turnScore = 0

class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def decide(self):
        threshold = min(25, 100 - self.score)
        if self.turnScore >= threshold:
            return 'h'
        else:
            return 'r'

class Die:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return  random.randint(1, self.sides)

class Game:
    def __init__(self, players):
        random.seed(0)
        self.die = Die(6)
        self.players = players
        self.currentPlayer =  self.players[0]
        self.gameOver = False
        self.turn = 0
        self.rolls = 0
        self.winner = []

    def switchTurn(self):
        if self.players.index(self.currentPlayer) == len(self.players) - 1:
            self.currentPlayer = self.players[0]
        else:
            self.currentPlayer = self.players[self.players.index(self.currentPlayer) + 1]

    def takeTurn(self):
        self.turn += 1
        still = ''
        while not self.gameOver:
            self.scoreboard()
            print(f"{still}{self.currentPlayer.name}'s turn!")
            result = self.die.roll()
            self.rolls += 1
            print(f'{self.currentPlayer.name} rolled a: {result}')
            still = 'Still '

            if result == 1:
                print(f"Oh no! Your turn is over! You lost {self.currentPlayer.turnScore} points!")
                self.currentPlayer.resetTurnScore()
                input('Press enter to pass the die: ')
                self.switchTurn()
                break
            else:
                self.currentPlayer.turnScore += result
                if self.currentPlayer.score + self.currentPlayer.turnScore >= 100:
                    self.currentPlayer.score += self.currentPlayer.turnScore
                    self.winner.append(self.currentPlayer)
                    self.gameEnd()
                    self.resetGame()
                    self.gameOver = True
                    return
                print(f"{self.currentPlayer.name}'s score this turn: {self.currentPlayer.turnScore}")

                if isinstance(self.currentPlayer, ComputerPlayer):
                    decision = self.currentPlayer.decide()
                else:
                    decision = input(f"{self.currentPlayer.name}, would you like to roll again or hold? Press r to roll or h to hold: ")

                while decision != 'r' and decision != 'h':
                    decision = input(f"Invalid input: {decision}. Please only input r to roll again, or h to hold: ")
                if decision == 'h':
                    print(f"{self.currentPlayer.name} holds with a turn score of: {self.currentPlayer.turnScore}")
                    self.currentPlayer.hold()
                    input('Press enter to pass the die ')
                    self.switchTurn()
                    break

    def gameEnd(self):
        if len(self.winner) == 1:
          print(f"{self.winner[0].name} has won with a score of {self.winner[0].score}!")
          self.winner[0].gameWins += 1
        else:
            print(f"It's a tie! The following players tied with the score of: {self.winner[0].score}")
            for player in self.winner:
                print(player.name)
                player.gameWins += 1
            print('They will all get game wins!')
        self.scoreboard()

    def resetGame(self):
        for player in self.players:
            player.score = 0
            player.turnScore = 0
        self.turn = 0
        self.rolls = 0
        self.gameOver = False
        self.winner = []


    def scoreboard(self):

        print('-------------------------------------------')
        print(f'SCOREBOARD --- Turn: {self.turn} --- Rolls: {self.rolls}')
        for player in self.players:
            if player in self.winner:
                print(f"{player.name}: {player.score} ---- WINNER!")
            else:
                print(f"{player.name}: {player.score}")
        print('-------------------------------------------')

class TimedGameProxy(Game):
    def __init__(self, players, timeLimit=60):
        super().__init__(players)
        self.timeLimit = timeLimit
        self.startTime = time.time()

    def takeTurn(self):
        timeLeft = time.time() - self.startTime
        if timeLeft >= self.timeLimit:
            print('-------------------------------------------')
            print("The time limit has been reached!")
            print('-------------------------------------------')
            self.gameOver = True
            self.declareWinner()
            return
        print('-------------------------------------------')
        print(f"There are {round(60 - timeLeft)} seconds left!")
        print('-------------------------------------------')
        super().takeTurn()
    def declareWinner(self):
        highScore = max(player.score for player in self.players)
        for player in self.players:
            if player.score == highScore:
                self.winner.append(player)
        self.gameEnd()

class Series:
    def __init__(self, gamesToWin, players, timed):
        self.gamesToWin = gamesToWin
        self.players = players
        self.winner = []
        self.seriesOver = False
        self.timed = timed

    def playGame(self):
        if self.timed == 't':
          game = TimedGameProxy(self.players)
        else:
          game = Game(self.players)
        self.scoreboard()
        while not game.gameOver:
            game.takeTurn()
        for player in self.players:
            if player.gameWins >= self.gamesToWin:
                self.winner.append(player)
        self.seriesEnd()
        self.seriesOver = True
        return

    def scoreboard(self):
        print(f"--------- SERIES SCOREBOARD ---------")
        for player in self.players:
            if player in self.winner:
                print(f"{player.name} game wins: {player.gameWins} ---- SERIES WINNER")
            else:
                print(f"{player.name} game wins: {player.gameWins}")
        print(f"-------------------------------------")

    def seriesEnd(self):
        if len(self.winner) == 1:
          print(f"{self.winner[0].name} wins the series!")
        else:
            print("The series is a tie!")
        self.scoreboard()



def main():
    players = []
    factory = PlayerFactory()
    while True:
        numberPlayers = input('How many players would you like to play Pig with: ')
        try:
            numberPlayers = int(numberPlayers)
            break
        except ValueError:
            print(f"Invalid input. Please input a number for number of players.")
    for i in range(numberPlayers):
        isComputer = input("Type 'c' if you want this player to be computer controlled: ")
        if isComputer.lower() == 'c':
            player = factory.createPlayer('computer', f"Computer {i+1}")
        else:
          playerName = input(f"Please enter Player {i+1} name: ")
          player = factory.createPlayer('human', playerName)
        players.append(player)
    while True:
        gamesToWin = input('How many games to win the whole series: ')

        try:
            gamesToWin = int(gamesToWin)
            break
        except ValueError:
            print(f"Invalid input. Please input number for number of games to win.")
    timed = input("Type 't' if you would like the games to be timed at 60 seconds: ")
    series = Series(gamesToWin, players, timed)
    while not series.seriesOver:
        series.playGame()




if __name__ == "__main__":
    pass


main()