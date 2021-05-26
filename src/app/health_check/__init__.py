from flask import Blueprint

health_check_api = Blueprint('health_check', __name__)

# from . import views
@health_check_api.route('/health_check')
def health_check():
  return 'health_check is OK'
