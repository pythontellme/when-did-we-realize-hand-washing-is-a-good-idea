import pandas as pd
import scrape_wikipedia_for_table as scrape
import matplotlib.pyplot as plt

''' Scrape and clean yearly data from Wikipedia '''

website = scrape.scraper('https://en.wikipedia.org/wiki/Ignaz_Semmelweis')

scraped_list = website.scrape('wikitable', 'tr')   

wrangled_list = scrape.wrangle_list(scraped_list)

scrape.remove_line_breaks(wrangled_list)

scrape.remove_comma(wrangled_list['Births'])

wrangled_list['Year'] = wrangled_list['Year'].apply(pd.to_datetime)

wrangled_list[['Births', 'Deaths']] = wrangled_list[['Births', 'Deaths']].apply(pd.to_numeric)   

# print(wrangled_list)

''' Scrape and clean yearly data from Wikipedia '''

website2 = scrape.scraper('https://en.wikipedia.org/wiki/Historical_mortality_rates_of_puerperal_fever')

scraped_list2 = website2.scrape('wikitable sortable', 'tr')

wrangled_list2 = scrape.wrangle_list2(scraped_list2)

scrape.remove_line_breaks(wrangled_list2)

wrangled_list2 = wrangled_list2[wrangled_list2['Births']!='na']

wrangled_list2['Year'] = wrangled_list2['Year'].apply(pd.to_datetime)

wrangled_list2[['Births', 'Deaths']] = wrangled_list2[['Births', 'Deaths']].apply(pd.to_numeric)   

wrangled_list2.reset_index(drop=True, inplace = True)

# print(wrangled_list2)

''' Analyze data '''

# Calculate proportion of deaths per no. births

yearly = wrangled_list

yearly['proportion_deaths'] = yearly['Deaths']/yearly['Births']

# Extract clinic 1 data into yearly1 and clinic 2 data into yearly2
yearly1 = yearly[yearly['Clinic']=='First']
yearly2 = yearly[yearly['Clinic']=='Second']

# Print out yearly1
# print(yearly1)

# Plot yearly proportion of Deaths at the two clinics
plot1 = yearly1.plot(x='Year', y='proportion_deaths', label='yearly1')
plot2 = yearly2.plot(x='Year', y='proportion_deaths', label='yearly2', ax=plot1)
plot2.set_ylabel('% deaths')
# plt.show()

monthly = wrangled_list2
# Calculate proportion of deaths per no. births
monthly["proportion_deaths"] = monthly["Deaths"]/monthly["Births"]

# Print out the first rows in monthly
# print(monthly.head())

# Plot monthly proportion of deaths
ax = monthly.plot(x='Year', y='proportion_deaths')
# plt.show()

# Date when handwashing was made mandatory
handwashing_start = pd.to_datetime('1847-06-01')

# Split monthly into before and after handwashing_start
before_washing = monthly[monthly["Year"]<handwashing_start]
after_washing = monthly[monthly["Year"]>=handwashing_start]

# Plot monthly proportion of deaths before and after handwashing
ax = before_washing.plot(x='Year', y='proportion_deaths', label='clinic1') 
after_washing.plot(x='Year', y='proportion_deaths', label='clinic2', ax=ax)
ax.set_ylabel("Proportion deaths")
# plt.show()

# Difference in mean monthly proportion of deaths due to handwashing
before_proportion =before_washing["proportion_deaths"]
after_proportion =after_washing["proportion_deaths"]
mean_diff = after_proportion.mean()-before_proportion.mean()
print(mean_diff)

# A bootstrap analysis of the reduction of deaths due to handwashing
boot_mean_diff = []
for i in range(3000):
    boot_before = before_proportion.sample(frac=1, replace=True)
    boot_after = after_proportion.sample(frac=1, replace=True)
    boot_mean_diff.append(boot_after.mean() - boot_before.mean())

# Calculating a 95% confidence interval from boot_mean_diff 
confidence_interval = pd.Series(boot_mean_diff).quantile([0.025, 0.975])
print(confidence_interval)