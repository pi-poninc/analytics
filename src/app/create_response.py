from flask import current_app

def create_response(content, status_code, mimetype):

    response = current_app.response_class(
        response=content,
        status=status_code,
        mimetype=mimetype
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Frame-Options'] = 'deny'

    return response