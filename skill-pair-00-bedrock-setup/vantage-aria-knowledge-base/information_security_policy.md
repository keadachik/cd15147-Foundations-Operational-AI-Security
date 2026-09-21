# Information Security Policy v3.0

| Field | Value |
|---|---|
| Policy owner | Information Security (CISO) |
| Effective date | February 1, 2025 |
| Review cycle | Annual |

## 1. Purpose

This policy sets the minimum security requirements that protect Vantage Technologies ("Vantage") systems, customer data, and employee information.

## 2. Scope

This policy applies to all employees, contractors, and third parties who access Vantage systems or data, and to all company-owned devices, cloud accounts, and networks. Violations may result in disciplinary action, up to and including termination.

## 3. Endpoint Security

- All company laptops and servers must run **CrowdStrike Falcon**. Disabling, uninstalling, or interfering with the Falcon sensor is prohibited.
- Full-disk encryption must be enabled on every laptop.
- Screens must lock automatically after 5 minutes of inactivity.
- Personal devices may not be used to store Confidential or Restricted data.
- Only IT-approved software may be installed on company devices. Requests for new software go through the IT Service Desk.

## 4. Identity and Access

- All employees must use Okta single sign-on with multi-factor authentication (MFA) enabled.
- Access is granted on a least-privilege basis and reviewed quarterly by system owners.
- Shared accounts are not permitted except for approved service accounts managed by IT.
- Access is removed within 24 hours of an employee's termination.

## 5. Network Security

- Internal systems are accessible only through the Vantage VPN or approved zero-trust access.
- Public Wi-Fi may not be used to access customer data.
- Production environments are segmented from corporate networks. Direct access to production requires a just-in-time access request.
- Firewall and security group changes must be reviewed by the Security team.

## 6. Data Security

### Data Classification

| Level | Description | Examples |
|---|---|---|
| Public | Approved for public release | Marketing website, published product documentation |
| Internal | For Vantage employees; low impact if disclosed | Most company policies, org charts, internal announcements |
| Confidential | Limited to those with a business need; significant impact if disclosed | Salary bands, customer contracts, pricing, financial results |
| Restricted | Highest sensitivity; strict need-to-know | Social Security numbers, bank details, customer production data, M&A plans |

### Handling Requirements

- Confidential and Restricted data must be encrypted at rest and in transit.
- Restricted data may not be copied into email, Slack, or AI tools unless the tool has been approved by Security for that classification.
- Documents should be labeled with their classification when created.
- Data must be retained and deleted according to the Records Retention Schedule.

## 7. Vulnerability Management

- Critical vulnerabilities must be patched or mitigated within **14 days** of disclosure.
- High vulnerabilities must be patched within **30 days**; medium within **90 days**.
- Security runs authenticated vulnerability scans weekly and an external penetration test annually.
- Systems that cannot be patched within these windows require a security exception.

## 8. Security Exceptions

Some business needs may require a temporary deviation from this policy.

- **All exceptions require a ticket to the Security team** describing the business need, the affected systems, the duration, and compensating controls.
- **Exceptions must be approved by the CISO** before the activity begins. Manager approval alone is not sufficient.
- Approved exceptions are time-limited (maximum 90 days) and are tracked in the exception register.
- **No software may be installed without approval.** Installing unapproved software while an exception request is pending is a policy violation.
- If you are unsure whether an activity needs an exception, ask the Security team before proceeding.

## 9. Incident Response

- Report suspected security incidents immediately to security@vantagetech.example or the Security hotline at x4499, or in the #security-incidents Slack channel.
- Examples include phishing emails, lost devices, suspected malware, unexpected MFA prompts, and accidental data exposure.
- Do not attempt to investigate or clean up an incident yourself. Preserve evidence and follow Security team instructions.
- The Security team triages reports within one hour during business hours and follows the Incident Response Plan for containment, eradication, recovery, and post-incident review.

## 10. Training

All employees must complete security awareness training at hire and annually thereafter.

## 11. Document History

| Version | Date | Summary |
|---|---|---|
| 2.0 | March 2023 | Added cloud and SaaS requirements |
| 2.1 | January 2024 | Added AI tool data handling guidance |
| 3.0 | February 2025 | Restructured policy; added Restricted classification and exception register |
