# Installation
    
    pip install google_closure_fabric

or for latest dev version:

    pip install https://github.com/batsuev/google-closure-fabric/archive/develop.zip

# Sample project structure
* my-project/
    * src/
        * js/
        * css/
        * templates/
    * dist/
    * pages/
    * libs-google/
    * fabfile.py

`src/js` - folder with javascript source code.  
`src/css` - css sources.  
`src/templates` - soy templates.  
`dist` - compiled output.  
`pages` - html files.  
`libs-google` - folder for all google libs.  
`fabfile.py` - fabric file.  

# Install/update libs/tools for your google closure project.

First of all, we need bootstrap task for setup all required libraries.
So, simple fabfile.py content:

    import google_closure_fabric, os

    PROJECT_PATH = os.path.dirname(__file__)

    def bootstrap():
        google_closure_fabric.bootstrap(
            PROJECT_PATH,
            dir_name='libs-google',
            plovr=False
        )

Running `fab bootstrap` in project folder will install all libraries to `libs-google` folder.
plovr installation is disabled in this example.

That will be installed:
* Google Closure Stylesheets (http://code.google.com/p/closure-stylesheets/)
* Google Closure Templates (https://developers.google.com/closure/templates/)
* Google Closure Compiler (https://developers.google.com/closure/compiler/)
* Google Closure Library (https://developers.google.com/closure/library/)
* Plovr (http://plovr.com)

You can disable some of them using bootstrap method arguments.

# Building templates
TBA

# Building stylesheets
TBA

# Checking source code
TBA

# Building dependencies
TBA

# Building javascript
TBA

# Simple server
TBA

# Changes watcher
TBA
