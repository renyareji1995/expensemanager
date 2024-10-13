from django.shortcuts import render,redirect

from django import forms

from django.views.generic import View

from budget.forms import ExpenseForm,RegistrationForm,SignInForm

from django.contrib import messages

from budget.models import Expense

from django.db.models import Q

from django.db.models import Count,Sum

from django.contrib.auth.models import User

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from budget.decorators import signin_required

from django.views.decorators.cache import never_cache

from django.utils.decorators import method_decorator

decs=[signin_required,never_cache]

@method_decorator(decs,name="dispatch")
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"expense_create.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()

            messages.success(request,"expense has been added")

            return redirect("expense-list")
        
        else:

            messages.error(request,"failed to add expense")

            return render(request,"expense_create.html",{"form":form_instance})
        
        
@method_decorator(decs,name="dispatch")
class ExpenseDetailView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        data=Expense.objects.get(id=id)

        return render(request,"expense_detail.html",{"obj":data})
    
    
@method_decorator(decs,name="dispatch")
class ExpenseListView(View):

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("search_text")

        selected_category=request.GET.get("category","all")

        if selected_category == "all":

            qs=Expense.objects.filter(user=request.user)

        else:

            qs=Expense.objects.filter(category=selected_category,user=request.user)

        if search_text!=None:

            qs=Expense.objects.filter(user=request.user)

            qs=qs.filter(Q(title__icontains=search_text))   #icontains---search caseinsesitive)

        return render(request,"expense_list.html",{"expenses":qs,"selected":selected_category})
    
    
@method_decorator(decs,name="dispatch")
class ExpenseUpdateView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        exp_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(instance=exp_obj)

        return render(request,"expense_edit.html",{"form":form_instance})
    


    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        exp_obj=Expense.objects.get(id=id)

        form_instance=ExpenseForm(request.POST,instance=exp_obj)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"expense updated")

            return redirect('expense-list')
       
        else:

            messages.error(request,"failed to update")

            return render(request,"expense_edit.html",{"form":form_instance})


@method_decorator(decs,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"expense deleted")

        return redirect("expense-list")
    
    
@method_decorator(decs,name="dispatch")
class ExpenseSummaryView(View):

    def get(self,request,*args,**kwargs):

        qs=Expense.objects.all()

        total_expense_count=qs.count()

        category_summary=Expense.objects.values("category").annotate(cat_count=Count("category"))
        print(category_summary)

        category_total=Expense.objects.all().values("category").annotate(cat_total=Sum("amount"))
        print(category_total)

        context={

            "total_expense_count":total_expense_count,
            "category_summary":category_summary,
            "category_total":category_total

        }

        return render(request,"dashboard.html",context)
    

class SignUpView(View):

    template_name="registration.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect('signin')
        
        else:

            return render(request,self.template_name,{"form":form_instance})
        
class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})
    

    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            #authenticate
            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("expense-list")
            
        return render(request,self.template_name,{"form":form_instance})
    
@method_decorator(decs,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")
    



class DashboardView(View):

    template_name="dashboard.html"

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name)









            
    











        


            




