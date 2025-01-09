async function loadProjects() {
  try {
    const response = await fetch('/api/proj/list');
    if (!response.ok) {
      throw new Error(`Failed to fetch projects: ${response.statusText}`);
    }

    const projects = await response.json();
    const projectsList = document.getElementById('projects');

    projects.forEach(project => {
      const listItem = document.createElement('li');
      listItem.textContent = project.projname;
      listItem.dataset.projectName = project.projname;
      listItem.onclick = () => loadModels(project.projname);

      projectsList.appendChild(listItem);
    });
  } catch (error) {
    console.error('Error loading projects:', error);
    const projectsList = document.getElementById('projects');
    projectsList.innerHTML = '<p style="color: red;">Failed to load projects.</p>';
  }
}

async function loadModels(projectName) {
  try {
    const response = await fetch(`/api/proj/?proj_name=${projectName}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch models for project ${projectName}: ${response.statusText}`);
    }

    const models = await response.json();
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = ''; // Очистка галереи перед загрузкой новых моделей

    models.forEach(model => {
      const item = document.createElement('div');
      item.className = 'gallery-item';

      const img = document.createElement('img');
      img.src = `/uploaded_files/${model.picture_path.replace('uploaded_files/', '')}`;
      img.alt = model.filename;

      const title = document.createElement('h3');
      title.textContent = model.filename;

      const description = document.createElement('p');
      description.textContent = model.description;

      const date = document.createElement('p');
      date.textContent = `Uploaded: ${new Date(model.date_upload).toLocaleDateString()}`;

      item.onclick = () => {
        window.location.href = `/static/model-viewer.html?model_id=${model.file_id}`;
      };

      item.appendChild(img);
      item.appendChild(title);
      item.appendChild(description);
      item.appendChild(date);

      gallery.appendChild(item);
    });
  } catch (error) {
    console.error('Error loading models:', error);
    const gallery = document.getElementById('gallery');
    gallery.innerHTML = '<p style="color: red;">Failed to load models.</p>';
  }
}

loadProjects();
