from javascript import require, On, Once, AsyncTask, once, off
from simple_chalk import chalk
from random import randint
from utils.vec3_conversion import vec3_to_str
import PySimpleGUI as sg

# Import the javascript libraries
mineflayer = require("mineflayer")
vec3 = require("vec3")

# Global bot parameters
#server_host = "localhost"
#server_port = 3000
reconnect = True

class MCBot:

    def __init__(self, bot_name):
        self.bot_args = {
            "host": server_host,
            "port": server_port,
            "username": bot_name,
            "hideErrors": False,
            #"auth": "microsoft"
        }
        self.reconnect = reconnect
        self.bot_name = bot_name
        self.start_bot()

    # Tags bot username before console messages
    def log(self, message):
        print(f"[{self.bot.username}] {message}")

    # Start mineflayer bot
    def start_bot(self):
        self.bot = mineflayer.createBot(self.bot_args)

        self.start_events()

    # Attach mineflayer events to bot
    def start_events(self):

        # Login event: Triggers on bot login
        @On(self.bot, "login")
        def login(this):

            # Displays which server you are currently connected to
            self.bot_socket = self.bot._client.socket
            self.log(
                (
                    f"Logged in to {self.bot_socket.server if self.bot_socket.server else self.bot_socket._host }"
                )
            )

        # Spawn event: Triggers on bot entity spawn
        @On(self.bot, "spawn")
        def spawn(this):
            self.bot.chat("Hi!")

        # Kicked event: Triggers on kick from server
        @On(self.bot, "kicked")
        def kicked(this, reason, loggedIn):
            if loggedIn:
                self.log((f"Kicked whilst trying to connect: {reason}"))

        # Chat event: Triggers on chat message
        @On(self.bot, 'chat')
        def msgHandler(this, user, message, *args):
            if "quit" in message:
                self.bot.chat("Goodbye!")
                self.reconnect = False
                this.quit()
            elif "coinflip" in message:
                if randint(1, 2) == 1:
                    self.bot.chat("Heads!")
                    self.log((f"Flipped a  coin!"))
                else:
                    self.bot.chat("Tails!")
                    self.log((f"Flipped a  coin!"))
            elif "dice" in message:
                self.bot.chat(f"You rolled a {randint(1, 6)}")
                self.log((f"Rolled a dice!"))   
            elif "break" in message:
                block = self.bot.blockAtCursor()
                if block:
                    self.bot.dig(block)
                    self.log(f"Breaking block!")
                else:
                    self.log(f"There is no block!")                
            elif "look" in message:
                player_position = self.bot.players[user].entity.position.offset(0, 1, 0)
                self.bot.lookAt(player_position)
        @On(self.bot, "end")
        def end(this, reason):
            self.log((f"Disconnected: {reason}"))

            # Turn off old events
            off(self.bot, "login", login)
            off(self.bot, "spawn", spawn)
            off(self.bot, "kicked", kicked)
            off(self.bot, "msgHandler", msgHandler)

            # Reconnect
            if self.reconnect:
                self.log((f"Attempting to reconnect"))
                self.start_bot()

            # Last event listener
            off(self.bot, "end", end)



layout = [
            [sg.Text("Setup your Bot", size=(15,1))],
            [sg.Text("Bot Name:", size =(15, 1)), sg.InputText(do_not_clear=False)],
            [sg.Text("Server Host:", size=(15,1)), sg.InputText(do_not_clear=False)],
            [sg.Text("Server Port:", size=(15,1)), sg.InputText(do_not_clear=False)],
            [sg.Checkbox("Auto-Reconnect", default=True)],
            [sg.Output(size=(60, 20), font=('Helvetica 10'))],
            [sg.Button("Start"), sg.Button("Exit")],
    ]

sg.theme("DarkGrey11")
window = sg.Window("MineBot | Create a Bot", layout, size=(1080, 700))

while True:
    event, values = window.read()
    bot_name = values[0]
    server_host = values[1]
    server_port = values[2]
    reconnect = values[3]

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "Start":
        bot = MCBot(bot_name)
window.close()
