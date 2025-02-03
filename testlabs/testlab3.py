import trimesh
import numpy as np
import pyvista as pv
from scipy.spatial import cKDTree

# Загрузка STL-моделей
mesh_old = trimesh.load('korito_final.stl')
mesh_new = trimesh.load('korito_v5252.stl')

if not mesh_old.is_watertight:
    raise ValueError("Старая модель должна быть водонепроницаемой (watertight) для корректного анализа.")

# Задаем порог для определения изменений
threshold = 0.01

# --- Определение новых вершин ---
tree_old = cKDTree(mesh_old.vertices)
dist_new, _ = tree_old.query(mesh_new.vertices)
added_indices = np.where(dist_new > threshold)[0]  # Индексы новых вершин
added_vertices = mesh_new.vertices[added_indices]  # Массив новых вершин

# --- Определение новых вершин внутри старой модели (вырезы) ---
inside_indices = []
outside_indices = []

for i, vertex in enumerate(added_vertices):
    if mesh_old.contains([vertex])[0]:  # Если вершина внутри старой модели
        inside_indices.append(i)
    else:
        outside_indices.append(i)  # Если вершина снаружи старой модели

# Подсвечиваем новые вершины внутри и вне старой модели
inside_points = added_vertices[inside_indices]
outside_points = added_vertices[outside_indices]

# --- Определение граней, которые должны быть подсвечены ---
cut_faces = []       # Вырезы (грани внутри старой модели) → красный
extruded_faces = []  # Экструзии (новые выступающие грани) → зеленый

for face in mesh_new.faces:
    face_vertices = set(face)  # Индексы вершин текущей грани

    # Если хотя бы одна вершина из новой модели внутри старой модели
    if any(v in inside_indices for v in face_vertices):
        cut_faces.append(face)  # Грань будет красной (вырез)

    # Если ВСЕ вершины новые → это экструдированная часть (вне модели)
    elif face_vertices.issubset(added_indices):
        extruded_faces.append(face)  # Грань будет зеленой (экструзия)

cut_faces = np.array(cut_faces) if cut_faces else np.empty((0, 3), dtype=int)
extruded_faces = np.array(extruded_faces) if extruded_faces else np.empty((0, 3), dtype=int)

# --- Создаем PolyData для вырезов (красный) ---
if cut_faces.size > 0:
    faces_cut = np.hstack([np.full((cut_faces.shape[0], 1), 3), cut_faces]).astype(np.int64)
    cut_mesh = pv.PolyData(mesh_new.vertices, faces_cut)
else:
    cut_mesh = None

# --- Создаем PolyData для экструзий (зеленый) ---
if extruded_faces.size > 0:
    faces_extruded = np.hstack([np.full((extruded_faces.shape[0], 1), 3), extruded_faces]).astype(np.int64)
    extruded_mesh = pv.PolyData(mesh_new.vertices, faces_extruded)
else:
    extruded_mesh = None

# --- Визуализация ---
plotter = pv.Plotter()

# Подсвечиваем саму модель для контекста
faces_new = np.hstack([np.full((mesh_new.faces.shape[0], 1), 3), mesh_new.faces]).astype(np.int64)
pv_mesh_new = pv.PolyData(mesh_new.vertices, faces_new)
plotter.add_mesh(pv_mesh_new, color='white', opacity=0.5, show_edges=True)

# Подсвечиваем вырезы (красный)
if cut_mesh:
    plotter.add_mesh(cut_mesh, color='red', opacity=0.8, show_edges=True, label='Вырезы')

# Подсвечиваем экструзии (зеленый)
if extruded_mesh:
    plotter.add_mesh(extruded_mesh, color='green', opacity=0.8, show_edges=True, label='Добавленные элементы (экструзия)')

plotter.add_legend()
plotter.show()
