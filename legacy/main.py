
from typing import Any, List, Optional, Union
import flet as ft
from flet_core.border import Border
from flet_core.charts.chart_axis import ChartAxis
from flet_core.charts.chart_grid_lines import ChartGridLines
from flet_core.charts.line_chart_data import LineChartData
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

from stock_data import get_stockData
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import mplcyberpunk
plt.style.use("dark_background")
matplotlib.use("svg")



tracker_style: dict = {
    "main":{
        #"expand": True,
        "bgcolor": "#17181d",
        "border_radius": 10,
        "width": 350, 
    },
    "title_symbol":{
        "size": 20,
        "color": "white54", 
        "weight": "bold"
    },
    "box_symbol":{
        "width": 200,
        "color": "teal600" ,

        
    }
}

class Symbol(ft.Container):
    def __init__(self) -> None:
        super().__init__(**tracker_style.get("main"))      

        self.title = ft.Text(value="Select a Symbol", 
                             **tracker_style.get("title_symbol"))
        
        self.default = "META"
        self.symbol_name = ft.TextField(label="Symbol", value=self.default,
                                        **tracker_style.get("box_symbol"))

        self.content = ft.Column(
            horizontal_alignment="center", 
            controls= [
                ft.Divider(height=15, color="transparent"),
                ft.Row(alignment="center", controls = [self.title]),
                ft.Row(alignment="center", controls = [self.symbol_name]),
                ft.Divider(height=15, color="transparent")
            ])
         



base_chart_style: dict ={
    "expand": True,
    "tooltip_bgcolor": ft.colors.with_opacity(0.8, ft.colors.WHITE),
    "left_axis": ft.ChartAxis(labels=50),
    "bottom_axis": ft.ChartAxis(labels_interval=1, labels_size=40),
    "horizontal_grid_lines": ft.ChartGridLines(
        interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
    ),
}



class BaseChart():
    def __init__(self, _nSymbol: str) -> None:
        super().__init__(**base_chart_style)
        self._nSymbol: str = _nSymbol

        self.start_date = "2022-01-01"
        self.end_date = "2023-01-01"  
       
        data = get_stockData(self._nSymbol, self.start_date, self.end_date)
        try:
            if data.empty:
                print(f"No hay datos para el símbolo {self._nSymbol} en el rango de fechas proporcionado.")
                return
        except Exception as e:
            print(f"Error al obtener datos para el símbolo {self._nSymbol}: {e}")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(data['Adj Close'], label=self._nSymbol)
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre Ajustado")
        plt.title(f"Gráfico de Acciones: {self._nSymbol}")
        plt.legend()
        mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)
        return MatplotlibChart(plt, expand=True)
        

        


graph_style: dict = {
    "expand": 1,
    "bgcolor": "#17181d",
    "border_radius": 10,
    "padding":30,
}

class Graph(ft.Container):
    def __init__(self, symbol_object = object) -> None:
        super().__init__(**graph_style)
        symbol_instance = symbol_object
        self.chart = BaseChart(_nSymbol=symbol_instance.symbol_name.value)
        self.content = self.chart




def main(page: ft.Page):
    page.padding = 30
    page.bgcolor = "#1f2128"
    
    # stock data
    symbol_block: ft.Container = Symbol()
    #graph: ft.Container = Graph(symbol_object = Symbol())
    
    classSymbol = "META"
    nameSymbol = Symbol().symbol_name.value


    start_date = "2022-01-01"
    end_date = "2023-01-01"  
    
    def makePlot(nameSymbol, start_date, end_date):
       data = get_stockData(nameSymbol, start_date, end_date)
       try:
        if data.empty:
            print(f"No hay datos para el símbolo {nameSymbol} en el rango de fechas proporcionado.")
            return
       except Exception as e:
            print(f"Error al obtener datos para el símbolo {nameSymbol}: {e}")
            return
       plt.figure(figsize=(10, 6))
       plt.plot(data['Adj Close'], label=nameSymbol)
       plt.xlabel("Fecha")
       plt.ylabel("Precio de Cierre Ajustado")
       plt.title(f"Gráfico de Acciones: {nameSymbol}")
       plt.legend()
       mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)
       return plt
       

    chart = makePlot(nameSymbol, start_date, end_date)
 

    

    # graph

    

    page.update()


    page.add(
        ft.Row(
            expand = True,
            controls = [symbol_block, MatplotlibChart(chart, expand=True)]
                )
            )
    

if __name__ == "__main__":
    ft.app(target=main)
#ft.app(target=main)
