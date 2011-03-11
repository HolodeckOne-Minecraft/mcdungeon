import materials
import random
from noise import *
from mymath import *

class Blank(object):
    _name = 'blank'

    def __init__ (self, parent):
        self.parent = parent

    def render (self):
        pass

class Cobble(Blank):
    _name = 'cobble'

    def render (self):
        if (sum_points_inside_flat_poly(*self.parent.canvas) > 0):
            for x in iterate_points_inside_flat_poly(*self.parent.canvas):
                self.parent.parent.setblock(x+self.parent.loc,
                                            materials.Cobblestone)

class DoubleSlab(Blank):
    _name = 'doubleSlab'

    def render (self):
        if (sum_points_inside_flat_poly(*self.parent.canvas) > 0):
            for x in iterate_points_inside_flat_poly(*self.parent.canvas):
                self.parent.parent.setblock(x+self.parent.loc,
                                            materials.DoubleSlab)

class WoodTile(Blank):
    _name = 'woodtile'

    def render (self):
        if (sum_points_inside_flat_poly(*self.parent.canvas) > 0):
            for x in iterate_points_inside_flat_poly(*self.parent.canvas):
                if ((x.x+x.z)&1 == 1):
                    self.parent.parent.setblock(x+self.parent.loc,
                                                materials.Wood)
                else:
                    self.parent.parent.setblock(x+self.parent.loc,
                                                materials.WoodPlanks)

class CheckerRug(Blank):
    _name = 'checkerrug'
    colors = (
        (7,8),   # dark grey / light grey
        (9,3),   # cyan / light blue
        #(14,10), # red / purple
        (11,9),  # dark blue / cyan
        (1,14),  # red / orange
        (7,15),  # dark grey / black
        #(3,4),   # light blue  / yellow
        (11,10), # dark blue  / purple
        (12,13), # brown  / dark green
        (15,13), # black  / dark green
        )

    def render (self):
        if (sum_points_inside_flat_poly(*self.parent.canvas) > 0):
            color = random.choice(self.colors)
            for x in iterate_points_inside_flat_poly(*self.parent.canvas):
                self.parent.parent.setblock(x+self.parent.loc,
                                            materials.Wool)
                if ((x.x+x.z)&1 == 1):
                    self.parent.parent.blocks[x+self.parent.loc].data = color[0]
                else:
                    self.parent.parent.blocks[x+self.parent.loc].data = color[1]
            if (random.randint(1, 100) < 50):
                return
            # Random chance to break it up.
            c = self.parent.canvasCenter()
            y = self.parent.canvasHeight()
            r = random.randint(1,1000)
            maxd = max(1, self.parent.canvasWidth(), self.parent.canvasLength())
            for x in iterate_points_inside_flat_poly(*self.parent.canvas):
                p = x+self.parent.loc
                d = ((Vec2f(x.x, x.z) - c).mag()) / maxd
                n = (pnoise3((p.x+r) / 2.3, y / 2.3, p.z / 2.3, 2) + 1.0) / 2.0
                if (n < d):
                    self.parent.parent.setblock(p, materials._floor)
                    self.parent.parent.blocks[p].data = 0

class BrokenDoubleSlab(Blank):
    _name = 'brokendoubleslab'
    def render (self):
        if (sum_points_inside_flat_poly(*self.parent.canvas) <= 0):
            return
        c = self.parent.canvasCenter()
        y = self.parent.canvasHeight()
        r = random.randint(1,1000)
        maxd = max(1, self.parent.canvasWidth(), self.parent.canvasLength())
        for x in iterate_points_inside_flat_poly(*self.parent.canvas):
            p = x+self.parent.loc
            d = ((Vec2f(x.x, x.z) - c).mag()) / maxd
            n = (pnoise3((p.x+r) / 2.3, y / 2.3, p.z / 2.3, 2) + 1.0) / 2.0
            if (n >= d):
                self.parent.parent.setblock(p, materials.DoubleSlab)

class Mud(Blank):
    _name = 'mud'
    def render (self):
        if (sum_points_inside_flat_poly(*self.parent.canvas) <= 0):
            return
        c = self.parent.canvasCenter()
        y = self.parent.canvasHeight()
        r = random.randint(1,1000)
        maxd = max(1, self.parent.canvasWidth(), self.parent.canvasLength())
        for x in iterate_points_inside_flat_poly(*self.parent.canvas):
            p = x+self.parent.loc
            d = ((Vec2f(x.x, x.z) - c).mag()) / maxd
            n = (pnoise3((p.x+r) / 2.3, y / 2.3, p.z / 2.3, 2) + 1.0) / 2.0
            if (n >= d+.50):
                self.parent.parent.setblock(p, materials.Water)
            elif (n >= d+.30):
                self.parent.parent.setblock(p, materials.SoulSand)
            elif (n >= d+.15):
                self.parent.parent.setblock(p, materials.Farmland)
                self.parent.parent.blocks[p].data = random.randint(0,1)
            elif (n >= d):
                self.parent.parent.setblock(p, materials.Dirt)

