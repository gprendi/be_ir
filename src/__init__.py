from src.app import define_app
import os

is_prod = os.environ.get('production') or None
print("is_prod " + is_prod)
if is_prod is not None:
    app = define_app()