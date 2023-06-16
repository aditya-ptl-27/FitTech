from django.shortcuts import render,redirect
from .models import User,Workout,Bmi
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.
def index(request):
	workout=Workout.objects.all()
	trainer=User.objects.filter(usertype='trainer')
	return render(request,'index.html',{'workout':workout,'trainer':trainer})

def signup(request):
	if request.method=='POST':
		user=User()
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.email=request.POST['email']
		user.mobile=request.POST['mobile']	
		user.password=request.POST['password']
		try:
			User.objects.get(email=request.POST['email'])
			msg='Email Already Registered'
			return render(request,'signup.html',{"msg":msg,'user':user})
		except:
			if request.POST['password']==request.POST['cpassword']:
				User.objects.create(
							fname=request.POST['fname'],
							lname=request.POST['lname'],
							email=request.POST['email'],
							mobile=request.POST['mobile'],
							password=request.POST['password'],
							profile_pic=request.FILES['profile_pic'],
							usertype=request.POST['usertype']
							)
				msg='User SignUp Successful'
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Does Not Match"
				return render(request,'signup.html',{'msg':msg,'user':user})
	else:
		return render(request,'signup.html')


def login(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			if user.password==request.POST['password']:
				if user.usertype=='user':
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return redirect('index')
				elif user.usertype=='trainer':
					request.session['email']=user.email
					request.session['fname']=user.fname
					request.session['profile_pic']=user.profile_pic.url
					return redirect('trainer_index')
			else:
				msg='Password Is Incorrect'
				return render(request,'login.html',{'msg':msg})
		except:
			msg='Email Does Not Exist'
			return render(request,'login.html',{'msg':msg})

	else:
		return render(request,'login.html')

def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_pic']
		return render(request,'login.html')

	except:
		return render(request,'login.html')

def change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==user.password:
				msg='You Cannot Use Your Old Password'
				return render(request,'change_password.html',{'msg':msg})
			else:

				if request.POST['new_password']==request.POST['cnew_password']:
					user.password=request.POST['new_password']
					user.save()
					del request.session['email']
					del request.session['fname']
					del request.session['profile_pic']
					msg='Password Changed Successfully'
					return render(request,'login.html',{'msg':msg})
				else:
					msg='New Password And Confirm New Password Does Not Match'
					return render(request,'change_password.html',{'msg':msg})
		else:
			msg='Old Password Is Incorrect'
			return render(request,'change_password.html',{'msg':msg})

	else:
		return render(request,'change_password.html')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg='Profile Updated Successfully'
		request.session['profile_pic']=user.profile_pic.url
		request.session['fname']=user.fname
		return render(request,'profile.html',{'msg':msg,'user':user})
	else:
		return render(request,'profile.html',{'user':user})

def forgot_password(request):
	if request.method=='POST':
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OTP For Forgot Password'
			message ='Hi '+ user.fname+ ', Your OTP For Forgot Password Is '+ str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			msg='OTP Sent Successfully'
			return render(request,'otp.html',{'otp':otp,'email':user.email,'msg':msg})
		except:
			msg='Email Not Registered'
			return render(request,'forgot_password.html',{'msg':msg}) 
	else:
		return render(request,'forgot_password.html')


def verify_otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'new_password.html',{'email':email})
	else:
		msg='OTP Does Not Match'
		return render(request,'otp.html',{'email':email,'otp':otp,'msg':msg})

def update_password(request):
	email=request.POST['email']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']
	if np==cnp:
		user=User.objects.get(email=email)
		if user.password==np:
			msg='You Cannot Use Your Old Password'
			return render(request,'new_password.html',{'email':email,'msg':msg})
		else:
			user.password=np
			user.save()
			# return redirect('logout')
			msg='Password Updated Successfully'
			return render(request,'login.html',{'msg':msg})
	else:
		msg='New Password & Confirm New Password Does Not Match'
		return render(request,'new_password.html',{'email':email,'msg':msg})

def trainer_index(request):
	# try:
	# 	user=User.objects.get(email=request.session['email'])
	# 	if user.usertype=='trainer':
	# 		products=Product.objects.all()
	# 		return render(request,'trainer_index.html',{'products':products})

	# 	else:
	# 		return render(request,'trainer_index.html')
	# except:
	# 	products=Product.objects.all()
	return render(request,'trainer_index.html')

def trainer_add_workout(request):
	if request.method=='POST':
		trainer=User.objects.get(email=request.session['email'])
		Workout.objects.create(
				trainer=trainer,
				w_type=request.POST['w_type'],
				w_name=request.POST['w_name'],
				w_description=request.POST['w_description'],
				w_difficulty=request.POST['w_difficulty'],
				w_gif=request.FILES['w_gif'],
				w_muscles_targeted=request.POST['w_muscles_targeted']
			)	
		msg='Workout Added Successfully'
		return render(request,'trainer_add_workout.html',{'msg':msg})

	else:
		return render(request,'trainer_add_workout.html')
	# return render(request,'trainer_add_workout.html')

