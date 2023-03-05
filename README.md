# ChatGptJsonTranslator

The ChatGptJsonTranslator is a fast and simple Python script that translates the content of a JSON file into different languages using the ChatGpt API. This script is perfect for developers who are struggling with the localization of their applications.

## Features

- Fast translation of JSON values without changing the keys
- Customizable translation to multiple languages
- Simple and easy to use
- customizable input and output file path

## Prerequisites

- Python 3.x
- ChatGpt API key (https://platform.openai.com/account/api-keys)
- JSON input file

## Getting Started

1. Create a virtual environment and activate it:
   ```
   python3 -m venv chatGptTranslator
   source chatGptTranslator/bin/activate
   ```
2. Install the required dependencies:
   ```
   pip3 install -r requirements.txt
   ```
3. Update your `apiKey`, `model`, `inputFilePath`, `outputFilepath`, and `translateTo` in the main function

   For Example

   ```
   # Credential and model for the chatGpt instance
   {
        "apiKey": "This-is-not-a-key",
        "roles": "user",
        "model": "gpt-3.5-turbo",
        "inputPath": "locales.json",
        "outputPath": "path/to/dest",
        "translateTo": ["french", "spanish", "japanese"]
    }
   ```

4. Run the script

   ```
   python3 chatGptTranslator.py
   ```

5. Your translated content will be saved in the specified output file(s).

## How to use

The translateTo parameter in the main function of chatGptTranslator.py determines which languages to translate the content to. To add or remove languages, simply update the list of languages:

```
translateTo = ["french", "japanese", "spanish"]
```

Here's an example of what an input JSON file might look like:

```
{
  "welcomeMessage": "Welcome to my app!",
  "loginMessage": "Please log in to continue."
}
```

And here's an example of what the output JSON files might look like after running the script:

```
// french.json
{
  "welcomeMessage": "Bienvenue dans mon application!",
  "loginMessage": "Veuillez vous connecter pour continuer."
}

// japanese.json
{
  "welcomeMessage": "私のアプリへようこそ！",
  "loginMessage": "続けるにはログインしてください。"
}

// spanish.json
{
  "welcomeMessage": "¡Bienvenido a mi aplicación!",
  "loginMessage": "Por favor, inicie sesión para continuar."
}
```

## TroubleShooting

If you encounter any issues while using the ChatGptJsonTranslator, please try the following:

- Check that you have the correct ChatGpt API key and model specified in the script
- Ensure that your input JSON file is valid and formatted correctly
- Verify that you have the necessary permissions to read from and write to the specified file paths

## License

MIT License.
