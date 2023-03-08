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

        self.maxGptWorkers = params["maxGptWorkers"]
        self.maxJsonFileWorkers = params["maxJsonFileWorkers"]

        self.debugMode = params["debugMode"]
        pass

    def updateFilePathAndLang(self, params):
        self.inputPath = params["inputPath"]
        self.outputPath = params["outputPath"]
        self.translateTo = params["translateTo"]

    def updateMaxWorkerNum(self, params):
        self.maxGptWorkers = params["maxGptWorkers"]
        self.maxJsonFileWorkers = params["maxJsonFileWorkers"]

    # Loop partitionedJson and send request to gpt endpoint
    def translatePartitionedJsonData(self, params):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxGptWorkers) as executor:
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
            messages=[{"role": self.role, "content": f"Please translate the below JSON into {self.translateTo[params['langIndex']]}, while keeping the key the same as the original JSON. The translation should be provided in valid JSON format using double quotes around keys and values. ```{params['partitionedJsonData']}```"}])

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
            if self.debugMode:
                for item in params["response"]:
                    print(item["content"])

    # entrypoint
    def start(self):
        jsonData = self.readFile()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.maxJsonFileWorkers) as executor:
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
        # The maximum size of the partitioned JSON in bytes in each chunk
        "maxChunkSize": 2048,
        # The maximum number of language translations that can be handled at the same time
        "maxJsonFileWorkers": 2,
        # The maximum number of translation requests that can be handled in each jsonFileWorker
        "maxGptWorkers": 3,
        "inputPath": "{YOU_INPUT_FILE_PATH}",
        "outputPath": "{YOU_OUTPUT_FILE_PATH}",
        "translateTo": [],
        "debugMode": True
    })

    translator.start()
