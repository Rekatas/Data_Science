import pandas as pd

def calculate_demographic_data(print_data=True):
    df = pd.read_csv('adult.data.csv')

    # 1. Count of each race
    race_count = df['race'].value_counts()

    # 2. Average age of men
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Percentage with Bachelor's degree
    percentage_bachelors = round(
        (df['education'] == 'Bachelors').sum() / len(df) * 100, 1
    )

    # 4. Higher education (>50K)
    higher_edu = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    higher_edu_rich = round(
        (higher_edu['salary'] == '>50K').sum() / len(higher_edu) * 100, 1
    )

    # 5. Lower education (>50K)
    lower_edu = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_edu_rich = round(
        (lower_edu['salary'] == '>50K').sum() / len(lower_edu) * 100, 1
    )

    # 6. Min work hours
    min_work_hours = df['hours-per-week'].min()

    # 7. % rich among those who work min hours
    min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round(
        (min_workers['salary'] == '>50K').sum() / len(min_workers) * 100, 1
    )

    # 8. Country with highest % >50K
    country_stats = df.groupby('native-country')['salary'].value_counts(normalize=True).unstack()
    highest_earning_country = country_stats['>50K'].idxmax()
    highest_earning_country_percentage = round(country_stats['>50K'].max() * 100, 1)

    # 9. Top occupation in India (>50K)
    top_IN_occupation = (
        df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
        ['occupation']
        .value_counts()
        .idxmax()
    )

    if print_data:
        print("Race count:\n", race_count)
        print("Average age of men:", average_age_men)
        print("% with Bachelors:", percentage_bachelors)
        print("% with higher education that earn >50K:", higher_edu_rich)
        print("% without higher education that earn >50K:", lower_edu_rich)
        print("Min work hours:", min_work_hours)
        print("% rich among min workers:", rich_percentage)
        print("Highest earning country:", highest_earning_country)
        print("Highest earning country %:", highest_earning_country_percentage)
        print("Top occupation in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_edu_rich,
        'lower_education_rich': lower_edu_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
