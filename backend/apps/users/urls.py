from django.db.models import Subquery, OuterRef, Sum, Count, Avg

class Teacher(models.Model):
    name = models.CharField(max_length=100)

class Subject(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    score = models.IntegerField()
    is_passed = models.BooleanField(default=False)


exam_subquery = Exam.objects.filter(
  subject__teacher=OuterRef('pk'),
).values('subject__teacher').annotate(avg=Avg('score')).values('avg')

teachers = Teacher.objects.annotate(
  avg_score=Subquery(exam_subquery)
)
