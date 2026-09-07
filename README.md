\# ☁️ Cloud Incident Response \& Digital Forensics Automation System



An event-driven cloud security and digital forensics system built using AWS services to automatically detect security-related activities, preserve forensic evidence, generate incident records, and notify security teams.



\---



\## 📌 Project Overview



The \*\*Cloud Incident Response \& Digital Forensics Automation System\*\* is designed to automate the initial stages of cloud security incident response.



The system monitors AWS API activity through \*\*AWS CloudTrail\*\*, detects selected security-related events using \*\*Amazon EventBridge\*\*, and automatically invokes an \*\*AWS Lambda\*\* function for incident processing.



For every detected incident, the system:



\- Detects security-related AWS activity

\- Classifies incident severity

\- Preserves the original event as forensic evidence

\- Generates a SHA-256 integrity hash

\- Maintains chain-of-custody information

\- Stores incident metadata in DynamoDB

\- Sends security alerts through SNS

\- Records processing logs in CloudWatch

\- Provides a Streamlit-based incident dashboard



\---



\## 🏗️ Architecture



```text

&#x20;                   AWS Activity

&#x20;                        │

&#x20;                        ▼

&#x20;                ┌───────────────┐

&#x20;                │  AWS CloudTrail│

&#x20;                └───────┬───────┘

&#x20;                        │

&#x20;                        ▼

&#x20;                ┌────────────────┐

&#x20;                │ Amazon EventBridge│

&#x20;                └───────┬────────┘

&#x20;                        │

&#x20;                        ▼

&#x20;             ┌────────────────────────┐

&#x20;             │ AWS Lambda              │

&#x20;             │ Incident Handler        │

&#x20;             └───────────┬────────────┘

&#x20;                         │

&#x20;         ┌───────────────┼────────────────┐

&#x20;         ▼               ▼                ▼

&#x20;  CloudWatch Logs       SNS           DynamoDB

&#x20;         │              Alert          Incident

&#x20;         │                             Record

&#x20;         │

&#x20;         └───────────────┬────────────────┘

&#x20;                         ▼

&#x20;                 Amazon S3 Evidence

&#x20;                         │

&#x20;                ┌────────┴────────┐

&#x20;                ▼                 ▼

&#x20;            SHA-256        Chain of Custody

&#x20;                │                 │

&#x20;                └────────┬────────┘

&#x20;                         ▼

&#x20;               Forensic Investigation

&#x20;                         │

&#x20;                         ▼

&#x20;                Streamlit Dashboard





🚀 Key Features

🔍 Automated Incident Detection



Amazon EventBridge monitors AWS CloudTrail API events and triggers the Lambda incident handler when selected security-related activities occur.



Currently monitored events include:



CreateBucket

DeleteBucket

PutBucketPolicy

DeleteBucketPolicy

⚠️ Incident Severity Classification



The system automatically classifies detected events into severity levels.



Severity	Example Events

HIGH	DeleteBucket, DeleteBucketPolicy, PutBucketPolicy

MEDIUM	CreateBucket, PutBucketAcl, PutBucketLogging, PutObject

LOW	Other monitored events

🧪 Digital Evidence Preservation



The original security event is serialized and preserved in Amazon S3.



Each evidence object contains metadata such as:



Incident ID

Event name

Severity

Source IP

Collection timestamp

Collector information

SHA-256 hash

🔐 SHA-256 Integrity Verification



A SHA-256 hash is generated for every preserved evidence file.



This allows investigators to verify that the evidence has not been modified after collection.



Example:



Original Evidence

&#x20;      ↓

&#x20;   SHA-256

&#x20;      ↓

Evidence Hash

&#x20;      ↓

Download Evidence

&#x20;      ↓

Calculate SHA-256 Again

&#x20;      ↓

Compare Hashes



Matching hashes indicate that the downloaded evidence is identical to the preserved evidence.



⛓️ Chain of Custody



The system records forensic chain-of-custody information including:



Collection timestamp

Collection source

Collector

Collection action

Evidence location

Hash algorithm

Evidence hash

Preservation status



This improves the traceability and integrity of digital evidence.



🗄️ Incident Management



Incident metadata is stored in Amazon DynamoDB.



Important fields include:



incident\_id

event\_name

severity

status

response\_action

evidence\_status

evidence\_sha256

evidence\_s3\_uri

custody\_collected\_at

custody\_collected\_by

custody\_source

custody\_action

custody\_status

📧 Security Alerts



Amazon SNS sends security alerts containing important incident information such as:



Incident ID

Event name

Severity

Source IP

Evidence location

SHA-256 hash

Response status

Chain-of-custody information

📊 Security Dashboard



A Streamlit dashboard provides a centralized view of security incidents.



Dashboard capabilities include:



Incident statistics

Severity distribution

Incident status

Event analysis

Incident timeline

Evidence preservation rate

Security alert status

Recent incidents

Forensic investigation details

SHA-256 evidence hash

Chain-of-custody information

CSV incident report download

🛠️ Technology Stack

Cloud Services

AWS CloudTrail

Amazon EventBridge

AWS Lambda

Amazon S3

Amazon DynamoDB

Amazon SNS

Amazon CloudWatch

Development

Python

Boto3

Streamlit

Pandas

Security

SHA-256

S3 Object Lock

Evidence metadata

Chain of custody

IAM permissions

📂 Project Structure

Cloud-Incident-Response-Digital-Forensics/

│

├── app.py

├── requirements.txt

├── .gitignore

│

├── architecture/

│   └── architecture.png

│

├── lambda/

│   └── cloud-forensics-incident-handler.py

│

├── screenshots/

│   ├── cloudtrail.png

│   ├── eventbridge-rule.png

│   ├── eventbridge-target.png

│   ├── lambda.png

│   ├── cloudwatch.png

│   ├── dynamodb.png

│   ├── s3-evidence.png

│   ├── evidence-verification.png

│   └── dashboard.png

│

└── docs/

&#x20;   └── project-documentation.pdf

⚙️ Incident Processing Workflow

1\. AWS API activity occurs

&#x20;       ↓

2\. CloudTrail records the activity

&#x20;       ↓

3\. EventBridge detects the selected event

&#x20;       ↓

4\. Lambda incident handler is triggered

&#x20;       ↓

5\. Incident severity is calculated

&#x20;       ↓

6\. Unique incident ID is generated

&#x20;       ↓

7\. Original event is converted into evidence

&#x20;       ↓

8\. SHA-256 hash is generated

&#x20;       ↓

9\. Evidence is preserved in S3

&#x20;       ↓

10\. Incident record is stored in DynamoDB

&#x20;       ↓

11\. SNS security alert is generated

&#x20;       ↓

12\. CloudWatch records processing logs

&#x20;       ↓

13\. Investigator reviews incident

&#x20;       ↓

14\. Streamlit dashboard displays results

🧪 Testing



The system was tested using controlled AWS security events.



Test Case 1 — Bucket Creation

Event: CreateBucket

Severity: MEDIUM

Evidence: PRESERVED

Response: OPEN



Expected result:



EventBridge detects the event

Lambda is invoked

Evidence is stored in S3

SHA-256 hash is generated

DynamoDB incident is created

SNS alert is sent

Test Case 2 — Bucket Deletion

Event: DeleteBucket

Severity: HIGH

Evidence: PRESERVED

Response: REQUIRES\_REVIEW



Expected result:



EventBridge detects the event

Lambda processes the incident

Evidence is preserved

DynamoDB record is created

SNS notification is sent

HIGH severity incident is flagged for security review

🔐 Security Considerations



The project follows several security-focused practices:



IAM-based access control

Least-privilege permissions for Lambda

S3 server-side encryption

S3 Object Lock for evidence preservation

SHA-256 evidence integrity verification

Chain-of-custody tracking

CloudWatch logging

Separation of incident metadata and forensic evidence

💰 Cost Considerations



The project is designed to minimize AWS costs by primarily using serverless services.



Main services used:



Lambda

EventBridge

DynamoDB

SNS

CloudWatch

S3

CloudTrail



Unused resources should be deleted after testing to avoid unnecessary AWS charges.



⚠️ Limitations



Current implementation focuses on selected AWS API security events.



The system does not currently provide:



Full enterprise SIEM functionality

Automated isolation of compromised EC2 instances

Malware analysis

Automated threat intelligence enrichment

Full AWS Security Hub integration

Multi-account incident orchestration

🔮 Future Scope



Possible future improvements include:



AWS Security Hub integration

GuardDuty integration

Automated EC2 isolation

Automated IAM credential response

Threat intelligence integration

Multi-account monitoring

Advanced risk scoring

Machine-learning-based anomaly detection

Automated forensic report generation

Role-based dashboard access

Real-time security monitoring

Integration with enterprise SIEM platforms

🎯 Learning Outcomes



This project demonstrates practical knowledge of:



AWS cloud security

Event-driven architecture

Serverless computing

AWS Lambda

CloudTrail monitoring

EventBridge automation

IAM

S3 evidence preservation

DynamoDB

SNS alerting

CloudWatch monitoring

Digital forensics

Evidence integrity

Chain of custody

Python automation

Streamlit dashboard development

👨‍💻 Author



Vivek Raj



B.Tech Computer Science \& Engineering



Cloud Computing | AWS | Python | Data Analytics



⭐ Project Highlights

☁️ AWS Cloud Security

🔍 Automated Incident Detection

⚡ Event-Driven Architecture

🧪 Digital Evidence Preservation

🔐 SHA-256 Integrity Verification

⛓️ Chain of Custody

📧 Automated Security Alerts

🗄️ DynamoDB Incident Management

📊 Streamlit Security Dashboard



📜 License



This project is developed for educational, academic, and portfolio purposes.

