# ESG Compliance Module User Guide

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Initial Setup](#initial-setup)
3. [Master Configuration](#master-configuration)
4. [Daily Operations](#daily-operations)
5. [Reports & Analytics](#reports-analytics)

## Architecture Overview

### Core Doctype Hierarchy

The ESG Compliance module uses a hierarchical structure of parent and child documents:

#### **ESG Audit** (Parent Document)
- **Purpose**: Records ESG compliance audits and assessments
- **Role**: Container for audit findings and team members
- **Key Fields**: Audit Type (Internal/External/Certification/Regulatory), Status (Planned/Ongoing/Completed/Reporting), Overall Rating
- **Child Tables**:
  - **ESG Audit Team**: Team members participating in the audit
  - **ESG Audit Finding**: Audit findings and non-conformances discovered
  - **ESG Audit Metric**: Specific metrics evaluated during the audit
  - **ESG Audit Policy**: Relevant policies reviewed in the audit

#### **ESG Metric** (Parent Document)
- **Purpose**: Defines ESG key performance indicators (KPIs) to be tracked
- **Role**: Master configuration for what to measure (Carbon Emissions, Water Usage, Employee Satisfaction, etc.)
- **Key Fields**: Metric Name, Data Type (Quantitative/Qualitative/Percentage/Ratio), Frequency (Daily/Weekly/Monthly/Quarterly/Annually), Collection Method
- **Thresholds**: Red/Yellow/Green thresholds for performance evaluation
- **Child Tables**: None (stores configuration only)

#### **ESG Metric Entry** (Parent Document)
- **Purpose**: Records actual measured values for ESG metrics
- **Role**: Data capture point - stores the real metric values over time
- **Key Fields**: Metric (Link to ESG Metric), Value (measured result), Entry Date, Verification Status
- **Related Data**: Company, Period dates, Source document reference
- **Child Tables**: None (stores individual metric readings)

#### **ESG Corrective Action** (Parent Document)
- **Purpose**: Tracks corrective actions for audit findings or metric non-conformance
- **Role**: Action item management - ensures issues are addressed
- **Child Tables**:
  - **ESG Action Item**: Individual action steps to resolve the issue

#### **ESG Compliance Checklist** (Parent Document)
- **Purpose**: Define ESG compliance requirements and standards
- **Role**: Template for compliance verification
- **Child Tables**:
  - **ESG Checklist Item**: Individual checklist items to be verified

### Data Flow Architecture

```
ESG Audit (What was audited?)
    ├── ESG Audit Finding (What issues were found?)
    ├── ESG Audit Metric (What metrics were evaluated?)
    ├── ESG Audit Team (Who conducted the audit?)
    └── ESG Audit Policy (What policies were reviewed?)
         └── ESG Corrective Action (How to fix issues?)
              └── ESG Action Item (Specific action steps)

ESG Metric (What to measure?)
    └── ESG Metric Entry (What are the actual values?)
         └── Verification Status (Is the data verified?)

ESG Compliance Checklist (What compliance requirements?)
    └── ESG Checklist Item (Individual compliance items)
```

### Document Relationships

- **ESG Metric Entry** references **ESG Metric**: Each entry is a measurement of a specific metric
- **ESG Audit Finding** references **ESG Audit**: Each finding belongs to an audit
- **ESG Corrective Action** references findings: Actions address identified issues
- **ESG Action Item** belongs to **ESG Corrective Action**: Action items track implementation steps

### Typical Workflow

1. **Setup Phase**: Create ESG Metrics defining what to track (Carbon Emissions, Water Usage, etc.)
2. **Data Collection**: Record ESG Metric Entries with actual measured values
3. **Auditing Phase**: Conduct ESG Audits to verify compliance and performance
4. **Finding Documentation**: Document issues in ESG Audit Findings
5. **Action Planning**: Create Corrective Actions with detailed Action Items
6. **Implementation Tracking**: Monitor implementation progress through Action Items
7. **Reporting & Analysis**: Analyze trends in ESG Metric Entries and generate reports

## Initial Setup

### Company Settings
1. Navigate to Company doctype
2. Set ESG related fields:
   - Baseline Emissions (Tonnes CO2e)
   - Baseline Year
   - Annual Emission Reduction Target %
   - Net Zero Target Year
   ![Company ESG Settings](assets/company_esg_settings.png)

### Item Master Configuration
1. Go to Item doctype
2. Configure ESG fields for each item:
   - Carbon Emission Factor (kg CO2e/unit)
   - Emission Source
   - Carbon Scope (1,2,3)
   - Calculation Method
   ![Item ESG Configuration](assets/item_esg_config.png)

### Customer ESG Profile
1. Access Customer doctype
2. Set sustainability preferences:
   - Carbon Offset Preference
   - Carbon Footprint Reporting Required
   - Sustainability Focus Status
   ![Customer ESG Profile](assets/customer_esg_profile.png)

### Supplier Carbon Management
1. Open Supplier doctype
2. Configure carbon credentials:
   - Carbon Certified status
   - Certification Type
   - Certificate Number
   - Certificate Expiry
   - Annual Carbon Emissions
   ![Supplier Carbon Profile](assets/supplier_carbon_profile.png)

## Daily Operations

### Sales Process
1. Sales Invoice Creation
   - System automatically calculates emissions
   - Shows carbon offset options if enabled
   ![Sales Carbon Tracking](assets/sales_carbon_tracking.png)

### Purchase Management
1. Purchase Invoice Processing
   - Tracks supplier emissions
   - Validates certification status
   ![Purchase Carbon Management](assets/purchase_carbon_mgmt.png)

### Manufacturing Operations
1. Work Order Carbon Tracking
   - Raw material emissions
   - Process emissions
   - Total manufacturing impact
   ![Work Order ESG](assets/work_order_esg.png)

2. Production Planning
   - Emission estimates
   - Carbon reduction targets
   ![Production ESG Planning](assets/production_esg_plan.png)

### Inventory Management
1. Stock Entry Carbon Impact
   - Material receipt impact
   - Transfer emissions
   - Issue carbon tracking
   ![Stock Carbon Tracking](assets/stock_carbon_track.png)

### Delivery Operations
1. Delivery Note Processing
   - Product carbon footprint
   - Transport emissions
   - Total delivery impact
   ![Delivery ESG](assets/delivery_esg.png)

## Reports & Analytics

### ESG Activity Log
1. Comprehensive activity tracking
2. Performance monitoring
3. Verification status
![ESG Activity Log](assets/esg_activity_log.png)

### ESG Analysis Report
1. Metric analysis
2. Target tracking
3. Performance trends
![ESG Analysis](assets/esg_analysis.png)

### ESG Overview Dashboard
1. Real-time KPIs
2. Performance charts
3. Initiative tracking
![ESG Dashboard](assets/esg_dashboard.png)

## Tips & Best Practices

1. Regular Updates
   - Keep emission factors current
   - Update certifications before expiry
   - Review targets quarterly



