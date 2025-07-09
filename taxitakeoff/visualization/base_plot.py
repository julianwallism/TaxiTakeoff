from abc import ABC, abstractmethod
import os
from typing import Optional
import matplotlib.pyplot as plt

from ..data.models import CleanedFlightData


class BasePlot(ABC):
    """Abstract base class for all flight data visualizations"""
    
    def __init__(self, output_dir: str = "output/plots"):
        self.output_dir = output_dir
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    @property
    @abstractmethod
    def plot_name(self) -> str:
        """Name of the plot (used for filename)"""
        pass
    
    @property
    @abstractmethod
    def plot_title(self) -> str:
        """Title of the plot"""
        pass
    
    @abstractmethod
    def _generate_plot(self, data: CleanedFlightData) -> None:
        """Generate the actual plot - implemented by subclasses"""
        pass
    
    def generate(self, data: CleanedFlightData) -> str:
        """Generate the plot and return the filepath"""
        plt.figure(figsize=(10, 5))
        
        self._generate_plot(data)
        
        plt.title(self.plot_title)
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, f"{self.plot_name}.png")
        plt.savefig(filepath)
        plt.close()
        
        return filepath
    
    def get_metadata(self) -> dict:
        """Get metadata about this plot"""
        return {
            "name": self.plot_name,
            "title": self.plot_title,
            "type": self.__class__.__name__
        }