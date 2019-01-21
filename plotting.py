from webcam import df
from bokeh.plotting import figure, show,output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M-%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M-%S") #converting date time column to string using datetime formatting method

cds=ColumnDataSource(df)
#standard way of converting columns to datasource objects

p=figure(x_axis_type='datetime', height=500,width=1000, title="Motion Graph")
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks=1

hover=HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

q=p.quad(left="Start",right="End",bottom=0,top=1, color="green",source=cds)

output_file("Graph.html")
show(p)
