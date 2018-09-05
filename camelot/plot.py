import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from .handlers import PDFHandler


def plot_geometry(filepath, pages='1', mesh=False, geometry_type='text', **kwargs):
    """

    Parameters
    ----------
    filepath
    pages
    mesh
    geometry_type
    kwargs
    """
    # explicit type conversion
    p = PDFHandler(filepath, pages)
    kwargs.update({'debug': geometry_type})
    __, geometry = p.parse(mesh=mesh, **kwargs)

    if geometry_type == 'text':
        for text in geometry.text:
            fig = plt.figure()
            ax = fig.add_subplot(111, aspect='equal')
            xs, ys = [], []
            for t in text:
                xs.extend([t[0], t[1]])
                ys.extend([t[2], t[3]])
                ax.add_patch(
                    patches.Rectangle(
                        (t[0], t[1]),
                        t[2] - t[0],
                        t[3] - t[1]
                    )
                )
            ax.set_xlim(min(xs) - 10, max(xs) + 10)
            ax.set_ylim(min(ys) - 10, max(ys) + 10)
            plt.show()
    elif geometry_type == 'contour':
        try:
            for img, table_bbox in geometry.images:
                for t in table_bbox.keys():
                    cv2.rectangle(img, (t[0], t[1]),
                                  (t[2], t[3]), (255, 0, 0), 3)
                plt.imshow(img)
                plt.show()
        except AttributeError:
            raise ValueError("This option can only be used with Lattice.")
    elif geometry_type == 'joint':
        try:
            for img, table_bbox in geometry.images:
                x_coord = []
                y_coord = []
                for k in table_bbox.keys():
                    for coord in table_bbox[k]:
                        x_coord.append(coord[0])
                        y_coord.append(coord[1])
                max_x, max_y = max(x_coord), max(y_coord)
                plt.plot(x_coord, y_coord, 'ro')
                plt.axis([0, max_x + 100, max_y + 100, 0])
                plt.imshow(img)
                plt.show()
        except AttributeError:
            raise ValueError("This option can only be used with Lattice.")
    elif geometry_type == 'line':
        try:
            for v_s, h_s in geometry.segments:
                for v in v_s:
                    plt.plot([v[0], v[2]], [v[1], v[3]])
                for h in h_s:
                    plt.plot([h[0], h[2]], [h[1], h[3]])
                plt.show()
        except AttributeError:
            raise ValueError("This option can only be used with Lattice.")
    elif geometry_type == 'table':
        try:
            for tables in geometry.tables:
                for table in tables:
                    for r in range(len(table.rows)):
                        for c in range(len(table.cols)):
                            if table.cells[r][c].left:
                                plt.plot([table.cells[r][c].lb[0],
                                          table.cells[r][c].lt[0]],
                                         [table.cells[r][c].lb[1],
                                          table.cells[r][c].lt[1]])
                            if table.cells[r][c].right:
                                plt.plot([table.cells[r][c].rb[0],
                                          table.cells[r][c].rt[0]],
                                         [table.cells[r][c].rb[1],
                                          table.cells[r][c].rt[1]])
                            if table.cells[r][c].top:
                                plt.plot([table.cells[r][c].lt[0],
                                          table.cells[r][c].rt[0]],
                                         [table.cells[r][c].lt[1],
                                          table.cells[r][c].rt[1]])
                            if table.cells[r][c].bottom:
                                plt.plot([table.cells[r][c].lb[0],
                                          table.cells[r][c].rb[0]],
                                         [table.cells[r][c].lb[1],
                                          table.cells[r][c].rb[1]])
                plt.show()
        except AttributeError:
            raise ValueError("This option can only be used with Lattice.")
    else:
        raise UserWarning("This method can only be called after"
            " debug has been specified.")