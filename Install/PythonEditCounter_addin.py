import arcpy
import pythonaddins
import re

def UpdateLayerText(lyr):
    arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")
    valueDict = {}
    symbology = lyr.symbology
    valueList = [str(row[0]) for row in arcpy.da.SearchCursor(lyr,symbology.valueField)]
    for value in symbology.classValues:
        valueDict[value] = valueList.count(value)
    newLabels = []
    for i,v in enumerate(symbology.classValues):
        curLabel = re.sub(r'\([^)]*\)', '', symbology.classLabels[i]).strip()
        classLabel = curLabel + " ({0} | {1}".format(valueDict[v],int(100*valueDict[v]/len(valueList))) + "%)"
        newLabels.append(classLabel)
    lyr.symbology.classLabels = newLabels
    arcpy.RefreshTOC()

class PythonEditCounter(object):
    """Implementation for PythonEditCounter_addin.extension2 (Extension)"""
    
    def __init__(self):
        # For performance considerations, please remove all unused methods in this class.
        self.enabled = True

    def onCreateFeature(self):
        lyr = self.currentLayer
        if lyr.symbologyType == 'UNIQUE_VALUES':
            UpdateLayerText(lyr)
        
    def onDeleteFeature(self):
        lyr = self.currentLayer
        if lyr.symbologyType == 'UNIQUE_VALUES':
            UpdateLayerText(lyr)

    def onChangeFeature(self):
        lyr = self.currentLayer
        if lyr.symbologyType == 'UNIQUE_VALUES':
            UpdateLayerText(lyr)