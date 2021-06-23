from api import serializers
from api.models import User
from api.serializers import UserSignupSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import BadRequest, ValidationError
import pytz
from datetime import datetime, timedelta
import random



class UserServices():

    def user_sign_up(self, request, format=None):
        try:
            email = request.data['email']
        except:
            return "Please Enter Email ID"
        try:
            user = User.objects.get(email=request.data['email'])
            return "User with the entered Email Address Already Exists"
        except:
            request.data['role'] = 2
            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                self.send_email(serializer.data["email"].lower())
                return {"data":serializer.data, "message":"User Created Successfully", "status":200}

            else:
                return {"data":serializer.errors, "message":"Some Error Occured", "status":500}

    def verify_otp(self, request, format=None):
        # self.validate_otp_data (request.data)

        if 'TIME-ZONE' in request.headers:
            member_time_zone = "UTC"
        else:
            member_time_zone = "UTC"

        tz = pytz.timezone(member_time_zone)

        current_time = datetime.now (tz)
        now_date = current_time.strftime ('%m/%d/%y')
        now_time = current_time.strftime ('%H:%M')

        user_email = request.data['email'].lower()
        otp = request.data['otp']
        try:
            user = User.objects.get(email=user_email.lower(), otp=otp)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_no=user_email.lower(), otp=otp)
            except User.DoesNotExist:
                return {"data": None, "code": 200, "message": "USER_DOES_NOT_EXIST"}
        if user:
            otp_send_time = user.otp_send_time
            otp_send_time = otp_send_time.astimezone (tz) + timedelta (hours=1)

            otp_date = datetime.strftime (otp_send_time, '%m/%d/%y')
            otp_time = datetime.strftime (otp_send_time, '%H:%M')

            if now_date == otp_date and now_time <= otp_time:
                if user.otp_varification == False:
                    user.profile_completion =  str(round((float(user.profile_completion) + 7.692),3))
                    user.profile_status = 2
                    user.is_active = True
                    user.otp_varification = True
                
                if user.password_reset_otp_verification == False:
                    user.password_reset_otp_verification = True
                user.save()
                data={}
                data['id'] = user.id

            

                
                return {"data": data, "code": 200, "message": "OTP_VERIFID"}
            else:
                return {"data": None, "code": 400, "message": "OTP_EXPIRED"}
        else:
            return {"data": None, "code": 400, "message": "DETAILS_INCORRECT"}
    def send_email(self, email):
        try:

            # if 'TIME-ZONE' in request.headers:
            #     member_time_zone = "UTC"
            # else:
            #     member_time_zone = "UTC"
            member_time_zone = "UTC"
            tz = pytz.timezone(member_time_zone)

            current_time = datetime.now(tz)
            # try:
            #     user = User.objects.get(email=email.lower(), is_deleted=False, role=4)
            # except User.DoesNotExist:
            print("email: {}".format(email))

            try:
                user = User.objects.get(email=email.lower())
            except User.DoesNotExist:
                raise Exception ({
                    'email': "Email Does not Exist"
                })
            # user = self.get_object_by_email (email)
            otp = random.randint (100000, 999999)
            # user.otp = otp
            user.otp_send_time = current_time
            user.otp = otp
            user.save ()
            context = {"otp": otp}
            body_msg = "Your OTP is " + otp
            msg = EmailMultiAlternatives("Email Varification<Don't Reply>", body_msg, "sagarseth@apptunix.com", [email])
            msg.content_subtype = "html"
            msg.send()
            return "Success"
        except Exception as e:
            raise ValidationError({"error":e})
            