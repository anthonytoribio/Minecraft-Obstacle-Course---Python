#MineCraft Parkour Course
from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi.minecraftstuff import MinecraftTurtle
import math
import time
import random


class Decoration:
    def __init__(self):
        self.mc = Minecraft.create("localhost",4711)
        self.turtle = MinecraftTurtle(self.mc)
        self.turtle.speed(0)


    def create_tornado(self):
        radius = 15
        x = 191
        y = 168
        z = 272
        for i in range(32):
            self.turtle.mcDrawing.drawHorizontalCircle(x,y,z,radius,35,8)
            y -= 1
            radius -= .5

    def create_tie(self):
        radius = 5
        self.turtle.mcDrawing.drawSphere(195,150,334,radius,35,8)
        x1 = 194
        for i in range(3):
            self.turtle.mcDrawing.drawLine(x1,150,329,x1,150,326,35,8)
            self.turtle.mcDrawing.drawLine(x1,150,339,x1,150,342,35,8)
            x1 += 1
        y2 = 146
        for i in range(10):
            self.turtle.mcDrawing.drawLine(192,y2,325,199,y2,325,35,15)
            self.turtle.mcDrawing.drawLine(192,y2,343,199,y2,343,35,15)
            y2 += 1



class MC:
    
    def __init__(self):
        self.mc = Minecraft.create("localhost", 4711)
        self.p_id = self.mc.getPlayerEntityId('Shapeshifter1256')
        self._checkps = [(126,148,277)]
        self.check = (126.6,148,277.5)
        self.finished = 0
        self.x = 127
        self.y = 147
        self.z = 277
        

    def clear_all(self):
        self.mc.setBlocks(120,125,230,306,300,387,0)


    def tp_start(self):
        self.mc.player.setPos(126.6,148,277.5)

    def player_pos(self):
        return self.mc.player.getPos()

    def get_cps(self):
        return self._checkps

    def move_cp(self,x,y,z):
        self.check = (x,y,z)
        if (math.floor(x),math.floor(y),math.floor(z)) == self._checkps[-1]:
            self.finished += 1
        if self.finished == 1:
            self.mc.postToChat("Congratulations on Finishing!!!!")

    def tp_check(self):
        x,y,z = self.check
        self.mc.player.setPos(x,y,z)
        
    
    def make_starting_area(self):
        self.mc.setBlocks(125,147,276,127,147,278,41)
        self.mc.postToChat("Welcome to the Parkour Challenge!!")

    def make_a1(self):   #stage 1: Dirt
        for i in range(11):
            self.x += 3
            self.mc.setBlock(self.x, 147,277,3)
        self._checkps.append((self.x,self.y+1,self.z))
 

    def make_a2(self):  #Stage 2: Stone
        for i in range(10): #makes course move right
            self.x += random.randint(-1,1)
            self.y += random.randint(-1,1)
            self.z += random.randint(3,4)
            self.mc.setBlock(self.x,self.y,self.z,1)
        for i in range(15):   #makes the course move forward
            self.x += random.randint(2,4)
            self.y += random.randint(-1,1)
            self.mc.setBlock(self.x, self.y, self.z,1)
        self._checkps.append((self.x,self.y+1,self.z))

        
    def make_a3(self):  #Stage 3: Ladder 
        for i in range(5):
            self.x += 2 
            self.y += 3
            self.mc.setBlock(self.x,self.y-1,self.z,65,4)
            self.mc.setBlock(self.x,self.y-3,self.z,65,3)
        

    def make_a4(self): #Stage 4: Iron Block
        self._checkps.append((self.x,self.y+1,self.z))
        self.x += 2
        self.mc.setBlock(self.x,self.y,self.z,42)
        for i in range(9):
            self.x += 2
            self.y += random.randint(-1,1)
            self.z += random.randint(-1,1)
            self.mc.setBlock(self.x,self.y,self.z,42)
        self._checkps.append((self.x,self.y+1,self.z))


    def make_a5(self,x,y,z):
        '''
        Stage 5: Diamond block;
        If player moves within the constrained linear path then a
        diamond block will appear such that the player will not fall
        '''
        if math.floor(y) == self.y and math.floor(z) == self.z:
            if math.floor(x+1) in range(self.x+1,self.x+20):
                self.mc.setBlock(x,y-1,z,57)

    def gen_a6(self):
        '''
        Stage 6: Diamond block part 2;
        Creates two functions, make_a6 and del_a6. The function
        make_a6 creates the diamond blocks. The function
        del_a6 deletes any leftover diamond blocks. Together these
        functions make the illusion that the block is moving.
        '''

        def make_a6(ub = 6, lb = -6):
            if make_a6.movement == ub:
                make_a6.direction = 'left'
            elif make_a6.movement == lb:
                make_a6.direction = 'right'
            if make_a6.direction == 'right':
                make_a6.movement += 1
            else:
                make_a6.movement -= 1
            return self.mc.setBlocks(self.x+22,self.y-1,self.z + make_a6.movement,self.x+22,self.y-1,self.z+2+make_a6.movement,57)
        def del_a6():
            return self.mc.setBlocks(self.x+22,self.y-1,self.z-6,self.x+23,self.y,self.z+8,0)
        make_a6.direction = 'right'
        make_a6.movement = 0
        return make_a6,del_a6
                
                
    def make_ending_area(self):
        self._checkps.append((self.x + 26,self.y+1,self.z))
        self.mc.setBlocks(self.x + 26,self.y,self.z -1,self.x + 27,self.y,self.z + 1,41)


    def run(self):
        self.tp_start()
        self.make_starting_area()
        self.make_a1()
        self.make_a2()
        self.make_a3()
        self.make_a4()
        self.make_ending_area()
        make_a6, del_a6 = self.gen_a6()
        while True:
            x,y,z = self.player_pos()
            if y < 130:
                self.tp_check()
            if (math.floor(x),math.floor(y),math.floor(z)) in self.get_cps():
                self.move_cp(x,y,z)
            self.make_a5(x,y,z)
            del_a6()
            make_a6()
            time.sleep(.025)
        

    

if __name__ == "__main__":
    m = MC()
    drawing = Decoration()
    m.clear_all()
    drawing.create_tornado()
    drawing.create_tie()
    m.run()

