from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, colorChange):

        self.depth  = 3
        
        color_name = "Blue" if colorChange else "Green"
        color_rgba = ["0.0", "0.0", "1.0"] if colorChange else ["0.0", "1.0", "0.0"]

        self.string1 = '<material name="' + str(color_name) + '">'
        self.string2 = '    <color rgba="' + color_rgba[0] + ' ' + color_rgba[1] + ' ' + color_rgba[2] + ' 1.0"/>'
        self.string3 = '</material>'


    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )