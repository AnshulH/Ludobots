from pyrosim.commonFunctions import Save_Whitespace

class GEOMETRY_URDF: 

    def __init__(self,size, shape='box'):
        self.depth   = 3

        self.string1 = '<geometry>'

        if shape == 'box':
            sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])
            self.string2 = '   <box'
            self.string3 = '       size="' + sizeString + '">'
            self.string4 = '   </box>'
        elif shape == 'sphere':
            sizeString = str(size[0])
            self.string2 = '   <sphere'
            self.string3 = '       radius="' + sizeString + '">'
            self.string4 = '   </sphere>'

        self.string5 = '</geometry>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )

        Save_Whitespace(self.depth, f)

        f.write(self.string4 + '\n')

        Save_Whitespace(self.depth, f)

        f.write(self.string5 + '\n')
