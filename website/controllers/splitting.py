from website.models import Models


class SplittingController:

    def count_dataWithLabel():
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
        data_labeling = instance_model.select()
        return data_labeling