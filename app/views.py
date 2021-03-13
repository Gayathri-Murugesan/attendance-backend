import json
import math
from json.decoder import JSONDecodeError, JSONDecoder
import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, exceptions, HTTP_HEADER_ENCODING
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.authentication import get_authorization_header
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# Create your views here.


@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@csrf_exempt
def login(request):
    if not request:
        return Response({'Error': "Please provide username/password"}, status="400")
    request = json.loads(request.body)
    username = request['username']
    password = request['password']
    print(username, password)
    try:
        user = User.objects.get(username=username)
        # check_password
    except User.DoesNotExist:
        print("111111111111111")
        return Response({'Error': "Invalid username/password"}, status="400")
    if user and user.password == password or user.check_password(password):

        payload = {
            'id': user.id,
            'email': user.email,
        }
        jwt_token = {"token": jwt.encode(payload, "SECRET_KEY")}
        print(jwt_token)
        print("222222222222")
        return Response(
            jwt_token,
            status=200,
            content_type="application/json"
        )
    else:
        print("3333333333333333")
        return HttpResponse(
            json.dumps({'Error': "Invalid credentials"}),
            status=400,
            content_type="application/json"
        )


@csrf_exempt
def authenticate(request):
    print("in authenticate function ....")
    auth = get_authorization_header(request).split()
    print("AUTH = ", auth)
    print(auth[0].lower())
    print(type(auth[0].lower()))
    msg = "invalid token format sent"
    if not auth or auth[0].lower() != b'token':
        raise exceptions.AuthenticationFailed(msg)
    if len(auth) == 1:
        msg = 'Invalid token header. No credentials provided.'
        print("MSG = ", msg)
        raise exceptions.AuthenticationFailed(msg)
    try:
        token = auth[1]
        if token == "null":
            msg = 'Null token not allowed'
            print("MSG = ", msg)
            raise exceptions.AuthenticationFailed(msg)
    except UnicodeError:
        msg = 'Invalid token header. Token string should not contain invalid characters.'
        print("MSG = ", msg)
        raise exceptions.AuthenticationFailed(msg)

    return authenticate_credentials(token)


def authenticate_credentials(token):
    print("in auth_cred function ... ")
    payload = jwt.decode(token, "SECRET_KEY", "HS256")
    email = payload['email']
    userid = payload['id']
    print("before try ... ")
    msg = {'Error': "Token mismatch", 'status': "401"}
    try:

        user = User.objects.get(
            email=email,
            id=userid,
            is_active=True
        )
        print("USER = ", user)
        data = {
            'id': user.id,
            'email': user.email,
        }
        print("DATA = ", data)
        if not jwt.encode(data, "SECRET_KEY", "HS256") == token:
            raise exceptions.AuthenticationFailed(msg)

    except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
        return HttpResponse({'Error': "Token is invalid"}, status="403")
    except User.DoesNotExist:
        return HttpResponse({'Error': "Internal server error"}, status="500")
    # return ("success")
    return JsonResponse(
        {'user_id': user.id, 'email': user.email},
        status=200,
        content_type="application/json"
    )


@csrf_exempt
def profile(request):
    token = get_authorization_header(request).split()[1]
    payload = jwt.decode(token, "SECRET_KEY", "HS256")
    email = payload['email']
    userid = payload['id']
    print("user id = ", userid)
    try:
        user_obj = User.objects.get(pk=int(userid))
        # .values('address', 'User__username')
        profile_obj = user_profile.objects.get(pk=userid)
        d_name = department.objects.get(pk=profile_obj.dept_id_id).dept_name
        print("user_obj = ", user_obj)
        print("profile_obj = ", profile_obj)
    except:
        return HttpResponse({'Error': "Data can't be fetched, Internal server error"}, status="500")
    return_josn = {"name": user_obj.first_name + user_obj.last_name, "email": user_obj.email,
                   "dept_name": d_name, "phone_no": profile_obj.phone_no, "address": profile_obj.address}
    print("return json = ", return_josn)
    return JsonResponse(return_josn, status=200, content_type="application/json", safe=False)


@csrf_exempt
def sessions(request):
    token = get_authorization_header(request).split()[1]
    payload = jwt.decode(token, "SECRET_KEY", "HS256")
    userid = payload['id']
    print("user id = ", userid)
    return_json = {}
    index = 1
    print("****** = ", User.objects.get(pk=userid).is_staff)
    if User.objects.get(pk=userid).is_staff is not True:
        course_enrolled_obj = course_enrolled.objects.filter(student_id=userid)
        for _i in course_enrolled_obj:
            course_obj = course.objects.get(pk=_i.course_id_id)
            session_obj = session.objects.get(pk=_i.session_id_id)
            obj = {"course_string": course_obj.course_string, "session_name": session_obj.session_name,
                   "course_name": course_obj.course_name, "term": _i.term, "year": _i.year}
            print("josn obj = ", obj)
            return_json.update({index: obj})
            index += 1

    else:
        session_obj = session.objects.filter(faculty_id=userid)
        for _i in session_obj:
            course_obj = course.objects.get(pk=_i.course_id_id)
            obj = {"course_string": course_obj.course_string, "session_name": _i.session_name,
                   "course_name": course_obj.course_name, "term": course_obj.term, "year": course_obj.year}
            print("josn obj = ", obj)
            return_json.update({index: obj})
            index += 1

        return JsonResponse(return_json, status=200, content_type="application/json", safe=False)


def get_attendance(request, session_id, course_id):
    print("session id = ", session_id)
    print("course id = ", course_id)
    token = get_authorization_header(request).split()[1]
    payload = jwt.decode(token, "SECRET_KEY", "HS256")
    userid = payload['id']
    print("user id = ", userid)
    return_json = {}
    return_json['attendance_data'] = []
    index = 0
    attended = 0
    attendance_obj = attendance.objects.filter(pk=userid)
    print("11111111")
    for _i in attendance_obj:
        if _i.attendance == True:
            attended += 1
        print("year = ", _i.date.year)
        print("month = ", _i.date.month)
        print("day = ", _i.date.day)
        year = _i.date.year
        month = _i.date.month
        day = _i.date.day
        obj = {"date": str(month)+"/"+str(day)+"/" +
               str(year), "attended": _i.attendance}
        print("obj = ", obj)
        return_json['attendance_data'].append(obj)
        index += 1
    print("22222222")
    return_json["all_sessions"] = index
    return_json["attended"] = attended
    return_json["percentage"] = str(math.ceil((attended/index))*100)+"%"

    return JsonResponse(return_json, status=200, content_type="application/json", safe=False)


"""
@csrf_exempt
def login(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        try:
            cred = models.credential.objects.get(pk = received_json_data['login_id'])
            if cred.password == received_json_data['password']:
                # calling respective view function ... 
                if cred.role == 'student':
                    # return HttpResponse("login successful !")
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
                # models.credential.objects.add(new_user)
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

    """
