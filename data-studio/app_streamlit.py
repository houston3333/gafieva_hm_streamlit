import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import scipy.stats as stats
import plotly.express as px
import streamlit as st


numeric = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
non_numeric = ['object','category']


def violinStrip_plot(dataframe):
    columns = np.concatenate([['Select'],list(dataframe.columns)])

    column1 = st.selectbox("Column 1(non-categorical)", columns)
    column2 = st.selectbox("Column 2(non-categorical)", columns)

    if column1 != 'Select' and column2 != 'Select':
        if column1 != column2:
            sd = st.selectbox("Plot", ["Select","Strip Plot", "Violin Plot"])

            if sd != 'Select':
                    fig = plt.figure(figsize=(12, 6))

                    if sd == "Strip Plot":
                        sns.stripplot(x = column1, y = column2, data = dataframe)
                        st.pyplot(fig)
                    
                    elif sd == "Violin Plot":
                        if dataframe[column1].dtypes in numeric or dataframe[column2].dtypes in numeric:
                            sns.violinplot(x = column1, y = column2, data = dataframe)
                            st.pyplot(fig)
                        else:
                            st.error('To create a Violin Plot select at least one column with a numeric value.', icon="🚨")
        else:
            st.error('Identical columns. Please use different columns.', icon="🚨")


def piechart_plot(dataframe):
    columns = dataframe.columns.to_list()

    column1 = st.selectbox("Column 1(categorical)", np.concatenate([['Select'], columns]))
    column2 = st.selectbox("Column 2(non-categorical)", np.concatenate([['Select'], columns]))

    if column1 != 'Select' and column2 != 'Select':
        if dataframe[column1].dtype in non_numeric and dataframe[column2].dtype in numeric: 

            if column1 != column2:  
                grouped_by_category = dataframe[[column1, column2]].groupby(by=[column1]).sum().groupby(level=[0]).cumsum()
                sorted_by_column2 = grouped_by_category.sort_values(by=column2, ascending=False)
                st.write(sorted_by_column2)

                fig = px.pie(sorted_by_column2, values=column2, title= f'By {column2}', height=300, width=200)
                fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error('Identical columns. Please use different columns.', icon="🚨")

        else:
            st.error('Error. Select a categorical variable for the first column and a numeric variable for the second.', icon="🚨")



def test(dataframe):
    columns = list(dataframe.columns)

    column1 = st.selectbox("Column 1", np.concatenate([['Select'], columns]))
    column2 = st.selectbox("Column 2", np.concatenate([['Select'], columns]))


    if column1 != 'Select' and column2 != 'Select':
        if dataframe[column1].dtype in numeric and dataframe[column2].dtype in numeric:
            if column1 != column2:
                stest = st.selectbox("Test", 
                        ["Select",
                        "t-test", 
                        "mann-whitney U-test"])
                
                group1 = dataframe[column1]
                group2 = dataframe[column2]

                if stest != 'Select':
                    match stest:
                        case "t-test":
                            result = stats.ttest_ind(a=group1, b=group2, equal_var=True)
                            pvalue = result[1]

                        case "mann-whitney U-test":
                            result = stats.mannwhitneyu (group1, group2, alternative='two-sided')
                            pvalue = result[1]

                    st.header('Result')

                    if pvalue > 0.05:
                        st.write("Две гипотезы для этого конкретного двухвыборочного t-критерия следующие:", 
                                    "H 0 : µ 1 = µ 2 (две средние совокупности равны)",
                                    "H A : µ 1 ≠ µ 2 (две средние совокупности не равны)",
                                    f'Поскольку p-значение нашего теста {round(pvalue,3)} больше, чем альфа = 0,05,',
                                    "мы не можем отвергнуть нулевую гипотезу теста.")
                    elif pvalue < 0.05:
                        st.write("Две гипотезы для этого конкретного двухвыборочного t-критерия следующие:", 
                                    "H 0 : µ 1 = µ 2 (две средние совокупности равны)",
                                    "H A : µ 1 ≠ µ 2 (две средние совокупности не равны)",
                                    f'Поскольку p-значение нашего теста {round(pvalue,3)} меньше, чем альфа = 0,05,',
                                    "мы можем отвергнуть нулевую гипотезу теста.")
            else:
                st.error('Identical columns. Please use different columns.', icon="🚨")
        
        else:
            st.error('Error. Select numeric variables for both columns.', icon="🚨")

    
        

def run():
    st.title("DATA STUDIO")
    html_temp="""
    
    """

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv']) 

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        if dataframe is not None:
            st.write(dataframe)
            st.write('Types',dataframe.dtypes)

            sb = st.selectbox("Variables", 
                    ["Select",
                    "2 non-categorical", 
                    "1 non-categorical, 1 categorical"])

            match sb:
                case "2 non-categorical":
                    violinStrip_plot(dataframe)

                case "1 non-categorical, 1 categorical":
                    piechart_plot(dataframe)

            st.header('Tests')
            test(dataframe)


if __name__=='__main__':
    run()