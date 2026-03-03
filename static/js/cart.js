// Функция для получения CSRF токена
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

// Функция удаления товара из модального окна
window.removeItemModal = function(itemId) {
    fetch(`/cart/remove/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const item = document.querySelector(`#cart-modal-content [data-item-id="${itemId}"]`);
            if (item) item.remove();
            
            const totalEl = document.getElementById('modal-cart-total');
            if (totalEl) totalEl.textContent = data.cart_total + ' ₽';
            
            const items = document.querySelectorAll('#cart-modal-content .cart-item');
            if (items.length === 0) {
                document.getElementById('cart-modal-content').innerHTML = '<div class="text-center py-4"><p class="text-muted mb-0">Корзина пуста</p></div>';
            }
            
            updateCartCount();
        }
    });
};

// Загрузка корзины при открытии модального окна
document.getElementById('cartModal').addEventListener('show.bs.modal', function() {
    fetch('/cart/modal/')
        .then(response => response.text())
        .then(html => {
            document.getElementById('cart-modal-content').innerHTML = html;
        });
});

// Обновление счетчика корзины
function updateCartCount() {
    fetch('/cart/modal/')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const count = doc.querySelectorAll('.cart-item').length;
            document.getElementById('cart-count').textContent = count;
        });
}

// Обновляем счетчик при загрузке страницы
updateCartCount();
