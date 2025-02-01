1. Add new table in the staging schema.yml
2. Generate model (correct the location)
3. Design this stg_table.sql model


This helps to fulfill schema.yml skeleton from stg:

{% set models_to_generate = codegen.get_models(directory='staging', prefix='stg_') %}
{{ codegen.generate_model_yaml(
    model_names = models_to_generate
) }}


{% set models_to_generate = codegen.get_models(directory='core') %}
{{ codegen.generate_model_yaml(
    model_names = models_to_generate
) }}

4. Design fact table

* Missing permissions gcs storage viewer for the dbt IAM

dbt build -> tables created in dbt_rosejos dataset

Commit changes and merge to main via PR -> 