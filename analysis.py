import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')

#print(df.head())

print("shape :", df.shape)
print("columns : ", df.columns.tolist())
print("\ndata types : \n", df.dtypes)
print("\nmissing values : \n", df.isnull().sum())

print("\nsummary : \n", df.describe())

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

print(df[['Order Date','Year','Month']].head())


# Total Revenue, Profit and Number of Orders?

total_revenue = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
profit_margin = (total_profit / total_revenue) * 100

print("===== KEY KPIs =====")
print(f"Total Revenue  : ${total_revenue:,.2f}")
print(f"Total Profit   : ${total_profit:,.2f}")
print(f"Total Orders   : {total_orders}")
print(f"Profit Margin  : {profit_margin:.2f}%")


# Which Category makes the most Sales & Profit?

category_analysis = df.groupby('Category')[['Sales','Profit']].sum().round(2)
print("\n===== SALES & PROFIT BY CATEGORY =====")
print(category_analysis)


# Which Region performs best?

region_analysis = df.groupby('Region')[['Sales','Profit']].sum().round(2)
print("\n===== SALES & PROFIT BY REGION =====")
print(region_analysis)


# Do high discounts hurt profit?

df['Discount Category'] = pd.cut(df['Discount'],
                                  bins=[-1, 0, 0.2, 0.4, 1],
                                  labels=['No Discount', 'Low (0-20%)',
                                          'Medium (20-40%)', 'High (40%+)'])

discount_impact = df.groupby('Discount Category', observed=True)['Profit'].mean().round(2)
print("\n===== AVERAGE PROFIT BY DISCOUNT LEVEL =====")
print(discount_impact)


# What are the Top 10 best-selling products? 

top_products = df.groupby('Product Name')['Sales'].sum()\
                 .sort_values(ascending=False).head(10).round(2)
print("\n===== TOP 10 PRODUCTS BY SALES =====")
print(top_products)



plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12


# Sales & Profit by Category 

category_data = df.groupby('Category')[['Sales', 'Profit']].sum()

x = range(len(category_data.index))
width = 0.35

fig, ax = plt.subplots()
bars1 = ax.bar([i - width/2 for i in x], category_data['Sales'],
               width, label='Sales', color='steelblue')
bars2 = ax.bar([i + width/2 for i in x], category_data['Profit'],
               width, label='Profit', color='coral')

ax.set_title('Sales & Profit by Category')
ax.set_xlabel('Category')
ax.set_ylabel('Amount (USD)')
ax.set_xticks(list(x))
ax.set_xticklabels(category_data.index)
ax.legend()

plt.tight_layout()
plt.savefig('chart1_category.png')
plt.show()
print("Chart 1 saved!")


# Sales by Region

region_sales = df.groupby('Region')['Sales'].sum()

plt.figure()
plt.pie(region_sales,
        labels=region_sales.index,
        autopct='%1.1f%%',
        startangle=140)
plt.title('Sales Distribution by Region')

plt.tight_layout()
plt.savefig('chart2_region.png')
plt.show()
print("Chart 2 saved!")


# Monthly Sales Trend

monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
monthly_sales['Period'] = monthly_sales['Month'].astype(str) + '/' + \
                           monthly_sales['Year'].astype(str)

plt.figure()
for year in monthly_sales['Year'].unique():
    data = monthly_sales[monthly_sales['Year'] == year]
    plt.plot(data['Month'], data['Sales'], marker='o', label=str(year))

plt.title('Monthly Sales Trend by Year')
plt.xlabel('Month')
plt.ylabel('Total Sales (USD)')
plt.xticks(range(1, 13),
           ['Jan','Feb','Mar','Apr','May','Jun',
            'Jul','Aug','Sep','Oct','Nov','Dec'])
plt.legend(title='Year')
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('chart3_monthly_trend.png')
plt.show()
print("Chart 3 saved!")



# Discount Impact on Profit

discount_profit = df.groupby('Discount Category', observed=True)['Profit'].mean()

colors = ['green', 'gold', 'orange', 'red']

plt.figure()
bars = plt.bar(discount_profit.index, discount_profit.values,
               color=colors, edgecolor='black')

plt.title('Average Profit by Discount Level')
plt.xlabel('Discount Category')
plt.ylabel('Average Profit (USD)')
plt.axhline(y=0, color='black', linewidth=1.2, linestyle='--')

# Add value labels on bars
for bar, val in zip(bars, discount_profit.values):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 1,
             f'${val:.1f}',
             ha='center', fontsize=11)

plt.tight_layout()
plt.savefig('chart4_discount_profit.png')
plt.show()
print("Chart 4 saved!")