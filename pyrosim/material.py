from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, color):

        self.depth  = 3

        # self.string1 = '<material name="Cyan">'

        # self.string2 = '    <color rgba="0 1.0 1.0 1.0"/>'

        # self.string3 = '</material>'

        self.colorCoords = {
            "Blue" : ["0.01", "0.54", "1.0"],
            "Green": ["0.25", "0.76", "0.50"]
        }

        self.string1 = '<material name="' + color + '">'
        self.string2 = '    <color rgba="' + self.colorCoords[color][0] + ' ' + self.colorCoords[color][1] + ' ' + self.colorCoords[color][2] + ' 1.0"/>'
        self.string3 = '</material>'


    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
