# Configuration dictionary to hold numeric values for different clients
CONFIG = {
    "default": {
        "order": {
            "timewindow": True # stands for the availability of time windows in the order data 
        },
        "break_duration": {
            "fullDay": 2100, #in seconds this equals 35 minutes
            "halfDay": 900 #in seconds this equals 15 minutes
        },
        "break_times": {
            "fullDay": ["11:00:00", "13:00:00"],
            "halfDay": ["09:00:00", "12:00:00"]
        },
        "customer_Lieferschein": {
            "default": True,
            "alternativeDataColumn": 'Auftr.-Nr.' # this is the column name in the order data that contains the Lieferschein number
        },
        "fleet": {
            "dedicatedVehicles": {
                "speedFactor": 0.75,
                "costs": {
                    "fixed": {"fullDay": 'defined in depot_file', "halfDay": 'defined in depot_file'},
                    "distance": {"fullDay": 0.001, "halfDay": 0.0015},
                    "time": {"fullDay": 0.014, "halfDay": 0.020}
                },
                "shifts": {
                    "start_location_depot": True, # vehicles start at the depot as defined in the depot file
                    "end_location_depot": False # vehicles ends at the depot as defined in the depot file
                },
                "limits": {
                    "maxDistance": {"fullDay": 350000, "halfDay": 250000}, #in meters, this equals 350 km and 250 km
                    "shiftTime": {"fullDay": 30600, "halfDay": 18000} #in seconds, this equals 8.5 hours and 5 hours
                }
            },
            "openVehicles": {
                "fleet_ids": {
                    "0-SPRINTER-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 1000,
                            "distance": 0.002, #cost per meter, a km costs 2 Euro
                            "time": 0.015 #cost per second, an hour costs 0.9 Euro
                        },
                        "capacity": [50, 1200], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","DEFAULT_SKILL"],
                        "amount": 5,
                        "shifts": [
                            {
                                "start": "07:00:00",
                                "end": "16:00:00"
                            }
                        ]
                    },
                    "0-SPRINTER_TAIL_LIFT-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 1200,
                            "distance": 0.0025, #cost per meter, a km costs 2.5 Euro
                            "time": 0.018 #cost per second, an hour costs 1.08 Euro
                        },
                        "capacity": [55, 750], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","SPRINTER_TAIL_LIFT","DEFAULT_SKILL"],
                        "amount": 5,
                        "shifts": [
                            {
                                "start": "07:00:00",
                                "end": "16:00:00"
                            }
                        ]
                    }
                }
            }
        },
        "job": {
            "pickup_duration": 900, #in seconds this equals 15 minutes
            "delivery_duration": 900 #in seconds this equals 15 minutes
        },
        "advancedObjectives": [
            [
                {"type": "minimizeUnassigned"}
            ],
            [
                {"type": "minimizeCost"}
            ],
            [
                {"type": "minimizeTours"}
            ],
            [
                {"type": "maximizeTerritoryJobs"}
            ]
        ]
    },
    "Kemmler": {
        "order": {
            "timewindow": True # stands for the availability of time windows in the order data 
        },
        "break_duration": {
            "fullDay": 2100, #in seconds this equals 35 minutes
            "halfDay": 900 #in seconds this equals 15 minutes
        },
        "break_times": {
            "fullDay": ["11:00:00", "13:00:00"],
            "halfDay": ["09:00:00", "12:00:00"]
        },
        "customer_Lieferschein": {
            "default": False,
            "alternativeDataColumn": 'Auftr.-Nr.' # this is the column name in the order data that contains the Lieferschein number
        },
        "fleet": {
            "dedicatedVehicles": {
                "speedFactor": 0.75,
                "costs": {
                    "fixed": {"fullDay": 'defined in depot_file', "halfDay": 'defined in depot_file'},
                    "distance": {"fullDay": 0.001, "halfDay": 0.0015},
                    "time": {"fullDay": 0.014, "halfDay": 0.020}
                },
                "shifts": {
                    "start_location_depot": False, # vehicles start at the depot as defined in the depot file
                    "end_location_depot": False # vehicles ends at the depot as defined in the depot file
                },
                "limits": {
                    "maxDistance": {"fullDay": 350000, "halfDay": 250000}, #in meters, this equals 350 km and 250 km
                    "shiftTime": {"fullDay": 36000, "halfDay": 18000} #in seconds, this equals 9 hours and 5 hours
                }
            },
            "openVehicles": {
                "fleet_ids": {
                    "0-SPRINTER-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 10000,
                            "distance": 0.002, #cost per meter, a km costs 2 Euro
                            "time": 0.015 #cost per second, an hour costs 0.9 Euro
                        },
                        "capacity": [50, 1200], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","DEFAULT_SKILL"],
                        "amount": 5,
                        "shifts": [
                            {
                                "start": "07:00:00",
                                "end": "16:00:00"
                            }
                        ]
                    },
                    "0-SPRINTER_TAIL_LIFT-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 12000,
                            "distance": 0.0025, #cost per meter, a km costs 2.5 Euro
                            "time": 0.018 #cost per second, an hour costs 1.08 Euro
                        },
                        "capacity": [55, 750], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","SPRINTER_TAIL_LIFT","DEFAULT_SKILL"],
                        "amount": 3,
                        "shifts": [
                            {
                                "start": "07:00:00",
                                "end": "16:00:00"
                            }
                        ]
                    }
                }
            }
        },
        "job": {
            "pickup_duration": 900, #in seconds this equals 15 minutes
            "delivery_duration": 900 #in seconds this equals 15 minutes
        },
        "advancedObjectives": [
            [
                {"type": "minimizeUnassigned"}
            ],
            [
                {"type": "minimizeCost"}
            ],
            [
                {"type": "minimizeTours"}
            ],
            [
                {"type": "maximizeTerritoryJobs"}
            ],
            [
                {"type": "balanceDuration",
                    "options": {
                        "threshold": 0.4 #0...1 (higher value is more liked to be enforced in comparison to the other objectives)
                    }
                }
            ]
        ]
    },
    "Stark": {
        "order": {
            "timewindow": True # stands for the availability of time windows in the order data 
        },
        "break_duration": {
            "fullDay": 2100, #in seconds this equals 35 minutes
            "halfDay": 900 #in seconds this equals 15 minutes
        },
        "break_times": {
            "fullDay": ["11:00:00", "13:00:00"],
            "halfDay": ["09:00:00", "12:00:00"]
        },
        "customer_Lieferschein": {
            "default": True,
            "alternativeDataColumn": 'Auftr.-Nr.' # this is the column name in the order data that contains the Lieferschein number
        },
        "fleet": {
            "dedicatedVehicles": {
                "speedFactor": 0.75,
                "costs": {
                    "fixed": {"fullDay": 'defined in depot_file', "halfDay": 'defined in depot_file'},
                    "distance": {"fullDay": 0.001, "halfDay": 0.0015},
                    "time": {"fullDay": 0.014, "halfDay": 0.020}
                },
                "shifts": {
                    "start_location_depot": True, # vehicles start at the depot as defined in the depot file
                    "end_location_depot": False # vehicles ends at the depot as defined in the depot file
                },
                "limits": {
                    "maxDistance": {"fullDay": 350000, "halfDay": 250000}, #in meters, this equals 350 km and 250 km
                    "shiftTime": {"fullDay": 30600, "halfDay": 18000} #in seconds, this equals 8.5 hours and 5 hours
                }
            },
            "openVehicles": {
                "fleet_ids": {
                    "0-SPRINTER-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 50,
                            "distance": 0.002, #cost per meter, a km costs 2 Euro
                            "time": 0.015 #cost per second, an hour costs 0.9 Euro
                        },
                        "capacity": [50, 1200], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","DEFAULT_SKILL"],
                        "amount": 5,
                        "shifts": [
                            {
                                "start": "07:00:00",
                                "end": "16:00:00"
                            }
                        ]
                    },
                    "0-SPRINTER_TAIL_LIFT-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 60,
                            "distance": 0.0025, #cost per meter, a km costs 2.5 Euro
                            "time": 0.018 #cost per second, an hour costs 1.08 Euro
                        },
                        "capacity": [80, 750], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","SPRINTER_TAIL_LIFT", "DEFAULT_SKILL"],
                        "amount": 5,
                        "shifts": [
                            {
                                "start": "07:00:00",
                                "end": "16:00:00"
                            }
                        ]
                    }
                }
            }
        },
        "job": {
            "pickup_duration": 900, #in seconds this equals 15 minutes
            "delivery_duration": 900 #in seconds this equals 15 minutes
        },
        "advancedObjectives": [
            [
                {"type": "minimizeUnassigned"}
            ],
            [
                {"type": "minimizeCost"}
            ],
            [
                {"type": "minimizeTours"}
            ],
            [
                {"type": "maximizeTerritoryJobs"}
            ]
        ]
    },
    "laminatDepot_MultiBranch": {
        "order": {
            "timewindow": False, # stands for the availability of time windows in the order data
            "volume_unit_size": 50,
            "customer_hohe_cm":100,
            "customer_breite_cm":80,
            "customer_lange_cm":120,
            "customer_einheit": 'Europalette',
            "customer_menge": True # stands for using standardized 'customer_shipment_volume_units' column in the order data
        },
        "geocoding": {
            "pickup": False, # stands for the pickup location needs to be geocoded
            "dropoff": True # stands for the dropoff location needs to be geocoded
        },
        "dedicated_branches": {
            "customer_branch_cluster": {
                "HAN": {
                    "pickup_lat": 52.424259, # laminatDepot Hannover
                    "pickup_lng": 9.830880,
                    "strict_territory": True
                },
                "BI": {
                    "pickup_lat": 52.03518, # laminatDepot Bielefeld
                    "pickup_lng": 8.553195,
                    "strict_territory": False
                },
                "PW": {
                    "pickup_lat": 52.25688, # laminatDepot Porta Westfalica
                    "pickup_lng": 8.898211,
                    "strict_territory": False,
                    "earliest_pickup_time": "10:00:00",
                    "latest_pickup_time": "16:00:00"
                },
                "PB": {
                    "pickup_lat": 51.69869, # laminatDepot Paderborn
                    "pickup_lng": 8.731449,
                    "strict_territory": False,
                    "earliest_pickup_time": "10:00:00",
                    "latest_pickup_time": "16:00:00"
                }
            }
        },
        "break_duration": {
            "fullDay": 2100, #in seconds this equals 35 minutes
            "halfDay": 900 #in seconds this equals 15 minutes
        },
        "break_times": {
            "fullDay": ["11:00:00", "13:00:00"],
            "halfDay": ["09:00:00", "12:00:00"]
        },
        "customer_Lieferschein": {
            "default": False,
            "alternativeDataColumn": 'Auftr.-Nr.' # this is the column name in the order data that contains the Lieferschein number
        },
        "fleet": {
            "dedicatedVehicles": {
                "speedFactor": 0.75,
                "costs": {
                    "fixed": {"fullDay": 'defined in depot_file', "halfDay": 'defined in depot_file'},
                    "distance": {"fullDay": 0.001, "halfDay": 0.0015},
                    "time": {"fullDay": 0.014, "halfDay": 0.020}
                },
                "shifts": {
                    "start_location_depot": True, # vehicles start at the depot as defined in the depot file
                    "end_location_depot": True # vehicles ends at the depot as defined in the depot file
                },
                "limits": {
                    "maxDistance": {"fullDay": 350000, "halfDay": 250000}, #in meters, this equals 350 km and 250 km
                    "shiftTime": {"fullDay": 36000, "halfDay": 18000} #in seconds, this equals 9 hours and 5 hours
                }
            },
            "openVehicles": {
                "fleet_ids": {
                    "0-SPRINTER_TAIL_LIFT-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 12000,
                            "distance": 0.0025, #cost per meter, a km costs 2.5 Euro
                            "time": 0.018 #cost per second, an hour costs 1.08 Euro
                        },
                        "capacity": [55, 750], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","SPRINTER_TAIL_LIFT","DEFAULT_SKILL"],
                        "amount": 1,
                        "shifts": [
                            {
                                "start": "10:00:00",
                                "end": "18:00:00"
                            }
                        ]
                    }
                }
            }
        },
        "job": {
            "pickup_duration": 300, #in seconds this equals 5 minutes
            "delivery_duration": 1200 #in seconds this equals 20 minutes
        },
        "advancedObjectives": [
            [
                {"type": "minimizeUnassigned"}
            ],
            [
                {"type": "minimizeTours"}
            ],
            [
                {"type": "balanceDuration",
                    "options": {
                        "threshold": 0.7 #0...1 (higher value is more liked to be enforced in comparison to the other objectives)
                    }
                }
            ],
            [
                {"type": "maximizeTerritoryJobs"}
            ],
            [
                {"type": "minimizeCost"}
            ]
        ]
    },
    "Wigger": {
        "order": {
            "timewindow": True # stands for the availability of time windows in the order data 
        },
        "break_duration": {
            "fullDay": 2100, #in seconds this equals 35 minutes
            "halfDay": 900 #in seconds this equals 15 minutes
        },
        "break_times": {
            "fullDay": ["11:00:00", "13:00:00"],
            "halfDay": ["09:00:00", "12:00:00"]
        },
        "customer_Lieferschein": {
            "default": False,
            "alternativeDataColumn": 'Auftr.-Nr.' # this is the column name in the order data that contains the Lieferschein number
        },
        "fleet": {
            "dedicatedVehicles": {
                "speedFactor": 0.75,
                "costs": {
                    "fixed": {"fullDay": 'defined in depot_file', "halfDay": 'defined in depot_file'},
                    "distance": {"fullDay": 0.001, "halfDay": 0.0015},
                    "time": {"fullDay": 0.014, "halfDay": 0.020}
                },
                "shifts": {
                    "start_location_depot": True, # vehicles start at the depot as defined in the depot file
                    "end_location_depot": True # vehicles ends at the depot as defined in the depot file
                },
                "limits": {
                    "maxDistance": {"fullDay": 2500000, "halfDay": 1500000}, #in meters, this equals 350 km and 250 km
                    "shiftTime": {"fullDay": 86400, "halfDay": 86400} #in seconds, this equals 9 hours and 5 hours
                },
                "skills": ["SPRINTER","SPRINTER_TAIL_LIFT","LKW_7_5""DEFAULT_SKILL"]
            },
            "openVehicles": {
                "fleet_ids": {
                    "0-SPRINTER_TAIL_LIFT-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 100000,
                            "distance": 0.0025, #cost per meter, a km costs 2.5 Euro
                            "time": 0.018 #cost per second, an hour costs 1.08 Euro
                        },
                        "capacity": [55, 750], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","SPRINTER_TAIL_LIFT","DEFAULT_SKILL"],
                        "amount": 1,
                        "shifts": [
                            {
                                "start": "07:00:00",
                                "end": "16:00:00"
                            }
                        ]
                    }
                }
            }
        },
        "job": {
            "pickup_duration": 600, #in seconds this equals 10 minutes
            "delivery_duration": 600 #in seconds this equals 10 minutes
        },
        "advancedObjectives": [
            [
                {"type": "minimizeUnassigned"}
            ],
            [
                {"type": "minimizeCost"}
            ],
            [
                {"type": "maximizeTerritoryJobs"}
            ]
        ]
    },
    "Obi_Buchholz": {
        "order": {
            "timewindow": True # stands for the availability of time windows in the order data 
        },
        "break_duration": {
            "fullDay": 2100, #in seconds this equals 35 minutes
            "halfDay": 900 #in seconds this equals 15 minutes
        },
        "break_times": {
            "fullDay": ["11:00:00", "13:00:00"],
            "halfDay": ["09:00:00", "12:00:00"]
        },
        "customer_Lieferschein": {
            "default": False,
            "alternativeDataColumn": 'Auftr.-Nr.' # this is the column name in the order data that contains the Lieferschein number
        },
        "fleet": {
            "dedicatedVehicles": {
                "speedFactor": 0.75,
                "costs": {
                    "fixed": {"fullDay": 'defined in depot_file', "halfDay": 'defined in depot_file'},
                    "distance": {"fullDay": 0.001, "halfDay": 0.0015},
                    "time": {"fullDay": 0.014, "halfDay": 0.020}
                },
                "shifts": {
                    "start_location_depot": True, # vehicles start at the depot as defined in the depot file
                    "end_location_depot": True # vehicles ends at the depot as defined in the depot file
                },
                "limits": {
                    "maxDistance": {"fullDay": 250000, "halfDay": 150000}, #in meters, this equals 350 km and 250 km
                    "shiftTime": {"fullDay": 36000, "halfDay": 18000} #in seconds, this equals 9 hours and 5 hours
                }
            },
            "openVehicles": {
                "fleet_ids": {
                    "0-SPRINTER_TAIL_LIFT-0": {
                        "speedFactor": 0.75,
                        "costs": {
                            "fixed": 150,
                            "distance": 0.0025, #cost per meter, a km costs 2.5 Euro
                            "time": 0.018 #cost per second, an hour costs 1.08 Euro
                        },
                        "capacity": [55, 750], # [volume, weight] repesented in pallet spaces and kg
                        "skills": ["SPRINTER","SPRINTER_TAIL_LIFT","DEFAULT_SKILL"],
                        "amount": 1,
                        "shifts": [
                            {
                                "start": "07:30:00",
                                "end": "16:00:00"
                            }
                        ]
                    }
                }
            }
        },
        "job": {
            "pickup_duration": 600, #in seconds this equals 10 minutes
            "delivery_duration": 600 #in seconds this equals 10 minutes
        },
        "advancedObjectives": [
            [
                {"type": "minimizeUnassigned"}
            ],
            [
                {"type": "minimizeCost"}
            ],
            [
                {"type": "maximizeTerritoryJobs"}
            ]
        ]
    }
}