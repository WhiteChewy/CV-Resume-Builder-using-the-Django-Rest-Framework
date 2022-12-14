from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_delete

# Create your models here.

class ResumeTemplate(models.Model):
    
    '''
    This is used as the template options for Resume model.
    HTML Template can be added directly.
    '''
    name = models.CharField(max_length=300)
    template_image = models.ImageField(upload_to='resume_samples/')
    html_file = models.FileField(upload_to='resume_templates/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):

        '''Deletes old file when making an update to file'''
        try:
            old = ResumeTemplate.objects.get(id=self.id)
            if old.html_file != self.html_file:
                old.html_file.delete(save=False)
            
            if old.template_image != self.template_image:
                old.template_image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)

@receiver(post_delete, sender=ResumeTemplate)
def file_delete(sender, instance, **kwargs):
    
    '''Post_delete signal for deleting `Resume Template` resource to prevent orphaned files'''
    instance.html_file.delete(save=False)
    instance.template_image.delete(save=False)


class Resume(models.Model):

    '''Resume model'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    job_title = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    professional_summary = models.TextField()
    resume_template = models.ForeignKey(
        ResumeTemplate,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.first_name


class EmploymentHistory(models.Model):

    '''Employment History model'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='employment_histories')
    role = models.CharField(max_length=200)
    employer = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Employment Histories'
    
    def __str__(self):
        return self.role


class EducationHistory(models.Model):

    '''Education History model'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education_histories')
    school = models.CharField(max_length=400)
    degree = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Educational Histories'
    
    def __str__(self):
        return self.degree


class WebLink(models.Model):

    '''Web Link model (VK, Facebook, Twitter etc.'''    
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='links')
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return self.name


class Skill(models.Model):

    '''Skills technical and non-technical'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    is_soft_skill = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class Qualification(models.Model):

    '''Additional education, courses etc'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='qualifications')
    course = models.CharField(max_length=200, blank=False, null=False)
    institution = models.CharField(max_length=400)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)

    def __str__(self):
        return self.course


class Reference(models.Model):

    '''Reference model holds the resume owner refrees'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    reference_full_name = models.CharField(max_length=500)
    company = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self.reference_full_name
