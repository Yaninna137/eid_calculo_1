# app/core/Graph_ellipse.py
from .Math_ellipse import Elipse
from .Items_ellipse import ElipseVisual
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import io
import base64

tick_color = ['#BBBBBB', '#888888', '#999999', '#AAAAAA'] 
colores = [
    "#4DD0E1",  # Azul cian suave
    "#9575CD",  # Violeta suave
    "#F06292",  # Rosa sandía
    "#FFB74D",  # Naranja suave
    "#81C784",  # Verde menta
    "#BA68C8",  # Violeta medio
    "#2A2A2A"   # Blanco (para último punto si se desea)
]

def formatear_numero(n):
    return int(n) if n == int(n) else round(n, 1)

# GRAFICO 2D - INDIVIDUAL ELIPSE =>

def grafico_2d_simple(elipse: Elipse, escala=1.0):
    puntos = elipse.calcular_puntos(n=50)
    
    if isinstance(elipse, ElipseVisual): # Asegurando de usar puntos con etiquetas desde ElipseVisual
        puntos_etiquetados = elipse.puntos_con_etiquetas()
    else:
        elipse_ext = ElipseVisual(**elipse.__dict__)
        puntos_etiquetados = elipse_ext.puntos_con_etiquetas()

    x_vals = [x * escala for x, _ in puntos]
    y_vals = [y * escala for _, y in puntos]

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor('#121212')
    ax.set_facecolor('#121212')
    ax.plot(x_vals, y_vals, color="#0080FF66", linewidth=1, label="Elipse")

    # Centro
    ax.scatter(elipse.h * escala, elipse.k * escala, color='red', zorder=5)
    ax.text(elipse.h * escala + 0.2, elipse.k * escala + 0.2, f"({elipse.h}, {elipse.k})", color='red')

    # Ejes cartesianos
    ax.axhline(0, color='gray', linewidth=1)
    ax.axvline(0, color='gray', linewidth=1)

    # Limites
    margen = max(elipse.a, elipse.b) * 1.5 * escala
    ax.set_xlim((elipse.h - margen) * escala, (elipse.h + margen) * escala)
    ax.set_ylim((elipse.k - margen) * escala, (elipse.k + margen) * escala)

    # Diseño para la Grafica
    info_labels = []
    for i, (x, y, label) in enumerate(puntos_etiquetados):
        x_scaled, y_scaled = x * escala, y * escala
        ax.plot(x_scaled, y_scaled, 'o', color=colores[i], markersize=8,
                markeredgecolor=colores[i], markeredgewidth=0.8, zorder=3)
        
        texto = f"{label} ({formatear_numero(x)}, {formatear_numero(y)})"
        info_labels.append((texto, colores[i]))

    # Personalizar leyenda 
    x_rel = 0.02
    y_rel_base = 0.02
    espaciado = 0.05  
    for idx, (texto, color) in enumerate(info_labels[:-1]):
        y_rel = y_rel_base + idx * espaciado
        ax.text(x_rel, y_rel, f"● {texto}",
                transform=ax.transAxes,
                fontsize=11, fontweight='bold',
                verticalalignment='bottom',
                color=color)
        
    ax.set_aspect('equal')  # CRUCIAL para que no se deforme la elipse
    ax.grid(True, linestyle='-', alpha=0.5, color='#3A3A3A')  # Color de linias graficas
    ax.set_title("Elipse centrada en ({}, {})".format(elipse.h, elipse.k),color="#FF4C4C", fontsize=14, fontweight='bold')

    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")

    ax.tick_params(axis='x', colors=tick_color[0]) # Color de los números de los ejes X
    ax.tick_params(axis='y', colors=tick_color[0]) # Color de los números de los ejes Y
    ax.xaxis.label.set_color(tick_color[0]) # Color de las etiquetas de los ejes
    ax.yaxis.label.set_color(tick_color[0]) # Color del título (opcional, para consistencia)


    # Guardar como imagen base64
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    buf.close()

    return img_base64

