const baseUrl = '/yak-shop'

function getDay() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const day = parseInt(urlParams.get('day'));
    return !Number.isNaN(day) && day > 0 ? day : 0
}

async function loadHerd() {
    const day = getDay()
    const response = await fetch(`${baseUrl}/herd/${day}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json();
    const herdTable = document.getElementById('herdTable');

    let rows = '';

    const herd = myJson.herd;
    herd.forEach(labyak => {
        rows += `<tr><td>${labyak.name}</td><td>${labyak.age}</td><td>${labyak['age-last-shaved']}</td></tr>`;
    })
    herdTable.innerHTML = rows;
}

async function loadStock() {
    const day = getDay()
    const response = await fetch(`${baseUrl}/stock/${day}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const myJson = await response.json();
    const milkCell = document.getElementById('milkCell');
    const skinsCell = document.getElementById('skinsCell');

    milkCell.innerText = myJson.milk;
    skinsCell.innerText = myJson.skins;
}

function updateDayBanner() {
    const day = getDay();
    const day_banner = document.getElementById('day_banner');
    day_banner.innerText = 'Day: ' + day
}

function updateDayNavigation() {
    const day = getDay();
    if (day > 0) {
        const prev_day_button = document.getElementById('prev_day_button');
        const next_day_button = document.getElementById('next_day_button');
        prev_day_button.href = '/overview?day=' + (day - 1)
        next_day_button.href = '/overview?day=' + (day + 1)
    }
}

async function placeOrder() {
    const day = getDay();
    const customer = document.getElementById('customer').value;
    const milk = parseFloat(document.getElementById('milk').value);
    const skins = parseInt(document.getElementById('skins').value);
    const messageBox = document.getElementById('messageBox');
    const body = {
        customer,
        order: {
            milk,
            skins,
        }
    };
    console.log(body);
    messageBox.innerHTML = '';
    const response = await fetch(`${baseUrl}/order/${day}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    const responseBody = await response.text();
    switch (response.status) {
        case 201:
            messageBox.innerHTML = `<div class="message success">Order successfully placed</div>`
            break;
        case 206:
            messageBox.innerHTML = `<div class="message partialSuccess">Order partially placed</div>`
            break;
        case 400:
            messageBox.innerHTML = `<div class="message error">Invalid input:<br>${responseBody}</div>`
            break;
        case 404:
            messageBox.innerHTML = `<div class="message error">Not enough stock</div>`
            break;
        default:
            messageBox.innerHTML = `<div class="message error">Something is totaly broken<br>${responseBody}</div>`
    }
    // fire and forget
    loadStock();
    loadOrders();
    return false;
}

async function loadOrders() {
    const day = getDay()
    const response = await fetch(`${baseUrl}/order/${day}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const orders = await response.json();
    const orderTable = document.getElementById('orderTable');

    if (orders.length > 0) {
        let rows = '';

        orders.forEach(order => {
            rows += `<tr>` +
                `<td>${order.customer}</td>` +
                `<td>${order.requested.milk}</td>` +
                `<td>${order.requested.skins}</td>` +
                `<td>${order.allocated.milk}</td>` +
                `<td>${order.allocated.skins}</td>` +
                `<td>${order.status}</td>` +
                `</tr>`;
        })
        orderTable.innerHTML = rows;
    }
}

window.onload = function () {
    updateDayBanner();
    updateDayNavigation();
    loadStock();
    loadHerd();
    loadOrders();
}