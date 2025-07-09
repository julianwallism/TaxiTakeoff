from typing import List, Type

from .base_plot import BasePlot
from .time_plots import (
    DailyDeparturePlot,
    HourlyDeparturePlot,
    FifteenMinuteDeparturePlot,
    WeeklyDeparturePlot
)


class PlotRegistry:
    """Registry for managing available plots"""
    
    def __init__(self):
        self._plots: List[Type[BasePlot]] = [
            DailyDeparturePlot,
            HourlyDeparturePlot,
            FifteenMinuteDeparturePlot,
            WeeklyDeparturePlot
        ]
    
    def register_plot(self, plot_class: Type[BasePlot]) -> None:
        """Register a new plot class"""
        if plot_class not in self._plots:
            self._plots.append(plot_class)
    
    def get_all_plots(self) -> List[Type[BasePlot]]:
        """Get all registered plot classes"""
        return self._plots.copy()
    
    def get_plot_by_name(self, name: str) -> Type[BasePlot]:
        """Get a plot class by its name"""
        for plot_class in self._plots:
            if plot_class().plot_name == name:
                return plot_class
        raise ValueError(f"Plot with name '{name}' not found")
    
    def get_available_plot_names(self) -> List[str]:
        """Get names of all available plots"""
        return [plot_class().plot_name for plot_class in self._plots]
    
    def create_all_plots(self, output_dir: str = "output/plots") -> List[BasePlot]:
        """Create instances of all registered plots"""
        return [plot_class(output_dir) for plot_class in self._plots]


# Global registry instance
plot_registry = PlotRegistry()