from javascript import require
import subprocess,sys
mineflayer = require('mineflayer')

bot = (mineflayer.createBot({"username":f"Max's Sex Slave",
                            'host': "162.19.20.129",
                            "port": 41823,
                            "version": "1.16.5"
                        }))

@On(bot, 'end')
def ened(reason,LOL):
    subprocess.call([sys.executable, os.path.realpath("main.py")] + sys.argv[1:])
    sys.exit()

@On(bot, 'respawn')
def ened(reason=False,LOL=False,asd=False):
    subprocess.call([sys.executable, os.path.realpath("main.py")] + sys.argv[1:])
    sys.exit()

@On(bot, 'kicked')
def ened(reason=False,LOL=False,asdasd=False,asdasddd=False):
    subprocess.call([sys.executable, os.path.realpath("main.py")] + sys.argv[1:])
    sys.exit()
