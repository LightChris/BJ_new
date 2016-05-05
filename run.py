from Classes.Game import Game
from Classes.Server import Server

server = Server()
game = Game(server)
game.mainloop()
