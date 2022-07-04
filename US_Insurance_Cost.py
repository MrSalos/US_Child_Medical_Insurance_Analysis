import csv

male_minors_list = []
female_minors_list = []
all_minors_list = []

minors_filtered_region = {
    'southeast': [],
    'southwest': [],
    'northeast': [], 
    'northwest': []   
}


#function to know if the user has a healthy bmi
def bmi_classifier(population):
    obese = []
    overweight = []
    underweight = []

    bmi_percentiles = {  #These threholds were taken out of files provided by the CDC ()
        'm':{
            'healthy': 18.2,
            'overweight': 25.6,
            'obese': 29
        },
        'f':{
            'healthy': 17.6,
            'overweight': 25.6,
            'obese': 30.2
        }
    }

    for person in population:
        if person['sex'] == 'male':
            # Compare each persons BMI to know how's their health state and classify those unhealthy in different categories
            if float(person['bmi']) < bmi_percentiles['m']['healthy']:
                underweight.append(person)
            elif float(person['bmi']) > bmi_percentiles['m']['overweight'] and float(person['bmi']) < bmi_percentiles['m']['obese']:
                overweight.append(person)
            elif float(person['bmi']) > bmi_percentiles['m']['obese']:
                obese.append(person)
        
        elif person['sex'] == 'female':
            if float(person['bmi']) < bmi_percentiles['f']['healthy']:
                underweight.append(person)
            elif float(person['bmi']) > bmi_percentiles['f']['overweight'] and float(person['bmi']) < bmi_percentiles['f']['obese']:
                overweight.append(person)
            elif float(person['bmi']) > bmi_percentiles['f']['obese']:
                obese.append(person)

    return obese, overweight, underweight

def avg_price_per_region(region):
    summatory = 0
    divider = len(minors_filtered_region[region])
    
    for kid in minors_filtered_region[region]:
        summatory += float(kid['charges'])

    avg_price = round(summatory/divider, 2)

    return avg_price


def main():
    # get minors from csv
    with open('datasets\insurance.csv', newline='') as insurance_csv:   #Open the file
        insurance_reader = csv.DictReader(insurance_csv)
        for person in insurance_reader:
            if int(person['age']) < 21:
                all_minors_list.append(person)
            
            if int(person['age']) < 21 and person['sex'] == 'male':
                male_minors_list.append(person)
            elif int(person['age']) < 21 and person['sex'] == 'female':
               female_minors_list.append(person)

    #Filter by region
    for kid in all_minors_list:
        if kid['region'].lower() in minors_filtered_region:
            minors_filtered_region[kid['region']].append(kid)

            
    # get obese, overweight and underweight lists
    obese_list, overweight_list, underweight_list = bmi_classifier(all_minors_list)

    #Analizes
    print(f"The total number of minors is: {len(all_minors_list)}")
    print(f'Total number of obese minors: {len(obese_list)}\nTotal number of overweight minors: {len(overweight_list)}\nTotal number of underweight minors: {len(underweight_list)}')
    for region in minors_filtered_region:
        print(f'The average price for {region} is ${avg_price_per_region(region)}')

if __name__ == '__main__':
    main()