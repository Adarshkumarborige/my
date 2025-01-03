from django.shortcuts import render,redirect
from .models import* 
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
import face_recognition
import cv2
from twilio.rest import Client
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#Add yourr own credentials
account_sid = 'AC3f0fff3bc848b9266c5478d8b7476162'
auth_token = 'cd11987e82ee2ef9fc1c392d37492b7d'
twilio_whatsapp_number = '+12694487393'

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
        else:
            # Create the user
            User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')

    return render(request, 'registeru.html')
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Get the user by email
            user = User.objects.get(email=email)

            # Authenticate the user
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')

    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request,"index.html")

def send_whatsapp_message(to,context):
    client = Client(account_sid, auth_token)
    whatsapp_message = (
    f"Dear {context['fathers_name']},\n\n"
    f"We are pleased to inform you that the missing person missing from {context['missing_from']} and you were concerned about has been found. "
    "The person was located in a camera footage, and we have identified their whereabouts.\n\n"
    "Here are the details:\n"
    f" - Name: {context['first_name']} {context['last_name']}\n"
    f" - Date and Time of Sighting: {context['date_time']}\n"
    f" - Location: {context['location']}\n"
    f" - Aadhar Number: {context['aadhar_number']}\n\n"
    #"We understand the relief this news must bring to you. If you have any further questions or require more information, please do not hesitate to reach out to us.\n\n"
    "Thank you for your cooperation and concern in this matter.\n\n"
    "Sincerely,\n\n"
    "Team Bharatiya Rescue ")
    message = client.messages.create(
        body=whatsapp_message,
        from_='whatsapp:' + twilio_whatsapp_number,
        to='whatsapp:' + to
    )

    print(f"WhatsApp message sent: {message.sid}")

# def detect(request):
#     video_capture = cv2.VideoCapture(0)
#     if not video_capture.isOpened():
#         print("Error: Could not access the camera.")
#         return render(request, "error.html", {"message": "Camera not accessible."})
    
#     process_this_frame = True
#     face_detected = False

#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             print("Error: Failed to capture frame.")
#             break

#         # Resize frame to 1/4 size for faster face detection
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

#         # Process every other frame
#         if process_this_frame:
#             face_locations = face_recognition.face_locations(small_frame)
#             face_encodings = face_recognition.face_encodings(small_frame, face_locations)

#             for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
#                 for person in MissingPerson.objects.all():
#                     stored_image = face_recognition.load_image_file(person.image.path)
#                     stored_face_encoding = face_recognition.face_encodings(stored_image)[0]

#                     matches = face_recognition.compare_faces([stored_face_encoding], face_encoding, tolerance=0.6)

#                     if any(matches):
#                         name = f"{person.first_name} {person.last_name}"
#                         cv2.rectangle(frame, (left * 4, bottom * 4 - 35), (right * 4, bottom * 4), (0, 0, 255), cv2.FILLED)
#                         font = cv2.FONT_HERSHEY_DUPLEX
#                         cv2.putText(frame, name, (left * 4 + 6, bottom * 4 - 6), font, 1.0, (255, 255, 255), 1)

#                         if not face_detected:
#                             print(f"Hi {name} is found")
#                             current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
#                             subject = 'Missing Person Found'
#                             from_email = 'signingintolobby@gmail.com'
#                             recipientmail = person.email
#                             recipient_phone_number = '+91' + str(person.phone_number)
#                             context = {"first_name": person.first_name, "last_name": person.last_name,
#                                        'fathers_name': person.father_name, "aadhar_number": person.aadhar_number,
#                                        "missing_from": person.missing_from, "date_time": current_time, "location": "India"}
#                             send_whatsapp_message(recipient_phone_number, context)
#                             html_message = render_to_string('findemail.html', context=context)
#                             send_mail(subject, '', from_email, [recipientmail], fail_silently=False, html_message=html_message)
#                             face_detected = True
#                             break

#             if not face_detected:
#                 name = "Unknown"
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left * 4 + 6, bottom * 4 - 6), font, 1.0, (255, 255, 255), 1)

#         process_this_frame = not process_this_frame

#         # Display the resulting image
#         cv2.imshow('Camera Feed', frame)

#         # Exit on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     video_capture.release()
#     cv2.destroyAllWindows()
#     return render(request, "surveillance.html")

# import cv2
import face_recognition
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import MissingPerson

