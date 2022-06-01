from django.db import models

class bookModel(models.Model):
    name = models.CharField(max_length=100, null=False)
    isbn = models.CharField(max_length=17, null=False)
    author = models.CharField(max_length=200, null=False)
    desc = models.TextField(blank=True, default='')
    publish = models.CharField(max_length=200, null=False)
    publishyear = models.CharField(max_length=200, null=False)
    theme = models.CharField(max_length=200, null=False)
    time = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default = False)
    borrower = models.CharField(max_length=200, blank=True, default='')
    burl = models.CharField(max_length=100, null=False)
    bhit = models.IntegerField(default=0)
    redate = models.CharField(max_length=100, blank=True, default='')
    connection = models.CharField(max_length=100, blank=True, default='') 
    readurl = models.CharField(max_length=100, blank=True, default='') 
    
    def __str__(self):
        return self.name
