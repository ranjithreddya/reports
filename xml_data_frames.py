import pandas as pd
import logging
import json

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compare_dataframes(df_actual, df_expect):

    ignore_columns = {'cdts_tracking', 'rpt_date', 'row_uniq_identifier'}

    columns_to_compare = set(df_expect.columns).union(set(df_actual.columns)) - ignore_columns

    merged_df = pd.merge(df_actual, df_expect, on=['cdts_tracking', 'row_uniq_identifier', 'rpt_date'], suffixes=('_actual', '_expect'))

    comparison_results = []

    for _, row in merged_df.iterrows():
        row_uniq_identifier = row['row_uniq_identifier']
        cdts_tracking = row['cdts_tracking']
        rpt_date = row['rpt_date']

        for column in columns_to_compare:
            actual_val = row[f'{column}_actual']
            expect_val = row[f'{column}_expect']

            if actual_val is None:
                actual_val = 'None'
            if expect_val is None:
                expect_val = 'None'

            if expect_val != actual_val:
                if expect_val == 'None' or actual_val == 'None':
                    if expect_val == 'None':
                        result = 'FAIL - Expect NA'
                    else:
                        result = 'FAIL - Actual NA'

                    comparison_results.append({
                        'row_uniq_identifier': row_uniq_identifier,
                        'cdts_tracking': cdts_tracking,
                        'field_nm': column,
                        'expect_val': expect_val,
                        'actual_val': actual_val,
                        'compare_result': result
                    })
                else:
                    comparison_results.append({
                        'row_uniq_identifier': row_uniq_identifier,
                        'cdts_tracking': cdts_tracking,
                        'field_nm': column,
                        'expect_val': expect_val,
                        'actual_val': actual_val,
                        'compare_result': 'FAIL'
                    })
            else:
                if expect_val == 'None' and actual_val == 'None':
                    continue
                else:
                    comparison_results.append({
                        'row_uniq_identifier': row_uniq_identifier,
                        'cdts_tracking': cdts_tracking,
                        'field_nm': column,
                        'expect_val': expect_val,
                        'actual_val': actual_val,
                        'compare_result': 'PASS'
                    })

    if comparison_results:
        logger.info("Differences found between tables:")
        for result in comparison_results:
            logger.info(result)
    else:
        logger.info("No differences found between the tables.")

    print("*" * 100)
    print(json.dumps(comparison_results, indent=4))

    print("#" * 100)

    filtered_results = [result for result in comparison_results if result['row_uniq_identifier'] == 'DTA100357_2']

    print(json.dumps(filtered_results, indent=4))

    return comparison_results


# Sample usage
data_actual = [
    {'cdts_tracking': 'DTA100357', 'rpt_date': '2024-11-04', 'pair1': '92', 'pair2': None, 'row_uniq_identifier': 'DTA100357_1', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None},
    {'cdts_tracking': 'DTA100357', 'rpt_date': '2024-11-04', 'pair1': None, 'pair2': 'RECO', 'row_uniq_identifier': 'DTA100357_2', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None},
    {'cdts_tracking': 'DTA100358', 'rpt_date': '2024-11-04', 'pair1': '92', 'pair2': None, 'row_uniq_identifier': 'DTA100357_1', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None},
    {'cdts_tracking': 'DTA100358', 'rpt_date': '2024-11-04', 'pair1': None, 'pair2': 'RECO', 'row_uniq_identifier': 'DTA100357_2', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None},
]

data_expect = [
    {'cdts_tracking': 'DTA100357', 'rpt_date': '2024-11-04', 'pair1': '23', 'pair2': 'None', 'row_uniq_identifier': 'DTA100357_1', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None},
    {'cdts_tracking': 'DTA100357', 'rpt_date': '2024-11-04', 'pair1': None, 'pair2': 'PARD', 'row_uniq_identifier': 'DTA100357_2', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None},
    {'cdts_tracking': 'DTA100358', 'rpt_date': '2024-11-04', 'pair1': '23', 'pair2': 'None', 'row_uniq_identifier': 'DTA100357_1', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None},
    {'cdts_tracking': 'DTA100358', 'rpt_date': '2024-11-04', 'pair1': None, 'pair2': 'PARD', 'row_uniq_identifier': 'DTA100357_2', 'new_txid': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'modi_txid': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None}
]

df_actual = pd.DataFrame(data_actual)
df_expect = pd.DataFrame(data_expect)

a = compare_dataframes(df_actual, df_expect)

print(a)
