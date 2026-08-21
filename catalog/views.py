from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, CourseWithLessonsSerializer


# ============================================
# ViewSet yang sudah ada (jangan dihapus)
# ============================================
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# ============================================
# VERSI A — TANPA OPTIMASI (N+1 Query Problem)
# ============================================
@api_view(['GET'])
def course_list_unoptimized(request):
    """
    Endpoint: GET /api/courses/unoptimized/
    Total query: 1 + N
    """
    connection.queries_log.clear()

    courses = Course.objects.filter(is_active=True)
    serializer = CourseWithLessonsSerializer(courses, many=True)

    query_count = len(connection.queries)

    return Response({
        'version': 'A (Unoptimized)',
        'query_count': query_count,
        'courses': serializer.data
    })


# ============================================
# VERSI B — DENGAN OPTIMASI (prefetch_related)
# ============================================
@api_view(['GET'])
def course_list_optimized(request):
    """
    Endpoint: GET /api/courses/optimized/
    Total query: 2
    """
    connection.queries_log.clear()

    courses = Course.objects.filter(is_active=True).prefetch_related('lessons')
    serializer = CourseWithLessonsSerializer(courses, many=True)

    query_count = len(connection.queries)

    return Response({
        'version': 'B (Optimized)',
        'query_count': query_count,
        'courses': serializer.data
    })