// Sample product data (replace with real API fetch later)
const products = [
    { id: 1, name: 'Organic Compost', price: 20, desc: 'Natural soil enhancer', img: 'https://via.placeholder.com/200x150/4CAF50/FFFFFF?text=Compost' },
    { id: 2, name: 'Nitrogen Fertilizer', price: 15, desc: 'Boosts plant growth', img: 'https://via.placeholder.com/200x150/2196F3/FFFFFF?text=Nitrogen' },
    { id: 3, name: 'Phosphate Mix', price: 25, desc: 'For root development', img: 'https://via.placeholder.com/200x150/FF9800/FFFFFF?text=Phosphate' },
    { id: 4, name: 'Potash Booster', price: 18, desc: 'Improves crop yield', img: 'https://via.placeholder.com/200x150/9C27B0/FFFFFF?text=Potash' },
];

let cart = [];

// Render products
function renderProducts(filtered = products) {
    const productGrid = document.getElementById('products');
    productGrid.innerHTML = '';
    filtered.forEach(product => {
        const div = document.createElement('div');
        div.className = 'product';
        div.innerHTML = `
            <img src="${product.img}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.desc}</p>
            <p>$${product.price}</p>
            <button onclick="addToCart(${product.id})">Add to Cart</button>
        `;
        productGrid.appendChild(div);
    });
}

// Filter products by search
function filterProducts() {
    const query = document.getElementById('search').value.toLowerCase();
    const filtered = products.filter(p => 
        p.name.toLowerCase().includes(query) || p.desc.toLowerCase().includes(query)
    );
    renderProducts(filtered);
}

// Add to cart
function addToCart(id) {
    const product = products.find(p => p.id === id);
    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    updateCart();
    alert(`${product.name} added to cart!`); // Optional feedback
}

// Update cart display
function updateCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    let total = 0;
    cart.forEach(item => {
        total += item.price * item.quantity;
        const li = document.createElement('li');
        li.innerHTML = `
            ${item.name} x${item.quantity} - $${item.price * item.quantity} 
            <button onclick="removeFromCart(${item.id})">Remove</button>
        `;
        cartItems.appendChild(li);
    });
    document.getElementById('total').textContent = total.toFixed(2);
    document.getElementById('cart-count').textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
}

// Remove from cart
function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    updateCart();
}

// Show/hide sections
function showSection(sectionId) {
    document.querySelectorAll('section').forEach(sec => {
        sec.classList.add('hidden');
        sec.classList.remove('active');
    });
    document.getElementById(sectionId).classList.remove('hidden');
    document.getElementById(sectionId).classList.add('active');
}

// Checkout
function checkout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    document.getElementById('checkout-modal').classList.remove('hidden');
}

// Close modal
function closeModal() {
    document.getElementById('checkout-modal').classList.add('hidden');
    document.getElementById('checkout-form').reset();
}

// Handle form submit (simulate order)
document.getElementById('checkout-form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Order placed successfully! Thank you for your purchase.');
    cart = [];
    updateCart();
    closeModal();
    showSection('home');
});

// Initial render
renderProducts();