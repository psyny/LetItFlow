import os
import json
import pickle

class FileManager:
    # --------------------------------------------------------------
    # Internal Tools
    # --------------------------------------------------------------   

    def _getBasePath(subPaths: list = [], fileName: str = None):
        if fileName:
            return os.path.join(".", *subPaths, fileName)  
        else:
            return os.path.join(".", *subPaths)  

    # --------------------------------------------------------------
    # Files
    # --------------------------------------------------------------    
    def getFiles(parentPaths: list = [], extension: str = None):
        path = FileManager._getBasePath(parentPaths)   

        subFiles = list()
        for entry in os.scandir(path):
            if entry.is_file():
                if extension != None and extension != FileManager.getFileExtension(entry.name):
                    continue
                subFiles.append(entry.name)

        return subFiles
    
    def getFileExtension(fileName: str):
        fileParts = fileName.split(".")
        return fileParts[-1]
    
    def getFileParts(fileName: str):
        fileParts = fileName.split(".")
        return ".".join(fileParts[0:-1]) , fileParts[-1]
    
    def fileExists(fileName: str, folder: list):
        path = FileManager._getBasePath(folder, fileName) 
        return os.path.exists(path)           

    # --------------------------------------------------------------
    # Folders
    # --------------------------------------------------------------    
    def getFolders(parentPaths: list = []):
        path = FileManager._getBasePath(parentPaths)   

        subFolders = list()
        for entry in os.scandir(path):
            if entry.is_dir():
                subFolders.append(entry.name)

        return subFolders

    def createFolders(folderStructure: list):
        path = FileManager._getBasePath(folderStructure) 
        if not os.path.exists(path):
            os.makedirs(path)

    def folderExists(folderStructure: list):
        path = FileManager._getBasePath(folderStructure) 
        return os.path.exists(path)    

    # --------------------------------------------------------------
    # File Load/Save
    # --------------------------------------------------------------

    # Helpers
    def _getFilePathToWrite(fileName: str, parentFolders: list):
        path = FileManager._getBasePath(parentFolders) 
        if not os.path.exists(path):
            FileManager.createFolders(parentFolders)
        path = FileManager._getBasePath(parentFolders, fileName) 
        return path
    
    def _getFilePathToRead(fileName: str, parentFolders: list):
        path = FileManager._getBasePath(parentFolders, fileName) 
        if not os.path.exists(path):
            return None
        return path


    # Text File
    def saveTextFile(text: str, fileName: str, parentFolders: list = []):
        path = FileManager._getFilePathToWrite(fileName, parentFolders)
        file = open(path, "w")
        text = file.write(text)
        file.close()
        return True
    
    def loadTextFile(fileName: str, parentFolders: list = []):        
        path = FileManager._getFilePathToRead(fileName, parentFolders) 
        if not path:
            return None
        
        file = open(path, "r")
        text = file.read()
        file.close()
        return text
    

    # Json File
    def saveJsonFile(pyObject: object, fileName: str, parentFolders: list = []):
        path = FileManager._getFilePathToWrite(fileName, parentFolders)
        file = open(path, "w")
        json.dump(pyObject, file)
        file.close()
        return True    
    
    def loadJsonFile(fileName: str, parentFolders: list = []):
        path = FileManager._getFilePathToRead(fileName, parentFolders) 
        if not path:
            return None
        
        file = open(path, "r")
        pyObj = json.load(file)
        file.close()
        return pyObj     


    # Pickle
    def savePickleFile(pyObject: object, fileName: str, parentFolders: list = []):
        path = FileManager._getFilePathToWrite(fileName, parentFolders)
        file = open(path, "wb")
        pickle.dump(pyObject, file)
        file.close()
        return True    
    
    def loadPickleFile(fileName: str, parentFolders: list = []):
        path = FileManager._getFilePathToRead(fileName, parentFolders) 
        if not path:
            return None
                
        file = open(path, "rb")
        pyObj = pickle.load(file)
        file.close()
        return pyObj          
