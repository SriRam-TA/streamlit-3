import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

df = pd.read_csv(r"./data.csv")


st.markdown(
    """
    <h3 style="
        text-align: center; 
        background-color: #000000; 
        color: white; 
        padding: 10px;
        border-radius: 8px;
    ">
        Bacardi Demand Forecasting
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)

gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
    cellStyle={'textAlign': 'center'},
)

gb.configure_column(
    field="Name",
    header_name="Name",
)

gb.configure_column(
    field="Created Date",
    header_name="Created Date",
    valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
)

gb.configure_column(
    field="Created by",
    header_name="Created By",
)

gb.configure_column(
    field="Revenue",
    header_name="Revenue ($)",
    type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
    valueFormatter="x.toLocaleString()",
)

gb.configure_column(
    field="Capital Costs",
    header_name="Capital Costs",
    type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
    valueFormatter="x.toLocaleString()",
)

gb.configure_column(
    field="profit",
    header_name="Profit",
    type=['numericColumn', 'numberColumnFilter', 'customNumericFormat'],
    valueFormatter="x.toLocaleString()",
)

gb.configure_column(
    field="prec_profit",
    header_name="Profit %",
)

grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    theme='streamlit',
    enable_enterprise_modules=False,
    fit_columns_on_grid_load=True
)

selected_rows = grid_response['selected_rows']


if selected_rows is not None:
    selected_df = pd.DataFrame(selected_rows)
    # X axis groups
    x_groups = ['Revenue', 'Capital Costs', 'Profit']

    fig = go.Figure()

    # For each Item, add bars for Quantity and Price grouped by attribute
    for i, item in enumerate(selected_df['Name']):
        fig.add_trace(go.Bar(
            name=item,
            x=x_groups,
            y=[selected_df.loc[selected_df['Name'] == item, 
                               'Revenue'].values[0],
               selected_df.loc[selected_df['Name'] == item,
                               'Capital Costs'].values[0],
               selected_df.loc[selected_df['Name'] == item, 
                               'profit'].values[0]],
            marker_color=px.colors.qualitative.Plotly[i % 10]
        ))

    fig.update_layout(
        barmode='group',
        title="Scenario Comparision",
        yaxis_title="Value",
        legend_title="Scenarios",
        margin=dict(l=40, r=40, t=80, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Select rows using the checkboxes to display the chart.")
