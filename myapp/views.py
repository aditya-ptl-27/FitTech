from django.shortcuts import render,redirect
from .models import User,Workout,BlogModel
from django.conf import settings
from django.core.mail import send_mail
import random
from .form import *

# Create your views here.

def chat(request):
	return render(request,'chat.html')

def index(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.all()
			blogs=BlogModel.objects.all()
			trainer=User.objects.filter(usertype='trainer')
			context={'workout':workout,'trainer':trainer,'blogs':blogs,'user':user}
			return render(request,'index.html',context)
		else:
			return redirect('trainer_index')
	except:
		workout=Workout.objects.all()
		blogs=BlogModel.objects.all()
		trainer=User.objects.filter(usertype='trainer')
		context={'workout':workout,'trainer':trainer,'blogs':blogs}
		return render(request,'index.html',context)

def signup(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return redirect('index')
		else:
			return redirect('trainer_index')
	except:	
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
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return redirect('index')
		else:
			return redirect('trainer_index')
	except:
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
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='user':
		if request.method=='POST':
			if user.password==request.POST['old_password']:
				if request.POST['new_password']==user.password:
					msg='You Cannot Use Your Old Password'
					return render(request,'change_password.html',{'msg':msg,'user':user})
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
						return render(request,'change_password.html',{'msg':msg,'user':user})
			else:
				msg='Old Password Is Incorrect'
				return render(request,'change_password.html',{'msg':msg,'user':user})

		else:
			return render(request,'change_password.html',{'user':user})
	else:
		return redirect('trainer_change_password')

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='user':
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
	else:
		return redirect('trainer_profile')

def forgot_password(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return redirect('change_password')
		else:
			return redirect('trainer_change_password')
	except:
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
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return redirect('index')
		else:
			return redirect('trainer_index')
	except:
		email=request.POST['email']
		otp=request.POST['otp']
		uotp=request.POST['uotp']

		if otp==uotp:
			return render(request,'new_password.html',{'email':email})
		else:
			msg='OTP Does Not Match'
			return render(request,'otp.html',{'email':email,'otp':otp,'msg':msg})

def update_password(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return redirect('index')
		else:
			return redirect('trainer_index')
	except:
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
				msg='Password Updated Successfully'
				return render(request,'login.html',{'msg':msg})
		else:
			msg='New Password & Confirm New Password Does Not Match'
			return render(request,'new_password.html',{'email':email,'msg':msg})

def trainer_index(request):
	trainer=User.objects.get(email=request.session['email'])
	user=User.objects.get(email=request.session['email'])
	if trainer.usertype=='trainer':
		blogs=BlogModel.objects.filter(user=user)
		workout=Workout.objects.filter(trainer=trainer)
		trainers=User.objects.filter(usertype='trainer')
		context={'workout':workout,'trainers':trainers,'blogs':blogs,'user':user}
		return render(request,'trainer_index.html',context)
	else:
		return redirect('index')

def trainer_add_workout(request):
	user=User.objects.get(email=request.session['email'])
	trainer=User.objects.get(email=request.session['email'])
	if trainer.usertype=='trainer':
		if request.method=='POST':
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
			return render(request,'trainer_add_workout.html',{'msg':msg,'user':user})

		else:
			return render(request,'trainer_add_workout.html',{'user':user})
	else:
		return redirect('index')


def trainer_view_workouts(request):
	user=User.objects.get(email=request.session['email'])
	trainer=User.objects.get(email=request.session['email'])
	if trainer.usertype=='trainer':
		workouts=Workout.objects.filter(trainer=trainer)
		return render(request,'trainer_view_workouts.html',{'workouts':workouts,'user':user})
	else:
		return redirect('home_workouts')

def trainer_workout_detail(request,pk):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		workout=Workout.objects.get(pk=pk)
		return render(request,'trainer_workout_detail.html',{'workout':workout,'user':user})
	else:
		return redirect('home_workouts')

def trainer_workout_edit(request,pk):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
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
			return render(request,'trainer_workout_edit.html',{'workout':workout,'msg':msg,'user':user})

		else:
			return render(request,'trainer_workout_edit.html',{'workout':workout,'user':user})
	else:
		return redirect('index')

def trainer_workout_delete(request,pk):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		workout=Workout.objects.get(pk=pk)
		workout.delete()
		msg='Product Deleted Successfully'
		return redirect('trainer_view_workouts')
	else:
		return redirect('index')


def trainer_profile(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
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
	else:
		return redirect('profile')

def trainer_change_password(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		if request.method=='POST':
			if user.password==request.POST['old_password']:
				if request.POST['new_password']==user.password:
					msg='You Cannot Use Your Old Password'
					return render(request,'trainer_change_password.html',{'msg':msg,'user':user})
				else:

					if request.POST['new_password']==request.POST['cnew_password']:
						user.password=request.POST['new_password']
						user.save()
						del request.session['email']
						del request.session['fname']
						del request.session['profile_pic']
						msg='Password Changed Successfully'
						return render(request,'login.html',{'msg':msg,'user':user})
					else:
						msg='New Password And Confirm New Password Does Not Match'
						return render(request,'trainer_change_password.html',{'msg':msg,'user':user})
			else:
				msg='Old Password Is Incorrect'
				return render(request,'trainer_change_password.html',{'msg':msg,'user':user})


		else:
			return render(request,'trainer_change_password.html',{'user':user})
	else:
		return redirect('change_password')

def calculate_bmi(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request, 'calculate_bmi.html',{'user':user})
		else:
			return redirect('trainer_index')
	except:
		return render(request, 'calculate_bmi.html')

def ideal_body_weight(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request,'ideal_body_weight.html',{'user':user})
		else:
			return redirect('trainer_index')
	except:
		return render(request,'ideal_body_weight.html')

def daily_calorie_intake(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request,'daily_calorie_intake.html',{'user':user})
		else:
			return redirect('trainer_index')
	except:
		return render(request,'daily_calorie_intake.html')

def calories_burnt(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request,'calories_burnt.html',{'user':user})
		else:
			return redirect('trainer_index')
	except:
		return render(request,'calories_burnt.html')

def about(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			trainer=User.objects.filter(usertype='trainer')
			return render(request,'about.html',{'trainer':trainer,'user':user})
		else:
			return redirect('trainer_index')
	except:
		trainer=User.objects.filter(usertype='trainer')
		return render(request,'about.html',{'trainer':trainer})

def home_workouts(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request,'home_workouts.html',{'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		return render(request,'home_workouts.html')

def beginner_workouts(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_difficulty="Beginner")
			return render(request,'beginner_workouts.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_difficulty="Beginner")
		return render(request,'beginner_workouts.html',{'workout':workout})

def intermediate_workouts(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_difficulty="Intermediate")
			return render(request,'intermediate_workouts.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_difficulty="Intermediate")
		return render(request,'intermediate_workouts.html',{'workout':workout})

def advanced_workouts(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_difficulty="Advanced")
			return render(request,'advanced_workouts.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_difficulty="Advanced")
		return render(request,'advanced_workouts.html',{'workout':workout})

def trainer_home_workouts(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request,'home_workouts.html',{'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		return render(request,'trainer_home_workouts.html')
	
def full_body(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_type='Full Body')
			return render(request,'full_body.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_type='Full Body')
		return render(request,'full_body.html',{'workout':workout})

def lower_body(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_type='Lower Body')
			return render(request,'lower_body.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_type='Lower Body')
		return render(request,'lower_body.html',{'workout':workout})

def weight_loss(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_type='Weight Loss')
			return render(request,'weight_loss.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_type='Weight Loss')
		return render(request,'weight_loss.html',{'workout':workout})

def get_fit(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_type='Get Fit')
			return render(request,'get_fit.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_type='Get Fit')
		return render(request,'get_fit.html',{'workout':workout})

def build_muscle(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_type='Build Muscle')
			return render(request,'build_muscle.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_type='Build Muscle')
		return render(request,'build_muscle.html',{'workout':workout})

def gain_strength(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_type='Gain Strength')
			return render(request,'gain_strength.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_type='Gain Strength')
		return render(request,'gain_strength.html',{'workout':workout})


def upper_body(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.filter(w_type='Upper Body')
			return render(request,'upper_body.html',{'workout':workout,'user':user})
		else:
			return redirect('trainer_view_workouts')
	except:
		workout=Workout.objects.filter(w_type='Upper Body')
		return render(request,'upper_body.html',{'workout':workout})


def workout_detail(request,pk):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			workout=Workout.objects.get(pk=pk)
			trainer=workout.trainer
			latest_workouts=Workout.objects.order_by("-id")[:3]
			latest_workouts_02=Workout.objects.order_by("id")[:3]
			context={'workout':workout,
					'trainer':trainer,
					'latest_workouts':latest_workouts,
					'latest_workouts_02':latest_workouts_02,'user':user}
			return render(request,'workout_detail.html',context)

		else:
			return redirect('trainer_view_workouts')
	except:
		return redirect('login')

def trainer(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			trainer=User.objects.filter(usertype='trainer')
			return render(request,'trainer.html',{'trainer':trainer,'user':user})
		else:
			return redirect('trainer_index')
	except:
		trainer=User.objects.filter(usertype='trainer')
		return render(request,'trainer.html',{'trainer':trainer})


def contact(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			return render(request,'contact.html',{'user':user})
		else:
			return redirect('trainer_index')
	except:
		return render(request,'contact.html')

def blog(request):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			blogs=BlogModel.objects.all()
			return render(request, 'blog.html',{'blogs':blogs,'trainer':trainer,'user':user})
		else:
			return redirect('trainer_view_blogs')
	except:
		blogs=BlogModel.objects.all()
		return render(request, 'blog.html',{'blogs':blogs,'trainer':trainer})

def blog_detail(request, slug):
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=='user':
			blog=BlogModel.objects.get(slug=slug)
			trainer=blog.user
			latest_blogs=BlogModel.objects.order_by("-id")[:3]
			latest_blogs_02=BlogModel.objects.order_by("id")[:3]
			print(trainer)
			context = {'trainer':trainer,'latest_blogs':latest_blogs,
					'latest_blogs_02':latest_blogs_02,'user':user}
			try:
				blog_obj = BlogModel.objects.filter(slug=slug).first()
				context['blog_obj'] = blog_obj
			except Exception as e:
				print(e)
			return render(request, 'blog_detail.html', context)
		else:
			return redirect('trainer_view_blogs')
	except:
		blog=BlogModel.objects.get(slug=slug)
		trainer=blog.user
		latest_blogs=BlogModel.objects.order_by("-id")[:3]
		latest_blogs_02=BlogModel.objects.order_by("id")[:3]
		print(trainer)
		context = {'trainer':trainer,'latest_blogs':latest_blogs,
				'latest_blogs_02':latest_blogs_02}
		try:
			blog_obj = BlogModel.objects.filter(slug=slug).first()
			context['blog_obj'] = blog_obj
		except Exception as e:
			print(e)
		return render(request, 'blog_detail.html', context)

def trainer_add_blog(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		context = {'form': BlogForm,'user':user}
		context1={'form':BlogForm,'user':user}
		try:
			if request.method == 'POST':
				form = BlogForm(request.POST)
				print(request.FILES)
				image = request.FILES.get('image', '')
				title = request.POST.get('title')
				user=User.objects.get(email=request.session['email'])
			
				if form.is_valid():
					print('Valid')
					content = form.cleaned_data['content']

				blog_obj = BlogModel.objects.create(
					user=user, title=title,
					content=content, image=image
					)
				print(blog_obj)
				msg="Blog Added Successfully"
				context['msg']=msg
				return render(request,'trainer_add_blog.html',context)
		except Exception as e:
			print(e)

		return render(request, 'trainer_add_blog.html', context1)
	else:
		return redirect('index')

def trainer_view_blogs(request):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		blogs=BlogModel.objects.filter(user=user)
		return render(request, 'trainer_view_blogs.html',{'blogs':blogs,'user':user})
	else:
		return redirect('blog')

def trainer_blog_detail(request, slug):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		trainer=BlogModel.objects.get(slug=slug)
		print(trainer)
		context = {'user':user}
		try:
			blog_obj = BlogModel.objects.filter(slug=slug).first()
			context['blog_obj'] = blog_obj
		except Exception as e:
			print(e)
		return render(request, 'trainer_blog_detail.html', context)
	else:
		return redirect('blog')

def trainer_blog_edit(request,slug):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		blog_obj=BlogModel.objects.get(slug=slug)
		initial_dict = {'content': blog_obj.content}
		form = BlogForm(initial=initial_dict)
		if request.method=='POST':
			form = BlogForm(request.POST)
			blog_obj.title=request.POST['title']
			blog_obj.content=request.POST['content']
			
			try:
				blog_obj.image=request.FILES['image']
			except:
				pass
			blog_obj.save()
			msg="Blog Updated Successfully"
			return render(request,'trainer_blog_edit.html',{'blog_obj':blog_obj,'msg':msg,'form':form,'user':user})

		else:
			return render(request,'trainer_blog_edit.html',{'blog_obj':blog_obj,'form':form,'user':user})
	else:
		return redirect('index')

def trainer_blog_delete(request, id):
	user=User.objects.get(email=request.session['email'])
	if user.usertype=='trainer':
		try:
			blog_obj = BlogModel.objects.get(id=id)
			blog_obj.delete()
			return redirect('trainer_view_blogs')

		except Exception as e:
			print(e)

			return redirect('trainer_view_blogs')
	else:
		return redirect('index')