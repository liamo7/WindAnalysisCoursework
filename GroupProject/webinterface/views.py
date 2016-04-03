from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, views
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from .models import Project, Turbine, Analysis, Column
from .serializer import ProjectSerializer, TurbineSerializer, AnalysisSerializer, ColumnSerializer
from windAnalysis.dummy_analysis import dummy
from windAnalysis.ppaTypes import *
import jsonpickle
from GroupProject.settings import MEDIA_ROOT, MEDIA_URL

def index(request):
    return render(request, 'base.html')


class TurbineViewSet(viewsets.ModelViewSet):
    lookup_field = 'name'
    queryset = Turbine.objects.all()
    serializer_class = TurbineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        print(serializer)

        if serializer.is_valid():
            print(serializer.validated_data)
            turbine = Turbine.objects.create(**serializer.validated_data)
            turbine.addOneMetreHorizontalStripes()
            return Response()

        print(serializer.errors)
        return Response()


class ProjectViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    #parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        print(request.data)
        print(serializer)

        print(request.FILES)

        turbine = Turbine.objects.get(name=request.data['turbine']['name'])

        if turbine:
            if serializer.is_valid():
                print(serializer.validated_data)
                project = Project.objects.create(turbine=turbine, **serializer.validated_data)

                windFile  = project.addDatafile('mast.txt', project.directory + '\\media/' + project.title + '\\rawDataFiles/', FileType.METEO, columnSeparator='\t')
                powerFile = project.addDatafile('power.txt', project.directory + '\\media/' + project.title + '\\rawDataFiles/', FileType.POWER, columnSeparator='\t')
                lidarFile = project.addDatafile('lidar.txt', project.directory + '\\media/' + project.title + '\\rawDataFiles/', FileType.LIDAR, columnSeparator='\t')

                print(windFile)

                list = [windFile.filename, powerFile.filename, lidarFile.filename]
                project.addDataFileNames(list)

                project.windDataFile = jsonpickle.encode(windFile)
                project.powerDataFile = jsonpickle.encode(powerFile)
                project.lidarDataFile = jsonpickle.encode(lidarFile)

                project.save()

                print("Project setup complete")
                return Response()

        print(serializer.errors)
        return Response()

    def update(self, request, *args, **kwargs):
        print("Update Occur")
        print(request.data)

        project = Project.objects.get(title=request.data['projectTitle'])

        if 'mastFile' in request.data:
            project.mastFile = request.data['mastFile']

        if 'lidarFile' in request.data:
            project.lidarFile = request.data['lidarFile']

        if 'powerFile' in request.data:
            project.powerFile = request.data['powerFile']

        project.save()

        return Response()


class AnalysisViewSet(viewsets.ModelViewSet):
    lookup_field = 'title'
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        print(serializer)

        project = Project.objects.get(title=request.data['project']['title'])

        if project:
            if serializer.is_valid():
                print(serializer.validated_data)
                Analysis.objects.create(project=project, **serializer.validated_data)

                windFile = jsonpickle.decode(project.windDataFile)
                powerFile = jsonpickle.decode(project.powerDataFile)
                lidarFile = jsonpickle.decode(project.lidarDataFile)

                fileList = [windFile, powerFile, lidarFile]
                dummy(project, fileList)
                return Response()

        print(serializer.errors)
        return Response()

    def list(self, request, title=None):
        analysis = Analysis.objects.get(title=title)
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)

    def retrieve(self, request, title=None):
        project = Project.objects.get(title=title)
        serializer = AnalysisSerializer(Analysis.objects.filter(project=project), many=True)
        return Response(serializer.data)


class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

class ColumnTypeViewSet(views.APIView):

    def get(self, request, *args, **kwargs):
        myList = []
        for colType in ColumnType:
            myList.append(colType.name)
        return Response(myList)

class ValueTypeViewSet(views.APIView):

    def get(self, request, *args, **kwargs):
        myList = []
        for valType in ValueType:
            myList.append(valType.name)
        return Response(myList)