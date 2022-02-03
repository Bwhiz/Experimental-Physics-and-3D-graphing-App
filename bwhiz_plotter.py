import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp


st.set_page_config(
    page_title='Bwhiz plotting app',
    page_icon="random",
    layout= "wide"
)

def main():
    page = st.sidebar.selectbox(
        "Select task to perform",
        [
            "plot from table of values",
            "plot from function"
        ]
    )

    if page =="plot from table of values":
        plot_table()
    
    elif page =="plot from function":
        plot_func()

def plot_table():

    st.title('Bwhiz plotting app')
    st.warning("Input your values and separate them with a comma, e.g: -1,0,1")

    def plotter():
        a , b= np.polyfit(processed_x,processed_y,1)
        fig =plt.figure(figsize=(10,5))
        ax1 = plt.subplot2grid((1,1), (0,0))
        #control of spines
        ax1.spines[['top','right']].set_visible(False)
        ax1.spines[['left','bottom']].set_position(('data',0.0))

        #control of x and y labels
        ax1.set_xlabel(xlabel,fontweight = 'bold',loc='right')
        ax1.set_ylabel(ylabel,fontweight = 'bold', loc='top')

       
        ax1.set_title(graph_title,fontweight = 'bold', fontsize = 16)
        ax1.grid()
        ax1.scatter(processed_x,processed_y, color="k")
        ax1.plot(processed_x, a*(processed_x)+b, color='red', linestyle='--',
        linewidth=2,
        label=f"{ylabel} = {round(a,2)}*({xlabel}) + ({round(b,2)})")
        ax1.legend(loc = 'lower right')
        #for plots having non-negative values, the spines left empty spaces in the plot, I came up with this next line of code
        #to address all plots have a touch of this negative value for balance, it doesn't alter the line of best fit
        ax1.plot(-0,-0,color='white')
        st.pyplot(fig)

    col1, col2 = st.columns([1,2])

    with col1:
        form = st.form(key='my_form')

        x = form.text_input(label='Please input your x-data')
        xlabel = form.text_input(label='what is the label of the X-axis')
        y = form.text_input(label='please input your y-data')
        ylabel = form.text_input(label='what is the label of the Y-axis')
        graph_title = form.text_input(label='what is the title of the graph')

        if x and y != '':
            processed_x = np.array([float(i) for i in x.split(',')])
            processed_y = np.array([float(i) for i in y.split(',')])

        submit = form.form_submit_button(label='click here to get your graph')

    with col2:
        if submit:

            st.header("Output")

            plotter()



def plot_func():

    x_symb = sp.Symbol('x')
    y_symb = sp.Symbol('y')

    def x_range(a, b):
        return np.arange(a, b+1, 0.1)


    def plot_2d(function, a, b):
        func_x = sp.sympify(function)

        domain = x_range(a, b)
        range = [func_x.subs(x_symb, i) for i in domain]

        fig = plt.figure(figsize=(10,10))
        ax = plt.subplot2grid((1,1), (0,0))
        ax.spines[['top','right']].set_visible(False)
        ax.spines[['left','bottom']].set_position(('data',0.0))
        ax.grid()
        ax.set_title("graph of $"+function.replace("**","^").replace("*","")+"$")
        ax.set_xlabel("$x$", loc='right')
        ax.set_ylabel("$y$", loc='top')
        ax.plot(domain, range)
        st.pyplot(fig)


    def plot_3d(function, a, b, azimuth, elevation):
        func_xy = sp.lambdify((x_symb , y_symb), sp.sympify(function))

        dom_x = x_range(a, b)
        dom_y = x_range(a, b)
        dom_x, dom_y = np.meshgrid(dom_x, dom_y)
        range = func_xy(dom_x, dom_y)


        fig = plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.set_title("3D plot of $"+function.replace("**","^").replace("*","")+"$")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$"+function.replace("**","^").replace("*","")+"$")
        ax.azim = azimuth
        ax.elev = elevation
        ax.plot_surface(dom_x, dom_y, range, rstride=1, cstride=1, cmap='viridis')

        st.pyplot(fig)


    st.title("Bwhiz 2D/3D function plotter")
    col1, col2 = st.columns([1,2])

    #form = st.form(key='my_form')

    with col1:
        st.warning(" Use \* for multiplication and \*\* for 'raise to power', e.g: $$2x^2$$ would be written symbollically as 2*x**2")
        function = st.text_input("Enter your function here").lower()

        st.warning("keep the domain of the function above in mind while inputting your [min, max], and limit values to smaller ranges for faster rendering e.g [-1,1]")
        val_a = st.text_input("Enter your min plot value [a, ]")
        val_b = st.text_input("Enter your max plot value [ ,b]")

        azimuth = st.select_slider(
            'select a value for the azimuthal angle of plot',
            [0,30,60,90,120,150,180],
            value=60
        )

        elevation = st.select_slider(
            'select a value for the elevation of plot',
            [-90,-60,-30,0,30,60,90],
            value=30
        )


    with col2:
        if val_a and val_b !="":
            val_a = float(val_a)
            val_b = float(val_b)

            st.header("Output")

            if "x" and not "y" in function:
                plot_2d(function, val_a, val_b)

            elif "x" and "y" in function:
                plot_3d(function, val_a, val_b,azimuth, elevation)

            else:
                st.write("Input a valid function")



if __name__=="__main__":
    main()


    
