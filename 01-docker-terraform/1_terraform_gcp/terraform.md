# Terraform Basics

## What is Terraform?
Terraform is an Infrastructure as Code (IaC) tool that allows you to define, provision, and manage infrastructure resources using declarative configuration files.

### Benefits:
- **Simplicity**: Makes it easier to keep track of infrastructure.
- **Collaboration**: Enables teams to work together effectively.
- **Reproducibility**: Ensures infrastructure can be recreated consistently.
- **Resource Cleanup**: Ensures that resources are properly removed when no longer needed.

### Limitations:
- **Does not manage or update code** running on infrastructure.
- **Cannot change immutable resources**; they must be recreated.
- **Does not manage resources** not explicitly defined in your Terraform files.

## Terraform Providers
Providers are the components that allow Terraform to interact with cloud platforms, services, or APIs to manage resources. Examples include:
- Google Cloud Platform (GCP)
- AWS
- Azure

## Key Terraform Commands
1. **`terraform init`**: Initializes the Terraform project and downloads the required providers.
2. **`terraform plan`**: Previews the changes Terraform will apply.
3. **`terraform apply`**: Executes the plan and applies the changes defined in the configuration files.
4. **`terraform destroy`**: Removes all resources defined in the configuration files.

### Additional Commands
- **Format Terraform files:**
  ```bash
  terraform fmt
  ```

## Using Terraform with Google Cloud Platform
### Authentication
1. Authenticate with Google Cloud:
   ```bash
   gcloud auth application-default login
   ```
2. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your service account key file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
   ```

### Workflow
1. **Initialize the project:**
   ```bash
   terraform init
   ```
2. **Preview the changes:**
   ```bash
   terraform plan
   ```
3. **Apply the changes:**
   ```bash
   terraform apply
   ```
4. **Destroy resources:**
   ```bash
   terraform destroy
   ```

### Handling Failed Applies
If `terraform apply` fails midway, any successfully created resources will remain. Running `terraform apply` again will attempt to create the remaining resources without duplicating the existing ones.

## Managing Variables
When using variables in Terraform, you can pass them directly via the command line:

### Example:
```bash
terraform plan -var="project=XXXXXXXX-XXXXXX"
terraform apply -var="project=XXXXXXXX-XXXXXX"
terraform destroy -var="project=XXXXXXXX-XXXXXX"
```

### Best Practices for Variables:
- Use a `terraform.tfvars` file to avoid passing variables repeatedly:
  ```hcl
  project = "XXXXXXXX-XXXXXX"
  ```
  Then run:
  ```bash
  terraform plan
  terraform apply
  terraform destroy
  ```
- Alternatively, set variables as environment variables:
  ```bash
  export TF_VAR_project="XXXXXXXX-XXXXXX"
  ```
  Then run:
  ```bash
  terraform plan
  terraform apply
  terraform destroy
  ```

