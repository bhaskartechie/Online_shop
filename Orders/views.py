from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from Cart.cart import Cart
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import pdfkit
from django.template import loader

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('Payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


# @staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = loader.render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    path_wkhtmltopdf = r"C:\Users\Administrator\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    output = pdfkit.from_string(html, output_path=False, configuration=config, css=settings.STATIC_ROOT + 'css/pdf.css')
    response.write(output)
    # pdfkit.from_url(response, 'hi.pdf', configuration=config)
    # weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response

