from rest_framework import serializers
from open_api.models import Folder, File

class FolderSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField()
	type = serializers.SerializerMethodField()
	class Meta: 
		model = Folder
		fields = ['id', 'type', 'url', 'date', 'parentId']
		# fields = '__all__'
	

	def validate_id(self, value):
		try:
			File.objects.get(pk=value)
		except File.DoesNotExist:
			return value
		# print(f"Found file with the same as new folder id: {value}")
		raise serializers.ValidationError(f"Found file with the same as new folder id: {value}")


	def get_url(self, obj):
		return None

	def get_type(self, obj):
		return "FOLDER"



class FileSerializer(serializers.ModelSerializer):
	children = serializers.SerializerMethodField()
	type = serializers.SerializerMethodField()

	class Meta: 
		model = File
		fields = ['id', 'url', 'type', 'date', 'parentId', 'size', 'children']

	def validate_size(self, value):
		if value < 1:
			raise serializers.ValidationError("File size must be positive")
		return value

	def validate_id(self, value):
		try:
			Folder.objects.get(pk=value)
		except Folder.DoesNotExist:
			return value
		# print(f"Found folder with the same as new file id: {value}")
		raise serializers.ValidationError(f"Found folder with the same as new file id: {value}")

	def get_children(self, obj):
		return None

	def get_type(self, obj):
		return "FILE"

	# def update(self, instance, validated_data):
	# 	print(instance)
	# 	print('DAT:', validated_data)
	# 	instance['url'] = validated_data.get('url')
	# 	instance['date'] = validated_data.get('date')
	# 	instance['parentId'] = validated_data.get('parentId')
	# 	instance['size'] = validated_data.get('size')
	# 	return instance