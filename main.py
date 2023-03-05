import openai
import os
import json
import concurrent.futures

class Translator:
    def __init__(self, params):
        self.apiKey = params["apiKey"]
        self.role = params["roles"]
        self.model = params["model"]
        self.inputPath = params["inputPath"]
        self.outputPath = params["outputPath"]
        self.translateTo = params["translateTo"]
        
        self.jsonData = None
        pass

    # Get response from gptBot
    def getResponse(self, index):
        openai.api_key = self.apiKey 

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": self.role, "content": f"Translate the below jsonStr to {self.translateTo[index]}, in proper JSON format. {self.jsonData}"}])
        return response.choices[0].message

    # Read input jsonFile
    def readFile(self):
        with open(self.inputPath, 'r') as f:
            self.jsonData  = json.load(f)
    
    # Write translated json to destination
    def writeFile(self, params): 
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)
        
        destination = f'{self.outputPath}/{self.translateTo[params["index"]]}.json'

        try:
            jsonObj = json.loads(params["translatedJson"])
            with open(destination, 'w') as f:
                json.dump(jsonObj, f, indent=2, ensure_ascii=False)
        except e:
            print(e)
            print(f"failed to translate to {self.translateTo[params['index']]}")
    
    # start sending request with processPool for faster performance
    def startTranslating(self):
        self.readFile()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_results = [executor.submit(self.translate, index) for index in range(len(self.translateTo))]

            for future in concurrent.futures.as_completed(future_results):
                _ = future.result()
            
            print("done")

    def translate(self, index):
        print(f"translating to {self.translateTo[index]}")
        translatedJson = self.getResponse(index)
        self.writeFile({"translatedJson": translatedJson["content"], "index": index})
        return 


if __name__ == "__main__":
    # check readme to see how to set up your config
    translator = Translator({
        "apiKey": "{YOUR-API-KEY}",
        "roles": "user",
        "model": "gpt-3.5-turbo",
        "inputPath": "{YOUR-INPUT-FILE-PATH}",
        "outputPath": "{YOUR-OUTPUT-FILE-PATH}",
        "translateTo": []
    })

    translator.startTranslating()




