# Flask Auto Translate
1. This is an automatic translation tool that defaults to the API format of Discuz!
2. You can define your own API format and language, model, welcome to use it

## Installation

Requirements:
-    Python 3.10

## Ubuntu install
```
    bash flask_auto_translate_install.sh
```
### Check Service
```
    sudo systemctl status flask_auto_translate.service
```

## Develop install

### Install requirement
```
    python3 setup.py install
```
### Start Flask Auto Translate
```
    python3 dist/Flask_Auto_Translate/Start_Flask_Auto_Translate.py
```

## Usage

### Language
#### Modifying ```schedule/TranslationBasic.py``` (Line 12) can change the language
```
    // Default hindi
    text[code]['hindi_text']
```

### Translation model
#### Modifying ```flask_auto_translate_config.ini```  can change the translation model, mode
```
    model = m2m100 / mbart50
```
