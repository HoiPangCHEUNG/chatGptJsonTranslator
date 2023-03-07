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

        self.inputPath = params["inputPath"]
        self.outputPath = params["outputPath"]
        self.translateTo = params["translateTo"]

        self.maxGptWoker = params["maxGptWoker"]
        self.maxJsonFileWorker = params["maxJsonFileWorker"]
        pass

    def updateFilePathAndLang(self, params):
        self.inputPath = params["inputPath"]
        self.outputPath = params["outputPath"]
        self.translateTo = params["translateTo"]

    def updateMaxWorkerNum(self, params):
        self.maxGptWoker = params["maxGptWoker"]
        self.maxJsonFileWorker = params["maxJsonFileWorker"]

    # Loop partitionedJson and send request to gpt endpoint
    def translatePartitionedJsonData(self, params):
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.maxGptWoker) as executor:
            future_results = [executor.submit(
                self.getGptResponse, {"partitionedJsonData": partitionedJsonData, "index": index, "langIndex": params["langIndex"]}) for index, partitionedJsonData in enumerate(params["jsonData"])]

            response = [future.result()
                        for future in concurrent.futures.as_completed(future_results)]

        return response

    # Get response from gpt endpoint
    def getGptResponse(self, params):
        print(
            f"Translating part {params['index']} to {self.translateTo[params['langIndex']]}")

        openai.api_key = self.apiKey
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": self.role, "content": f"Translate the value of below jsonStr to {self.translateTo[params['langIndex']]}, in proper JSON format. {params['partitionedJsonData']}"}])

        print(
            f"Translated Part {params['index']} to {self.translateTo[params['langIndex']]}")
        return response.choices[0].message

    # Read input jsonFile
    def readFile(self):
        with open(self.inputPath, 'r') as f:
            jsonData = json.load(f)

        partitionedJsonDataList = []
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
                partitionedJsonDataList.append(partitionedJsonData)
                partitionedJsonData = {key: jsonData[key]}
                size = sys.getsizeof(jsonData[key])

        if partitionedJsonData:
            partitionedJsonDataList.append(partitionedJsonData)

        return partitionedJsonDataList

    # Write translated json to destination
    def writeFile(self, params):
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath)

        destination = f'{self.outputPath}/{self.translateTo[params["langIndex"]]}.json'

        try:
            jsonObjDict = {}
            jsonObjList = [json.loads(translatedJson["content"])
                           for translatedJson in params["response"]]

            for jsonStr in jsonObjList:
                jsonObjDict.update(jsonStr)

            with open(destination, 'w') as f:
                json.dump(jsonObjDict, f, indent=2, ensure_ascii=False)

            print(
                f"Translation of JSON file in {self.translateTo[params['langIndex']]} created!")
        except Exception as e:
            print(e)
            print(
                f"Failed to translate to {self.translateTo[params['langIndex']]}")

    # entrypoint
    def start(self):
        jsonData = self.readFile()

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.maxJsonFileWorker) as executor:
            future_results = [executor.submit(
                self.translateAndWriteFiles, {"langIndex": index, "jsonData": jsonData}) for index in range(len(self.translateTo))]

            [future.result()
             for future in concurrent.futures.as_completed(future_results)]

            print("Tasks Completed")

    # start translating json to different language
    def translateAndWriteFiles(self, params):
        response = self.translatePartitionedJsonData(params)
        self.writeFile(
            {"response": response, "langIndex": params["langIndex"]})

        return


if __name__ == "__main__":
    # check readme to see how to set up your config
    translator = Translator({
        "apiKey": "{YOUR_API_KEY}",
        "roles": "user",
        "model": "gpt-3.5-turbo",
        "maxChunkSize": 2048,
        # Only change the number of workers when you know what you are doing
        "maxGptWoker": 4,
        "maxJsonFileWorker": 2,
        "inputPath": "{YOU_INPUT_FILE_PATH}",
        "outputPath": "{YOU_OUTPUT_FILE_PATH}",
        "translateTo": []
    })

    translator.start()
