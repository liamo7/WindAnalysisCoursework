__author__ = 'brian'

import matplotlib.pyplot as plt, mpld3
import windAnalysis.calculation as calculation
import windAnalysis.plotting as plotting
from windAnalysis.ppaTypes import *
from .models import JsonDataFile, Analysis
import json
from .utils import PythonObjectEncoder, as_python_object
from GroupProject.settings import MEDIA_ROOT, STATIC_DIR
import os

def processAnalysis(project, files, calc, analysis):


    derivedFile = files[-1]
    # For an analysis, a file will be selected on which to perform the analysis on
    # this could be combined file, raw data files ?
    #

    #-------Processing stage analysis---------------------#
    siteCalibrationFactors = {190: {'slope': 1.0152, 'offset': 0},
                              200: {'slope': 1.0135, 'offset': 0},
                              210: {'slope': 0.9957, 'offset': 0},
                              220: {'slope': 1.0094, 'offset': 0},
                              230: {'slope': 1.0211, 'offset': 0},
                              240: {'slope': 1.0063, 'offset': 0}}

    derivedFile.applyInstrumentCalibrations(removeOriginalCalibration=True)


    for count, row in enumerate(calc):
        kwargDict = {}
        count += 1
        index = str(count)
        for key, value in calc['row' + index]['kwargs'].items():
            if key == 'powerCurve':
                kwargDict['powerCurve'] = eval('project.turbine.' + calc['row' + index]['kwargs']['powerCurve'] + '()')

            if key == 'factors':
                kwargDict['factors'] = siteCalibrationFactors

        if 'powerCurve' in calc['row' + index]['kwargs']:
            del calc['row' + index]['kwargs']['powerCurve']

        if 'factors' in calc['row' + index]['kwargs']:
            del calc['row' + index]['kwargs']['factors']


        kwargs = {**calc['row'+index]['kwargs'], **kwargDict}
        derivedFile.addDerivedColumn(newColumn=calc['row' + index]['calcType'], functionToApply=eval('calculation.' + calc['row' + index]['calcType']), columnArguments=calc['row' + index]['cols'], columnType=ColumnType(calc['row' + index]['colType'] + 1), kwargs=kwargs, project=project)

    derivedFile.selectData()
    derivedFile.saveAs('derived.txt', project.getDerivedFilePath() + '/' + analysis.title + '/')

    jsonDataFile, created = JsonDataFile.objects.get_or_create(name='derived', analysisID=analysis.id)
    jsonDataFile.jsonData = json.dumps(derivedFile, cls=PythonObjectEncoder)
    jsonDataFile.save()
    analysis.derivedDataFile = jsonDataFile
    analysis.save()


def postAnalysis(project, currentAnalysis, plotTypes):

    analysis = Analysis.objects.get(title='Analysis2')

    dataFileObj = JsonDataFile.objects.get(name='derived', analysisID=analysis.id)
    data = json.loads(dataFileObj.jsonData, object_hook=as_python_object)

    # # -------PostProcessing stage analysis---------------------#
    # measuredPowerCurve = project.makeMeasuredPowerCurve(data.data, 'normalisedWindSpeed', 'Power mean (kW)', 'bin')
    # measuredPowerCurve.calculatePowerCoefficients(project.turbine.radius())
    #
    # meanWindSpeed = 7.5
    #
    # measuredPowerCurve.aepAdded(meanWindSpeed)
    # measuredPowerCurve.statistics()
    # print(measuredPowerCurve.aepMeasured(meanWindSpeed))
    # print(measuredPowerCurve.aepExtrapolated(meanWindSpeed))

    plotData = {}

    for sType in plotTypes:

        if 'PowerCurve' in plotTypes[sType]['plotType']:
            createPowerCurve(data, plotTypes[sType]['cols'], currentAnalysis)
        if 'Distribution' in plotTypes[sType]['plotType']:
            plotData['Distribution'] = {}
            plotData['Distribution'] = createDistribution(data, plotTypes[sType]['cols'], currentAnalysis)
        if 'Correlation' in plotTypes[sType]['plotType']:
            createCorrelation(data, plotTypes[sType]['cols'], currentAnalysis)
        if 'FFT' in plotTypes[sType]['plotType']:
            createFFT(data, plotTypes[sType]['cols'], currentAnalysis)

    return json.dumps(plotData)


def createDirForPlot(currentAnalysis):
    if not os.path.exists(STATIC_DIR + '/plots/' + currentAnalysis.title + '/'):
        os.makedirs(STATIC_DIR + '/plots/' + currentAnalysis.title + '/')


def createPowerCurve(data, cols, currentAnalysis):
    plt.switch_backend('agg')
    fg, ax = plt.subplots()
    plt.title('Power curve scatter')
    plotting.powerCurve(data.data, cols[0], cols[1], ax)
    createDirForPlot(currentAnalysis)
    plt.savefig(STATIC_DIR + '/plots/' + currentAnalysis.title +'/powerCurve.png')

def createCorrelation(data, cols, currentAnalysis):
    plt.switch_backend('agg')
    fg, ax = plt.subplots()
    plt.title('Correlation')
    plotting.correlation(data.data, cols[0], cols[1], ax)
    createDirForPlot(currentAnalysis)
    plt.savefig(STATIC_DIR + '/plots/' + currentAnalysis.title +'/correlation.png')


def createDistribution(data, cols, currentAnalysis):
    plt.switch_backend('agg')
    fg, ax = plt.subplots()
    plt.title('Distribution')
    plotting.distribution(data.data, cols[0])
    createDirForPlot(currentAnalysis)
    plt.savefig(STATIC_DIR + '/plots/' + currentAnalysis.title +'/distribution.png')
    return convertDescibeData(data.data[cols[0]].describe())



def createFFT(data, cols, currentAnalysis):
    plt.switch_backend('agg')
    fg, ax = plt.subplots()
    plt.title('FFT')
    plotting.fft(data.data, cols[0], ax)
    createDirForPlot(currentAnalysis)
    plt.savefig(STATIC_DIR + '/plots/' + currentAnalysis.title +'/fft.png')


def createPlotObj(name, analysisID=None, projectID=None, data=None):
    jsonData, created = JsonDataFile.objects.get_or_create(name=name, analysisID=analysisID, projectID=projectID)
    jsonData.jsonData = json.dumps(data, cls=PythonObjectEncoder)
    jsonData.save()


def convertDescibeData(data):
    #An array is brought in

    keyList = ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']

    dataDict = dict(zip(keyList, data))
    return dataDict

