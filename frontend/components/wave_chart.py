import plotly.graph_objects as go
from typing import List, Dict, Any

def create_wave_height_chart(history_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Build Significant Wave Height (Hs) Plotly chart matching Reference Image 4.
    """
    times = [d["time"] for d in history_data]
    heights = [d["wave_height"] for d in history_data]
    
    fig = go.Figure()
    
    # Threshold Lines
    fig.add_hline(
        y=3.5, line_dash="dash", line_color="#ef4444", line_width=1.5,
        annotation_text="Rough Threshold", annotation_position="top right",
        annotation_font=dict(size=10, color="#ef4444")
    )
    fig.add_hline(
        y=2.5, line_dash="dash", line_color="#f59e0b", line_width=1.5,
        annotation_text="Moderate Threshold", annotation_position="top right",
        annotation_font=dict(size=10, color="#f59e0b")
    )
    fig.add_hline(
        y=1.5, line_dash="dash", line_color="#10b981", line_width=1.5,
        annotation_text="Calm Threshold", annotation_position="top right",
        annotation_font=dict(size=10, color="#10b981")
    )
    
    # Wave Height Series
    fig.add_trace(go.Scatter(
        x=times,
        y=heights,
        mode="lines",
        name="Hs (m)",
        line=dict(color="#00d2ff", width=2.8),
        hovertemplate="Time: %{x}<br>Hs: <b>%{y:.2f} m</b><extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="<b>1. Significant Wave Height (Hs)</b>", font=dict(color="#ffffff", size=14)),
        paper_bgcolor="#070d18",
        plot_bgcolor="#070d18",
        height=320,
        margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#162238",
            tickfont=dict(color="#64748b", size=10),
            showline=False
        ),
        yaxis=dict(
            title=dict(text="Height (m)", font=dict(color="#94a3b8", size=11)),
            showgrid=True,
            gridcolor="#162238",
            tickfont=dict(color="#64748b", size=10),
            range=[0.5, 4.0]
        ),
        showlegend=False
    )
    return fig

def create_wave_period_chart(history_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Build Peak Wave Period (Tp) Plotly chart matching Reference Image 4.
    """
    times = [d["time"] for d in history_data]
    periods = [d["wave_period"] for d in history_data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=times,
        y=periods,
        mode="lines",
        name="Tp (s)",
        line=dict(color="#a855f7", width=2.6),
        hovertemplate="Time: %{x}<br>Tp: <b>%{y:.1f} s</b><extra></extra>"
    ))
    
    fig.update_layout(
        title=dict(text="<b>2. Peak Wave Period (Tp)</b>", font=dict(color="#ffffff", size=14)),
        paper_bgcolor="#070d18",
        plot_bgcolor="#070d18",
        height=320,
        margin=dict(l=40, r=20, t=40, b=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#162238",
            tickfont=dict(color="#64748b", size=10),
            showline=False
        ),
        yaxis=dict(
            title=dict(text="Period (seconds)", font=dict(color="#94a3b8", size=11)),
            showgrid=True,
            gridcolor="#162238",
            tickfont=dict(color="#64748b", size=10),
            range=[2, 14]
        ),
        showlegend=False
    )
    return fig

def create_12h_trajectory_chart(trajectory_points: List[Dict[str, Any]]) -> go.Figure:
    """
    Build 12-Hour Forward Wave Height Trajectory chart matching Reference Image 1.
    """
    times = [p["time"] for p in trajectory_points]
    heights = [p["predicted_height"] for p in trajectory_points]
    lowers = [p["lower_bound"] for p in trajectory_points]
    uppers = [p["upper_bound"] for p in trajectory_points]
    
    fig = go.Figure()
    
    # 1. Shaded Confidence Band (Upper and Lower)
    fig.add_trace(go.Scatter(
        x=times,
        y=uppers,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=times,
        y=lowers,
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(0, 210, 255, 0.16)",
        name="Model Confidence (±1σ)",
        hoverinfo="skip"
    ))
    
    # 2. Reference Threshold Lines
    fig.add_hline(
        y=3.5, line_dash="dash", line_color="#ef4444", line_width=1.5,
        annotation_text="Rough (3.5m)", annotation_position="top right",
        annotation_font=dict(size=10, color="#ef4444")
    )
    fig.add_hline(
        y=2.5, line_dash="dash", line_color="#f59e0b", line_width=1.5,
        annotation_text="Moderate (2.5m)", annotation_position="top right",
        annotation_font=dict(size=10, color="#f59e0b")
    )
    fig.add_hline(
        y=1.5, line_dash="dash", line_color="#10b981", line_width=1.5,
        annotation_text="Calm (1.5m)", annotation_position="top right",
        annotation_font=dict(size=10, color="#10b981")
    )
    
    # 3. Trajectory Line with Point Markers
    fig.add_trace(go.Scatter(
        x=times,
        y=heights,
        mode="lines+markers",
        name="Predicted Wave Height",
        line=dict(color="#00d2ff", width=3.0),
        marker=dict(size=7, color="#ffffff", line=dict(color="#00d2ff", width=2)),
        hovertemplate="Hour: %{x}<br>Predicted: <b>%{y:.2f} m</b><extra></extra>"
    ))
    
    fig.update_layout(
        paper_bgcolor="#070d18",
        plot_bgcolor="#070d18",
        height=360,
        margin=dict(l=40, r=20, t=20, b=30),
        xaxis=dict(
            showgrid=True,
            gridcolor="#162238",
            tickfont=dict(color="#64748b", size=10),
            showline=False
        ),
        yaxis=dict(
            title=dict(text="Predicted Height (m)", font=dict(color="#94a3b8", size=11)),
            showgrid=True,
            gridcolor="#162238",
            tickfont=dict(color="#64748b", size=10),
            range=[0.5, 4.2]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#94a3b8", size=11),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return fig
