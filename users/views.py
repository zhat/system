from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import ChangeForm,ChangepwdForm
from django.contrib.auth.models import User

def logout_view(request):
    """注销用户"""
    logout(request)
    return HttpResponseRedirect(reverse('order:search'))

def register(request):
    """注册新用户"""
    if request.method!='POST':
        #显示空的注册表单
        form=UserCreationForm()
    else:
        #处理填写好的表单
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #让用户自动登录，再重定向到主页
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('blog:index'))
    context={'form':form}
    return render(request,'users/register.html',context)

def about(request):
    return render(request,'users/about.html',{})

@login_required
def changepwd(request):
    if request.method == 'POST':
        uf = ChangeForm(request.POST)
        user = request.user
        if uf.is_valid():
            old_password = uf.cleaned_data['old_password']
            new_password1 = uf.cleaned_data['new_password1']
            new_password2 = uf.cleaned_data['new_password2']
            if new_password1!=new_password2:
                error = "两次输入密码不一致"
                return render(request, 'users/change.html', {'uf': uf, 'error': error})

            ##判断用户原密码是否匹配
            username = user.username
            user = authenticate(username=username, password=old_password)
            if user:
                user.set_password(new_password1)
                user.save()
                return HttpResponseRedirect(reverse('order:search'))
            else:
                error='原密码输入不正确'
                return render(request,'users/change.html',{'uf':uf,'error':error})
    else:
        uf = ChangeForm()
        return render(request,'users/change.html', {'uf': uf})