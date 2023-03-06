import openai
import os
import json
import concurrent.futures
import sys


class Translator:
    def __init__(self, params):
        self.apiKey = params["apiKey"]
        self.role = params["roles"]
        self.model = params["model"]
        self.maxChunkSize = params["maxChunkSize"]
        self.jsonData = []
        pass

    def setFilePathAndLang(self, params):
        self.inputPath = params["inputPath"]
        self.outputPath = params["outputPath"]
        self.translateTo = params["translateTo"]

    # Get response from gpt endpoint
    def getResponse(self, index):
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            future_results = [executor.submit(
                self.loopPartitionedJsonData, {"partitionedJsonData": partitionedJsonData, "index": index}) for partitionedJsonData in self.jsonData]

            response = []
            for future in concurrent.futures.as_completed(future_results):
                response.append(future.result())

        return response

    # loop partitionedJson and send request to gpt endpoint
    def loopPartitionedJsonData(self, params):
        openai.api_key = self.apiKey
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": self.role, "content": f"Translate the value of below jsonStr to {self.translateTo[params['index']]}, in proper JSON format. {params['partitionedJsonData']}"}])

        return response.choices[0].message

    # Read input jsonFile
    def readFile(self):
        with open(self.inputPath, 'r') as f:
            jsonData = json.load(f)

        partitionedJsonData = {}
        size = 0
        for key in jsonData:
            size += sys.getsizeof(jsonData[key])
            if size < self.maxChunkSize:
                partitionedJsonData.update({key: jsonData[key]})
            elif not partitionedJsonData:
                print(
                    "Sorry, the JSON data is too large to break down. Aborting mission.")
                exit()
            else:
                self.jsonData.append(partitionedJsonData)
                partitionedJsonData = {}
                size = 0

        if partitionedJsonData:
            self.jsonData.append(partitionedJsonData)

    # Write translated json to destination
    def writeFile(self, params):
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        destination = f'{self.outputPath}/{self.translateTo[params["index"]]}.json'

        try:
            jsonStrList = [json.loads(translatedJson["content"])
                           for translatedJson in params["response"]]
            jsonObj = {}
            for jsonStr in jsonStrList:
                jsonObj.update(jsonStr)
            with open(destination, 'w') as f:
                json.dump(jsonObj, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(e)
            print(
                f"failed to translate to {self.translateTo[params['index']]}")

    # entrypoint
    def start(self):
        self.readFile()

        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            future_results = [executor.submit(
                self.translate, index) for index in range(len(self.translateTo))]

            for future in concurrent.futures.as_completed(future_results):
                _ = future.result()

            print("done")

    # start translating json to different language
    def translate(self, index):
        print(f"translating to {self.translateTo[index]}")
        response = self.getResponse(index)
        print(
            f"translated to {self.translateTo[index]}, writing to destination...")
        self.writeFile(
            {"response": response, "index": index})
        return


if __name__ == "__main__":
    # check readme to see how to set up your config
    translator = Translator({
        "apiKey": "{YOUR_API_KEY}",
        "roles": "user",
        "model": "gpt-3.5-turbo",
        "maxChunkSize": 2048,
    })

    translator.setFilePathAndLang({
        "inputPath": "{YOU_INPUT_FILE_PATH}",
        "outputPath": "{YOU_OUTPUT_FILE_PATH}",
        "translateTo": []
    })

    translator.start()
