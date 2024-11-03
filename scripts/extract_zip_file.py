"""
/***************************************************************************
                              Extract Zip file
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
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFolderDestination)
import zipfile

class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    ZIP_FILE = 'ZIP_FILE'
    OUTPUT_DIRECTORY = 'OUTPUT_DIRECTORY'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExampleProcessingAlgorithm()

    def name(self):
        return 'myscript'

    def displayName(self):
        return self.tr('Extract ZIP')

    def group(self):
        return self.tr('Vector general')

    def groupId(self):
        return 'examplescripts'

    def shortHelpString(self):
        return self.tr("Algorithm that extracts a ZIP file to a specified folder")

    def initAlgorithm(self, config=None):
        # Paramètre pour sélectionner le fichier ZIP
        self.addParameter(
            QgsProcessingParameterFile(
                self.ZIP_FILE,
                self.tr('ZIP file to decompress'),
                extension='zip'
            )
        )

        # Paramètre pour définir le dossier de sortie
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT_DIRECTORY,
                self.tr('Output directory for decompression')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Obtenir le fichier ZIP et le dossier de sortie
        zip_file_path = self.parameterAsFile(parameters, self.ZIP_FILE, context)
        output_directory = self.parameterAsString(parameters, self.OUTPUT_DIRECTORY, context)
        
        # Extraction du fichier ZIP
        self.extract_zip(zip_file_path, output_directory, feedback)
        
        feedback.pushInfo(f"Extraction terminée dans le dossier : {output_directory}")
        
        return {self.OUTPUT_DIRECTORY: output_directory}

    def extract_zip(self, zip_file_path, output_directory, feedback):
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(output_directory)
            feedback.pushInfo(f"Fichiers extraits dans : {output_directory}")
        except zipfile.BadZipFile:
            feedback.reportError("Le fichier ZIP est corrompu ou invalide.")
