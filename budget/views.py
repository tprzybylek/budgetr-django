import json
import decimal

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import Sum

from django.contrib.auth.models import User
from .models import Operation, Budget, Category
from .forms import AddOperationForm, AddBudgetForm

from django.utils import timezone

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

# Create your views here.

@login_required
def last_operations(request):
    current_user = request.user
    operations = Operation.objects.filter(user=current_user)
    return render(request, 'budget/last_operations.html', {'operations': operations})

def add_operation(request):
    if request.method == 'POST':
        form = AddOperationForm(request.POST, user=request.user)

        if form.is_valid():
            cd = form.cleaned_data
            operation = Operation(datetime=cd['datetime'],
                                  category=cd['category'],
                                  budget=cd['budget'],
                                  user=request.user,
                                  value=cd['value'],
                                  is_recurring=cd['is_recurring'],
                                  is_income=cd['is_income'],
                                  comment=cd['comment'])
            operation.save()

            return render(request,
                          'budget/add_operation.html',
                          {'user_form': form})
    else:
        form = AddOperationForm(user=request.user)
    return render(request,
                  'budget/add_operation.html',
                  {'user_form': form})



    return render(request, 'budget/add_operation.html')

def view_budgets(request):
    current_user = request.user
    budgets = Budget.objects.filter(user=current_user)
    return render(request, 'budget/view_budgets.html', {'budgets': budgets})

def add_budget(request):
    if request.method == 'POST':
        form = AddBudgetForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            budget = Budget(name=cd['name'],
                               user=request.user,
                               value=cd['value'],
                               )
            budget.save()

            return render(request,
                          'budget/add_budget.html',
                          {'user_form': form})
    else:
        form = AddBudgetForm()
    return render(request,
                  'budget/add_budget.html',
                  {'user_form': form})

def view_categories(request):
    categories = Category.objects.filter(user=None) | Category.objects.filter(user=request.user)

    return render(request, 'budget/view_categories.html', {'categories': categories})

def overview(request):
    def build_category_tree(categories):
        def build_category_branch(category, category_dict=None):
            cat =  Category.objects.get(pk=category['category'])
            parent = cat.parent

            if category_dict == None:
                category_dict = {'category': cat.pk,
                                 'name': cat.name,
                                 'value': category['value__sum']}

            else:
                for c in category_tree:
                    if c['category'] == cat.pk:
                        c['subcategories'].append(category_dict)
                        return c

                category_dict = {'category': cat.pk,
                                 'name': cat.name,
                                 'subcategories': [category_dict]}

            if parent is not None:
                category_dict = build_category_branch({'category': parent.pk}, category_dict)
                return category_dict
            else:
                return category_dict

        category_tree = []

        for category in categories:
            branch = build_category_branch(category, category_dict=None)
            category_tree.append(branch)
        return category_tree


    def generate_calendar(first_operation):
        current_year = timezone.now().year

        first_year = first_operation.datetime.year

        years = []

        for year in range(first_year, current_year+1):
            years.append(year)

        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        return {'years': years, 'months': months}

    current_user = request.user
    operations = Operation.objects.filter(user=current_user).order_by('datetime')
    first_operation = operations.first()

    if request.GET.get('active_year') == None and request.GET.get('active_month') == None:
        current_year = timezone.now().year
        current_month = timezone.now().month
        operations = operations.filter(datetime__month=current_month, datetime__year=current_year)

    elif request.GET.get('active_year') !=None and request.GET.get('active_month') == None:
        current_year = int(request.GET.get('active_year'))
        current_month = None
        operations = operations.filter(datetime__year=current_year)

    else:
        current_year = int(request.GET.get('active_year'))
        current_month = int(request.GET.get('active_month'))

        operations = operations.filter(datetime__month=current_month, datetime__year=current_year)



    calendar = generate_calendar(first_operation)

    categories = operations.values('category').annotate(Sum('value'))

    l = build_category_tree(categories)
    categories = []

    for i in range(len(l)):
        if l[i] not in l[i + 1:]:
            categories.append(l[i])

    categories = json.dumps(categories, cls=DecimalEncoder)


    if operations.count() == 0:
        operations = None

    return render(request, 'budget/overview.html', {'operations': operations,
                                                    'categories': categories,
                                                    'calendar': calendar,
                                                    'current_year': current_year,
                                                    'current_month': current_month})