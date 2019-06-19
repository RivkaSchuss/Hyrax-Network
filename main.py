

def main():
    hyrax_list = [2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 19, 21, 22, 23, 24, 25, 26, 29, 33, 36, 39]
    last_n_days = [1, 10]

    import Learning as lr
    lr.make_db_and_train_by_hours(hyrax_list)

    lr.make_db_and_train(hyrax_list,
                         last_n_list=last_n_days, sex=True, group=False,
                         canyon=False, should_make_graph=True)

    print("Done")


if __name__ == '__main__':
    main()
