import os
import logging
from flask import Flask, render_template, Response, send_from_directory, request, current_app

app = Flask(__name__)
logging.basicConfig()
log = logging.getLogger(__name__)


@app.route("/")
def main():
    return render_template('main.html', title='pyDashie')

@app.route("/dashboard/<dashlayout>/")
def custom_layout(dashlayout):
    return render_template('%s.html'%dashlayout, title='pyDashie')

@app.route("/assets/application.js")
def javascripts():
    if not hasattr(current_app, 'javascripts'):
        import coffeescript
        scripts = [
            'assets/javascripts/jquery.js',
            'assets/javascripts/es5-shim.js',
            'assets/javascripts/d3.v2.min.js',

            'assets/javascripts/batman.js',
            'assets/javascripts/batman.jquery.js',

            'assets/javascripts/jquery.gridster.js',
            'assets/javascripts/jquery.leanModal.min.js',

            #'assets/javascripts/dashing.coffee',
            'assets/javascripts/dashing.gridster.coffee',

            'assets/javascripts/jquery.knob.js',
            'assets/javascripts/rickshaw.min.js',
            #'assets/javascripts/application.coffee',
            'assets/javascripts/app.js',
            #'widgets/clock/clock.coffee',
            'widgets/number/number.coffee',
        ]
        nizzle = True
        if not nizzle:
            scripts = ['assets/javascripts/application.js']

        output = []
        for path in scripts:
            output.append('// JS: %s\n' % path)
            if '.coffee' in path:
                log.info('Compiling Coffee for %s ' % path)
                try:
                    contents = coffeescript.compile_file(path)
                except Exception:
                    logging.error('Error compiling: %s', path)
            else:
                f = open(path)
                contents = f.read()
                f.close()

            output.append(contents)

        if nizzle:
            f = open('/tmp/foo.js', 'w')
            for o in output:
                print(o, file=f)
            f.close()

            f = open('/tmp/foo.js', 'rb')
            output = f.read()
            f.close()
            current_app.javascripts = output
        else:
            current_app.javascripts = ''.join(output)


    return Response(current_app.javascripts, mimetype='application/javascript')

@app.route('/assets/application.css')
def application_css():
    scripts = [
        'assets/stylesheets/application.css',
    ]
    output = ''
    for path in scripts:
        output = output + open(path).read()
    return Response(output, mimetype='text/css')

@app.route('/assets/images/<path:filename>')
def send_static_img(filename):
    directory = os.path.join('assets', 'images')
    return send_from_directory(directory, filename)

@app.route('/views/<widget_name>.html')
def widget_html(widget_name):
    html = '%s.html' % widget_name
    path = os.path.join('widgets', widget_name, html)
    if os.path.isfile(path):
        f = open(path)
        contents = f.read()
        f.close()
        return contents
