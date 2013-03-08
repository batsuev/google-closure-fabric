# Installation
    
    pip install google_closure_fabric

or for latest dev version:

    pip install https://github.com/batsuev/google-closure-fabric/archive/develop.zip

# Boilerplate
You can create new project using gclosureboilerplate script. Sample:

    mkdir my-project
    cd my-project
    gclosureboilerplate .
    fab bootstrap
    fab build
    fab serve

Open http://localhost:8000/ and enjoy. Or http://localhost:8000/index.min.html for compiled version.
All changes in sources will rebuild automatically.

# Boilerplate project structure
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
`fabfile.py` - fabric file with all required tasks.

# Google Closure libraries and tools

Running `fab bootstrap` in project folder will install all libraries to `libs-google` folder.
plovr installation is disabled in this example.

That will be installed:
* Google Closure Stylesheets (http://code.google.com/p/closure-stylesheets/)
* Google Closure Templates (https://developers.google.com/closure/templates/)
* Google Closure Compiler (https://developers.google.com/closure/compiler/)
* Google Closure Library (https://developers.google.com/closure/library/)
* Plovr (http://plovr.com)

# fabfile.py

    import google_closure_fabric, os

    PROJECT_PATH = os.path.dirname(__file__)
    SRC = 'src/js'

    def __get_css_builder():
        css = google_closure_fabric.StylesheetsBuilder(PROJECT_PATH)
        css.add_stylesheet('src/css/app.css')
        css.set_output_file('dist/css/app.min.css')
        return css

    def __get_deps_builder():
        deps = google_closure_fabric.DepsBuilder(PROJECT_PATH)
        deps.set_source(SRC)
        return deps

    def __get_templates_builder():
        soy = google_closure_fabric.TemplatesBuilder(PROJECT_PATH)
        soy.add_template('src/templates/app.soy')
        soy.set_output_path_format('src/js/templates/app.soy.js')
        return soy

    def __get_js_builder():
        js_builder = google_closure_fabric.JSBuilder(PROJECT_PATH)
        js_builder.set_output_file('dist/js/app.min.js')
        js_builder.set_sources_folder('src/js')
        js_builder.set_main_file('app.js')
        return js_builder

    def __get_linter():
        linter = google_closure_fabric.Linter(PROJECT_PATH, strict=True, ignore_80_symbols=True)
        linter.add_sources('src/js')
        linter.add_exclude('src/js/templates/app.soy.js')
        linter.add_exclude('src/js/soy.js')
        linter.add_exclude('src/js/deps.js')
        return linter

    def bootstrap():
        google_closure_fabric.bootstrap(
            PROJECT_PATH,
            dir_name='libs-google',
            plovr=False
        )

    def serve():
        deps = __get_deps_builder()
        deps.set_custom_path_prefix('../'+SRC)
        google_closure_fabric.serve(
            PROJECT_PATH,
            html_folder='pages',
            deps_builder=deps,
            stylesheets_builder=__get_css_builder(),
            templates_builder=__get_templates_builder(),
            js_builder=__get_js_builder()
        )

    def autofix():
        __get_linter().autofix()

    def build():
        deps = __get_deps_builder()
        deps.set_custom_path_prefix(SRC)
        deps.set_output_file('src/js/deps.js')
        deps.build()

        __get_linter().lint()
        __get_css_builder().build()
        __get_templates_builder().build()
        __get_js_builder().build()


