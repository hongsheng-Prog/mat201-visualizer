import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Multivariable Calculus Visualizer", layout="wide")

st.title("Interactive Visualizer: Functions of Several Variables")
st.markdown("""
This application is designed to visualize the meaning of functions with multiple variables.
Select a mode below to explore **Functions of Two Variables** ($z = f(x,y)$) or **Functions of Three Variables** ($w = f(x,y,z)$).
""")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Settings")
mode = st.sidebar.radio("Select Topic Level:",
                        ["Function of Two Variables (2D Domain)", "Function of Three Variables (3D Domain)"])

# ==========================================
# TOPIC 1.1: FUNCTIONS OF TWO VARIABLES
# ==========================================
if mode == "Function of Two Variables (2D Domain)":
    st.header("1. Functions of Two Variables: $z = f(x,y)$")
    st.markdown("""
    **Concept:** A function of two variables assigns a unique real number $z$ to each pair of real numbers $(x, y)$ in its domain.
    * **Graph:** A surface in 3D space.
    * **Level Curves:** The 2D curves formed by cutting the surface with horizontal planes ($z = k$).
    """)

    # --- INPUTS ---
    st.sidebar.subheader("Function Parameters")
    # Satisfies "2 examples (two different complexities)"
    function_choice = st.sidebar.selectbox(
        "Choose an Example Function:",
        ("Simple: Paraboloid (x^2 + y^2)",
         "Complex: Ripple (sin(sqrt(x^2 + y^2)))",
         "Saddle: Hyperbolic Paraboloid (x^2 - y^2)")
    )

    resolution = st.sidebar.slider("Grid Resolution", 20, 100, 50)
    range_val = st.sidebar.slider("Axis Range", 1, 10, 5)

    # --- DATA GENERATION ---
    x = np.linspace(-range_val, range_val, resolution)
    y = np.linspace(-range_val, range_val, resolution)
    X, Y = np.meshgrid(x, y)

    # 精确匹配选项，避免歧义
    if function_choice == "Simple: Paraboloid (x^2 + y^2)":
        Z = X ** 2 + Y ** 2
        formula = r"\large $z = x^2 + y^2$"
    elif function_choice == "Complex: Ripple (sin(sqrt(x^2 + y^2)))":
        Z = np.sin(np.sqrt(X ** 2 + Y ** 2))
        formula = r"\large $z = \sin ( \sqrt{x^2 + y^2} )$"
    else:  # 对应 "Saddle: Hyperbolic Paraboloid (x^2 - y^2)"
        Z = X ** 2 - Y ** 2
        formula = r"\large $z = x^2 - y^2$"

    st.latex(formula)

    # --- VISUALIZATION ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("3D Surface Plot")
        fig_3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
        fig_3d.update_layout(title='Surface Representation', autosize=True, scene_aspectmode='cube')
        st.plotly_chart(fig_3d, use_container_width=True)

    with col2:
        st.subheader("Contour Plot (Level Curves)")
        # 使用 Matplotlib 创建等高线图
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(5, 4))
        contour = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
        ax.contour(X, Y, Z, levels=20, colors='black', linewidths=0.5)
        ax.set_title('Domain Map (Top-Down View)')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        plt.colorbar(contour, ax=ax, label='z value')
        st.pyplot(fig)
        plt.close(fig)

# ==========================================
# TOPIC 1.2: FUNCTIONS OF THREE VARIABLES
# ==========================================
elif mode == "Function of Three Variables (3D Domain)":
    st.header("2. Functions of Three Variables: $w = f(x,y,z)$")
    st.markdown("""
    **Concept:** A function of three variables assigns a number $w$ to a triplet $(x, y, z)$.
    * **Visualization:** We cannot graph this in 4D. Instead, we use **Level Surfaces**.
    * **Level Surface:** The set of all points $(x,y,z)$ where the function equals a constant $k$ (i.e., $f(x,y,z) = k$).
    """)

    # --- INPUTS ---
    st.sidebar.subheader("Level Surface Settings")
    iso_val = st.sidebar.slider("Level Value (k)", 1, 20, 9)

    st.latex(rf"\large w = x^2 + y^2 + z^2 = {iso_val}")
    st.caption(rf"Visualizing the **level surface** where the function value $w$ is constant: $w = {iso_val}$.")

    # --- DATA GENERATION (Sphere) ---
    # We generate a point cloud to represent the surface for simplicity in this demo
    phi = np.linspace(0, np.pi, 30)
    theta = np.linspace(0, 2 * np.pi, 30)
    phi, theta = np.meshgrid(phi, theta)

    radius = np.sqrt(iso_val)
    x_3d = radius * np.sin(phi) * np.cos(theta)
    y_3d = radius * np.sin(phi) * np.sin(theta)
    z_3d = radius * np.cos(phi)

    # --- VISUALIZATION ---
    fig_iso = go.Figure(data=[go.Surface(x=x_3d, y=y_3d, z=z_3d, opacity=0.8, colorscale='Plasma')])
    fig_iso.update_layout(
        title=f'Level Surface for k={iso_val}',
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
    )
    st.plotly_chart(fig_iso, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    As you change the slider $k$, you are selecting a different "slice" of the 4D function $w = x^2 + y^2 + z^2$. 
    For $w$ to increase (higher temperature, density, etc.), the sphere must grow larger.
    """)

# --- FOOTER ---
st.divider()
st.markdown("Created for MAT201 Assignment 2.")
