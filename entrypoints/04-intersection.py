import numpy as np
import urenderer

# Renderiza uma cena em que o algoritmo do pintor (painter's algorithm) falha
#
# O algoritmo do pintor ordena os triângulos pela profundidade média (Z) e os
# desenha do mais distante ao mais próximo. Ele falha quando dois objetos se
# intersectam, pois não existe uma ordenação global válida: parte do objeto A
# está à frente do objeto B e parte está atrás, simultaneamente.
#
# Nesta cena colocamos dois cubos que se intersectam levemente ao longo do eixo Z.
# Visualmente, o algoritmo pintará um cubo inteiro por cima do outro, produzindo
# uma oclusão incorreta em pelo menos uma das metades da interseção.

if __name__ == "__main__":
    urenderer.utils.clear_workdir("04-intersection")
    renderer = urenderer.renderer.PyplotRenderer(1920, 1080)
    runtime = urenderer.application.Runtime(renderer, name="04-intersection")

    """
    Raciocínio:
        Para expor a falha do algoritmo do pintor escolhemos dois cubos que se
        cruzam mutuamente:

        - cubo_a está ligeiramente à esquerda e mais ao fundo (Z mais negativo),
          mas sua metade frontal penetra no volume ocupado por cubo_b.
        - cubo_b está ligeiramente à direita e mais à frente, mas sua metade
          traseira penetra no volume de cubo_a.

        Como a profundidade média de cada cubo está próxima, o algoritmo escolhe
        uma ordem de pintura fixa (ex.: cubo_a por cima de cubo_b) que é errada
        em pelo menos uma região da tela. Isso produz artefatos visuais claros:
        um cubo parece "passar na frente" do outro mesmo onde deveria estar atrás.

        Rotacionamos ambos em 45° para que as faces fiquem visíveis e o artefato
        seja mais perceptível.
    """

    # Cubo A — levemente mais ao fundo, deslocado à esquerda
    cubo_a = urenderer.node.Node("cubo_a")
    cubo_a.translation = np.array([-0.6, 0, -5.0], np.float64)
    cubo_a.rotation = np.array([20, 45, 0], np.float64)
    cubo_a.scale = np.array([2, 2, 2], np.float64)
    cubo_a.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()

    # Cubo B — levemente mais à frente, deslocado à direita
    # A sobreposição em X e Z faz os dois cubos se intersectarem
    cubo_b = urenderer.node.Node("cubo_b")
    cubo_b.translation = np.array([0.6, 0, -4.4], np.float64)
    cubo_b.rotation = np.array([20, 45, 0], np.float64)
    cubo_b.scale = np.array([2, 2, 2], np.float64)
    cubo_b.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()

    runtime.scene.add_child(cubo_a)
    runtime.scene.add_child(cubo_b)

    runtime.iter(capture=True)
