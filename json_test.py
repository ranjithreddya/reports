import json

data3 = {
    "type_changes": {
        "root['TxDtls']['RcncltnRpt']": {
            "old_type": "<class 'list'>",
            "new_type": "<class 'dict'>",
            "old_value": [
                {
                    "TxId": {
                        "UnqIdr": {
                            "UnqTxIdr": "NK040824243049TC99999SEUREFIT51547XCOMNEGR93"
                        }
                    },
                    "MtchgCrit": {
                        "CtrctMtchgCrit": {
                            "ISIN": {
                                "Val2": "US9311421039"
                            },
                            "UnqPdctIdr": {
                                "Val1": {
                                    "Id": "QZTF0Q7B08N4"
                                }
                            }
                        },
                        "TxMtchgCrit": {
                            "PltfmIdr": {
                                "Val1": "AAPA",
                                "Val2": "4AXE"
                            }
                        }
                    }
                },
                {
                    "TxId": {
                        "UnqIdr": {
                            "UnqTxIdr": "NK040824243049TC99999SEUREFIT51547XCOMNEGR94"
                        }
                    },
                    "MtchgCrit": {
                        "CtrctMtchgCrit": {
                            "ISIN": {
                                "Val2": "US9311421039"
                            },
                            "UnqPdctIdr": {
                                "Val1": {
                                    "Id": "QZTF0Q7B08N4"
                                }
                            }
                        },
                        "TxMtchgCrit": {
                            "PltfmIdr": {
                                "Val1": "AAPA",
                                "Val2": "4AXE"
                            }
                        }
                    }
                }
            ],
            "new_value": {
                "TxId": {
                    "UnqIdr": {
                        "UnqTxIdr": "NK040824243049TC99999SEUREFIT51547XCOMNEGR93"
                    }
                },
                "MtchgCrit": {
                    "CtrctMtchgCrit": {
                        "ISIN": {
                            "Val2": "US9311421039"
                        },
                        "UnqPdctIdr": {
                            "Val1": {
                                "Id": "QZTF0Q7B08N4"
                            }
                        }
                    },
                    "TxMtchgCrit": {
                        "PltfmIdr": {
                            "Val1": "AAPA",
                            "Val2": "4AXE"
                        }
                    }
                }
            }
        }
    }
}

# Convert dictionary to formatted JSON string
json_string = json.dumps(data3, indent=4)

# Print the formatted JSON string
print(json_string)
