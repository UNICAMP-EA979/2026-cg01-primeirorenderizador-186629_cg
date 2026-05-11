import numpy as np
import urenderer

# Cria uma cena com três objetos em cadeia:
#   scene -> objeto0 -> objeto1 -> objeto2
#
# As transformações são configuradas de forma que todos os objetos
# sejam visíveis simultaneamente na primeira renderização.
# Em seguida, o nó avô (objeto0) é rotacionado e a cena é renderizada
# novamente — os filhos se movem junto com ele, demonstrando o scene graph.

if __name__ == "__main__":
    urenderer.utils.clear_workdir("03-grandchild")
    renderer = urenderer.renderer.PyplotRenderer(1920, 1080)
    runtime = urenderer.application.Runtime(renderer, name="03-grandchild")

    """
    Raciocínio:
        Montamos a hierarquia objeto0 -> objeto1 -> objeto2 via add_child.
        A transformação acumulada de cada nó é calculada pelo runtime como:
            T_mundo = T_avo @ T_pai @ T_local
        Portanto posicionamos objeto0 no centro da cena e deslocamos os filhos
        relativamente ao seu pai, mantendo todos dentro do frustum da câmera.

        Na segunda renderização apenas rotacionamos objeto0; como objeto1 e
        objeto2 são seus descendentes, eles acompanham o movimento, ilustrando
        a propagação de transformações no scene graph.
    """

    # --- Nó avô (objeto0) ---
    objeto0 = urenderer.node.Node("objeto0")
    objeto0.translation = np.array([0, 0, -7], np.float64)
    objeto0.rotation = np.array([20, 30, 0], np.float64)
    objeto0.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()

    # --- Nó pai (objeto1) — filho de objeto0 ---
    objeto1 = urenderer.node.Node("objeto1")
    objeto1.translation = np.array([2.5, 0, 0], np.float64)   # deslocado à direita do avô
    objeto1.rotation = np.array([0, 45, 0], np.float64)
    objeto1.scale = np.array([0.7, 0.7, 0.7], np.float64)
    objeto1.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()

    # --- Nó filho (objeto2) — filho de objeto1 ---
    objeto2 = urenderer.node.Node("objeto2")
    objeto2.translation = np.array([2.0, 0, 0], np.float64)   # deslocado à direita do pai
    objeto2.rotation = np.array([0, 0, 45], np.float64)
    objeto2.scale = np.array([0.6, 0.6, 0.6], np.float64)
    objeto2.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()

    # Monta a hierarquia: scene -> objeto0 -> objeto1 -> objeto2
    objeto1.add_child(objeto2)
    objeto0.add_child(objeto1)
    runtime.scene.add_child(objeto0)

    # Primeira renderização: todos os objetos nas posições originais
    runtime.iter(capture=True)

    """
    Raciocínio da segunda renderização:
        Rotacionamos apenas objeto0 (o avô). Como objeto1 e objeto2 herdam
        sua transformação, eles giram junto com ele — demonstrando que alterar
        um nó ancestral afeta toda a subárvore abaixo dele.
    """

    # Rotaciona o nó avô e renderiza novamente
    objeto0.rotation = np.array([20, 130, 0], np.float64)

    runtime.iter(capture=True)
