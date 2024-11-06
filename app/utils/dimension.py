def normalize_to_pixel_coords(normalized_vertices, page_width, page_height):
    pixel_vertices = []
    print("hoit")
    for vertex in normalized_vertices.vertices:
        pixel_x = vertex["x"] * page_width
        pixel_y = vertex["y"] * page_height
        pixel_vertices.append((pixel_x, pixel_y))
    return pixel_vertices
