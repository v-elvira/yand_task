from datetime import datetime
from django.shortcuts import render
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view
from open_api.models import Folder, File
from .serializers import FolderSerializer, FileSerializer
from rest_framework.exceptions import ParseError, MethodNotAllowed, ValidationError



@api_view(['GET'])
def test(request):
	first_rest = {"Hello": "world", "number": 42}
	return(Response(first_rest))

@api_view(['GET'])
def get_all(request):
	folders = Folder.objects.all()
	folder_serializer = FolderSerializer(folders, many=True)
	# files = Files.objects.all()
	# file_serializer = FileSerializer(files, many=True)
	# return(Response(file_serializer.data))
	return(Response(folder_serializer.data))

@api_view(['GET'])
def all_files(request):
	files = File.objects.all()
	file_serializer = FileSerializer(files, many=True)
	return(Response(file_serializer.data))


@api_view(['GET'])
def nodes(request, id):
	element = find_element_by_id(id)
	if element is None:
		return Response({"code": 404, "message": "Item not found"}, status=404)
	# print(element)
	# print(type(element))
	# print(element["children"])
	if isinstance(element, File):
		file_res = FileSerializer(element).data
		# file_res.update({"type": "FILE", "children": None})
		return(Response(file_res))	

	# element is Folder
	# folder_res = FolderSerializer(element).data
	# print("ROOT:", folder_res)#, type(folder_serializer.data))
	# child_files = File.objects.filter(parentId=id)
	# sum_size = child_files.aggregate(Sum('size'))['size__sum']
	# print(sum_size)
	# # print(child_files)
	# child_info = FileSerializer(child_files, many=True).data
	# # print(FileSerializer(child_files, many=True).data)
	# folder_res.update({"size": sum_size, "children": child_info})
	# # with_children.update(folder_serializer.data)
	# # folder_serializer.data["children"] = "hello" #FileSerializer(child_files, many=True).data
	# # print(folder_serializer.data)


	folder_res = get_folder_size_and_info(element)[1] # (size, info)

	return(Response(folder_res))



@api_view(['POST'])
def imports(request):
	# print('here in POST')
	# print(request)
	# print(request.body)
	# body = json.loads(request.body)
	# print("BODY:", body)
	# print('data:', (body.get("updateDate")))

	try:
		date = request.data["updateDate"]

		for item in request.data["items"]:
			item["date"] = date
			update_mode = False
			if item["type"] == "FILE":
				try:
					old_file = File.objects.get(pk = item["id"])
					old_parent_id = None if old_file.parentId is None else old_file.parentId.pk
					serializer = FileSerializer(old_file, data=item)
					update_mode = True
				except:
					serializer = FileSerializer(data=item)
			elif item["type"] == "FOLDER":
				try:
					old_folder = Folder.objects.get(pk = item["id"])
					old_parent_id = None if old_folder.parentId is None else old_folder.parentId.pk
					serializer = FolderSerializer(old_folder, data=item)
					update_mode = True
				except:
					serializer = FolderSerializer(data=item)
			else:
				return Response({"code": 400, "message": "Validation Failed"}, status=400)


			if serializer.is_valid():
				if update_mode:
					serializer.save(force_update=True)
					change_parents_date(old_parent_id, date)
				else:
					serializer.save()

				change_parents_date(item["parentId"], date)

			else:
				return Response({"code": 400, "message": "Validation Failed"}, status=400)
	except Exception as e:
		print("WEIRD place", e)
		return Response({"code": 400, "message": "Validation Failed"}, status=400)
			
	return Response({}, status=200)


def change_parents_date(parent_id, date):
	# print(parent_id, date)
	if parent_id is None:
		return
	parent = Folder.objects.get(pk=parent_id)
	parent.date = date
	parent.save()
	if parent.parentId is not None:
		change_parents_date(parent.parentId.pk, date)



def get_folder_size_and_info(folder):
	sum_size = 0
	folder_res = FolderSerializer(folder).data

	child_files = File.objects.filter(parentId=folder.id)
	if child_files:
		sum_size += child_files.aggregate(Sum('size'))['size__sum']
	child_info = FileSerializer(child_files, many=True).data

	child_folders = Folder.objects.filter(parentId=folder.id)
	child_folders_info = []
	sum_fold_size = 0
	for child_fold in child_folders:
		sub_size, sub_info = get_folder_size_and_info(child_fold)
		sum_fold_size += sub_size
		child_folders_info.extend([sub_info])
	sum_size += sum_fold_size
	# print("CHILD INFO: ", child_info, type(child_info))
	# print("CHILD FOLDERS INFO:", child_folders_info, type(child_folders_info))
	child_info.extend(child_folders_info)

	folder_res.update({"size": sum_size, "children": child_info})
	return (sum_size, folder_res)



def datetime_valid(dt_str):
	try:
		datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
	except:
		return False
	return True

def find_element_by_id(id):
	element = None
	try:
		element = File.objects.get(pk=id)
	except:
		try:
			element = Folder.objects.get(pk=id)
		except:
			pass
	return element


@api_view(['DELETE'])
def delete(request, id):
	# for i in request.query_params:
	# 	print(i, request.query_params[i])
	# print(request.query_params)

	if 'date' not in request.query_params:
		return Response({"code": 400, "message": "Validation Failed"}, status=400)

	if not datetime_valid(request.query_params['date']):
		return Response({"code": 400, "message": "Validation Failed"}, status=400)

	element = find_element_by_id(id)

	if element is None:
		return Response({"code": 404, "message": "Item not found"}, status=404)
		
	else:
		element.delete()
		return Response({}, status=200)


