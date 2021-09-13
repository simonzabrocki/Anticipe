from tasks.post_process import make_timeseries_excel, make_imputation_report, make_data_report, make_indicator_correlation_matrix, make_indicator_box_plots



if __name__ == '__main__':  
    print('Formating time series to excel')
    make_timeseries_excel()
    print('Making imputation report')
    make_imputation_report()

    # make_data_report()
    print('Making indicator boxplots')
    make_indicator_box_plots()
    print('Making correlation matrix')
    make_indicator_correlation_matrix()