class Sand(Blank):
    _name = 'sand'
    def render (self):
        if (sum_points_inside_flat_poly(*self.parent.canvas) <= 0):
            return
        c = self.parent.canvasCenter()
        y = self.parent.canvasHeight()
        r = random.randint(1,1000)
        maxd = max(1, self.parent.canvasWidth(), self.parent.canvasLength())
        for x in iterate_points_inside_flat_poly(*self.parent.canvas):
            p = x+self.parent.loc
            d = ((Vec2f(x.x, x.z) - c).mag()) / maxd
            n = (pnoise3((p.x+r) / 2.3, y / 2.3, p.z / 2.3, 2) + 1.0) / 2.0
            if (n >= d+.20):
                self.parent.parent.setblock(p, materials.Sand)
            elif (n >= d+.10):
                self.parent.parent.setblock(p, materials.Sandstone)
            elif (n >= d):
                self.parent.parent.setblock(p, materials.Gravel)

class Bridges(Blank):
    _name = 'bridges'
    def render(self):
        # Find all the valid halls. These are halls with a size > 0.
        # We'll store a random position within the range of the hall.
        halls = [0,0,0,0]
        for h in xrange(4):
            if (self.parent.halls[h].size > 0):
                halls[h] = \
                    self.parent.halls[h].offset + 1 + \
                    random.randint(0, self.parent.halls[h].size - 3)
        midpoint = self.parent.parent.room_size / 2 - 2
        y = self.parent.canvasHeight()
        offset = self.parent.loc
        # Look for the X bounds between halls.
        if (halls[0] != 0 and halls[2] != 0):
            x1 = halls[0]
            x2 = halls[2]
        elif (halls[0] != 0):
            x1 = halls[0]
            x2 = x1
        elif (halls[2] != 0):
            x2 = halls[2]
            x1 = x2
        else:
            x1 = midpoint
            x2 = midpoint
        # Look for the Z bounds between halls.
        if (halls[1] != 0 and halls[3] != 0):
            z1 = halls[1]
            z2 = halls[3]
        elif (halls[1] != 0):
            z1 = halls[1]
            z2 = z1
        elif (halls[3] != 0):
            z2 = halls[3]
            z1 = z2
        else:
            z1 = midpoint
            z2 = midpoint
        # Now construct our points. 
        # c1-4 are the corners of the connecting
        # box. h0-3 are the start points of the halls.
        c1 = Vec(x1, y, z1)
        c2 = Vec(x2, y, z1)
        c3 = Vec(x2, y, z2)
        c4 = Vec(x1, y, z2)
        h0 = Vec(x1,
                 y,
                 self.parent.hallLength[0])
        h1 = Vec(self.parent.parent.room_size-self.parent.hallLength[1]-1,
                 y,
                 z1)
        h2 = Vec(x2,
                 y,
                 self.parent.parent.room_size-self.parent.hallLength[2]-1)
        h3 = Vec(self.parent.hallLength[3],
                 y,
                 z2)
        # Draw the bridges, if a hallway exists.
        # h0 -> c1
        # h1 -> c2
        # h2 -> c3
        # h3 -> c4
        if (self.parent.halls[0].size > 0):
            for p in iterate_cube(offset+h0,offset+c1):
                self.parent.parent.setblock(p, materials.StoneSlab)
                self.parent.parent.blocks[p].data = 2
        if (self.parent.halls[1].size > 0):
            for p in iterate_cube(offset+h1,offset+c2):
                self.parent.parent.setblock(p, materials.StoneSlab)
                self.parent.parent.blocks[p].data = 2
        if (self.parent.halls[2].size > 0):
            for p in iterate_cube(offset+h2,offset+c3):
                self.parent.parent.setblock(p, materials.StoneSlab)
                self.parent.parent.blocks[p].data = 2
        if (self.parent.halls[3].size > 0):
            for p in iterate_cube(offset+h3,offset+c4):
                self.parent.parent.setblock(p, materials.StoneSlab)
                self.parent.parent.blocks[p].data = 2
        # Draw the connecting bridges.
        # c1 -> c2
        # c2 -> c3
        # c3 -> c4
        for p in iterate_cube(offset+c1,offset+c2):
            self.parent.parent.setblock(p, materials.StoneSlab)
            self.parent.parent.blocks[p].data = 2
        for p in iterate_cube(offset+c2,offset+c3):
            self.parent.parent.setblock(p, materials.StoneSlab)
            self.parent.parent.blocks[p].data = 2
        for p in iterate_cube(offset+c3,offset+c4):
            self.parent.parent.setblock(p, materials.StoneSlab)
            self.parent.parent.blocks[p].data = 2

def new (name, parent):
    if (name == 'cobble'):
            return Cobble(parent)
    if (name == 'doubleslab'):
            return DoubleSlab(parent)
    if (name == 'woodtile'):
            return WoodTile(parent)
    if (name == 'checkerrug'):
            return CheckerRug(parent)
    if (name == 'brokendoubleslab'):
            return BrokenDoubleSlab(parent)
    if (name == 'mud'):
            return Mud(parent)
    if (name == 'sand'):
            return Sand(parent)
    if (name == 'bridges'):
            return Bridges(parent)
    return Blank(parent)
