
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
import time

base_chart_style: dict ={
    "expand": True,
    "tooltip_bgcolor": ft.colors.with_opacity(0.8, ft.colors.WHITE),
    "left_axis": ft.ChartAxis(labels=50),
    "bottom_axis": ft.ChartAxis(labels_interval=1, labels_size=40),
    "horizontal_grid_lines": ft.ChartGridLines(
        interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
    ),
}



class BaseChart(ft.LineChart):
    def __init__(self, line_color: str) -> None:
        super().__init__(**base_chart_style)
        
        # create empty list to store coordinates 
        self.points: list = []
        
        # set the min and max X axis
        if self.points:
            self.min_x = int(min(self.points, key = lambda x: x[0][0]))
            self.max_x = int(max(self.points, key = lambda x: x[0][0]))
        else:
            self.min_x = None
            self.max_x = None

        # main line 
        self.line: Any = ft.LineChartData(
            color = line_color,
            stroke_width=2, 
            curved=True,
            stroke_cap_round=True,
            # gradient styling
            below_line_gradient=ft.LinearGradient(
                begin=ft.alignment.top_center, 
                end=ft.alignment.bottom_center,
                colors=[ft.colors.with_opacity(0.25, line_color),
                        "transparent"],
                        ),
        )

        self.line.data_points = self.points
        self.data_series = [self.line]
        

    def create_data_points(self, x, y) -> None:
        self.points.append(
            ft.LineChartDataPoint(
                x, y,
                selected_below_line=ft.ChartPointLine(
                    width=0.5, color="white54", dash_pattern=[2, 4]
                ),
                selected_point=ft.ChartCirclePoint(stroke_width=1)
                )
        )
        self.update()




graph_style: dict = {
    "expand": 1,
    "bgcolor": "#17181d",
    "border_radius": 10,
    "padding":30,
}

class Graph(ft.Container):
    def __init__(self) -> None:
        super().__init__(**graph_style)
        self.chart = BaseChart(line_color="teal600")
        self.content = self.chart
    


table_style: dict = {
    "data_table":{
        "columns": [
            ft.DataColumn(ft.Text("Open"), numeric=True),
            ft.DataColumn(ft.Text("Heigh"), numeric=True),
            ft.DataColumn(ft.Text("Low"), numeric=True),
            ft.DataColumn(ft.Text("Close"), numeric=True),
            ft.DataColumn(ft.Text("Adj Close"), numeric=True),
            ft.DataColumn(ft.Text("Volume"), numeric=True),
        ],
        #"width": 800,
        "expand" : True,
        #"heading_row_height": 50, 
        #"data_row_max_height": 30,        
    },
    "data_table_container": {
        "expand" : True,
        #"width" : 450,
        "padding": 10,
        "border_radius": ft.border_radius.only(top_left=10, top_right=10),
        "shadow": ft.BoxShadow(
            spread_radius=8, 
            blur_radius=15,
            color=ft.colors.with_opacity(0.15, "black"),
            offset=ft.Offset(4,4),
        ),
        "bgcolor": ft.colors.with_opacity(0.75, "#1f2128"),

    }
    
}

class Table(ft.Container):
    def __init__(self, _lgraph: object) -> None:
        super().__init__(**table_style.get("data_table_container"))
        self._lgraph: object = _lgraph
        self.headTab = ft.DataTable(**table_style.get("data_table"))
        
        self.content = ft.Column(
            #horizontal_alignment="center", 
            controls= [
                ft.Divider(height=15, color="transparent"),
                ft.Container(**table_style.get("data_table_container"), 
                             content =  ft.Column(
                                 expand = True,
                                 scroll = "hidden",
                                 controls = [self.headTab],
                                 )),
                ft.Divider(height=15, color="transparent")
            ])
        
        #self.symbol = "META"
        #self.start_date = "2022-01-01"
        #self.end_date = "2023-01-01"  
       
        #def getData(self): 
        #        data = get_stockData(self.symbol , self.start_date, self.end_date)
        #        return data
        
        self.x = 10
        self.y = 8
        #self.data = getData(self)
        #self._lgraph.chart.create_data_points(x = self.x, y = self.y)        

        def update_data_table(self) ->  None:
            timestamp = int(time.time())
            data = ft.DataRow(
                cells=ft.DataCell(ft.Text(timestamp))
            )

            self.table.rows.append(data)
            self.table.update
            return timestamp
        
        
        


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
        


def main(page: ft.Page):
    page.padding = 30
    page.bgcolor = "#1f2128"
    
    
    symbol = "AAPL"
    t = ft.Text(value=symbol, color=ft.colors.PURPLE_200)
    symbol_sel = ft.TextField(label="Symbol", value="TSLA")

    # dates
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    # stock data
    data = get_stockData(symbol_sel.value, start_date, end_date)
    graph: ft.Container = Graph()
    symbol_block: ft.Container = Symbol()
    table: ft.Container = Table(_lgraph = graph)



    # graph

    plt.figure(figsize=(10, 6))
    plt.plot(data['Adj Close'], label=symbol_sel.value)
    plt.xlabel("Fecha")
    plt.ylabel("Precio de Cierre Ajustado")
    plt.title(f"Gráfico de Acciones: {symbol_sel.value}")
    plt.legend()
    mplcyberpunk.add_gradient_fill(alpha_gradientglow=0.5)

    page.update()


    page.add(
        ft.Row(
            expand = True,
            controls = [symbol_block,  
                        ft.Column(expand = True, controls = 
                                  [MatplotlibChart(plt, expand=True), 
                                   table])]))
    

if __name__ == "__main__":
    ft.app(target=main)
#ft.app(target=main)
