const accounts = [
    {
        name: 'Cuenta A',
        number: '1234567890',
        type: 'Ahorro',
        color: '#4CAF50',
        initialBalance: '$1000',
        currentBalance: '$1500',
        bank: 'Banco A',
        affiliation: 'Afiliación A',
        logo: 'path/to/logoA.png'
    },
    {
        name: 'Cuenta B',
        number: '0987654321',
        type: 'Corriente',
        color: '#FF5722',
        initialBalance: '$2000',
        currentBalance: '$2500',
        bank: 'Banco B',
        affiliation: 'Afiliación B',
        logo: 'path/to/logoB.png'
    }
];

const accountMenu = document.getElementById('account-menu');
const accountCarousel = document.getElementById('account-carousel');

accounts.forEach((account, index) => {
    const menuItem = document.createElement('li');
    menuItem.innerHTML = `
        ${account.name}
        <img src="${account.logo}" class="rotating-logo" alt="Logo">
    `;
    menuItem.dataset.index = index;
    menuItem.style.backgroundColor = account.color;
    accountMenu.appendChild(menuItem);

    const card = document.createElement('div');
    card.classList.add('card');
    card.innerHTML = `
        <div class="card-header">
            <h2>${account.name}</h2>
            <img src="${account.logo}" class="rotating-logo card-logo" alt="Logo">
        </div>
        <p>Número de cuenta: ${account.number}</p>
        <p>Tipo de cuenta: ${account.type}</p>
        <p style="color: ${account.color};">Color de identificación</p>
        <p>Saldo inicial: ${account.initialBalance}</p>
        <p>Saldo actual: ${account.currentBalance}</p>
        <p>Banco: ${account.bank}</p>
        <p>Afiliación: ${account.affiliation}</p>
    `;
    card.style.backgroundColor = account.color;
    accountCarousel.appendChild(card);
});

let currentIndex = 0;

function showCard(index) {
    const cards = document.querySelectorAll('.carousel .card');
    const menuItems = document.querySelectorAll('#account-menu li');
    cards.forEach((card, i) => {
        card.style.display = (i === index) ? 'block' : 'none';
    });
    menuItems.forEach((item, i) => {
        item.classList.toggle('active', i === index);
    });
}

document.querySelector('.nav-btn.prev').addEventListener('click', () => {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : accounts.length - 1;
    showCard(currentIndex);
});

document.querySelector('.nav-btn.next').addEventListener('click', () => {
    currentIndex = (currentIndex < accounts.length - 1) ? currentIndex + 1 : 0;
    showCard(currentIndex);
});

accountMenu.addEventListener('click', (e) => {
    if (e.target.tagName === 'LI' || e.target.tagName === 'IMG') {
        currentIndex = parseInt(e.target.closest('li').dataset.index);
        showCard(currentIndex);
    }
});

showCard(currentIndex);
