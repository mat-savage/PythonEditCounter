import arcpy
import pythonaddins
import re

def UpdateLayerText(lyr):
    arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")
    valueDict = {}
    symbology = lyr.symbology
    valueList = [str(row[0]) for row in arcpy.da.SearchCursor(lyr,symbology.valueField)]
    for value in symbology.classValues:
        if value != "<Null>":
            valueDict[value] = valueList.count(value)
        else:
            valueDict[value] = valueList.count('None')
    newLabels = []
    for i,v in enumerate(symbology.classValues):
        curLabel = re.sub(r'\([^)]*\)', '', symbology.classLabels[i]).strip()
        classLabel = curLabel + " ({0} | {1}".format(valueDict[v],int(100*valueDict[v]/len(valueList))) + "%)"
        newLabels.append(classLabel)
    lyr.symbology.classLabels = newLabels
    arcpy.RefreshTOC()

def GetCurrentLayer(geometryObj,oidList,layerList):
    layer = None
    for layer in layerList:
        if layer.isFeatureLayer:
            oidField = arcpy.Describe(layer).OIDFieldName
            query = "{0} in {1}".format(oidField,str(oidList).replace('[','(').replace(']',')'))
            with arcpy.da.SearchCursor(layer,[oidField,"SHAPE@"],where_clause=query) as rows:
                for row in rows:
                    geom = row[1]
                    if geom.JSON == geometryObj.JSON:
                        return layer

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
        if lyr is not None:
            if lyr.symbologyType == 'UNIQUE_VALUES':
                UpdateLayerText(lyr)
        else:
            #print self.editWorkspace
            curFeat = self.currentFeature
            curSel = self.editSelection
            mxd = arcpy.mapping.MapDocument("CURRENT")
            layers = arcpy.mapping.ListLayers(mxd)
            #print curFeat,curSel
            lyr = GetCurrentLayer(curFeat,curSel,layers)
            if lyr is not None:
                #print "Layer Found"
                if lyr.symbologyType == 'UNIQUE_VALUES':
                    UpdateLayerText(lyr)
            #else:
            #    print "Layer not found"

            
