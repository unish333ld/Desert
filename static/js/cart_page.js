function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function updateQuantity(itemId, action) {
    fetch(`/cart/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: `action=${action}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.quantity === 0) {
                document.querySelector(`[data-item-id="${itemId}"]`).remove();
            } else {
                document.querySelector(`[data-item-id="${itemId}"] .quantity`).textContent = data.quantity;
                document.querySelector(`[data-item-id="${itemId}"] .item-total`).textContent = data.item_total + ' ₽';
            }
            document.getElementById('cart-total').textContent = data.cart_total + ' ₽';
            
            if (document.querySelectorAll('.cart-item').length === 0) {
                location.reload();
            }
        }
    });
}

function removeItem(itemId) {
    if (!confirm('Удалить товар из корзины?')) return;
    
    fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector(`[data-item-id="${itemId}"]`).remove();
            document.getElementById('cart-total').textContent = data.cart_total + ' ₽';
            
            if (document.querySelectorAll('.cart-item').length === 0) {
                location.reload();
            }
        }
    });
}
