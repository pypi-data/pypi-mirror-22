from armine import ARM, ARMClassifier

data = [['Bread', 'Milk'],
        ['Bread', 'Diapers', 'Beer', 'Eggs'],
        ['Milk', 'Diapers', 'Beer', 'Cola'],
        ['Bread', 'Milk', 'Diapers', 'Beer'],
        ['Bread', 'Milk', 'Diapers', 'Cola']]

data1 = [['apple', 'beer', 'rice', 'chicken'],
         ['apple', 'beer', 'rice'],
         ['apple', 'beer'],
         ['apple', 'mango'],
         ['milk', 'beer', 'rice', 'chicken'],
         ['milk', 'beer', 'rice'],
         ['milk', 'beer'],
         ['milk', 'mango']]


def test_arm():
    ar = ARM()
    ar.load(data1)
    ar.learn(0.1, 0.1)
    ar.print_rules()


def test_arm_classifier():
    ar = ARMClassifier()
    ar.load_from_csv('raw.csv', -1, False)
    ar.learn(0.3, 0.1)
    ar.print_rules()
    ar.learn(0.6, 0.1)
    ar.print_rules()
    ar.learn(0.8, 0.1)
    ar.print_rules()
    data = ['April', 'Div6' ,'Dep4',
            'Normal', 'MH', 'GW', 'MW',
            'UC', 'Employee', 'SPI1',
            'IPS3', 'EDS5', 'SS12',
            'BD2', 'Beh', 'SINF']
    result = ar.classify(data)
    print(result)


def main():
    test_arm()
    test_arm_classifier()


if __name__ == '__main__':
    main()
