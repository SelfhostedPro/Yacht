from flask import render_template

from app.main.views import main
import traceback


@main.app_errorhandler(403)
def forbidden(_):
    return render_template('errors/403.html'), 403


@main.app_errorhandler(404)
def page_not_found(_):
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(_):
    raw_tb = traceback.format_exc()
    tb = "<br />".join(raw_tb.split("\n"))
    return render_template('errors/500.html', exception=_, tb=tb ), 500
