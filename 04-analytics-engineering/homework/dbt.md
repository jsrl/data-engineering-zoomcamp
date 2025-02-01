# Steps to Design and Generate Models in DBT

1. **Add New Table in the Staging `schema.yml`**

   - Add the new table to your `schema.yml` under the staging schema.

2. **Generate Model (Correct the Location)**

   - Ensure that the model is generated at the correct location within your DBT project.

3. **Design the `stg_table.sql` Model**

   - Design your `stg_table.sql` model file with the appropriate logic to process the staging data.

### Code to Fulfill the `schema.yml` Skeleton from Staging:

```sql
{% set models_to_generate = codegen.get_models(directory='staging', prefix='stg_') %}
{{ codegen.generate_model_yaml(
    model_names = models_to_generate
) }}

{% set models_to_generate = codegen.get_models(directory='core') %}
{{ codegen.generate_model_yaml(
    model_names = models_to_generate
) }}
```

4. **Design fact table**

   - Design your `stg_table.sql` model file with the appropriate logic to process the staging data.

   * Missing permissions gcs storage viewer for the dbt IAM

   * dbt build -> tables created in dbt_rosejos dataset

   * Commit changes and merge to main via PR -> prod dataset