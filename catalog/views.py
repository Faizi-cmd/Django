from django.db import connection, reset_queries
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=['get'], url_path='unoptimized')
    def unoptimized(self, request):
        reset_queries()
        courses = Course.objects.all()
        data = []
        for c in courses:
            lessons = c.lessons.all()
            data.append({
                'course': c.title,
                'lessons': [l.title for l in lessons]
            })
        query_count = len(connection.queries)
        return Response({
            'version': 'A (Unoptimized)',
            'query_count': query_count,
            'data': data
        })

    @action(detail=False, methods=['get'], url_path='optimized')
    def optimized(self, request):
        reset_queries()
        courses = Course.objects.prefetch_related('lessons').all()
        data = []
        for c in courses:
            lessons = c.lessons.all()
            data.append({
                'course': c.title,
                'lessons': [l.title for l in lessons]
            })
        query_count = len(connection.queries)
        return Response({
            'version': 'B (Optimized)',
            'query_count': query_count,
            'data': data
        })


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('course').all()
    serializer_class = LessonSerializer