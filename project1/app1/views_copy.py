import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse
from . import models
from django.db.models import class_room
from django.db.models import department
from django.db.models import user_profile
from django.db.models import course
from django.db.models import session
from django.db.models import course_enrolled
from django.db.models import attendance


from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        try:
            cred = models.credential.objects.get(pk = received_json_data['login_id'])
            if cred.password == received_json_data['password']:
                # calling respective view function ... 
                if cred.role == 'student':
                    #return HttpResponse("login successful !")
                    return JsonResponse(student_view(received_json_data['login_id']))
                if cred.role == 'faculty':
                    return JsonResponse(faculty_view(received_json_data['login_id']))
                else:
                    return HttpResponse('admin view is been called')
            else:
                return HttpResponse('<h3>Login not successful ! Enter valid cred </h3>')
        except models.credential.DoesNotExist:
            return HttpResponse('<h3>Not a registered user</h3>')
    
        
@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        print ("received data = ", received_json_data)
        if models.credential.objects.filter(pk = received_json_data['login_id']).exists():
            return HttpResponse("user already exists")
        else:
            try:
                models.credential.objects.create(login_user_id = received_json_data['login_id'], password = received_json_data['password'], role = received_json_data['role'], permission_id_id = received_json_data['permission_id'])
                #models.credential.objects.add(new_user)
                return HttpResponse("sign-up successful")
            except Exception as e:
                return HttpResponse("sign-up not successful")

    return HttpResponse('GET is not accpeted')

# internal function for student view 
def student_view(email):
    student = models.student.objects.get(email_id = email)
    print (student)
    view_json = {}
    # view_json = {1: {course_string(course tbl): "", session_name(session): "", course_name(course): "", term(course_en): "", year(course_en): ****}}
    s_name = student.student_name
    view_json.update({"s_name": s_name})
    s_id = student.student_id
    s_course_enrolled = models.course_enrolled.objects.filter(student_id = s_id)
    index = 1
    for _i in s_course_enrolled:
        c_id = _i.course_id_id
        print ("^^^^^^^ = ", c_id)
        c_term = _i.term
        print ("^^^^^^^ = ", c_term)
        c_year = _i.year
        s_id = _i.session_id_id
        c_obj = models.course.objects.get(course_id = c_id)
        c_name = c_obj.course_name
        c_string = c_obj.course_string
        s_obj = models.session.objects.get(session_id = s_id)
        s_name = s_obj.session_name
        obj = {"c_string": c_string,"s_name": s_name , "c_name": c_name, "c_term": c_term, "c_year": c_year}
        print ("josn obj = ", obj)
        view_json.update({index: obj})
        index += 1

    return view_json

# internal function for faculty view
def faculty_view(email):
    # view_json = {1: {course_string(course tbl): "", session_name(session): "", course_name(course): "", term(course_en): "", year(course_en): ****}}
    faculty = models.faculty.objects.get(email_id = email)
    print (faculty)
    view_json = {}
    index = 1
    f_name = faculty.faculty_name
    view_json.update({"f_name": f_name})
    f_id = faculty.faculty_id
    s_obj = models.session.objects.filter(faculty_id = f_id)
    for _i in s_obj:
        s_id = _i.session_id
        s_name = _i.session_name
        c_id = _i.course_id_id
        c_obj = models.course.objects.get(pk = c_id)
        c_name = c_obj.course_name
        c_string = c_obj.course_string
        ce_obj = models.course_enrolled.objects.get(course_id = c_id, session_id = s_id)
        f_term = ce_obj.term
        f_year = ce_obj.year
        obj = {'c_string': c_string, 's_name': s_name, 'c_name': c_name, 'c_term': f_term, 'c_year': f_year}
        print ("josn obj = ", obj)
        view_json.update({index : obj})
        index += 1

    return view_json

@csrf_exempt
def profile(request, role, id):
    return_josn = {}
    if role == 'student':
        obj = models.student.objects.get(pk = int(id))
        d_name = models.department.objects.get(pk = obj.dept_id_id).dept_name
        return_josn = {"name": obj.student_name, "email": obj.email_id, 'dept_name': d_name, 'phone_no': obj.phone_no, 'address': obj.address}
    if role == 'faculty':
        obj = models.faculty.objects.get(pk = int(id))
        d_name = models.department.objects.get(pk = obj.dept_id_id).dept_name
        return_josn = {"name": obj.faculty_name, "email": obj.email_id, 'dept_name': d_name, 'phone_no': obj.phone_no, 'address': obj.address}
    return JsonResponse(return_josn)