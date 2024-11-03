"""
/***************************************************************************
                              Copy vector Layer
                             --------------------
        begin           : 2024-11-03
        copyright       : (C) 2024 by Ghassen Aouinti
        email           : ghassen.aouinti@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License v3.0 as          *
 *   published by the Free Software Foundation.                            *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFeatureSink,
                       QgsFeatureSink)

class CopyVectorLayer(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def createInstance(self):
        return CopyVectorLayer()

    def name(self):
        return 'copy_vector_layer'

    def displayName(self):
        return QCoreApplication.translate("CopyVectorLayer", "Copy vector layer")

    def group(self):
        return QCoreApplication.translate("CopyVectorLayer", "Vector general")

    def groupId(self):
        return 'vectorgeneral'

    def shortHelpString(self):
        return QCoreApplication.translate("CopyVectorLayer", "Creates a full copy of a vector layer")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                QCoreApplication.translate("CopyVectorLayer", "Input layer"),
                [QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                QCoreApplication.translate("CopyVectorLayer", "Copy of the vector layer")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsVectorLayer(
            parameters,
            self.INPUT,
            context
        )
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            source.fields(),
            source.wkbType(),
            source.sourceCrs())

        features = [f for f in source.getFeatures()]
        sink.addFeatures(features, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: dest_id}