def trainer_view_workouts(request):
	trainer=User.objects.get(email=request.session['email'])
	workouts=Workout.objects.filter(trainer=trainer)
	return render(request,'trainer_view_workouts.html',{'workouts':workouts})

def trainer_workout_detail(request,pk):
	user=User.objects.get(email=request.session['email'])
	workout=Workout.objects.get(pk=pk)
	return render(request,'trainer_workout_detail.html',{'workout':workout,'user':user})

def trainer_workout_edit(request,pk):
	workout=Workout.objects.get(pk=pk)
	if request.method=='POST':
		workout.w_type=request.POST['w_type']
		workout.w_name=request.POST['w_name']
		workout.w_description=request.POST['w_description']
		workout.w_difficulty=request.POST['w_difficulty']
		workout.w_muscles_targeted=request.POST['w_muscles_targeted']
		try:
			workout.w_gif=request.FILES['w_gif']
		except:
			pass
		workout.save()
		msg="Workout Updated Successfully"
		return render(request,'trainer_workout_edit.html',{'workout':workout,'msg':msg})

	else:
		return render(request,'trainer_workout_edit.html',{'workout':workout})

def trainer_workout_delete(request,pk):
	workout=Workout.objects.get(pk=pk)
	workout.delete()
	msg='Product Deleted Successfully'
	return redirect('trainer_view_workouts')


def trainer_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg='Profile Updated Successfully'
		request.session['profile_pic']=user.profile_pic.url
		request.session['fname']=user.fname
		return render(request,'trainer_profile.html',{'msg':msg,'user':user})
	else:
		return render(request,'trainer_profile.html',{'user':user})

def trainer_change_password(request):
	if request.method=='POST':
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==user.password:
				msg='You Cannot Use Your Old Password'
				return render(request,'trainer_change_password.html',{'msg':msg})
			else:

				if request.POST['new_password']==request.POST['cnew_password']:
					user.password=request.POST['new_password']
					user.save()
					del request.session['email']
					del request.session['fname']
					del request.session['profile_pic']
					msg='Password Changed Successfully'
					return render(request,'login.html',{'msg':msg})
				else:
					msg='New Password And Confirm New Password Does Not Match'
					return render(request,'trainer_change_password.html',{'msg':msg})
		else:
			msg='Old Password Is Incorrect'
			return render(request,'trainer_change_password.html',{'msg':msg})

	else:
		return render(request,'trainer_change_password.html')

def calculate_bmi(request):
	if request.method == 'POST':
		weight = float(request.POST.get('weight'))
		height = float(request.POST.get('height'))
		final_bmi=0
		if weight <= 0 or height <= 0:
			return HttpResponse('Please enter valid weight and height values.')
		else:
			return redirect('calculate_bmi')
		bmi = weight / (height * height)
		final_bmi=bmi*10000
		context={'final_bmi':final_bmi}
	return render(request,'calculate_bmi.html',context)

# def calculate_bmi(request):
# 	if request.method == 'POST':
  
#   		height =int(request.POST["height"])
#   		weight =int(request.POST["weight"])
  
#   		bmi = weight / (height * height)
  
#   		context = {
#     			"bmi": bmi,
#   				}
#   		return render(request, "result_bmi.html", context)
# 	else:
# 		return render(request,'calculate_bmi.html')

# def calculate_bmi(request):


def about(request):
	return render(request,'about.html')

def home_workouts(request):

	return render(request,'home_workouts.html')

def trainer_home_workouts(request):
	return render(request,'trainer_home_workouts.html')

def full_body(request):
	workout=Workout.objects.filter(w_type='Full Body')
	return render(request,'full_body.html',{'workout':workout})

def lower_body(request):
	workout=Workout.objects.filter(w_type='Lower Body')
	return render(request,'lower_body.html',{'workout':workout})

def weight_loss(request):
	workout=Workout.objects.filter(w_type='Weight Loss')
	return render(request,'weight_loss.html',{'workout':workout})

def get_fit(request):
	workout=Workout.objects.filter(w_type='Get Fit')
	return render(request,'get_fit.html',{'workout':workout})

def build_muscle(request):
	workout=Workout.objects.filter(w_type='Build Muscle')
	return render(request,'build_muscle.html',{'workout':workout})

def gain_strength(request):
	workout=Workout.objects.filter(w_type='Gain Strength')
	return render(request,'gain_strength.html',{'workout':workout})


def upper_body(request):
	workout=Workout.objects.filter(w_type='Upper Body')
	return render(request,'upper_body.html',{'workout':workout})

# def classes_details(request):
# 	return render(request,'classes-details.html')

def workout_detail(request,pk):
	workout=Workout.objects.get(pk=pk)
	trainer=workout.trainer
	return render(request,'workout_detail.html',{'workout':workout,'trainer':trainer})

def trainer(request):
	return render(request,'trainer.html')


def blog(request):
	return render(request,'blog.html')

def single_blog(request):
	return render(request,'single-blog.html')

def events(request):
	return render(request,'events.html')

def event_details(request):
	return render(request,'event-details.html')

def contact(request):
	return render(request,'contact.html')