document.addEventListener('DOMContentLoaded', () => {
  const printerGallery = document.getElementById('printer-gallery');
  const apiUrl = 'http://192.168.31.66:8001/api/printers/';

  const openFormBtn = document.getElementById('open-form-btn');
  const closeFormBtn = document.getElementById('close-form-btn');
  const formContainer = document.getElementById('printer-form-container');
  const printerForm = document.getElementById('printer-form');

  // Функция для создания карточки принтера
  function createPrinterCard(name, address) {
    const card = document.createElement('div');
    card.className = 'gallery-item';

    card.innerHTML = `
      <h3>${name}</h3>
      <p>${address}</p>
      <a href="http://${address}" target="_blank" class="printer-link">Go to Printer</a>
    `;

    return card;
  }

  // Загрузка данных с API
  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      Object.keys(data).forEach(cluster => {
        Object.entries(data[cluster]).forEach(([address, name]) => {
          const printerCard = createPrinterCard(name, address);
          printerGallery.appendChild(printerCard);
        });
      });
    })
    .catch(error => {
      console.error('Ошибка загрузки данных о принтерах:', error);
      printerGallery.innerHTML = '<p>Не удалось загрузить данные о принтерах.</p>';
    });

  // Открытие формы
  openFormBtn.addEventListener('click', () => {
    formContainer.style.display = 'flex';
  });

  // Закрытие формы
  closeFormBtn.addEventListener('click', () => {
    formContainer.style.display = 'none';
  });

  // Обработка отправки формы
  printerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const priner_name = document.getElementById('name').value;
    const addr = document.getElementById('addr').value;
    const clustername = document.getElementById('clustername').value;

    const data = {
      name: priner_name,
      addr: addr,
      clustername: clustername,
    };

    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const data = await response.json(); // получение ответа от сервера
      console.log('Принтер добавлен:', data);

      // Закрываем форму и обновляем список принтеров
      formContainer.style.display = 'none';
      // Добавляем новую карточку принтера
      const printerCard = createPrinterCard(priner_name, addr);
      printerGallery.appendChild(printerCard);

      // Сообщение об успешном добавлении
      document.getElementById('responseMessage').textContent = `Printer "${priner_name}" added successfully!`;
      document.getElementById('responseMessage').style.color = 'green';
    } else {
      const error = await response.json();
      document.getElementById('responseMessage').textContent = `Error: ${error.detail || 'Something went wrong'}`;
      document.getElementById('responseMessage').style.color = 'red';
    }
  });
});