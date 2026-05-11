import numpy as np
import urenderer
from urenderer.node import Node

# Crie uma cena com animação
#
# Observe o método urenderer.application.runtime.Runtime::iter
# A iteração da aplicação consiste em 2 etapas:
#  - update: executa códigos da aplicação
#  - render: renderiza a cena
#
# O update funciona a partir de callbacks: cada nó pode possuir uma ou mais funções de callback
# que são executadas no update.
#
# Vamos utilizar o update para criar uma animação simples.
# Crie uma cena simples e utilize funções como a "animate_over_time" para animar objetos
#


def animate_over_time(node: Node, deltaTime: float, time_since_start: float) -> None:
    """
    Anima um nó

    Args:
        node (Node): nó a ser animado
        deltaTime (float): tempo desde o último update
        time_since_start (float): tempo desde o começo da aplicação
    """
    node.rotation[1] = 360*np.sin(time_since_start)


if __name__ == "__main__":
    urenderer.utils.clear_workdir("05-animation")
    renderer = urenderer.renderer.PyplotRenderer(1920, 1080, show=False)
    runtime = urenderer.application.Runtime(renderer, name="05-animation")

    node = urenderer.node.Node()
    node.callbacks.append(animate_over_time)

    # Crie a cena

    runtime.loop(n=10, capture=True)

    urenderer.utils.image_to_video("05-animation")
