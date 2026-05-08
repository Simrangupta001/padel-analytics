def generate_shot_summary(df):

    print("\nShot Counts By Player:\n")

    pivot = df.groupby(
        ["player", "shot"]
    ).size().unstack(fill_value=0)

    print(pivot)

    print("\nOverall Shot Counts:\n")

    print(df["shot"].value_counts())