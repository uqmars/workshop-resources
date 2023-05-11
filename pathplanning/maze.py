import numpy as np
import cv2 as cv
from collections import deque

def diagonal(n):
    for a in range(n):
        for b in range(a + 1):
            yield a - b, b
    for a in range(n - 1):
        for b in range(n - a - 1):
            yield n - b - 1, b + 1 + a

def get_neighbors(maze, node):
    neighbors = []
    row, col = node
    for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
        new_row, new_col = row+dx, col+dy
        if 0 <= new_row < maze.shape[0] and 0 <= new_col < maze.shape[1] and maze[new_row][new_col] != 0:
            neighbors.append((new_row, new_col))
    return neighbors

def dijkstra(img, maze, start):
    distances = np.ones_like(maze) * np.inf
    queue = deque([start])
    visited = set()
    path = {start: None}
    distances[start[0], start[1]] = 0.0
    while queue:
        current_node = queue.popleft()
        if current_node in visited:
            continue
        visited.add(current_node)
        hsv = np.array([[[int(distances[current_node[0], current_node[1]]) % 180, 255, 255]]], dtype=np.uint8)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        img[current_node[0], current_node[1]] = bgr[0, 0, :]
        img_resize = cv.resize(img, (800, 800), interpolation=cv.INTER_NEAREST)
        cv.imshow('maze', img_resize)
        cv.waitKey(1)
        for neighbor in get_neighbors(maze, current_node):
            if neighbor not in visited:
                distance = distances[current_node[0], current_node[1]] + np.sqrt((neighbor[0] - current_node[0]) ** 2 + (neighbor[1] - current_node[1]) ** 2)
                if distance < distances[neighbor[0], neighbor[1]]:
                    distances[neighbor[0], neighbor[1]] = distance
                    path[neighbor] = current_node
                    queue.append(neighbor)
    
    img_resize = cv.resize(img, (img.shape[0], img.shape[1]), interpolation=cv.INTER_NEAREST)
    cv.imshow('maze', img_resize)
    cv.waitKey()

import heapq

# Euclidean Heuristic
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def a_star(img, maze, start, end):
    distances = np.ones_like(maze) * np.inf
    queue = []
    visited = set()
    path = {start: None}
    distances[start[0], start[1]] = 0.0
    heapq.heappush(queue, (0, start))
    
    shortest_path = []
    while queue:
        _, current_node = heapq.heappop(queue)
        if current_node == end:
            break
        if current_node in visited:
            continue
        visited.add(current_node)
        
        hsv = np.array([[[int(distances[current_node[0], current_node[1]]) % 180, 255, 255]]], dtype=np.uint8)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        img[current_node[0], current_node[1]] = bgr[0, 0, :]
        img_resize = cv.resize(img, (800, 800), interpolation=cv.INTER_NEAREST)
        cv.imshow('maze', img_resize)
        cv.waitKey(1)
        
        for neighbor in get_neighbors(maze, current_node):
            if neighbor in visited:
                continue
            new_distance = distances[current_node[0], current_node[1]] + np.sqrt((neighbor[0] - current_node[0]) ** 2 + (neighbor[1] - current_node[1]) ** 2)
            if new_distance < distances[neighbor[0], neighbor[1]]:
                distances[neighbor[0], neighbor[1]] = new_distance
                priority = new_distance + heuristic(end, neighbor)
                heapq.heappush(queue, (priority, neighbor))
                path[neighbor] = current_node
    node = end
    path_list = [node]
    while node != start:
        node = path[node]
        path_list.append(node)
    path_list.reverse()
    return path_list


def main():
    maze = cv.imread('maze.png', cv.IMREAD_GRAYSCALE)
    img = cv.imread('maze.png', cv.IMREAD_COLOR)
    # Pick an non-obstructed starting point
    for r, c in diagonal(img.shape[0] * img.shape[1]):
        if maze[r, c] == 255:
            r0, c0 = r, c
            break
    # Pick an non-obstructed ending point
    for r, c in diagonal(img.shape[0] * img.shape[1]):
        if maze[img.shape[0] - 1 - r, img.shape[1] - 1 - c] == 255:
            r1, c1 = img.shape[0] - 1 - r, img.shape[1] - 1 - c
            break
    img[r0, c0, :] = np.array([120, 120, 255])
    start = (r0, c0)
    end = (r1, c1)
    img[r1, c1, :] = np.array([255, 120, 120])
    path_list = a_star(img, maze, start, end)
    for r, c in path_list:
        img[r, c, :] = np.array([80, 80, 255])
        img_resize = cv.resize(img, (800, 800), interpolation=cv.INTER_NEAREST)
        cv.imshow('maze', img_resize)
        cv.waitKey(1)
    cv.waitKey()


if __name__ == "__main__":
    main()
