from django.db import models

class Folder(models.Model):
	"""Модель папок"""
	id = models.CharField(primary_key=True, max_length=255)
	# url = models.CharField(max_length=255, blank=False)
	date = models.DateTimeField()
	parentId = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	#size = models.IntegerField()


class File(models.Model):
	"""Модель папок"""
	id = models.CharField(primary_key=True, max_length=255)
	url = models.CharField(blank=False, max_length=255)
	date = models.DateTimeField()
	parentId = models.ForeignKey('Folder', on_delete=models.CASCADE, blank=True, null=True)
	size = models.PositiveIntegerField() 