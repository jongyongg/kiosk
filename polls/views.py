from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Question, Choice, Order, Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    # Create an order only if the user is authenticated
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
    selected_choice.votes += 1
    selected_choice.save()
   
     #else:
       
        # Create an order only if the user is authenticated
       # if request.user.is_authenticated:
       #     quantity = 1  # Assuming quantity is always 1 for a vote
       #     price = 0  # You might need to set the price
    #         total_price = price * quantity
    #         Order.objects.create(question=question, user=request.user, quantity=quantity, price=price, total_price=total_price)
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, pk=product_id)
        total_price = product.price * quantity
        # 주문을 생성합니다.
        Order.objects.create(product=product, user=request.user, quantity=quantity, price=product.price, total_price=total_price)
        return redirect('polls:confirm_order')
    else:
        products = Product.objects.all()
        return render(request, 'polls/order.html', {'products': products})

@login_required
def confirm_order(request):
    # 현재 로그인된 사용자의 주문 목록을 가져옵니다.
    orders = Order.objects.filter(user=request.user)
    # 총 가격을 계산합니다.
    total_price_all = sum(order.total_price for order in orders)
    return render(request, 'polls/confirm_order.html', {'orders': orders, 'total_price_all': total_price_all})
