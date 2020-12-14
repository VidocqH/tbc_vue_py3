from app import create_app, db
from app.models import User, Shops
from app.api.data_getter.start_proxy import start_proxy

start_proxy()
app = create_app()

@app.shell_context_processor
def make_shall_context():
    return {'db':db, 'User':User, 'Shops':Shops}