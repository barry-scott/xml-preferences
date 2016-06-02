#
#   test_xml_preferences.py
#

import sys

from xml_preferences import XmlPreferences, Scheme, SchemeNode, PreferencesNode

class Preferences(PreferencesNode):
    def __init__( self ):
        super().__init__()

        self.edit = None
        self.view = None
        self.window = None

class Edit(PreferencesNode):
    def __init__( self ):
        super().__init__()

        self.program = None
        self.options = None

class View(PreferencesNode):
    def __init__( self ):
        super().__init__()

        self.mode = None

class Window(PreferencesNode):
    def __init__( self ):
        super().__init__()

        self.geometry = None

        self.all_colours = {}

    def setColour( self, name, fg, bg ):
        if name not in self.all_colours:
            self.all_colours[ name ] = Colour( name )

        colour = self.all_colours[ name ]
        colour.fg = fg
        colour.bg = bg

    def setChildNodeMap( self, name, key, node ):
        if name == 'colour':
            self.all_colours[ key ] = node

        else:
            raise RuntimeError( 'unknown name %r' % (name,) )

    def getChildNodeMap( self, name ):
        return sorted( self.all_colours.values() )

class Colour(PreferencesNode):
    def __init__( self, name ):
        super().__init__()

        self.name = name

        # can default based on name if required

        self.fg = None
        self.bg = None

    def __lt__( self, other ):
        return self.name < other.name

scheme = (Scheme(
        (SchemeNode( Preferences, 'preferences',  )
        << SchemeNode( Edit, 'edit', ('program', 'options') )
        << SchemeNode( View, 'view', ('mode',) )
        <<  (SchemeNode( Window, 'window', ('geometry',))
            << SchemeNode( Colour, 'colour', ('fg', 'bg'), key_attribute='name' )
            )
        )
    ) )

test_xml_1 = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<preferences>
    <edit program="fred" />
    <window>
        <colour name="normal" fg="1,2,3" bg="4,5,6"/>
    </window>
</preferences>
'''

def main( argv ):
    print( '# --- dumpScheme ---' )
    scheme.dumpScheme( sys.stdout )

    xml_prefs = XmlPreferences( scheme )
    prefs = xml_prefs.loadString( test_xml_1 )

    print( '# --- prefs API ---' )
    print( 'edit program', prefs.edit.program )
    print( 'edit options', prefs.edit.options )

    print( '# --- dumpNode ---' )
    prefs.dumpNode( sys.stdout )

    print( '# --- saveToFile ---' )
    prefs.window.setColour( 'bold', '99,0,99', '00,99,00' )

    xml_prefs.saveToFile( prefs, sys.stderr )

    return 0

if __name__ == '__main__':
    sys.exit( main( sys.argv ) )
