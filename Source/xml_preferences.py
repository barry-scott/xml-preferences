#
#   xml_preferences.py
#
import xml.parsers.expat
import xml.dom.minidom
import xml.sax.saxutils

class ParseError(Exception):
    def __init__( self, value ):
        self.value = value

    def __str__( self ):
        return str(self.value)

    def __repr__( self ):
        return repr(self.value)

class XmlPreferences:
    def __init__( self, scheme ):
        self.scheme = scheme
        self.filename = None

    def load( self, filename ):
        self.filename = filename

        with open( self.filename, encoding='utf-8' ) as f:
            return self.loadString( f.read() )

    def saveAs( self, filename ):
        self.filename = filename
        self.save()

    def save( self ):
        pass

    def loadString( self, text ):
        try:
            dom = xml.dom.minidom.parseString( text )

        except IOError as e:
            raise ParseError( str(e) )

        except xml.parsers.expat.ExpatError as e:
            raise ParseError( str(e) )

        return self.__loadNode( self.scheme.document_root, dom.documentElement )

    def __loadNode( self, scheme_node, xml_parent ):
        if scheme_node.key_attribute is not None:
            if not xml_parent.hasAttribute( scheme_node.key_attribute ):
                raise ParseError( 'Element %s missing mandated attribute %s' %
                        (scheme_node.element_name, scheme_node.key_attribute) )

            node = scheme_node.factory( xml_parent.getAttribute( scheme_node.key_attribute ) )

        else:
            node = scheme_node.factory()

        # store all attribute values in the node
        for attr_name in scheme_node.all_attribute_names:
            # assume the factory creates an object that defaults all attributes
            if xml_parent.hasAttribute( attr_name ):
                node.setAttr( attr_name, xml_parent.getAttribute( attr_name ) )

        # look for supported child nodes
        for xml_child in xml_parent.childNodes:
            if xml_child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                if scheme_node.hasSchemeChild( xml_child.tagName ):
                    scheme_child_node = scheme_node.getSchemeChild( xml_child.tagName )
                    child_node = self.__loadNode( scheme_child_node, xml_child )

                    if scheme_child_node.element_plurality:
                        if scheme_child_node.key_attribute is not None:
                            node.setChildNodeMap( xml_child.tagName, scheme_child_node.key_attribute, child_node )

                        else:
                            node.setChildNodeList( xml_child.tagName, child_node )

                    else:
                        node.setChildNode( xml_child.tagName, child_node )

        # tell the node that it has all attributes and child node
        node.finaliseNode()

        return node

class Scheme:
    def __init__( self, document_root ):
        self.document_root = document_root

    def dumpScheme( self, f ):
        f.write( 'Scheme document root: %r' '\n' % (self.document_root,) )
        self.document_root.dumpScheme( f, 4 )

class SchemeNode:
    #
    # factory makes a class that the parser will set the values of all
    # the present attributes found in the element_name.
    #
    # plurality is False if this node can apprear only once
    # or true is many can be present.
    #
    # when plurality is true the nodes can be store in a list of a dict.
    # set the key_attribute to store in a dict
    #
    def __init__( self, factory, element_name, all_attribute_names=None, element_plurality=False, key_attribute=None ):
        self.factory = factory
        self.element_name = element_name
        self.element_plurality = element_plurality
        self.all_attribute_names = all_attribute_names if all_attribute_names is not None else tuple()
        self.key_attribute = key_attribute

        # convient defaulting
        if self.key_attribute is not None:
            self.element_plurality = True

        assert key_attribute is None or key_attribute not in self.all_attribute_names, 'must not put key_attribute in all_attribute_names'

        self.all_child_scheme_nodes = {}

    def __repr__( self ):
        return '<SchemeNode: %s>' % (self.element_name,)

    def dumpScheme( self, f, indent ):
        f.write( '%*s' 'SchemeNode %s plurality %r key %r attr %r' '\n' %
                (indent, '', self.element_name, self.element_plurality, self.key_attribute, self.all_attribute_names) )

        for child_name in sorted(  self.all_child_scheme_nodes ):
            child = self.all_child_scheme_nodes[ child_name ]
            child.dumpScheme( f, indent+4 )

    def addSchemeChild( self, scheme_node ):
        self.all_child_scheme_nodes[ scheme_node.element_name ] = scheme_node
        return self

    def __lshift__( self, scheme_node ):
        return self.addSchemeChild( scheme_node )

    def hasSchemeChild( self, name ):
        return name in self.all_child_scheme_nodes

    def getSchemeChild( self, name ):
        return self.all_child_scheme_nodes[ name ]

class PreferencesNode:
    def __init__( self ):
        pass

    def finaliseNode( self ):
        # called after all attributes and children have been set
        pass

    def setAttr( self, name, value ):
        setattr( self, name, value )

    def setChildNode( self, name, node ):
        setattr( self, name, node )

    def setChildNodeList( self, name, node ):
        getattr( self, name ).append( node )

    def setChildNodeMap( self, name, key, node ):
        getattr( self, name )[ key ] = node 

    def dumpNode( self, f, indent=0, prefix='' ):
        f.write( '%*s' '%s%r:' '\n' % (indent, '', prefix, self) )
        indent += 4
        for name in sorted( dir( self ) ):
            if name.startswith( '_' ):
                continue
            value = getattr( self, name )

            if callable( value ):
                continue

            if isinstance( value, PreferencesNode ):
                value.dumpNode( f, indent, '%s -> ' % (name,) )

            else:
                f.write( '%*s' '%s -> %r' '\n' % (indent, '', name, value) )
