# Stage 1 audit findings

                            check  value
                         raw_rows  73100
                    prepared_rows  73100
                    missing_cells      0
                 exact_duplicates      0
            invalid_required_rows      0
       store_product_combinations    100
                 series_with_gaps      0
products_with_multiple_categories     20
     stores_with_multiple_regions      5
  sales_above_beginning_inventory      0

Decisions:
- Raw data unchanged; prepared copy saved separately.
- Exact duplicates removed only if present.
- Essential invalid values and conflicting daily keys stop processing.
- Missing dates are not filled with zero.
- Synthetic business inconsistencies retained and reported.
- Demand Forecast excluded from later model inputs until provenance is established.
- Model-specific transformations will be fitted on training data only.
- EDA uses the full dataset for teaching; it must not be used to tune models against the held-out test period.