# GRAFICO 2D INTERACTIVO - MULTIPLE ELIPSE =>

def grafico_2d_interactivo(elipses: list, ruts_limpios: list, escala=1.0):
    fig = go.Figure()
    
    # Asegurarse de que tenemos elipses y RUTs
    if not elipses or not ruts_limpios or len(elipses) != len(ruts_limpios):
        return fig
    
    for idx, elipse in enumerate(elipses):
        # Verificar que la elipse tiene los atributos necesarios
        if not hasattr(elipse, 'calcular_puntos'):
            continue
            
        puntos = elipse.calcular_puntos(n=100)
        x_vals = [p[0] * escala for p in puntos]
        y_vals = [p[1] * escala for p in puntos]
        color = colores[idx % len(colores)]

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            name=f"RUT {ruts_limpios[idx]}",
            line=dict(color=color, width=2.5),
            hoverinfo='name'
        ))
        
        # Punto central
        fig.add_trace(go.Scatter(
            x=[elipse.h * escala],
            y=[elipse.k * escala],
            mode='markers+text',
            text=[f"({elipse.h:.1f}, {elipse.k:.1f})"],
            textposition="top right",
            marker=dict(color=color, size=8),
            showlegend=False
        ))

    fig.update_layout(
        plot_bgcolor='#121212',
        paper_bgcolor='#121212',
        font=dict(color='#FFFFFF', size=12),
        xaxis=dict(title="Eje X", gridcolor="#2A2A2A"),
        yaxis=dict(title="Eje Y", gridcolor="#2A2A2A", scaleanchor="x", scaleratio=1),
        legend=dict(bgcolor='#121212', bordercolor='#AAAAAA', borderwidth=1)
    )
    
    return fig

# GRAFICO 3D INTERACTIVO - MULTIPLE ELIPSE =>

def generar_elipsoide(cx, cy, cz, rx, ry, rz, n=30):
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, np.pi, n)
    x = rx * np.outer(np.cos(u), np.sin(v)) + cx
    y = ry * np.outer(np.sin(u), np.sin(v)) + cy
    z = rz * np.outer(np.ones_like(u), np.cos(v)) + cz
    return x, y, z

def detectar_colision(c1, r1, c2, r2):
    distancia = np.linalg.norm(np.array(c1) - np.array(c2))
    return distancia < (max(r1) + max(r2))

def Grafico_3D_multiple(elipses: list, ruts_limpios: list, escala=0.5):
    fig = go.Figure()

    centros = []
    radios = []

    # Construir y guardar datos para colisión
    for elipse in elipses:
        centros.append((elipse.h * escala, elipse.k * escala, 0))  # centro en z=0
        radios.append((elipse.a * escala, elipse.b * escala, elipse.b * escala))  # usar 'b' para Z como aproximación

    # Recorrer elipses para graficar y detectar colisión
    for idx, elipse in enumerate(elipses):
        cx, cy, cz = centros[idx]
        rx, ry, rz = radios[idx]

        colisiona = False
        for jdx in range(idx):
            if detectar_colision(centros[idx], radios[idx], centros[jdx], radios[jdx]):
                colisiona = True
                break

        color = '#FF3D00' if colisiona else colores[idx % len(colores)]

        x, y, z = generar_elipsoide(cx, cy, cz + idx * 2, rx, ry, rz)

        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            opacity=0.5,
            showscale=False,
            colorscale=[[0, color], [1, color]],
            name=f"RUT {ruts_limpios[idx]}"
        ))

    fig.update_layout(
        title="Visualización 3D de zonas de drones y colisiones",
        scene=dict(
            xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
            xaxis=dict(backgroundcolor='#121212', gridcolor='#424242'),
            yaxis=dict(backgroundcolor='#121212', gridcolor='#424242'),
            zaxis=dict(backgroundcolor='#121212', gridcolor='#424242'),
        ),
        paper_bgcolor='#121212',
        plot_bgcolor='#121212',
        font_color='white',
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig