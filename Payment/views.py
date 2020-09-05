import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from Orders.models import Order

# Create your views here.
# instantiate braintree gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        result = gateway.transaction.sale({'amount': f'{total_cost}',
                                           'payment_method_nonce': nonce,
                                           'options': {'submit_for_settlement': True}})
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('Payment:done')
        else:
            return redirect('Payment:canceled')
    else:
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_cancelled(request):
    return render(request, 'payment/canceled.html')
