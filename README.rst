Module xml_preferences
----------------------

xml_preferences uses a scheme to create a hierarchy of objects that
represent the data stored in an XML files. CHanges to the objects can
later to saved back into an XML file.

The inspiration for this module is to store preferences for applications.

Classes
-------

  class xml_preferences.XmlPreferences

    __init__( scheme )

        The *scheme* is an instance of xml_preferences.Scheme.

    load( filename )

        Reads the preferences from the *filename* and returns the resulting
        tree of xml_preferences.PreferencesNode objects.

        In case of an error xml_preferences.ParseError is raise.

    loadString( text )

        Reads the preferences from the string *text* and returns the resulting
        tree of xml_preferences.PreferencesNode objects.

        In case of an error xml_preferences.ParseError is raise.

    save( data_node )

        Write the xml_preferences.PreferencesNode *data_node* hierarchy
        into the file used to load() the preferences.

    saveAs( data_node, filename )

        Write the xml_preferences.PreferencesNode *data_node* hierarchy
        into *fileaname*.

    saveToString( data_node )

        Write the xml_preferences.PreferencesNode *data_node* hierarchy
        into a string and return the string.

    saveToFile( data_node, f )

        Write the xml_preferences.PreferencesNode *data_node* hierarchy
        into the file object *f*.

  class xml_preferences.Scheme

    __init__( document_root )

        The *document_root* is an instance of xml_preferences.SchemeNode
        and represent the top level XML document element.

    dumpScheme( f )

        Write a dump of the scheme into the file object *f*.

        This is useful for debugging issues with scheme design.

  class xml_preferences.SchemeNode

    __init__( factory, element_name, all_attribute_info=None, element_plurality=False, key_attribute=None, collection_name=None, store_as=None, default=True, default_attributes=None )

        The *SchemeNode* represents on XML element with the name *element_name*.

        Any attributes that element has are listed in *all_attribute_info*, which is a tuple/list of names or name,type pairs.
        For example:

            all_attribute_info=('description', ('count', int))

        The *SchemeNode* can represent an in three ways:

        1. The element will only appear once.
        2. The element has  *element_plurality* set to True and can appear many times and will be stored as a list of elements in its parent.
        3. The element has a *key_attribute* and can appear many times and will be stored as a dictionary in its parent.

        The *collection_name* defaults to the element_name. The *collection_name* is passed to the parent 
        setChildNodeList or setChildNodeMap functions.

        *store_as* defaults to the *element_name* and is used to name the python variable that this node is store in its in parent object.

        When *default* is True and there is not XML that matches this SchemeNode a default value will be stored in the parent object.

        When the node is defaulted the attributes of the node can be set from a dictionary pass as *default_attributes*.

    dumpScheme( f, indent=0 )

        Write a dump of the scheme into the file object *f*.

        This is useful for debugging issues with scheme design.

    addSchemeChild( scheme_node )
    __lshift__( scheme_node )

        Add *scheme_node* as a child element of this SchemeNode.
        The << operator is useful in making the scheme definition readable.

  class xml_preferences.PreferencesNode

    For typical use all the set and get functions provide all the necessary features.
    That can be overriden to create special behaviour. It is assumed that all
    attribures are initised to a suitable value in __init__.

    __init__()

        Derive from *PreferencesNode* to initialise the variables used to hold the parsed XML preferences.

    finaliseNode( self )

        Called after all attributes and child nodes have been set on this node.

        Use this call to default any missing preferences.

    setAttr( self, name, value )

        Called to save the value of an attribute. The default implemention is:

        setattr( self, name, value )

    setChildNode( self, name, node )

        Called to save the value of singleton child element. The default implemention is:

        setattr( self, name, node )

    setChildNodeList( self, collection_name, node )

        Called to save the value of the next element to added to a list. The default implemention is:

        getattr( self, collection_name ).append( node )

    setChildNodeMap( self, collection_name, key, node )

        Called to save the value of the next element into a dict using the *key*. The default implemention is:

        getattr( self, collection_name )[ key ] = node

    getAttr( self, name )

        Called to get the value of the *name* attribute. The default implemention is:

        return getattr( self, name )

    getChildNode( self, name )

        Called to get the value of the *name* child node. The default implemention is:

        return getattr( self, name )

    getChildNodeList( self, collection_name )

        Called to get a list of values of the *collection_name* child nodes, which are assumed to be stored in a list. The default implemention is:

        return getattr( self, name )

    getChildNodeMap( self, collection_name )

        Called to get a list value of the *collection_name* child nodes, which are assumed to be stored in a dict. The default implemention is:

        return getattr( self, name ).values()

    dumpNode( self, f, indent=0 )

        Write a dump of the PreferencesNode hierarchy into file object *f*.

        Set *indent* to the number of spaces to indent the dumped text.

        Useful when debugging.

Example
-------

    See test_xml_preferences.py for example use.
