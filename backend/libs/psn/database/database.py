from datetime import datetime
import copy

def getCurrentTime():
    now = datetime.now()
    nowStr = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return nowStr

class Database:
    def __init__(self, name, model, indexField: str = None, indexUnique: bool = True):
        self._name = name # Name of the database, unchangeable
        self._model = model # Model of the entries of the database
        self._entries = [] # Entries on this database

        self._internalIndexMap = {} # Index to Internal Index map
        self._indexField = indexField # Model field used as index
        self._indexUnique = indexUnique # Keep index unique

        # Flags if this database was changed
        self.changed = False  

    # --------------------------------------------------------------
    # Index managers
    # --------------------------------------------------------------  
    def _addToIndex(self, entryData):
        internalIndex = entryData.get("iid")
        index = entryData.get(self._indexField)

        if internalIndex == None or index == None:
            return False                
        
        if self._indexUnique == True:
            self._internalIndexMap[index] = internalIndex
        else:
            indexes = self._internalIndexMap.get(index)
            if indexes == None:
                indexes = []
                self._internalIndexMap[index] = indexes
            indexes.append(internalIndex)

        return True
    
    def _removeFromIndex(self, entryData):
        internalIndex = entryData.get("iid")
        index = entryData.get(self._indexField)


        if internalIndex == None or index == None:
            return False   
        
        if self._indexUnique == True:
            del self._internalIndexMap[index]
        else:
            indexes = self._internalIndexMap.get(index)            
            if len(indexes) <= 1:
                del self._internalIndexMap[index]
            else:
                indexes.remove(internalIndex)

        return True

    # --------------------------------------------------------------
    # Entry Getters
    # --------------------------------------------------------------    

    def getByInternalIndex(self, internalIndex: int):
        if internalIndex >= len(self._entries):
            return {
                "status": "error",
                "errorType": "index out of bounds",
                "errorInfo": internalIndex,
            }
        
        entry = self._entries[internalIndex]

        if entry == None:
            return {
                "status": "error",
                "errorType": "entry deleted",
                "errorInfo": internalIndex,
            }
        else:
            return {
                "status": "ok",
                "entryData": copy.deepcopy(entry["data"]),
            }
    
    def getAll(self, safe = True):
        entries = []
        for entry in self._entries:
            if entry != None:
                if safe == True:
                    entries.append(copy.deepcopy(entry["data"]))
                else:
                    entries.append(entry["data"])
        return entries

    def get(self, index: str):
        internalIndex = self._internalIndexMap.get(index)
        if internalIndex == None:
            return {
                "status": "error",
                "errorType": "index not found",
                "errorInfo": index,
            }
        
        if self._indexUnique == False:
            entries = []
            for iid in internalIndex:
                entry = self.getByInternalIndex(iid)
                if entry != None:
                    entries.append(entry["entryData"])
            return {
                "status": "ok",
                "entryData": entries,
            }
        
        else:
            entry = self.getByInternalIndex(internalIndex)            
            return {
                "status": "ok",
                "entryData": entry["entryData"],
            }

    # --------------------------------------------------------------
    # Entry Adders
    # --------------------------------------------------------------    

    # Gets a new free internal index
    def _getNewInternalIndex(self):
        return len(self._entries)
    
    # Add an entry without considering indexing
    def _add(self, entryData: dict):
        self.changed = True
        currTime = getCurrentTime()
        entry = {
            "data": entryData,
            "metaData": {
                "createdOn": currTime,
                "updatedOn": currTime,                
            }
        }
        internalIndex = self._getNewInternalIndex()
        entryData["iid"] = internalIndex        
        self._entries.append(entry)
        return internalIndex
        
    # Adds an entry and updates indexing
    def add(self, entryData: dict):
        # Checks if index is needed            
        if self._indexField == None:
            # No indexing, simple ADD
            self._add(entryData)
            return {
                    "status": "ok",
                    "entryData": entryData,
                }
        
        else:
            index = entryData.get(self._indexField)
            # Checks if index exists
            if index == None:
                return {
                    "status": "error",
                    "errorType": "index field not found",
                    "errorInfo": self._indexField,
                }
            
            # Gets current index
            currIndex = self._internalIndexMap.get(index)

            # Checks index collision
            if self._indexUnique == True:                
                if currIndex == None:
                    # ADD
                    self._add(entryData)
                    self._addToIndex(entryData)

                    return {
                            "status": "ok",
                            "entryData": entryData,
                        }

                else:
                    return {
                        "status": "error",
                        "errorType": "index already used",
                        "errorInfo": "",
                    }
                
            else:
                # ADD
                self._add(entryData)
                self._addToIndex(entryData)

                return {
                        "status": "ok",
                        "entryData": entryData,
                    }

    # --------------------------------------------------------------
    # Entry Setters
    # --------------------------------------------------------------    
    def _set(self, entryData: dict, internalIndex: int):
        self.changed = True
        currEntryData = self.getByInternalIndex(internalIndex)
        if currEntryData["status"] != "ok":
            return currEntryData
    
        currEntry = self._entries[internalIndex]
        currEntry["data"] = entryData
        currEntry["metaData"]["updatedOn"] = getCurrentTime()

    def set(self, entryData: dict):
        internalIndex = entryData.get("iid")        
        if internalIndex == None:
            return {
                "status": "error",
                "errorType": "Missing internal index",
                "errorInfo": "",
            }
        
        # Check for index renames
        if self._indexField != None:
            currEntryData = self.getByInternalIndex(internalIndex)["entryData"]
            currIndex = currEntryData.get(self._indexField)
            newIndex =  entryData.get(self._indexField)
            if newIndex != currIndex:
                # INDEX FIELD CHANGED, UPDATE INDEX MAP
                otherEntry = self._internalIndexMap.get(newIndex)
                if self._indexUnique == True:                    
                    if otherEntry != None:
                        return {
                            "status": "error",
                            "errorType": "Index colision",
                            "errorInfo": "Index field value changed, but new index collides with an existing one",
                        }

                self._removeFromIndex(currEntryData)
                self._addToIndex(entryData)
        
        # Set data     
        self._set(entryData, entryData["iid"])

        return {
                "status": "ok",
                "entryData": entryData,
            }
    
    # --------------------------------------------------------------
    # Entry Deleters
    # --------------------------------------------------------------        
    def delete(self, entryData):
        # Retrieves internal index
        internalIndex = entryData.get("iid")        
        if internalIndex == None:
            return {
                "status": "error",
                "errorType": "Missing internal index",
                "errorInfo": "",
            }
        
        # Check if entry exists
        currEntryData = self.getByInternalIndex(internalIndex)
        if currEntryData["status"] != "ok":
            return currEntryData
        
        # Delete it from indexes
        self.changed = True
        if self._indexField != None:
            self._removeFromIndex(currEntryData)

        # Delete it from entries
        self._entries[internalIndex] = None



