# ChatGptJsonTranslator

The ChatGptJsonTranslator is a simple Python script that translates the content of a JSON file into multiple languages using the ChatGpt API. This tool is especially useful for developers who need to localize their applications.

## Features

- Fast translation of JSON values without changing the keys
- Customizable translation to multiple languages
- Simple and easy to use
- Customizable input and output file path
- Automatic partitioning of large JSON files into smaller chunks
- Translation to different languages in parallel

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
3. Update the following parameters in the main function of the chatGptTranslator.py script:

- `apiKey`: Your ChatGpt API key
- `model`: The ChatGpt model to use for translation
- `inputPath`: The path to the input JSON file
- `outputPath`: The path to the output directory
- `translateTo`: A list of languages to translate the JSON content to

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

If you encounter `JSONDecodeError` during translation, you can try to translate the failed language only by isolating the specific value in `translateTo`.

If you encounter `Maximum Api requests reached` during translation, try translating to one language only first.

It's also worth noting that the answer from ChatGPT may vary from time to time, and the JSON string returned may not always be valid. In such cases, you may need to manually correct or modify the JSON string to make it valid before translating it.

## License

MIT License.
