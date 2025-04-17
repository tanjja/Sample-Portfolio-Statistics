import pandas as pd
import matplotlib.pyplot as plt
import math

def get_data(tickers, dates):
    df = pd.DataFrame(index=dates)
    # Default to determine dates traded
    if 'SPY' not in tickers:
        tickers.insert(0, 'SPY')
    
    for ticker in tickers:
        df_temp = pd.read_csv(
            f"data/{ticker}.csv",
            index_col="Date",

            # Columns Variable
            usecols=['Date', 'Adj Close'],
            na_values='nan',
            parse_dates=True
            )
        # Columns Name
        df_temp = df_temp.rename(columns={'Adj Close':ticker})
        df = df.join(df_temp)
        if ticker == 'SPY':
            df = df.dropna(subset=['SPY'])
    
    # Probably not needed
    df.fillna(method="ffill", inplace=True)
    df.fillna(method="bfill", inplace=True)
    return df

def plot_data(df, title='Stock Prices',ylabel='Price'):
    ax = df.plot(title=title, fontsize=10)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    ax.legend(loc='upper left')
    plt.savefig(f"images/{title}.png")
    plt.show()

def get_daily_return(df):
    daily_return = (df/df.shift(1)) - 1
    # daily_return.iloc[0,:] = 0
    daily_return = daily_return[1:]
    return daily_return

def get_cumulative_return(df):
    cumulative_return = (df/df[0]) - 1
    return cumulative_return

def portfolio_stats():
    # Starting Variables
    start_val = 1000000
    start_date = '2007-01-01'
    end_date = '2012-12-31'
    tickers = ['SPY','NVDA','GLD','TXN','YHOO']
    allocs = [0.3,0.2,0.2,0.15,0.15]

    dates = pd.date_range(start_date, end_date)

    # 1. Get adjust closing prices
    df = get_data(tickers, dates)
    plot_data(df)

    # 2. Normalize values
    norm_df = df/df.iloc[0]
    plot_data(norm_df,title="Normalized_Stock_Prices")

    # 3. Factor in allocations
    alloced = norm_df*allocs
    plot_data(alloced,title="Allocated_Prices")

    # 4. Get position values
    pos_vals = alloced*start_val
    plot_data(pos_vals,title="Position_Values")

    # 5. Get daily portfolio value
    port_val = pos_vals.sum(axis=1)
    plot_data(port_val,title="Portfolio_Value")

    # Portfolio Statistics
    print("Portolio Statistics")

    # Daily Returns
    daily_rets = get_daily_return(port_val)

    # Cumulative Returns
    cum_ret = get_cumulative_return(port_val)
    plot_data(cum_ret,title="Cumulative_Returns",ylabel="Cumulative Return")

    # Average Daily Returns
    avg_ret = daily_rets.mean()
    print(f"Average Daily Return: {avg_ret}")

    # Average Daily Standard Deviation (Risk)
    std_ret = daily_rets.std()
    print(f"Average Daily Standard Deviation (Risk): {std_ret}")

    # Sharpe Ratio
    daily_rf = 0 # approximate risk free rate to 0 for this project
    k = math.sqrt(252) # Daily samples
    sharpe = k*((avg_ret-daily_rf)/std_ret)
    print(f"Sharpe Ratio: {sharpe}")

if __name__ == "__main__":
    portfolio_stats()

