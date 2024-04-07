from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from .models import Question, Choice, Order, Product

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

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # 주문을 생성합니다.
        quantity = int(request.POST.get('quantity'))  # 주문 수량
        price = selected_choice.price  # 선택된 항목의 가격
        total_price = quantity * price  # 해당 주문의 총 가격

        # 주문 정보를 저장합니다.
        order = Order.objects.create(question=question, quantity=quantity, price=price, total_price=total_price, user=request.user)

        # 주문 확인 페이지로 리다이렉트합니다.
        return redirect('polls:confirm_order')

def order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = Product.objects.get(pk=product_id)
        total_price = product.price * quantity
        # 주문을 생성합니다.
        Order.objects.create(question=None, user=request.user, quantity=quantity, price=product.price, total_price=total_price)
        return redirect('polls:confirm_order')
    else:
        products = Product.objects.all()
        return render(request, 'polls/order.html', {'products': products})

def confirm_order(request):
    if not request.user.is_authenticated:
        # 사용자가 로그인되어 있지 않으면 로그인 페이지로 리다이렉트합니다.
        return redirect('login')

    # 현재 로그인된 사용자의 주문 목록을 가져옵니다.
    orders = Order.objects.filter(user=request.user)
    # 총 가격을 계산합니다.
    total_price_all = sum(order.total_price for order in orders)
    return render(request, 'polls/confirm_order.html', {'orders': orders, 'total_price_all': total_price_all})

