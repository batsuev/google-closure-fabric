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

# Install into your project

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

# Builders

## Building templates
For building soy templates there are `google_closure_fabirc.TemplatesBuilder` class.
Simple usage:

    def __get_templates_builder():
      soy = google_closure_fabric.TemplatesBuilder(PROJECT_PATH, use_goog=True)
      soy.add_template('src/templates/app.soy')
      soy.set_output_path_format('src/js/templates/{INPUT_FILE_NAME_NO_EXT}.soy.js')
      return soy

    def build():
      __get_templates_builder().build()
      
You can add multiple sources using `add_template` method.  
All additional arguments can be passed using `add_compiler_arg` method.  
All arguments are described here: https://developers.google.com/closure/templates/docs/javascript_usage  
If `use_goog` enabled in constructor, the following arguments will be added:

    --shouldProvideRequireSoyNamespaces
    --shouldGenerateJsdoc
    
### Example
For example, you have the following `src/templates/app.soy` file:

    {namespace app.templates.app}

    /**
     * Test template
     */
    {template .app}
    <div>test #2</div>
    {/template}
    
You need to build it to `src/js/templates/app.soy.js`, so just place the following code in your `fabfile.py`:

    import google_closure_fabric, os

    PROJECT_PATH = os.path.dirname(__file__)
    
    def __get_templates_builder():
        soy = google_closure_fabric.TemplatesBuilder(PROJECT_PATH, use_goog=True)
        soy.add_template('src/templates/app.soy')
        soy.set_output_path_format('src/js/templates/{INPUT_FILE_NAME_NO_EXT}.soy.js')
        return soy

    def bootstrap():
        google_closure_fabric.bootstrap(
            PROJECT_PATH,
            dir_name='libs-google',
            plovr=False
        )
        
    def build():
        __get_templates_builder().build()
        
After running `fab build` in your project, you've got the following content in your `src/js/templates/app.soy.js`:

    // This file was automatically generated from app.soy.
    // Please don't edit this file by hand.
    
    goog.provide('app.templates.app');
    
    goog.require('soy');
    goog.require('soydata');
    
    
    /**
     * @param {Object.<string, *>=} opt_data
     * @param {(null|undefined)=} opt_ignored
     * @return {string}
     * @notypecheck
     */
    app.templates.app.app = function(opt_data, opt_ignored) {
      return '<div>test #2</div>';
    };

## Building stylesheets
TBA

## Checking source code
TBA

## Building dependencies
TBA

## Building javascript
TBA

# Simple dev server
TBA

# Changes watcher
TBA
