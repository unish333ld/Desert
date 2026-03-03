from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, Review


@login_required
def add_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if Review.objects.filter(order=order).exists():
        return redirect('profile')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            order=order,
            user=request.user,
            rating=rating,
            comment=comment
        )
        return redirect('profile')
    
    return render(request, 'reviews/add_review.html', {'order': order})
