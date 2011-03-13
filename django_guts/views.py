import os
import re

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.importlib import import_module
from django.conf import settings
from django.http import HttpResponse, Http404

DEFAULT_IGNORE = (r'\..*\.swp', r'.*\.pyc', r'.*\.pyo')
DEFAULT_HL_EXTENSIONS = ('py', 'html', 'htm')

def apps(request):
    apps = settings.INSTALLED_APPS
    return render_to_response(
        'guts/index.html',
        dict(
            title='Apps',
            apps=sorted(apps),
        ),
        context_instance = RequestContext(request),
    )


def app_guts(request, app, cwd = '/', leaf = ''):
    mod = import_module(app)

    mod_dir = os.path.dirname(mod.__file__)

    full_path = os.path.join(mod_dir, '.' + cwd, leaf)
    full_path = full_path.replace(os.path.pardir, '')
    full_path = os.path.abspath(full_path)
    rel_path = os.path.relpath(full_path, mod_dir)

    ignore_list = getattr(settings, 'GUTS_IGNORE', DEFAULT_IGNORE)
    ignore_list = [re.compile('^%s$' % item) for item in ignore_list]

    def ignored(name):
        for rule in ignore_list:
            if rule.match(name):
                return True
        return False

    if not os.path.exists(full_path) or ignored(leaf):
        raise Http404()

    if os.path.isdir(full_path):
        files = os.listdir(full_path)
        files = (name for name in files if not ignored(name))
        files = (
            dict(name=name, is_dir=os.path.isdir(os.path.join(full_path, name)))
            for name in files
        )
        files = sorted(files, key=lambda item: (not item['is_dir'], item['name']))

        return render_to_response(
            'guts/dir.html',
            dict(
                title=os.path.normpath(os.path.join(app, rel_path)) + os.path.sep,
                app=app,
                cwd=cwd,
                leaf=leaf,
                rel_path=rel_path,
                full_path=full_path,
                files=files,
            ),
            context_instance = RequestContext(request),
        )
    else:
        base, ext = os.path.splitext(full_path)

        if ext and ext[1:] in getattr(settings, 'GUTS_HL_EXTENSIONS', DEFAULT_HL_EXTENSIONS):
            source = open(full_path).read()

            try:
                from pygments import highlight
                from pygments.lexers import get_lexer_for_filename
                from pygments.formatters import HtmlFormatter

                lexer = get_lexer_for_filename(full_path)
                formatter = HtmlFormatter(linenos=True, lineanchors='line', anchorlinenos=True)
                highlighted = highlight(source, lexer, formatter)
                hl_styles = formatter.get_style_defs('.highlight')
            except ImportError:
                highlighted = None
                hl_styles = None


            return render_to_response(
                'guts/source.html',
                dict(
                    title=os.path.join(app, rel_path),
                    app=app,
                    cwd=cwd,
                    leaf=leaf,
                    rel_path=rel_path,
                    full_path=full_path,
                    source=source,
                    highlighted=highlighted,
                    hl_styles=hl_styles,
                ),
                context_instance = RequestContext(request),
            )
        return HttpResponse(open(full_path).read())

