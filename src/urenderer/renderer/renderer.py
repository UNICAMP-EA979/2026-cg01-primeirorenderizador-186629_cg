import abc

import numpy as np
from urenderer.node import Camera, Node


class Renderer(abc.ABC):
    """
    Abstract class for renderers.

    It receives the elements of the scene and renders them.
    """

    def __init__(self, screen_width: float, screen_height: float) -> None:
        """
        Renderer initializer

        Args:
            screen_width (float): screen width
            screen_height (float): screen height
        """
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height

    @abc.abstractmethod
    def start(self, camera: Camera, view_matrix: np.ndarray, name: str) -> None:
        """
        Start the frame rendering

        Args:
            camera (Camera): current camera.
            view_matrix (np.ndarray): camera view matrix.
            name (str): name of the application
        """
        ...

    @abc.abstractmethod
    def validate(self, node: Node) -> bool:
        """
        Validate a node for rendering.

        Check if the node is compatible to be rendered with this renderer.

        Args:
            node (Node): node to validate.

        Returns:
            bool: True if the node is valid
        """
        ...

    def render(self, node: Node, model_transformation: np.ndarray) -> None:
        """
        Render a node, if valid

        Args:
            node (Node): node to render
            model_transformation (np.ndarray): node model transformation in the scene
        """
        if self.validate(node):
            self.render_valid_node(node, model_transformation)

    @abc.abstractmethod
    def render_valid_node(self, node: Node, model_transformation: np.ndarray) -> None:
        """
        Renders a validated node

        Args:
            node (Node): node to render
            model_transformation (np.ndarray): node model transformation in the scene
        """
        ...

    @abc.abstractmethod
    def end(self, capture: bool = False) -> None:
        """
        Ends the frame rendering

        Args:
            capture (bool, optional): if should save the current frame. Defaults to False.
        """
        ...
