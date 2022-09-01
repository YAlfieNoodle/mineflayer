from javascript import require, On, Once, AsyncTask, once, off
import time, subprocess, sys, random,os
mineflayer = require('mineflayer')
BADHINTS = require('dns')
Vec3 = require('vec3')
pathfinder = require('mineflayer-pathfinder')
mcData = require('minecraft-data')("1.16.5")

bot = (mineflayer.createBot({"username":f"Slave",
                            'host': "162.19.20.129",
                            "port": 41823,
                            "version": "1.16.5"
                        }))

bot.loadPlugin(pathfinder.pathfinder)
def move():
            movements = pathfinder.Movements(bot, mcData)
            if True:
                movements.scafoldingBlocks = []
                movements.blocksCantBreak.add(mcData.blocksByName.farmland.id)
                movements.blocksCantBreak.add(mcData.blocksByName.dirt.id)
                movements.blocksToAvoid.delete(mcData.blocksByName.wheat.id)
                movements.blocksToAvoid.delete(mcData.blocksByName.white_carpet.id)
                movements.blocksCantBreak.add(mcData.blocksByName.oak_fence.id)
                movements.blocksCantBreak.add(mcData.blocksByName.white_carpet.id)
                #movements.blocksCantBreak.add(mcData.blocksByName.spruce_gate.id)
                #movements.blocksCantBreak.add(mcData.blocksByName.torch.id)
                bot.pathfinder.setMovements(movements)

move()

def places():
        move()
        try:
            bot.pathfinder.setGoal(pathfinder.goals.GoalNear(-552,71,3558, 0))#player.x,player.y,player.z, 2))
        except Exception as e:
            print(e)

goingHome1 = False
depositCountdown = 0

def slaveFarm():
    global depositCountdown
    if False:
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(-497,70,3826, 0))#player.x,player.y,player.z, 2))
        time.sleep(5)
        bed = bot.findBlock({
            "matching": mcData.blocksByName.orange_bed.id,
            "maxDistance": 5,
        })
        if bed:
            try:
                bot.sleep(bed)
            except Exception as e:
                print(e)
        time.sleep(5)
        places()
        time.sleep(15)
    while True:
        if goingHome1:
            continue
        depositCountdown += 1
        def blockToSow():
            while True:
                try:
                    return bot.findBlocks({
                        "point": bot.entity.position,
                        "matching": mcData.blocksByName.farmland.id,
                        "maxDistance": 100,
                        "count": 10000
                    })
                    break
                except:
                    subprocess.call([sys.executable, os.path.realpath("main.py")] + sys.argv[1:])
                    sys.exit()
        def blockToHarvest():
            while True:
                try:
                    return bot.findBlocks({
                        "point": bot.entity.position,
                        "maxDistance": 100,
                        "matching": mcData.blocksByName.wheat.id,
                        #"matching": block.metadata == 7,
                        "count": 10000
                    })
                    break
                except:
                    subprocess.call([sys.executable, os.path.realpath("main.py")] + sys.argv[1:])
                    sys.exit()
        
        toHarvest = blockToHarvest()
        toSow = blockToSow()

        harvest = False
        sow = False

        if toSow:
            for block in toSow:
                try:
                    bot.blockAt(block.offset(0,1,0)).name
                except:
                    continue
                if bot.blockAt(block.offset(0,1,0)).name == "air":
                    sow = block
                    while True:
                        try:
                            print("pathfind")
                            move()
                            bot.pathfinder.setGoal(pathfinder.goals.GoalNear(sow.x,sow.y+1,sow.z, 0))
                            print("pathfind done")
                            break
                        except:
                            print("goal error")
                            continue
                    #once(bot,"goal_reached")
                    time.sleep(5)
                    break
                else:
                    continue
            if sow:
                try:
                    bot.equip(mcData.itemsByName.wheat_seeds.id, 'hand')
                except:
                    pass
                try:
                    bot.placeBlock(bot.blockAt(sow.offset(0,1,0)), Vec3(0, 1, 0))
                except Exception as e:
                    print(e)
        while True:
            try:
                heelth = bot.health
                break
            except:
                continue
        if toHarvest and heelth >= 16 and depositCountdown <= 4:
            for block in toHarvest:
                if bot.blockAt(block).metadata == 7:
                    harvest = block
                    while True:
                        try:
                            move()
                            bot.pathfinder.setGoal(pathfinder.goals.GoalNear(harvest.x,harvest.y,harvest.z, 0))
                            break
                        except:
                            print("goal error")
                            continue
                    #once(bot,"goal_reached")
                    time.sleep(2)
                    break
                else:
                    continue
            if harvest:
                try:
                    bot.dig(bot.blockAt(harvest))
                except:
                    continue
            else:
                print("oopsy harvest")
                print("--------")
                continue
            
            time.sleep(0.5)
            #.93750
            try:
                bot.equip(mcData.itemsByName.wheat_seeds.id, 'hand')
            except Exception as e:
                print(e)
            try:
                bot.placeBlock(bot.blockAt(harvest), Vec3(0, 1, 0))
            except Exception as e:
                print(e)
        else:
            depositCountdown = 0
            try:
                move()
                bot.pathfinder.setGoal(pathfinder.goals.GoalNear(-565,71,3559, 0))
            except:
                pass
            time.sleep(10)
            chesty = bot.findBlock({
                "maxDistance": 4,
                "matching": mcData.blocksByName.chest.id,
            })
            try:
                opened = bot.openChest(chesty)
            except:
                pass
            while True:
                try:
                    opened.deposit(mcData.itemsByName["wheat"].id,None,1)
                except Exception as e:
                    break
            time.sleep(1)
            try:
                opened.close()
            except:
                pass
            try:
                move()
                bot.pathfinder.setGoal(pathfinder.goals.GoalNear(-566, 73, 3548, 0))
            except:
                pass
            time.sleep(5)
            chesty = bot.findBlock({
                "maxDistance": 3,
                "matching": mcData.blocksByName.chest.id,
            })
            try:
                opened = bot.openContainer(chesty)
            except:
                pass
            while True:
                try:
                    opened.deposit(mcData.itemsByName["wheat_seeds"].id,None,1)
                except Exception as e:
                    break
            time.sleep(1)
            try:
                opened.close()
            except:
                pass

places()

@On(bot, 'chat')
def onChat(this, user, message, *rest):
    if user == "YAlfie" and "info" in message.lower():
        bot.chat(f"im at {bot.entity.position.x:.0f}, {bot.entity.position.y:.0f}, {bot.entity.position.z:.0f}")
        bot.chat(f"my hunger is at {bot.food}/20")
        bot.chat(f"my health is at {bot.health}/20")
        bot.chat(f"my oxygen level is at {bot.oxygenLevel}")
        bot.chat(f"my food saturation is at {bot.foodSaturation}")

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

time.sleep(20)

slaveFarm()
