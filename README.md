# Installation

    pip install https://github.com/batsuev/google-closure-fabric/archive/master.zip

# Usage with fabric
Example fabfile.py:

    import google_closure_fabric, os

    PROJECT_PATH = os.path.dirname(__file))

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
        t.build()

    def check_source_code():
        t = google_closure_fabric.Linter(PROJECT_PATH, strict=True)
        t.add_sources('js-app/src')
        t.add_exclude('js-app/src/templates/*.soy.js')
        t.lint()

    def autofix_source_code():
        t = google_closure_fabric.Linter(PROJECT_PATH, strict=True)
        t.add_sources('js-app/src')
        t.add_exclude('js-app/src/templates/*.soy.js')
        t.autofix()

    def build():
        check_source_code()
        build_deps()
        build_templates()
        build_stylesheets()

Run with:

    fab bootstrap

It will create contrib folder with google closure stylesheets, google closure templates, google closure library and plovr.

For building all just type:

    fab build
