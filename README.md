# Installation
    
    pip install google_closure_fabric
    
or

    pip install https://github.com/batsuev/google-closure-fabric/archive/master.zip

# Usage with fabric
Example fabfile.py:

    import google_closure_fabric, os

    PROJECT_PATH = os.path.dirname(__file__)

    def bootstrap():
        google_closure_fabric.bootstrap(PROJECT_PATH, dir_name = 'contrib')

    def build_templates():
        t = google_closure_fabric.TemplatesBuilder(PROJECT_PATH, use_goog=True)
        t.add_template('js-app/templates/test.soy')
        t.set_output_path_format('js-app/src/templates/test.soy.js')
        t.build()

    def build_stylesheets():
        t = google_closure_fabric.StylesheetsBuilder(PROJECT_PATH)
        t.add_stylesheet('js-app/styles/test_style.css')
        t.set_output_file('js-app/styles/test.min.css')
        t.build()

    def build_deps():
        t = google_closure_fabric.DepsBuilder(PROJECT_PATH)
        t.set_source('js-app/src')
        t.set_output_file('js-app/deps.js')
        # t.set_custom_path_prefix('/js') - generate deps with '/js' prefixed paths
        t.build()

    def check_source_code():
        t = google_closure_fabric.Linter(PROJECT_PATH, strict=True, ignore_80_symbols=True)
        t.add_sources('js-app/src')
        t.add_exclude('js-app/src/templates/*.soy.js')
        t.lint()

    def autofix_source_code():
        t = google_closure_fabric.Linter(PROJECT_PATH, strict=True, ignore_80_symbols=True)
        t.add_sources('js-app/src')
        t.add_exclude('js-app/src/templates/*.soy.js')
        t.autofix()

    def build_js():
        t = google_closure_fabric.JSBuilder(PROJECT_PATH, advanced=True)
        t.set_sources_folder('js-app/src')
        t.set_main_file('test-file.js')
        t.set_output_file('test.min.js')
        t.build()

    def build():
        check_source_code()
        build_deps()
        build_js()
        build_templates()
        build_stylesheets()

Run with:

    fab bootstrap

It will create contrib folder with google closure stylesheets, google closure templates,
google closure library, google closure compiler and plovr.

For building all just type:

    fab build
