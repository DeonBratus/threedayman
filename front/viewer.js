const modelId = new URLSearchParams(window.location.search).get('model_id');
if (!modelId) {
    alert('Model ID is missing in the URL!');
    throw new Error('Model ID is missing in the URL');
}

const viewer = document.getElementById('viewer');
const modelTitle = document.getElementById('model-title');
const uploadDate = document.getElementById('upload-date');
const fileType = document.getElementById('file-type');
const fileSize = document.getElementById('file-size');
const modelDescription = document.getElementById('model-description');
const downloadButton = document.getElementById('download-button');

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x2a2a2a);

const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
camera.position.set(0, 50, 100);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(viewer.offsetWidth, viewer.offsetHeight);
viewer.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);

const gridHelper = new THREE.GridHelper(200, 50, 0x555555, 0x333333);
scene.add(gridHelper);

const loader = new THREE.STLLoader();
loader.load(`/api/tdim/model_viewer?model_id=${modelId}`, (geometry) => {
    const material = new THREE.MeshLambertMaterial({ color: 0x2255aa });
    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    geometry.computeBoundingBox();
    const centerX = (geometry.boundingBox.max.x + geometry.boundingBox.min.x) / 2;
    const centerY = (geometry.boundingBox.max.y + geometry.boundingBox.min.y) / 2;
    const centerZ = (geometry.boundingBox.max.z + geometry.boundingBox.min.z) / 2;

    mesh.position.set(-centerX, -centerY, -centerZ);

    controls.update();
});

const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(1, 1, 1).normalize();
scene.add(light);

const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    renderer.setSize(viewer.offsetWidth, viewer.offsetHeight);
});

fetch(`/api/tdim/model_viewer/info?model_id=${modelId}`)
    .then(response => response.json())
    .then(data => {
        modelTitle.textContent = data.Filename || '3D Model Viewer';
        uploadDate.textContent = `Uploaded Date: ${data.Uploaded_date || 'N/A'}`;
        fileType.textContent = `Type: ${data.Format || 'N/A'}`;
        fileSize.textContent = `Size: ${data.Size || 'N/A'} KB`;
        modelDescription.textContent = data.Description || 'Description not available.';

        // Настройка кнопки скачивания
        downloadButton.addEventListener('click', () => {
            const link = document.createElement('a');
            link.href = `/api/tdim/model_viewer?model_id=${modelId}`;
            link.download = `${data.Filename}.stl` || 'model.stl';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    })
    .catch(error => {
        console.error('Error fetching model info:', error);
        modelDescription.textContent = 'Failed to load model information.';
    });
