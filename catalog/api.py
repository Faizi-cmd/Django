from ninja import NinjaAPI, Schema, Query
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
from catalog.models import Course

api = NinjaAPI(title="Course API", version="1.0.0")

# ========== SCHEMAS ==========
class CourseIn(Schema):
    code: str
    title: str
    description: str = ""
    is_active: bool = True

class CoursePatch(Schema):
    code: str | None = None
    title: str | None = None
    description: str | None = None
    is_active: bool | None = None

class CourseOut(Schema):
    id: int
    code: str
    title: str
    description: str
    is_active: bool

# ========== ENDPOINTS ==========

# GET /api/courses/?search=...&active=...
@api.get("/courses/", response=list[CourseOut])
@paginate
def list_courses(request, search: str = "", active: bool = None):
    qs = Course.objects.all()
    if search:
        qs = qs.filter(title__icontains=search)
    if active is not None:
        qs = qs.filter(is_active=active)
    return qs

# POST /api/courses/
@api.post("/courses/", response={201: CourseOut, 400: dict, 422: dict})
def create_course(request, payload: CourseIn):
    try:
        course = Course.objects.create(**payload.dict())
        return 201, course
    except Exception as e:
        return 400, {"detail": str(e)}

# GET /api/courses/{id}
@api.get("/courses/{id}", response={200: CourseOut, 404: dict})
def get_course(request, id: int):
    course = get_object_or_404(Course, id=id)
    return 200, course

# PATCH /api/courses/{id}
@api.patch("/courses/{id}", response={200: CourseOut, 404: dict, 422: dict})
def patch_course(request, id: int, payload: CoursePatch):
    course = get_object_or_404(Course, id=id)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(course, attr, value)
    try:
        course.save()
        return 200, course
    except Exception as e:
        return 400, {"detail": str(e)}

# DELETE /api/courses/{id}
@api.delete("/courses/{id}", response={204: None, 404: dict})
def delete_course(request, id: int):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return 204, None