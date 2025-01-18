document.getElementById('createProjectForm').addEventListener('submit', async function (e) {
    e.preventDefault();
  
    const projname = document.getElementById('projname').value;
    const pic = document.getElementById('pic').files[0];
  
    if (!projname || !pic) {
      alert("Please provide both project name and image.");
      return;
    }
  
    const formData = new FormData();
    formData.append('projname', projname);
    formData.append('pic', pic);
    const url = `/api/proj/?projname=${encodeURIComponent(projname)}`;
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData, // отправляем форму с данными
      });
  
      if (response.ok) {
        const result = await response.json(); // получение ответа от сервера
        document.getElementById('responseMessage').textContent = `Project "${projname}" created successfully!`;
        document.getElementById('responseMessage').style.color = 'green';
      } else {
        const error = await response.json();
        document.getElementById('responseMessage').textContent = `Error: ${error.detail || 'Something went wrong'}`;
        document.getElementById('responseMessage').style.color = 'red';
      }
    } catch (error) {
      document.getElementById('responseMessage').textContent = `Error: ${error.message}`;
      document.getElementById('responseMessage').style.color = 'red';
    }
  });
  