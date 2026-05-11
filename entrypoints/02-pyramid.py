import numpy as np
import urenderer

# Cria uma cena com uma pirâmide e renderiza ela utilizando o PyplotRenderer
#
# A geometria da pirâmide é obtida via get_ifs_pyramid, que define uma pirâmide
# de base triangular com 4 vértices e 4 faces.

if __name__ == "__main__":
    urenderer.utils.clear_workdir("02-pyramid")
    renderer = urenderer.renderer.PyplotRenderer(1920, 1080)
    runtime = urenderer.application.Runtime(renderer, name="02-pyramid")

    """
    Raciocínio:
        Criamos um nó para a pirâmide, configuramos sua posição no mundo
        (translação em Z negativo para ficar à frente da câmera) e aplicamos
        uma rotação para que a geometria fique visível de forma interessante.
        Em seguida adicionamos o nó como filho da cena e renderizamos.
    """

    pyramid = urenderer.node.Node("pyramid")

    pyramid.translation = np.array([0, 0, -5], np.float64)
    pyramid.rotation = np.array([20, 45, 0], np.float64)
    pyramid.scale = np.array([2, 2, 2], np.float64)
    pyramid.render_data = urenderer.geometry.polygonal_ifs.get_ifs_pyramid()

    runtime.scene.add_child(pyramid)

    runtime.iter(capture=True)
