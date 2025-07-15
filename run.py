# %% Add the parent directory to the sys.path
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# %% import libraries
from app import create_app

# %% create app
app = create_app()

# %% run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# %%
