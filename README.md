# Screen Tune
## [**Download latest release**](https://github.com/Quenary/screen-tune/releases/latest)
<img src="extras/screenshots/screen-tune-1.0.0.png?raw=true" alt="Alt text" width="600"/>

## Angular 19 / Pywebview
The app dynamically changes display settings (brightness, contrast, gamma) when the active window changes. It makes only one internet request to check for updates (this option can be disabled).
---
## Localization
* Russian
* English
---
## Tested
* Windows 10 22H1, Windows 11 22H2
* Common windows apps, fullscreen / borderless modes in several games
* NVidia, AMD GPUs
---
### TODOs:
* Add ngrx
* Write tests
* Improve logging
* Add linux support?
### Develop:
* Install node.js 22+ (nvm is recommended)
* Install python 3.12+ (python-is-python3, python3-venv if needed)
* Install frontend dependencies
    * ### Frontend
        ```
        cd frontend
        npm install
        npm run start | npm run watch | npm run build
        ```
    * ### Pywebview
        ```
        cd pywebview
        python -m venv venv
            # activate venv with
            source venv/bin/activate
            # or
            venv/scripts/activate
        pip install -r requirements.txt
        # Build with
        python build.py
        # Or run with
        python src/main.py
        ```