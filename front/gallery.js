async function loadGallery() {
  try {
    const response = await fetch('/api/tdim/gallery');
    if (!response.ok) {
      throw new Error(`Failed to fetch gallery info: ${response.statusText}`);
    }

    const galleryData = await response.json();
    const gallery = document.getElementById('gallery');

    galleryData.forEach(file => {
      const item = document.createElement('div');
      item.className = 'gallery-item';

      const img = document.createElement('img');
      img.src = `/uploaded_files/${file.picture_path.replace('uploaded_files/', '')}`;
      img.alt = file.filename;

      const title = document.createElement('h3');
      title.textContent = file.filename;

      const date = document.createElement('p');
      date.textContent = `Uploaded: ${new Date(file.date_upload).toLocaleDateString()}`;

      // Добавление события клика для перехода на страницу просмотра модели
      item.onclick = () => {
        window.location.href = `/static/model-viewer.html?model_id=${file.file_id}`;
      };

      item.appendChild(img);
      item.appendChild(title);
      item.appendChild(date);

      gallery.appendChild(item);
    });
  } catch (error) {
    console.error('Error loading gallery:', error);
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = '<p style="color: red;">Failed to load gallery.</p>';
  }
}

loadGallery();
