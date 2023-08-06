modeldocs
=========

modeldocs is a documentation generator for your model subclasses.

By parsing source code files, this generates documentation for your data models with
a documentation format similar to apidocs (https://github.com/apidoc/apidoc)

Installation
------------

From pypi::

    $ pip install modeldocs

Or from the project root directory::

    $ python setup.py install

Usage
-----

First, create a configuration file in json, like (optional "include")::

    {
        "name": "My Documentation",
        "version": "1.0.0",
        "title": "My Documentation Title",
        "description": "This documents my data models",
        "include": [
            "mymodule",
            "tests/myfile.py"
        ]
    }

Save it as modeldocs.json in the current directory.

Then simply run it, and it'll search for all modeldocs recursively from the current directory::

    $ modeldocs

Or, specify via the command line where to look and what files::

    $ modeldocs --include mymodule myfile.py

Or pass a path to your custom config, which may specify an "include" configuration variable::

    $ modeldocs --config my_model_docs.json

Also, you can specify a custom output directory (default "docs")::

    $ modeldocs --output mydocs

Use --help/-h to view info on the arguments::

    $ modeldocs --help

The format is pretty simple. It follows a very similar format to apidocs (check github link above), example::

    class Motorcycle(MongoCollection):
        '''
        @modelGroup Vehicles
        @modelTitle Motorcycle
        @modelDescription This represents a motorcycle and all its data.
        
        @modelField {String} name the motorcycle name
        @modelField {Number} year the year it was made
        @modelField {Datetime} purchased_at the datetime it was purchased
        @modelField {String="red","green","blue"} color the color of the motorcycle, with specified possible values.
        @modelField {String} [owner] the owner of the vehicle (optional due to brackets)
        @modelField {Number} [wheels=2] the number of wheels (default 2 as specified)

        @modelExample {json} Motorcycle Example
            {
                "name": "yamaha v-star 650",
                "year": 2002,
                ...
            }
        '''
        pass

That's all it takes. Just add doc strings like the above to all your classes and it will recursively discover them
and generate the documentation into the "docs" directory.

Release Notes
-------------

:0.1.3:
    Fix issue with labeltype description wrapping multiple lines
:0.1.2:
    Add note to readme
:0.1.1:
    Better method of parsing, without loading any python modules. Just give it an include directory.
:0.1.0:
    Generates docs!
:0.0.1:
    Project created
