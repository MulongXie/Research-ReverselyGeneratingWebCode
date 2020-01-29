import pandas as pd


def next_index(i, data_cat):
    def get_name(index):
        name = data_cat[index: index + 1]['App Package Name'].values[0]
        return name

    app_name_pre = get_name(i - 1)
    app_name = get_name(i)
    while app_name == app_name_pre:
        i += 1
        if i >= len(data_cat):
            break
        app_name_pre = get_name(i - 1)
        app_name = get_name(i)
    return i


def main():
    data = pd.read_csv('merged.csv', index_col=0)
    categories = data['Category'].value_counts()
    data_train = pd.DataFrame
    data_test = pd.DataFrame
    data_val = pd.DataFrame
    for cat in categories.keys():
        count = categories[cat]
        data_cat = data[data['Category'] == cat]

        # group the same app into same section
        c_train = int(count * 0.8)
        c_train = next_index(c_train, data_cat)
        if data_train.empty:
            data_train = data_cat[:c_train]
        else:
            data_train = data_train.append(data_cat[:c_train])

        if c_train == count: continue
        c_val = int((count - c_train) / 2) + c_train
        c_val = next_index(c_val, data_cat)
        if data_val.empty:
            data_val = data_cat[c_train: c_val]
        else:
            data_val = data_val.append(data_cat[c_train: c_val])

        if c_val == count: continue
        if data_test.empty:
            data_test = data_cat[c_val:]
        else:
            data_test = data_test.append(data_cat[c_val:])

    print(len(data) == len(data_train) + len(data_test) + len(data_val))
    data_train.to_csv('data_train.csv')
    data_test.to_csv('data_test.csv')
    data_val.to_csv('data_val.csv')


main()