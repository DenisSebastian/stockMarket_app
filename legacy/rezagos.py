
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
        
        