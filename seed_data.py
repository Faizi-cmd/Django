import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Course, Lesson


def seed():
    # Hapus data lama (opsional)
    Lesson.objects.all().delete()
    Course.objects.all().delete()

    courses = []
    for i in range(1, 21):
        course = Course.objects.create(
            code=f"CRS{i:03d}",
            title=f"Course Title {i}",
            description=f"Description for course {i}",
            is_active=True if i % 3 != 0 else False,  # sebagian non-aktif
        )
        courses.append(course)

    for course in courses:
        for j in range(1, 6):  # 5 lesson per course = 100 lesson total
            Lesson.objects.create(
                course=course,
                title=f"{course.title} - Lesson {j}",
                content=f"Content for lesson {j} of {course.title}",
                order=j,
            )

    print(f"Created {Course.objects.count()} courses")
    print(f"Created {Lesson.objects.count()} lessons")


if __name__ == "__main__":
    seed()