# Installation

    pip install https://github.com/batsuev/google-closure-fabric/archive/master.zip

# Usage with fabric
Example fabfile.py:

    import google_closure_fabric, os

    def bootstrap():
        google_closure_fabric.bootstrap(os.path.dirname(__file__), dir_name = 'contrib')

    def build_templates():
        t = google_closure_fabric.TemplatesBuilder(os.path.dirname(__file__), use_goog=True)
        t.add_template('js-app/templates/test.soy')
        t.set_output_path_format('js-app/src/templates/test.soy.js')
        t.build()

    def build_stylesheets():
        t = google_closure_fabric.StylesheetsBuilder(os.path.dirname(__file__))
        t.add_stylesheet('js-app/styles/test_style.css')
        t.set_output_file('js-app/styles/test.min.css')
        t.build()

Run with:

    fab bootstrap

It will create google-closure folder with google closure stylesheets, google closure templates, google closure library and plovr.