def detect(request):
    video_capture = cv2.VideoCapture(0)
    face_detected = False
    face_check_frequency = 10  # Check every 10th frame for face detection
    frame_count = 0  # To control frame checks

    while True:
        ret, frame = video_capture.read()
        frame_count += 1

        # Skip frames to reduce the load
        if frame_count % face_check_frequency != 0:
            continue

        # Find face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # Compare detected face with stored face images
            for person in MissingPerson.objects.all():
                stored_image = face_recognition.load_image_file(person.image.path)
                stored_face_encoding = face_recognition.face_encodings(stored_image)[0]

                # Compare face encodings using a tolerance value
                matches = face_recognition.compare_faces([stored_face_encoding], face_encoding)

                if any(matches):
                    name = person.first_name + " " + person.last_name
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                    # Send email if face is detected and it's the first time
                    if not face_detected:
                        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
                        subject = 'Missing Person Found'
                        from_email = 'signingintolobby@gmail.com'
                        recipientmail = person.email
                        recipient_phone_number = '+91'+str(person.phone_number)
                        
                        # Prepare the context for the email
                        context = {
                            "first_name": person.first_name,
                            "last_name": person.last_name,
                            'fathers_name': person.father_name,
                            "aadhar_number": person.aadhar_number,
                            "missing_from": person.missing_from,
                            "date_time": current_time,
                            "location": "India"
                        }

                        # Render the HTML email
                        html_message = render_to_string('findemail.html', context=context)
                        
                        # Send the email
                        send_mail(
                            subject,
                            '',  # Plain text version (leave empty if not required)
                            from_email,
                            [recipientmail],
                            fail_silently=False,
                            html_message=html_message
                        )

                        face_detected = True  # Mark that a face has been detected
                        break  # Exit after sending the email

        # Display the resulting image with the detected face name
        cv2.imshow('Camera Feed', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return render(request, "surveillance.html")

def surveillance(request):
    return render(request,"surveillance.html")

@login_required
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('fathers_name')
        date_of_birth = request.POST.get('dob')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenum')
        aadhar_number = request.POST.get('aadhar_number')
        missing_from = request.POST.get('missing_date')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        gender = request.POST.get('gender')
        aadhar = MissingPerson.objects.filter(aadhar_number=aadhar_number)
        if aadhar.exists():
            messages.info(request, 'Aadhar Number already exists')
            return redirect('/register')
        person = MissingPerson.objects.create(
            first_name = first_name,
            last_name = last_name,
            father_name = father_name,
            date_of_birth = date_of_birth,
            address = address,
            phone_number = phone_number,
            aadhar_number = aadhar_number,
            missing_from = missing_from,
            email = email,
            image = image,
            gender = gender,
        )
        person.save()
        messages.success(request,'Case Registered Successfully')
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        subject = 'Case Registered Successfully'
        from_email = 'pptodo01@gmail'
        recipientmail = person.email
        context = {"first_name":person.first_name,"last_name":person.last_name,
                    'fathers_name':person.father_name,"aadhar_number":person.aadhar_number,
                    "missing_from":person.missing_from,"date_time":current_time}
        html_message = render_to_string('regmail.html',context = context)
        # Send the email
        send_mail(subject,'', from_email, [recipientmail], fail_silently=False, html_message=html_message)

    return render(request,"register.html")


def  missing(request):
    queryset = MissingPerson.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(aadhar_number__icontains=search_query)
    
    context = {'missingperson': queryset}
    return render(request,"missing.html",context)

def delete_person(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id)
    person.delete()
    return redirect('missing')  # Redirect to the missing view after deleting


def update_person(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id)

    if request.method == 'POST':
        # Retrieve data from the form
        first_name = request.POST.get('first_name', person.first_name)
        last_name = request.POST.get('last_name', person.last_name)
        fathers_name = request.POST.get('fathers_name', person.fathers_name)
        dob = request.POST.get('dob', person.dob)
        address = request.POST.get('address', person.address)
        email = request.POST.get('email', person.email)
        phonenum = request.POST.get('phonenum', person.phonenum)
        aadhar_number = request.POST.get('aadhar_number', person.aadhar_number)
        missing_date = request.POST.get('missing_date', person.missing_date)
        gender = request.POST.get('gender', person.gender)

        # Check if a new image is provided
        new_image = request.FILES.get('image')
        if new_image:
            person.image = new_image

        # Update the person instance
        person.first_name = first_name
        person.last_name = last_name
        person.fathers_name = fathers_name
        person.dob = dob
        person.address = address
        person.email = email
        person.phonenum = phonenum
        person.aadhar_number = aadhar_number
        person.missing_date = missing_date
        person.gender = gender

        # Save the changes
        person.save()

        return redirect('missing')  # Redirect to the missing view after editing

    return render(request, 'edit.html', {'person': person})
